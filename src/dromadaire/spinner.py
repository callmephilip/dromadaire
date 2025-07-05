from rich.spinner import Spinner
from textual.widgets import Static


class SpinnerWidget(Static):
    """A spinner widget for loading animations."""
    
    def __init__(self, spinner_type="dots", text="Loading...", speed=1.0, id=None):
        """Initialize the spinner widget.
        
        Args:
            spinner_type: Type of spinner animation (dots, line, moon, bouncingBar, etc.)
            text: Text to display alongside the spinner
            speed: Animation speed multiplier
            id: Widget ID for styling
        """
        super().__init__("", id=id)
        self._spinner = Spinner(spinner_type, text=text, speed=speed)
        self.update_timer = None

    def on_mount(self) -> None:
        """Start the spinner animation when mounted."""
        self.update_timer = self.set_interval(1 / 60, self.update_spinner)

    def on_unmount(self) -> None:
        """Stop the spinner animation when unmounted."""
        if self.update_timer:
            self.update_timer.stop()

    def update_spinner(self) -> None:
        """Update the spinner animation frame."""
        self.update(self._spinner)

    def set_text(self, text: str) -> None:
        """Update the spinner text."""
        self._spinner.text = text

    def set_spinner_type(self, spinner_type: str) -> None:
        """Change the spinner animation type."""
        current_text = self._spinner.text
        current_speed = self._spinner.speed
        self._spinner = Spinner(spinner_type, text=current_text, speed=current_speed)

    def show_spinner(self) -> None:
        """Show the spinner."""
        self.display = True

    def hide_spinner(self) -> None:
        """Hide the spinner."""
        self.display = False