from numax.storage.memory_store import InMemoryStore
from numax.storage.repos import SessionRepository


def test_store_interface_compatible_with_repo() -> None:
    store = InMemoryStore()
    repo = SessionRepository(store)
    repo.save("s1", {"ok": True})
    assert repo.get("s1") == {"ok": True}
