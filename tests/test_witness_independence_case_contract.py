import json
from pathlib import Path

CASES = (
    Path(__file__).parent.parent
    / "specimens"
    / "witness_independence"
)

EXPECTED = {
    "WI-00_SINGLE_SOURCE.json": "INDEPENDENCE_NOT_ESTABLISHED",
    "WI-01_TWO_RECEIPTS_SAME_SOURCE.json": "CORRELATED_SOURCE",
    "WI-02_INDEPENDENT_SOURCES.json": "INDEPENDENCE_ESTABLISHED",
    "WI-03_SHARED_DERIVED_DATASET.json": "CORRELATED_SOURCE",
    "WI-04_INDEPENDENCE_UNKNOWN.json": "HOLD",
}


def load_case(filename: str) -> dict:
    return json.loads(
        (CASES / filename).read_text(encoding="utf-8")
    )


def test_all_witness_independence_cases_are_present() -> None:
    present = {path.name for path in CASES.glob("WI-*.json")}
    assert present == set(EXPECTED)


def test_case_ids_match_filenames() -> None:
    for filename in EXPECTED:
        data = load_case(filename)
        assert filename.startswith(data["case_id"])


def test_expected_standings_are_explicit() -> None:
    for filename, expected in EXPECTED.items():
        assert load_case(filename)["expected_standing"] == expected


def test_single_source_does_not_establish_independence() -> None:
    data = load_case("WI-00_SINGLE_SOURCE.json")

    assert len(data["receipts"]) == 1
    assert len({r["source_id"] for r in data["receipts"]}) == 1


def test_two_receipts_same_source_are_explicitly_correlated() -> None:
    data = load_case("WI-01_TWO_RECEIPTS_SAME_SOURCE.json")

    assert len(data["receipts"]) == 2
    assert len({r["source_id"] for r in data["receipts"]}) == 1


def test_distinct_sources_are_explicit() -> None:
    data = load_case("WI-02_INDEPENDENT_SOURCES.json")

    assert len({r["source_id"] for r in data["receipts"]}) == 2
    assert data["source_independence_known"] is True


def test_shared_derived_dataset_is_explicit() -> None:
    data = load_case("WI-03_SHARED_DERIVED_DATASET.json")

    derived = {
        r["derived_dataset_id"]
        for r in data["receipts"]
        if r["derived_dataset_id"] is not None
    }

    assert derived == {"D1"}


def test_unknown_independence_is_explicit() -> None:
    data = load_case("WI-04_INDEPENDENCE_UNKNOWN.json")

    assert data["source_independence_known"] is False