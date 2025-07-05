from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .data import get_supported_chains

@dataclass
class TradingPair:
    """Represents a trading pair with its data"""
    symbol: str
    pnl: str
    pnl_24h: str
    volume: str
    apr: str

@dataclass
class ChainInfo:
    """Represents blockchain information"""
    chain_id: str
    name: str
    connected: bool = False
    rpc_url: Optional[str] = None
    
class AppState:
    """Centralized state management for Dromadaire"""
    
    def __init__(self):
        self.selected_chains: List[str] = []
        self.trading_pairs: Dict[str, TradingPair] = {}
        self.chain_info: Dict[str, ChainInfo] = {}
        self.user_preferences: Dict[str, Any] = {
            "theme": "dark",
            "refresh_interval": 5.0,
            "default_slippage": 0.5
        }
        self._initialize_chains()
    
    def _initialize_chains(self) -> None:
        """Initialize chain information from supported chains"""
        for chain_id, chain_name in get_supported_chains():
            self.chain_info[chain_id] = ChainInfo(
                chain_id=chain_id,
                name=chain_name
            )
    
    def add_chain(self, chain_id: str) -> bool:
        """Add a chain to selected chains"""
        if chain_id not in self.selected_chains and chain_id in self.chain_info:
            self.selected_chains.append(chain_id)
            return True
        return False
    
    def remove_chain(self, chain_id: str) -> bool:
        """Remove a chain from selected chains"""
        if chain_id in self.selected_chains:
            self.selected_chains.remove(chain_id)
            return True
        return False
    
    def get_selected_chain_names(self) -> List[str]:
        """Get names of selected chains"""
        return [self.chain_info[chain_id].name 
                for chain_id in self.selected_chains 
                if chain_id in self.chain_info]
    
    def get_selected_chain_info(self) -> List[ChainInfo]:
        """Get ChainInfo objects for selected chains"""
        return [self.chain_info[chain_id] 
                for chain_id in self.selected_chains 
                if chain_id in self.chain_info]
    
    def update_chain_connection(self, chain_id: str, connected: bool, rpc_url: Optional[str] = None) -> None:
        """Update chain connection status"""
        if chain_id in self.chain_info:
            self.chain_info[chain_id].connected = connected
            if rpc_url:
                self.chain_info[chain_id].rpc_url = rpc_url
    
    def add_trading_pair(self, symbol: str, pnl: str, pnl_24h: str, volume: str, apr: str) -> None:
        """Add or update a trading pair"""
        self.trading_pairs[symbol] = TradingPair(
            symbol=symbol,
            pnl=pnl,
            pnl_24h=pnl_24h,
            volume=volume,
            apr=apr
        )
    
    def get_trading_pairs_for_chains(self, chain_ids: List[str]) -> List[TradingPair]:
        """Get trading pairs available for specific chains"""
        # TODO: Implement chain-specific filtering
        return list(self.trading_pairs.values())
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update user preference"""
        self.user_preferences[key] = value
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        return self.user_preferences.get(key, default)
    
    def reset_state(self) -> None:
        """Reset application state"""
        self.selected_chains.clear()
        self.trading_pairs.clear()
        for chain_info in self.chain_info.values():
            chain_info.connected = False
            chain_info.rpc_url = None