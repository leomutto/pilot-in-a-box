from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource

# ---- TRACES ----
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# ---- METRICS ----
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# ---- INSTRUMENTATION ----
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_otel(app):
    """
    Configura OpenTelemetry para:
    - Traces (FastAPI + Requests)
    - Métricas (latencia, throughput, errores)
    - Exportación al Collector vía OTLP
    """

    # ============================================================
    # RESOURCE (identidad del servicio)
    # ============================================================
    resource = Resource(attributes={
        "service.name": "pilot-in-a-box-backend"
    })

    # ============================================================
    # TRACES
    # ============================================================
    trace_exporter = OTLPSpanExporter(
        endpoint="http://otel-collector:4317",
        insecure=True
    )

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Instrumentación automática
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

    # ============================================================
    # METRICS
    # ============================================================
    metric_exporter = OTLPMetricExporter(
        endpoint="http://otel-collector:4317",
        insecure=True
    )

    metric_reader = PeriodicExportingMetricReader(metric_exporter)

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )

    metrics.set_meter_provider(meter_provider)