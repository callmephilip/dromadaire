from dotenv import load_dotenv
from textual import work, on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, DataTable, SelectionList, Input
from dromadaire.widgets import AddressWidget
from textual.containers import Horizontal, Container, Vertical
from textual.screen import ModalScreen
from textual.reactive import reactive
from typing import List, Tuple
from dromadaire.state import state

# Load environment variables from .env file
load_dotenv()

class AppHeader(Container):
    """Header component for trading app"""
    def __init__(self, wallet_address: str = ""):
        super().__init__(id="app-header")
        self.wallet_address = wallet_address
        print(f">>>>>>>>>>>>>>>>>>>>>. Wallet address: {self.wallet_address}")
    
    def compose(self) -> ComposeResult:
        yield Label(" 🐪 dromadaire", id="app-name")
        yield Label("v 0.1.0", id="app-version")
        yield AddressWidget(address=self.wallet_address, id="wallet-address") if self.wallet_address else Label("No wallet connected", id="wallet-address") 


class Pools(Container):
    """Left panel showing trading pairs"""

    def __init__(self):
        super().__init__(id="trading-pairs-panel")
        self.search_visible = False
        self.all_pools = []
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(placeholder="Search pools...", id="pools-search", classes="hidden")
            yield DataTable(id="pools-table")
    
    def on_mount(self) -> None:
        table = self.query_one("#pools-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("Pool", "TVL", "APR", "LP Address")
        table.loading = True
    
    
    def toggle_search(self) -> None:
        """Toggle search bar visibility"""
        search_input = self.query_one("#pools-search", Input)
        if self.search_visible:
            search_input.add_class("hidden")
            self.search_visible = False
            # Clear search and show all pools
            search_input.value = ""
            self.update_table_with_pools(self.all_pools)
            # Focus back to table
            self.query_one("#pools-table", DataTable).focus()
        else:
            search_input.remove_class("hidden")
            self.search_visible = True
            search_input.focus()
    
    def on_input_changed(self, event) -> None:
        """Handle search input changes"""
        if event.input.id == "pools-search":
            query = event.value
            if query:
                app_state = self.app.state
                filtered_pools = app_state.filter_pools(self.all_pools, query)
                self.update_table_with_pools(filtered_pools)
            else:
                self.update_table_with_pools(self.all_pools)
    
    def on_key(self, event) -> None:
        """Handle key events"""
        if event.key == "escape" and self.search_visible:
            # Clear search and exit search mode
            self.toggle_search()
            event.stop()
    
    def update_table_with_pools(self, pools) -> None:
        """Update DataTable with given pools"""
        table = self.query_one("#pools-table", DataTable)
        table.clear()
        
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

            # Get LP address and format it
            lp_address = getattr(pool, 'lp', '') or getattr(pool, 'address', '')
            formatted_lp = AddressWidget().format_address(lp_address) if lp_address else "N/A"
            
            table.add_row(
                f"[{chain_name}] {token_a} / {token_b}",
                f"${tvl:,.2f}" if tvl > 0 else "N/A",
                f"{pool.pool_fee:.2f}%" if pool.pool_fee else "N/A",
                formatted_lp,
                key=pool.lp  # Use pool LP address as row key for easy lookup
            )
    
    @work(exclusive=True)
    async def load_pool_data(self) -> None:
        """Update the DataTable with pools data"""
        try:
            table = self.query_one("#pools-table", DataTable)
            table.loading = True
            table.clear()

            app_state = self.app.state
            pools = await app_state.load_pools()
            self.all_pools = pools  # Store all pools for filtering

            self.update_table_with_pools(pools)
        except Exception as e:
            self.show_error(str(e))
        finally:
            table.loading = False
            # Set focus on the DataTable after pools are loaded
            table.focus()
    
    def show_error(self, error: str) -> None:
        """Show error message"""
        self.app.notify(f"Error loading pools: {error}")
    
    def get_pool_by_lp_address(self, lp_address: str):
        """Get pool object by LP address"""
        for pool in self.all_pools:
            if pool.lp == lp_address:
                return pool
        return None
   
    @on(DataTable.RowHighlighted)
    def on_pool_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle pool highlighting (arrow key navigation) to show details"""
        if event.data_table.id != "pools-table":
            return  # Only handle our pools table
        
        # Get the highlighted pool using the row key (which is the LP address)
        highlighted_pool = self.get_pool_by_lp_address(event.row_key)
        
        if highlighted_pool:
            # Get the pool details view and update it
            pool_details = self.parent.query_one(PoolDetailsView)
            pool_details.update_pool_details(highlighted_pool)
        

class PoolDetailsView(Container):
    """Right sidebar with deposit/trading form"""
    def __init__(self):
        super().__init__(id="pool-details-view")
        self.current_pool = None
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("", id="pool-details-content")
    
    def update_pool_details(self, pool) -> None:
        """Update the pool details view with selected pool information"""
        self.current_pool = pool
        
        # Format pool information
        chain_name = pool.chain_name
        token_a = pool.token0.symbol if pool.token0 else 'N/A'
        token_b = pool.token1.symbol if pool.token1 else 'N/A'
        
        # Calculate TVL
        tvl = 0
        if pool.reserve0 and pool.reserve1:
            try:
                tvl = pool.tvl if hasattr(pool, 'tvl') else (float(pool.reserve0.amount) + float(pool.reserve1.amount))
            except (ValueError, AttributeError):
                tvl = 0
        
        # Format details text
        details_text = f"""🏊 {token_a} / {token_b}
📍 Chain: {chain_name}
💰 TVL: ${tvl:,.2f}
📊 Pool Fee: {pool.pool_fee:.2f}%
🏭 Type: {'Stable' if pool.is_stable else 'Volatile'}
📍 LP Address: {AddressWidget().format_address(pool.lp)}

💎 Token Details:
{token_a}: {AddressWidget().format_address(pool.token0.token_address)}...
{token_b}: {AddressWidget().format_address(pool.token1.token_address)}...

📈 Reserves:
{token_a}: {pool.reserve0.amount:,.2f}
{token_b}: {pool.reserve1.amount:,.2f}

🎯 Pool Info:
Factory: {pool.factory[:10]}...
Total Supply: {pool.total_supply:,.2f}
Decimals: {pool.decimals}"""
        
        # Update the content label
        content_label = self.query_one("#pool-details-content", Label)
        content_label.update(details_text)

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

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Pick your chains"

    def compose(self) -> ComposeResult:
        with Container(id="chain-selection-modal"):
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
        ("s", "toggle_search", "Toggle search"),
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
        yield AppHeader(wallet_address=self.state.wallet_address)
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
    
    def action_toggle_search(self) -> None:
        """Toggle search bar visibility in pools."""
        pools_widget = self.query_one(Pools)
        pools_widget.toggle_search()
    
    async def watch_selected_chains(self, chains: List[Tuple[str, str]]) -> None:
        """Called when selected_chains changes"""
        # Sync with app state
        if chains:
            self.notify(f"Selected chains: {', '.join([chain_name for _, chain_name in chains])}")
            pools_widget = self.query_one(Pools)
            pools_widget.load_pool_data()
        else:
            self.notify("No chains selected")
