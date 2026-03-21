from numax.packs.install import install_pack


def test_pack_install_verified_bundle():
    result = install_pack("numax_repo_bundle")
    assert result.ok is True
