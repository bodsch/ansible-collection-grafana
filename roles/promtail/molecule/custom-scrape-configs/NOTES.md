

```bash
curl -v --resolve monitoring.molecule.lan:80:127.0.0.1 -v http://monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa
```

```bash
cat /var/log/nginx/monitoring.molecule.lan/error.log | promtail -config.file /etc/promtail/promtail.yml --stdin --dry-run -server.disable -log.level debug
```

## OUTPUT

```
2022-08-30T15:09:13.414683572+0000      {__path__="/var/log/nginx/**error.log", agent="promtail", env="molecule", host="instance", job="nginx", log_level="nginx_error"}        2022/08/30 14:44:57 [error] 13970#13970: *34 open() "/var/www/monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa" failed (2: No such file or directory), client: 127.0.0.1, server: monitoring.molecule.lan, request: "GET /bin/bashdfdslfnkjdsafifdsa HTTP/1.1", host: "monitoring.molecule.lan"
level=debug ts=2022-08-30T15:09:13.415374454Z caller=regex.go:121 component=pipeline component=stage type=regex msg="regex did not match" input="2022/08/30 15:04:58 [error] 13970#13970: *35 open() \"/var/www/monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa\" failed (2: No such file or directory), client: 127.0.0.1, server: monitoring.molecule.lan, request: \"GET /bin/bashdfdslfnkjdsafifdsa HTTP/1.1\", host: \"monitoring.molecule.lan\"" regex="(?P<timestamp>\\d{4}/\\d{2}/\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[(?P<severity>emerg|alert|crit|error|warn|notice|info)\\] (?P<process_id>\\d+)#(?P<thread_id>\\d+): \\*(?P<connection_id>\\d+) (?P<error>.+?) while (?P<context>.+?), client: (?P<client_ip>\\d+\\.\\d+\\.\\d+\\.\\d+), server: (?P<server>.+?), request: \\\"(?P<request_method>[A-Za-z]+?) (?P<request_path>\\/.+?) (?P<request_protocol>.+?)\\\"?, upstream: \\\"(?P<upstream>.+?)\\\"?, host: \\\"(?P<host>.+?)\\\"?(?:, referrer: \\\"(?P<referrer>.+?)\\\")?.*"
2022-08-30T15:09:13.414869437+0000      {__path__="/var/log/nginx/**error.log", agent="promtail", env="molecule", host="instance", job="nginx", log_level="nginx_error"}        2022/08/30 15:04:58 [error] 13970#13970: *35 open() "/var/www/monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa" failed (2: No such file or directory), client: 127.0.0.1, server: monitoring.molecule.lan, request: "GET /bin/bashdfdslfnkjdsafifdsa HTTP/1.1", host: "monitoring.molecule.lan"
level=debug ts=2022-08-30T15:09:13.415542207Z caller=regex.go:121 component=pipeline component=stage type=regex msg="regex did not match" input="2022/08/30 15:05:53 [error] 13970#13970: *36 open() \"/var/www/monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa\" failed (2: No such file or directory), client: 127.0.0.1, server: monitoring.molecule.lan, request: \"GET /bin/bashdfdslfnkjdsafifdsa HTTP/1.1\", host: \"monitoring.molecule.lan\"" regex="(?P<timestamp>\\d{4}/\\d{2}/\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[(?P<severity>emerg|alert|crit|error|warn|notice|info)\\] (?P<process_id>\\d+)#(?P<thread_id>\\d+): \\*(?P<connection_id>\\d+) (?P<error>.+?) while (?P<context>.+?), client: (?P<client_ip>\\d+\\.\\d+\\.\\d+\\.\\d+), server: (?P<server>.+?), request: \\\"(?P<request_method>[A-Za-z]+?) (?P<request_path>\\/.+?) (?P<request_protocol>.+?)\\\"?, upstream: \\\"(?P<upstream>.+?)\\\"?, host: \\\"(?P<host>.+?)\\\"?(?:, referrer: \\\"(?P<referrer>.+?)\\\")?.*"
2022-08-30T15:09:13.41487043+0000       {__path__="/var/log/nginx/**error.log", agent="promtail", env="molecule", host="instance", job="nginx", log_level="nginx_error"}        2022/08/30 15:05:53 [error] 13970#13970: *36 open() "/var/www/monitoring.molecule.lan/bin/bashdfdslfnkjdsafifdsa" failed (2: No such file or directory), client: 127.0.0.1, server: monitoring.molecule.lan, request: "GET /bin/bashdfdslfnkjdsafifdsa HTTP/1.1", host: "monitoring.molecule.lan"
level=info ts=2022-08-30T15:09:13.415675936Z caller=main.go:121 msg="Starting Promtail" version="(version=2.6.1, branch=HEAD, revision=6bd05c9a4)"

```


journalctl -u promtail -f -n 100

logcli query --tail '{agent="promtail",severity="error"}'
