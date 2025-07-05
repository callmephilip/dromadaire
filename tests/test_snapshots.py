from dromadaire.app import DromadaireApp


def test_app_snapshot(snap_compare):
    """Test that the app matches the expected snapshot."""
    assert snap_compare(DromadaireApp(), terminal_size=(80, 24))

def test_chain_selection_snapshot(snap_compare):
    """Test the chain selection modal matches the expected snapshot."""
    assert snap_compare(DromadaireApp(), press=["c"])

def test_chain_selection_with_add_base(snap_compare):
    """Test chain selection: show chain selector and add Base added."""
    assert snap_compare(DromadaireApp(), press=["c", "space", "enter"])