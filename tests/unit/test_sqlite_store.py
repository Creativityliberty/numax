from pathlib import Path

from numax.storage.sqlite import SQLiteStore


def test_sqlite_store_roundtrip(tmp_path: Path) -> None:
    store = SQLiteStore(db_path=str(tmp_path / "numax.db"))
    store.set("sessions/test", {"ok": True})

    value = store.get("sessions/test")
    assert value == {"ok": True}
