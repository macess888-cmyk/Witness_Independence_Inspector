from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class WitnessIndependenceState(str, Enum):
    INDEPENDENCE_ESTABLISHED = "INDEPENDENCE_ESTABLISHED"
    CORRELATED_SOURCE = "CORRELATED_SOURCE"
    INDEPENDENCE_NOT_ESTABLISHED = "INDEPENDENCE_NOT_ESTABLISHED"
    HOLD = "HOLD"


class WitnessIndependenceDiagnostic(str, Enum):
    INSUFFICIENT_INDEPENDENT_ORIGINS = (
        "INSUFFICIENT_INDEPENDENT_ORIGINS"
    )
    SHARED_UPSTREAM_SOURCE = "SHARED_UPSTREAM_SOURCE"
    SHARED_DERIVED_DATASET = "SHARED_DERIVED_DATASET"
    INDEPENDENCE_UNKNOWN = "INDEPENDENCE_UNKNOWN"


@dataclass(frozen=True)
class WitnessIndependenceFinding:
    state: WitnessIndependenceState
    diagnostics: tuple[WitnessIndependenceDiagnostic, ...]


def _values(
    receipts: Sequence[Mapping[str, object]],
    field: str,
) -> list[str]:
    return [
        value
        for receipt in receipts
        if isinstance((value := receipt.get(field)), str)
        and value
    ]


def inspect_witness_independence(
    *,
    receipts: Sequence[Mapping[str, object]],
    source_independence_known: bool,
) -> WitnessIndependenceFinding:
    if not source_independence_known:
        return WitnessIndependenceFinding(
            state=WitnessIndependenceState.HOLD,
            diagnostics=(
                WitnessIndependenceDiagnostic.INDEPENDENCE_UNKNOWN,
            ),
        )

    source_ids = _values(receipts, "source_id")

    derived_dataset_ids = _values(
        receipts,
        "derived_dataset_id",
    )

    if len(receipts) < 2 or len(set(source_ids)) < 2:
        if len(receipts) >= 2:
            return WitnessIndependenceFinding(
                state=WitnessIndependenceState.CORRELATED_SOURCE,
                diagnostics=(
                    WitnessIndependenceDiagnostic.SHARED_UPSTREAM_SOURCE,
                ),
            )

        return WitnessIndependenceFinding(
            state=(
                WitnessIndependenceState
                .INDEPENDENCE_NOT_ESTABLISHED
            ),
            diagnostics=(
                WitnessIndependenceDiagnostic
                .INSUFFICIENT_INDEPENDENT_ORIGINS,
            ),
        )

    if (
        derived_dataset_ids
        and len(set(derived_dataset_ids)) < len(derived_dataset_ids)
    ):
        return WitnessIndependenceFinding(
            state=WitnessIndependenceState.CORRELATED_SOURCE,
            diagnostics=(
                WitnessIndependenceDiagnostic.SHARED_DERIVED_DATASET,
            ),
        )

    return WitnessIndependenceFinding(
        state=WitnessIndependenceState.INDEPENDENCE_ESTABLISHED,
        diagnostics=(),
    )