from pathlib import Path

from numax.storage.local_json import LocalJsonStore


def test_local_json_store_roundtrip(tmp_path: Path) -> None:
    store = LocalJsonStore(root_dir=str(tmp_path))
    store.set("sessions/test", {"ok": True})

    value = store.get("sessions/test")

    assert value == {"ok": True}
