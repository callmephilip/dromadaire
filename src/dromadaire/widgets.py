from textual.widgets import Label
from textual.reactive import reactive


class AddressWidget(Label):
    """Widget for displaying shortened addresses in format: 0xac48...d1a24"""
    
    address: reactive[str] = reactive("")
    
    def __init__(self, address: str = "", **kwargs):
        super().__init__(**kwargs)
        self.address = address
    
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