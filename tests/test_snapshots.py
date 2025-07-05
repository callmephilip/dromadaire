from dromadaire.app import DromadaireApp


def test_app_snapshot(snap_compare):
    """Test that the app matches the expected snapshot."""
    app = DromadaireApp()
    assert snap_compare(app, terminal_size=(80, 24))