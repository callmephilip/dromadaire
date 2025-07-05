from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, Button, Input, Label, ListView, ListItem
from textual.containers import Horizontal, Container


class AppHeader(Container):
    """Header component for trading app"""
    def __init__(self):
        super().__init__(id="app-header")
    
    def compose(self) -> ComposeResult:
        yield Static("🐪 DROMADAIRE", id="app-name")
        yield Static("v 0.1.0", id="app-version")


class TradingPairsList(Container):
    """Left panel showing trading pairs"""
    def __init__(self):
        super().__init__(id="trading-pairs-panel")
    
    def compose(self) -> ComposeResult:
        yield Label("Trading Pairs", id="pairs-title")
        yield ListView(id="pairs-list")
    
    def on_mount(self) -> None:
        pairs_data = [
            ("SolMTC / xSolMTC", "-$27,402.85", "-$13.74", "-$7,855,711.14", "2.2889%"),
            ("WETH / weTH", "-$148,605.07", "-$29.72", "-$6,555,101.58", "13.21%"),
            ("sTETH / WETH", "-$258,599.28", "-$129.29", "-$3,862,016.7", "7.49145%"),
            ("WETH / LSK", "-$138,738.18", "-$416.21", "-$3,833,273.06", "1.15353%"),
            ("USDTO / USDC-e", "-$107,258.28", "-$10.72", "-$3,611,322.83", "4.11165%"),
            ("wstETH / WETH", "-$2,168,703.72", "-$195.18", "-$2,850,446.8", "6.64301%"),
            ("USDC / STG", "-$71,281.57", "-$213.84", "-$2,841,479.04", "5.03788%"),
        ]
        
        pairs_list = self.query_one("#pairs-list", ListView)
        for pair_data in pairs_data:
            pairs_list.append(ListItem(Label(f"{pair_data[0]}")))
        
        


class PoolDetailsView(Container):
    """Right sidebar with deposit/trading form"""
    def __init__(self):
        super().__init__(id="pool-details-view")
    
    def compose(self) -> ComposeResult:
        yield Label("Pool details")

class TradingInterface(Container):
    """Main trading interface layout"""
    def compose(self) -> ComposeResult:
        with Horizontal(id="main-trading-area"):
            yield TradingPairsList()
            yield PoolDetailsView()

class DromadaireApp(App):
    """Main trading application"""
    
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]
    
    TITLE = "Dromadaire"
    CSS_PATH = "app.tcss"
    
    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield TradingInterface()
        yield Footer()
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
