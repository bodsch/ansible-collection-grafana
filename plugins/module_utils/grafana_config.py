#!/usr/bin/python3

# (c) 2022-2026, Bodo Schulz <bodo@boone-schulz.de>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0)
# SPDX-License-Identifier: Apache-2.0

"""
Read-only access to the Grafana configuration (``grafana.ini``).

``grafana.ini`` is not a strict INI file in the sense of ``configparser``.
This module implements a small parser that follows the behaviour of Grafana
(and the go-ini library used by it):

- Keys before the first section (``app_mode``, ``instance_name``, ...) are
  valid and stored under the pseudo section ``__default__``.
- ``#`` and ``;`` start a comment, at the beginning of a line as well as
  inline (``key = value ; comment``).
- Values containing ``#`` or ``;`` must be wrapped in triple quotes
  (``\"\"\"...\"\"\"``) or backticks. Those values may span multiple lines.
- Simple single or double quotes around a value are removed.
- Key and value are separated by the first ``=`` or ``:``.
- Variable expansion: ``$__env{VAR}``, ``$__file{/path}`` and ``${VAR}``.
- Every value can be overridden by an environment variable
  ``GF_<SECTION>_<KEY>``. Section and key are upper-cased, ``.`` and ``-``
  are replaced by ``_``. Keys before the first section use
  ``GF_DEFAULT_<KEY>``.

An Ansible module does not run with the environment of the
``grafana-server`` service. The service environment comes from the systemd
``EnvironmentFile`` (``/etc/default/grafana-server`` or
``/etc/sysconfig/grafana-server``). :func:`grafana_environ` reads these files
and :func:`read_config` uses them by default.

Not supported:
    - ``%(key)s`` interpolation (kept as literal text).
    - Writing the configuration.
    - ``$__vault{}`` references.

Example:
    .. code-block:: python

        from ansible_collections.bodsch.grafana.plugins.module_utils.grafana_config import (
            GrafanaIni,
            grafana_environ,
            read_config,
        )

        # one section as dict (including GF_* overrides from the service environment)
        security = read_config(module, "/etc/grafana/grafana.ini", "security")
        if security:
            admin_user = security.get("admin_user")
            admin_pass = security.get("admin_password")

        # full access
        ini = GrafanaIni(module, "/etc/grafana/grafana.ini", environ=grafana_environ())
        http_port = ini.get("server", "http_port", "3000")
"""


import os
import re
import shlex
from collections import OrderedDict
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

#: Name of the pseudo section for keys before the first section header.
DEFAULT_SECTION = "__default__"

#: Default systemd ``EnvironmentFile`` locations of the grafana-server service
#: (Debian / RedHat based distributions).
DEFAULT_ENV_FILES = (
    "/etc/default/grafana-server",
    "/etc/sysconfig/grafana-server",
)

_SECTION_RE = re.compile(r"^\[(?P<name>[^]]+)\]$")
_ENV_RE = re.compile(r"\$__env\{(?P<name>[^}]+)\}")
_FILE_RE = re.compile(r"\$__file\{(?P<name>[^}]+)\}")
_SHELL_ENV_RE = re.compile(r"\$\{(?P<name>[^}]+)\}")


def env_key(section: str, key: str) -> str:
    """
    Build the name of the environment variable that overrides ``section.key``.

    Uses the same rules as Grafana's ``applyEnvVariableOverrides``:
    ``GF_<SECTION>_<KEY>``, upper-cased, with ``.`` and ``-`` replaced by ``_``.
    The pseudo section ``__default__`` maps to ``DEFAULT``.

    Args:
        section:
            Section name, e.g. ``"auth.ldap"`` or ``"__default__"``.
        key:
            Key name, e.g. ``"enabled"``. An empty string returns the
            prefix for the whole section (``"GF_AUTH_LDAP_"``).

    Returns:
        str: The environment variable name, e.g. ``"GF_AUTH_LDAP_ENABLED"``.
    """
    def _norm(s: str) -> str:
        return s.upper().replace(".", "_").replace("-", "_")

    if section == DEFAULT_SECTION:
        section = "DEFAULT"

    return f"GF_{_norm(section)}_{_norm(key)}"


