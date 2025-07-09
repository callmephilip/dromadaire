from textual.widgets import Label
from textual.reactive import reactive
from textual.message import Message


class AddressWidget(Label):
    """Widget for displaying shortened addresses in format: 0xac48...d1a24"""
    
    address: reactive[str] = reactive("")
    
    class Clicked(Message):
        """Message sent when address is clicked"""
        def __init__(self, widget: "AddressWidget") -> None:
            super().__init__()
            self.widget = widget
    
    def __init__(self, address: str = "", **kwargs):
        super().__init__(**kwargs)
        self.address = address
    
    def on_click(self) -> None:
        """Handle click events"""
        self.post_message(self.Clicked(self))
    
    def watch_address(self, address: str) -> None:
        """Update the display when address changes"""
        self.update(self.format_address(address))
    
    def format_address(self, address: str) -> str:
        """Format address to shortened version: 0xac48...d1a24"""
        if not address:
            return ""
        
        # Ensure address starts with 0x
        if not address.startswith("0x"):
            address = "0x" + address
        
        # Return full address if it's too short to shorten
        if len(address) <= 10:
            return address
        
        # Return shortened format: first 6 chars + ... + last 5 chars
        return f"{address[:6]}...{address[-5:]}"
    
    def on_mount(self) -> None:
        """Initialize the widget when mounted"""
        if self.address:
            self.update(self.format_address(self.address))