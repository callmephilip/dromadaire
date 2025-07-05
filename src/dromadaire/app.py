from dotenv import load_dotenv
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, Label, ListView, ListItem, SelectionList
from textual.containers import Horizontal, Container
from textual.screen import ModalScreen
from textual.reactive import reactive
from typing import List, Optional, Tuple
from .state import AppState

# Load environment variables from .env file
load_dotenv()

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

class ChainSelectionScreen(ModalScreen):
    """Modal screen for chain selection"""
    def __init__(self, selected_chains: List[Tuple[str, str]], supported_chains: List[Tuple[str, str]]):
        super().__init__()
        self.selected, self.all = selected_chains, supported_chains

    def compose(self) -> ComposeResult:
        currently_selected_ids = [chain_id for chain_id, _ in self.selected]
        with Container(id="chain-selection-modal"):
            yield Label("Select Chains", id="chain-selection-title")
            yield SelectionList[str](
                *[(name, id, id in currently_selected_ids) for id, name in self.all],
            )
            yield Label("Press Enter to confirm, Escape to cancel", id="chain-selection-help")
    
    def on_key(self, event) -> None:
        if event.key == "enter":
            selection_list = self.query_one(SelectionList)
            selected_chains = selection_list.selected
            self.dismiss(selected_chains)
        elif event.key == "escape":
            self.dismiss([])

class DromadaireApp(App):
    """Main trading application"""
    
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("c", "show_chain_selection", "Select chains"),
        ("q", "quit", "Quit"),
    ]
    
    TITLE = "Dromadaire"
    CSS_PATH = "app.tcss"
    
    # Global reactive state
    selected_chains: reactive[List[Tuple[str, str]]] = reactive([])

    def __init__(self):
        super().__init__()
        self.state = AppState()
        # Set default selected chains
        self.selected_chains = self.state.default_chains.copy()

    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield TradingInterface()
        yield Footer()
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_show_chain_selection(self) -> None:
        """Show the chain selection modal."""
        def handle_chain_selection(selected_chains):
            if selected_chains:
                # Convert selected chain IDs to tuples with names
                chains_data = self.state.supported_chains
                selected_tuples = [(chain_id, chain_name) for chain_id, chain_name in chains_data if chain_id in selected_chains]
                
                # Update both reactive state and app state
                self.selected_chains = selected_tuples
                self.state.selected_chains = selected_tuples
                # Get chain names for notification
                chain_names = [chain_name for _, chain_name in selected_tuples]
                self.notify(f"Selected chains: {', '.join(chain_names)}")
            else:
                self.selected_chains = []
                self.state.selected_chains = []
                self.notify("No chains selected")
        
        self.push_screen(ChainSelectionScreen(selected_chains=self.selected_chains, supported_chains=self.state.supported_chains), handle_chain_selection)
    
    def watch_selected_chains(self, chains: List[Tuple[str, str]]) -> None:
        """Called when selected_chains changes"""
        # Sync with app state
        self.state.selected_chains = chains
        # Update any UI components that depend on selected chains
        #self.refresh_trading_data()
    