def read_env_file(path: str) -> dict[str, str]:
    """
    Read a systemd ``EnvironmentFile`` or a shell style ``KEY=value`` file.

    Supports comments, single/double quoted values (also multi-line, e.g.
    ``OPTIONS="..."``) and an optional ``export`` prefix. If the file contains
    unbalanced quotes, a simple line based parser is used as fallback.

    Args:
        path:
            Path to the environment file.

    Returns:
        dict: Mapping of variable names to values. Empty if the file does
        not exist or cannot be read.
    """
    result: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return result

    try:
        tokens = shlex.split(content, comments=True, posix=True)
    except ValueError:
        # unbalanced quotes - fall back to a simple line based parser
        tokens = [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]

    for token in tokens:
        token = token.removeprefix("export ")
        name, sep, value = token.partition("=")
        if sep and name.strip():
            result[name.strip()] = value

    return result


class GrafanaIni:
    """
    Read-only parser for ``grafana.ini``.

    The file is parsed on instantiation. Afterwards ``GF_*`` overrides are
    applied to every key present in the file. Keys that exist only as
    environment variable are resolved on access via :meth:`section` and
    :meth:`get`.

    Attributes:
        module:
            Ansible module instance, used for logging only. May be ``None``.
        path:
            Path to the parsed file, or ``None`` if no file was parsed.
        expand:
            Whether ``$__env{}``, ``$__file{}`` and ``${}`` references are resolved.
        environ:
            Environment used for ``GF_*`` overrides and variable expansion.
        env_overrides:
            Whether ``GF_*`` overrides are applied.
        data:
            Parsed configuration: ``OrderedDict`` of section name to a dict of
            key/value pairs (all values are strings). Keys before the first
            section are stored under :data:`DEFAULT_SECTION`.
    """

    def __init__(
        self,
        module: Any,
        path: str | None,
        expand: bool = True,
        environ: Mapping[str, str] | None = None,
        env_overrides: bool = True,
    ) -> None:
        """
        Parse the configuration file and apply the environment overrides.

        Args:
            module:
                Ansible module instance (used for logging only, may be ``None``).
            path:
                Path to ``grafana.ini``. ``None`` skips parsing, the instance
                then only provides values from ``GF_*`` variables.
            expand:
                Resolve ``$__env{VAR}``, ``$__file{/path}`` and ``${VAR}``
                references. Defaults to ``True``.
            environ:
                Environment used for ``GF_*`` overrides and variable expansion.
                Defaults to ``os.environ``. Use :func:`grafana_environ` to get
                the environment of the grafana-server service.
            env_overrides:
                Apply ``GF_<SECTION>_<KEY>`` overrides. Defaults to ``True``.

        Raises:
            FileNotFoundError:
                If ``path`` is given but does not exist.
            PermissionError:
                If ``path`` cannot be read.
            UnicodeDecodeError:
                If ``path`` is not valid UTF-8.
        """
        self.module = module
        self.path = path
        self.expand = expand
        self.environ: Mapping[str, str] = os.environ if environ is None else environ
        self.env_overrides = env_overrides
        self.data: OrderedDict[str, dict[str, str]] = OrderedDict()

        if path is not None:
            self._load()

        if self.env_overrides:
            self._apply_env_overrides()

    # ------------------------------------------------------------------------------------

    def _log(self, msg: str) -> None:
        """
        Log a message via the Ansible module, if one is set.

        Args:
            msg:
                Message to log.
        """
        if self.module:
            self.module.log(msg)

    def _load(self) -> None:
        """
        Parse ``self.path`` line by line into ``self.data``.

        Empty lines, comment lines and lines without delimiter are skipped.
        The pseudo section :data:`DEFAULT_SECTION` is removed if it is empty.
        """
        current_section = DEFAULT_SECTION
        self.data[current_section] = OrderedDict()

        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            # empty line or comment line
            if not line or line[0] in "#;":
                continue

            # section header
            m_sec = _SECTION_RE.match(line)
            if m_sec:
                current_section = m_sec.group("name").strip()
                self.data.setdefault(current_section, OrderedDict())
                continue

            # key / value - split at the first '=' or ':'
            pos = self._find_delimiter(line)
            if pos < 0:
                self._log(f"GrafanaIni: ignore invalid line {i}: '{line}'")
                continue

            key = line[:pos].strip()
            raw = line[pos + 1:].lstrip()

            value, i = self._parse_value(raw, lines, i)

            self.data[current_section][key] = self._expand(value)

        if not self.data[DEFAULT_SECTION]:
            del self.data[DEFAULT_SECTION]

    def _apply_env_overrides(self) -> None:
        """
        Override every key present in ``self.data`` with its
        ``GF_<SECTION>_<KEY>`` variable, if set in ``self.environ``.

        Only the variable name is logged, never the value.
        """
        for section, items in self.data.items():
            for key in items:
                name = env_key(section, key)
                if name in self.environ:
                    self._log(f"GrafanaIni: '{section}.{key}' overridden by {name}")
                    items[key] = self._expand(self.environ[name])

    def _env_only_keys(self, section: str) -> dict[str, str]:
        """
        Collect ``GF_<SECTION>_*`` variables for keys not present in the file.

        Example: a commented out ``admin_password`` combined with
        ``GF_SECURITY_ADMIN_PASSWORD``.

        The original key name can't be restored exactly from the variable
        name, it is returned lower-cased (Grafana keys use ``_`` as separator
        anyway). Variables belonging to a more specific section known from
        the file are skipped (e.g. ``GF_AUTH_LDAP_*`` when requesting ``auth``
        and ``[auth.ldap]`` exists).

        Args:
            section:
                Section name.

        Returns:
            dict: Lower-cased key names mapped to their (expanded) values.
        """
        prefix = env_key(section, "")
        # prefixes of other, more specific sections
        others = [
            env_key(s, "")
            for s in self.data
            if s != section and len(env_key(s, "")) > len(prefix) and env_key(s, "").startswith(prefix)
        ]
        known = {env_key(section, k) for k in self.data.get(section, {})}

        result: dict[str, str] = {}
        for name, value in self.environ.items():
            if not name.startswith(prefix) or name == prefix or name in known:
                continue
            if any(name.startswith(o) for o in others):
                continue
            result[name[len(prefix):].lower()] = self._expand(value)

        return result

    @staticmethod
    def _find_delimiter(line: str) -> int:
        """
        Find the key/value delimiter (the first ``=`` or ``:``).

        Args:
            line:
                Stripped configuration line.

        Returns:
            int: Index of the delimiter, or ``-1`` if there is none (or the
            line starts with it, i.e. the key would be empty).
        """
        positions = [p for p in (line.find("="), line.find(":")) if p > 0]
        return min(positions) if positions else -1

    @staticmethod
    def _parse_value(raw: str, lines: Sequence[str], i: int) -> tuple[str, int]:
        """
        Parse the raw value of a key, following go-ini semantics.

        - ``\"\"\"...\"\"\"`` and backtick quoted values are taken literally
          and may continue on the following lines.
        - Otherwise everything after the first ``#`` or ``;`` is an inline
          comment and removed.
        - Simple single or double quotes around the value are removed.

        Args:
            raw:
                Value part of the line (everything after the delimiter).
            lines:
                All lines of the file, used for multi-line values.
            i:
                Index of the next unread line in ``lines``.

        Returns:
            tuple: ``(value, next_line_index)``. ``next_line_index`` is behind
            the last consumed line of a multi-line value.
        """
        for quote in ('"""', "`"):
            if raw.startswith(quote):
                rest = raw[len(quote):]
                end = rest.find(quote)
                if end >= 0:
                    return rest[:end], i

                # multi-line value
                parts = [rest]
                while i < len(lines):
                    nxt = lines[i]
                    i += 1
                    end = nxt.find(quote)
                    if end >= 0:
                        parts.append(nxt[:end])
                        return "\n".join(parts), i
                    parts.append(nxt)

                # no closing quote found - take everything
                return "\n".join(parts), i

        # inline comment (go-ini: first '#' or ';' outside of quotes)
        pos = min((p for p in (raw.find("#"), raw.find(";")) if p >= 0), default=-1)
        if pos >= 0:
            raw = raw[:pos]

        value = raw.strip()

        # simple quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]

        return value, i

    def _expand(self, value: str) -> str:
        """
        Resolve Grafana variable references in a value.

        Supported: ``$__env{VAR}``, ``$__file{/path}`` (file content, stripped)
        and ``${VAR}``. Unknown variables and unreadable files resolve to an
        empty string, like in Grafana. Does nothing if ``self.expand`` is
        ``False``.

        Args:
            value:
                Raw value.

        Returns:
            str: Value with all references resolved.
        """
        if not self.expand or "$" not in value:
            return value

        def _env(m):
            return self.environ.get(m.group("name").strip(), "")

        def _file(m):
            try:
                with open(m.group("name").strip(), "r", encoding="utf-8") as f:
                    return f.read().strip()
            except OSError:
                return ""

        value = _ENV_RE.sub(_env, value)
        value = _FILE_RE.sub(_file, value)
        value = _SHELL_ENV_RE.sub(_env, value)

        return value

    # ------------------------------------------------------------------------------------

    def sections(self) -> list[str]:
        """
        List the named sections found in the file.

        Returns:
            list: Section names in file order, without :data:`DEFAULT_SECTION`.
        """
        return [s for s in self.data if s != DEFAULT_SECTION]

    def section(self, name: str) -> dict[str, str] | None:
        """
        Get all values of a section.

        Contains the values from the file (with ``GF_*`` overrides applied)
        plus keys that exist only as ``GF_<SECTION>_*`` variable.

        Args:
            name:
                Section name, e.g. ``"security"``. Use :data:`DEFAULT_SECTION`
                for keys before the first section.

        Returns:
            dict or None: A copy of the section, or ``None`` if neither the
            section nor matching ``GF_*`` variables exist.
        """
        items = self.data.get(name)
        extra = self._env_only_keys(name) if self.env_overrides else {}

        if items is None and not extra:
            return None

        result = dict(items or {})
        result.update(extra)

        return result

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a single value.

        Lookup order: value from the file (with ``GF_*`` override applied),
        then the ``GF_<SECTION>_<KEY>`` variable, then ``default``.

        Args:
            section:
                Section name.
            key:
                Key name.
            default:
                Returned if the key is neither in the file nor in the
                environment. Defaults to ``None``.

        Returns:
            str or Any: The value as string, or ``default``.
        """
        if section in self.data and key in self.data[section]:
            return self.data[section][key]

        if self.env_overrides:
            name = env_key(section, key)
            if name in self.environ:
                return self._expand(self.environ[name])

        return default


def grafana_environ(env_files: Iterable[str] = DEFAULT_ENV_FILES) -> dict[str, str]:
    """
    Build the environment of the grafana-server service.

    Starts with ``os.environ`` and overlays the variables from the given
    environment files. Later files win. Missing files are ignored.

    Args:
        env_files:
            Environment files to read. Defaults to :data:`DEFAULT_ENV_FILES`.
            An empty list or ``None`` returns a copy of ``os.environ``.

    Returns:
        dict: The merged environment.
    """
    environ = dict(os.environ)
    for env_file in env_files or ():
        environ.update(read_env_file(env_file))

    return environ


def read_config(
    module: Any,
    config_file: str,
    section: str,
    env_files: Iterable[str] = DEFAULT_ENV_FILES,
) -> dict[str, str] | None:
    """
    Read one section of ``grafana.ini``, including ``GF_*`` overrides.

    The environment is built with :func:`grafana_environ` from ``env_files``.
    A missing ``config_file`` is not an error: the result then contains only
    values from ``GF_*`` variables.

    Args:
        module:
            Ansible module instance, used for logging.
        config_file:
            Path to ``grafana.ini``, e.g. ``"/etc/grafana/grafana.ini"``.
        section:
            Section name, e.g. ``"security"``.
        env_files:
            Environment files of the grafana-server service. Defaults to
            :data:`DEFAULT_ENV_FILES`. Pass an empty list to use only
            ``os.environ``.

    Returns:
        dict or None: Key/value pairs of the section, or ``None`` if neither
        the section nor matching ``GF_*`` variables exist.

    Raises:
        PermissionError:
            If ``config_file`` exists but cannot be read.
    """
    # module.log(f"read_config(module, config_file: {config_file}, section: {section})")
    environ = grafana_environ(env_files)

    path = config_file if os.path.exists(config_file) else None
    ini = GrafanaIni(module, path, environ=environ)

    # module.log(f"  sections: {ini.sections()}")

    return ini.section(section)
