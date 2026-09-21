import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from memory.drayl_backend import DraylBackend, _digest


def test_append_is_immutable_and_source_linked():
    with DraylBackend() as archive:
        result = archive.append("source-a", {"text": "Triangulum signal"}, source_ref="TRIANGULUM/note-1", tags=["signal"])
        assert result["namespace"] == "TRIANGULUM/ANDROMALIUS"
        assert len(archive.query("Triangulum")) == 1
        assert archive.snapshot("source-a")["payload"] == {"text": "Triangulum signal"}


def test_snapshot_records_unchanged_and_changed_observations():
    with DraylBackend() as archive:
        assert archive.append("source-a", {"v": 1})["changed"] is True
        assert archive.append("source-a", {"v": 1})["changed"] is False
        assert archive.append("source-a", {"v": 2})["changed"] is True
        snapshots = archive.snapshot("source-a", latest=False)
        assert [row["changed"] for row in snapshots] == [True, False, True]


def test_query_ranks_resonance_and_returns_payload():
    with DraylBackend() as archive:
        archive.append("one", {"text": "moon archive"}, tags=["moon"])
        archive.append("two", {"text": "ordinary note"})
        results = archive.query("moon")
        assert results[0]["source_id"] == "one"
        assert results[0]["resonance"] >= 1
        assert results[0]["payload"]["text"] == "moon archive"


def test_receipt_hash_is_reproducible_and_verified():
    with DraylBackend() as archive:
        result = archive.append("source-a", {"x": 1})
        receipt = archive.receipt(result["event_id"])
        assert receipt["receipt_hash"] == result["receipt_hash"]
        unsigned = {key: receipt[key] for key in receipt if key not in ("receipt_id", "receipt_hash")}
        assert receipt["receipt_hash"] == _digest(unsigned)
        assert hashlib.sha256(json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == receipt["receipt_hash"]
