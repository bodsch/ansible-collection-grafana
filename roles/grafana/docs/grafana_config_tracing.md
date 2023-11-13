# `grafana_config_tracing`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_tracing:
  # jaeger: {}
  #   # Enable by setting the address sending traces to jaeger (ex localhost:6831)
  #   address: localhost:6831
  #   # Tag that will always be included in when creating new spans. ex (tag1:value1,tag2:value2)
  #   always_included_tag: tag1:value1
  #   # Type specifies the type of the sampler: const, probabilistic, rateLimiting, or remote
  #   sampler_type: const
  #   # jaeger samplerconfig param
  #   # for "const" sampler, 0 or 1 for always false/true respectively
  #   # for "probabilistic" sampler, a probability between 0 and 1
  #   # for "rateLimiting" sampler, the number of spans per second
  #   # for "remote" sampler, param is the same as for "probabilistic"
  #   # and indicates the initial sampling rate before the actual one
  #   # is received from the mothership
  #   sampler_param: 1
  #   # sampling_server_url is the URL of a sampling manager providing a sampling strategy.
  #   sampling_server_url: ""
  #   # Whether or not to use Zipkin propagation (x-b3- HTTP headers).
  #   zipkin_propagation: false
  #   # Setting this to true disables shared RPC spans.
  #   # Not disabling is the most common setting when using Zipkin elsewhere in your infrastructure.
  #   disable_shared_zipkin_spans: false

  opentelemetry:
    jaeger: {}
    #   # jaeger destination (ex http://localhost:14268/api/traces)
    #   address: http://localhost:14268/api/traces
    #   # Propagation specifies the text map propagation format: w3c, jaeger
    #   propagation: jaeger

    # This is a configuration for OTLP exporter with GRPC protocol
    otlp: {}
    #   # otlp destination (ex localhost:4317)
    #   address: localhost:4317
    #   # Propagation specifies the text map propagation format: w3c, jaeger
    #   propagation: w3c
```
