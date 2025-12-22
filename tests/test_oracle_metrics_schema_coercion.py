import json
from uuid import uuid4

from src.shared_context.models import EndpointContext, HTTPMethod, Oracle
from src.validation.oracle_metrics import GroundTruth, OracleMetricsCalculator


def test_calculate_metrics_accepts_string_response_schema() -> None:
    endpoint = EndpointContext(name="Get foo", method=HTTPMethod.GET, url="/foo")

    ground_truth = GroundTruth(
        endpoint_id=endpoint.id,
        status_code=200,
        required_headers={},
        optional_headers={},
        response_schema={"type": "object", "properties": {"foo": {"type": "string"}}},
        business_rules=[],
        source="manual",
        confidence=1.0,
    )

    # Simulate an Oracle created via model_construct / non-validated pipeline
    # where response_schema ends up being stored as a JSON string.
    oracle = Oracle.model_construct(
        id=uuid4(),
        name="Oracle",
        endpoint_id=endpoint.id,
        status_code=200,
        required_headers=[],
        header_constraints={},
        response_schema=json.dumps(ground_truth.response_schema),
        json_path_assertions={},
        value_constraints={},
        business_rules=[],
        confidence_score=1.0,
        rationale=None,
        llm_model="mistral",
        generated_at=ground_truth.created_at,
    )

    calc = OracleMetricsCalculator()
    calc.add_ground_truth(ground_truth)

    metrics = calc.calculate_metrics(oracle=oracle, endpoint=endpoint)
    assert metrics.schema_precision == 1.0


def test_calculate_metrics_does_not_crash_on_unparseable_schema_string() -> None:
    endpoint = EndpointContext(name="Get foo", method=HTTPMethod.GET, url="/foo")

    ground_truth = GroundTruth(
        endpoint_id=endpoint.id,
        status_code=200,
        required_headers={},
        optional_headers={},
        response_schema={"type": "object", "properties": {"foo": {"type": "string"}}},
        business_rules=[],
        source="manual",
        confidence=1.0,
    )

    oracle = Oracle.model_construct(
        id=uuid4(),
        name="Oracle",
        endpoint_id=endpoint.id,
        status_code=200,
        required_headers=[],
        header_constraints={},
        response_schema="not-json",
        json_path_assertions={},
        value_constraints={},
        business_rules=[],
        confidence_score=1.0,
        rationale=None,
        llm_model="mistral",
        generated_at=ground_truth.created_at,
    )

    calc = OracleMetricsCalculator()
    calc.add_ground_truth(ground_truth)

    metrics = calc.calculate_metrics(oracle=oracle, endpoint=endpoint)
    # With an unparseable schema, we treat it as missing schema info.
    assert metrics.schema_precision == 0.0
