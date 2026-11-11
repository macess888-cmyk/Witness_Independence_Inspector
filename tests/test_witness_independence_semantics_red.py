import json
from pathlib import Path

import pytest

from witness_independence.inspector import (
    WitnessIndependenceDiagnostic,
    WitnessIndependenceState,
    inspect_witness_independence,
)

CASES = (
    Path(__file__).parent.parent
    / "specimens"
    / "witness_independence"
)


def load_case(filename: str) -> dict:
    return json.loads(
        (CASES / filename).read_text(encoding="utf-8")
    )


def inspect_case(filename: str):
    data = load_case(filename)

    return inspect_witness_independence(
        receipts=data["receipts"],
        source_independence_known=data[
            "source_independence_known"
        ],
    )


def test_single_source_does_not_establish_independence() -> None:
    result = inspect_case("WI-00_SINGLE_SOURCE.json")

    assert (
        result.state
        is WitnessIndependenceState.INDEPENDENCE_NOT_ESTABLISHED
    )
    assert result.diagnostics == (
        WitnessIndependenceDiagnostic.INSUFFICIENT_INDEPENDENT_ORIGINS,
    )


def test_two_receipts_same_source_are_correlated() -> None:
    result = inspect_case(
        "WI-01_TWO_RECEIPTS_SAME_SOURCE.json"
    )

    assert result.state is WitnessIndependenceState.CORRELATED_SOURCE
    assert result.diagnostics == (
        WitnessIndependenceDiagnostic.SHARED_UPSTREAM_SOURCE,
    )


def test_independent_sources_establish_independence() -> None:
    result = inspect_case("WI-02_INDEPENDENT_SOURCES.json")

    assert (
        result.state
        is WitnessIndependenceState.INDEPENDENCE_ESTABLISHED
    )
    assert result.diagnostics == ()


def test_shared_derived_dataset_is_correlated() -> None:
    result = inspect_case(
        "WI-03_SHARED_DERIVED_DATASET.json"
    )

    assert result.state is WitnessIndependenceState.CORRELATED_SOURCE
    assert result.diagnostics == (
        WitnessIndependenceDiagnostic.SHARED_DERIVED_DATASET,
    )


def test_unknown_source_independence_holds() -> None:
    result = inspect_case(
        "WI-04_INDEPENDENCE_UNKNOWN.json"
    )

    assert result.state is WitnessIndependenceState.HOLD
    assert result.diagnostics == (
        WitnessIndependenceDiagnostic.INDEPENDENCE_UNKNOWN,
    )


def test_expected_standing_is_not_inspection_input() -> None:
    data = load_case(
        "WI-01_TWO_RECEIPTS_SAME_SOURCE.json"
    )

    data["expected_standing"] = "INDEPENDENCE_ESTABLISHED"

    result = inspect_witness_independence(
        receipts=data["receipts"],
        source_independence_known=data[
            "source_independence_known"
        ],
    )

    assert result.state is WitnessIndependenceState.CORRELATED_SOURCE
    assert result.diagnostics == (
        WitnessIndependenceDiagnostic.SHARED_UPSTREAM_SOURCE,
    )


def test_correlated_result_does_not_discard_evidence() -> None:
    result = inspect_case(
        "WI-03_SHARED_DERIVED_DATASET.json"
    )

    assert not hasattr(result, "discard_evidence")
    assert not hasattr(result, "claim_truth")
    assert not hasattr(result, "authority")


@pytest.mark.parametrize(
    ("filename", "expected_state"),
    [
        (
            "WI-00_SINGLE_SOURCE.json",
            WitnessIndependenceState.INDEPENDENCE_NOT_ESTABLISHED,
        ),
        (
            "WI-01_TWO_RECEIPTS_SAME_SOURCE.json",
            WitnessIndependenceState.CORRELATED_SOURCE,
        ),
        (
            "WI-02_INDEPENDENT_SOURCES.json",
            WitnessIndependenceState.INDEPENDENCE_ESTABLISHED,
        ),
        (
            "WI-03_SHARED_DERIVED_DATASET.json",
            WitnessIndependenceState.CORRELATED_SOURCE,
        ),
        (
            "WI-04_INDEPENDENCE_UNKNOWN.json",
            WitnessIndependenceState.HOLD,
        ),
    ],
)
def test_case_state_matrix(
    filename: str,
    expected_state: WitnessIndependenceState,
) -> None:
    result = inspect_case(filename)

    assert result.state is expected_state