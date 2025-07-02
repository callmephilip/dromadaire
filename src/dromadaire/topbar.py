from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Horizontal
from textual.app import ComposeResult
from dromadaire import __version__ as version

class TopBar(Widget):
    """Custom top bar widget inspired by dolphie."""

    def compose(self) -> ComposeResult:
        """Compose the top bar layout."""
        with Horizontal(id="top-bar"):
            yield Static("Dromadaire", id="app-title")
            yield Static("Ready", id="status-text")
            yield Static(version, id="version-text")