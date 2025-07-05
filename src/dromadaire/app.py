from dotenv import load_dotenv
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, Label, DataTable, SelectionList
from textual.containers import Horizontal, Container
from textual.screen import ModalScreen
from textual.reactive import reactive
from typing import List, Tuple
from .state import state

# Load environment variables from .env file
load_dotenv()

class AppHeader(Container):
    """Header component for trading app"""
    def __init__(self):
        super().__init__(id="app-header")
    
    def compose(self) -> ComposeResult:
        yield Static("🐪 DROMADAIRE", id="app-name")
        yield Static("v 0.1.0", id="app-version")


class Pools(Container):
    """Left panel showing trading pairs"""
    
    
    
    def __init__(self):
        super().__init__(id="trading-pairs-panel")
    
    def compose(self) -> ComposeResult:
        yield DataTable(id="pools-table")
    
    def on_mount(self) -> None:
        table = self.query_one("#pools-table", DataTable)
        table.add_columns("Pool", "TVL", "APR")
        table.loading = True
    
    @work(exclusive=True)
    async def load_pool_data(self) -> None:
        """Update the DataTable with pools data"""
        try:
            table = self.query_one("#pools-table", DataTable)
            table.loading = True
            table.clear()

            app_state = self.app.state
            pools = await app_state.load_pools()

            for pool in pools:
                # Extract pool information
                chain_name = pool.chain_name
                token_a = pool.token0.symbol if pool.token0 else 'N/A'
                token_b = pool.token1.symbol if pool.token1 else 'N/A'
                
                # Calculate TVL from reserves
                tvl = 0
                if pool.reserve0 and pool.reserve1:
                    try:
                        tvl = float(pool.reserve0.amount) + float(pool.reserve1.amount)
                    except (ValueError, AttributeError):
                        tvl = 0

                table.add_row(
                    f"[{chain_name}] {token_a} / {token_b}",
                    f"${tvl:,.2f}" if tvl > 0 else "N/A",
                    f"{pool.pool_fee:.2f}%" if pool.pool_fee else "N/A"
                )
        except Exception as e:
            self.show_error(str(e))
        finally:
            table.loading = False
    
    def show_error(self, error: str) -> None:
        """Show error message"""
        table = self.query_one("#pools-table", DataTable)
        self.app.notify(f"Error loading pools: {error}")
        

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
            yield Pools()
            yield PoolDetailsView()

class ChainSelectionScreen(ModalScreen):
    """Modal screen for chain selection"""
    def __init__(self, selected_chains: List[Tuple[str, str]], supported_chains: List[Tuple[str, str]]):
        super().__init__()
        self.selected, self.all = selected_chains, supported_chains

    def compose(self) -> ComposeResult:
        with Container(id="chain-selection-modal"):
            yield Label("Select Chains", id="chain-selection-title")
            yield SelectionList[str](*[(name, id, id in [chain_id for chain_id, _ in self.selected]) for id, name in self.all])
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
        self.state = state()
    
    def on_mount(self) -> None:
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
        def handle_chain_selection(selected_chains): self.selected_chains = self.state.select_chains(selected_chains)
        self.push_screen(ChainSelectionScreen(selected_chains=self.selected_chains, supported_chains=self.state.supported_chains), handle_chain_selection)
    
    async def watch_selected_chains(self, chains: List[Tuple[str, str]]) -> None:
        """Called when selected_chains changes"""
        # Sync with app state
        if chains:
            self.notify(f"Selected chains: {', '.join([chain_name for _, chain_name in chains])}")
            pools_widget = self.query_one(Pools)
            pools_widget.load_pool_data()
        else:
            self.notify("No chains selected")
