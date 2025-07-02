from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static
from rich_pixels import Pixels
from rich.console import Console

class DromadaireApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = "Dromadairez"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        logo_pixels = Pixels.from_image_path("assets/dromadaire.png", resize=(20, 20))
        yield Static(logo_pixels, id="logo")
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )