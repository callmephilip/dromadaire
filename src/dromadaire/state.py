import asyncio
from typing import List, Tuple
from sugar import get_async_chain
from sugar.pool import LiquidityPool

class AppState:
    """Centralized state management for Dromadaire"""
    
    @property
    def supported_chains(self) -> List[Tuple[str, str]]:
        """List of all supported chains"""
        return sorted([
            ('10', 'Optimism'),
            ('8453', 'Base'),
            ('130', 'Unichain'),
            ('1135', 'Lisk'),
        ], key=lambda x: x[1])
    
    @property
    def default_chains(self) -> List[Tuple[str, str]]:
        """Default selected chains"""
        return [
            ('10', 'Optimism'),
            ('1135', 'Lisk'),
        ]
    
    @property
    def selected_chains(self) -> List[Tuple[str, str]]:
        """Currently selected chains"""
        return sorted(self._selected_chains, key=lambda x: x[1])

    def __init__(self):
        self._selected_chains: List[Tuple[str, str]] = self.default_chains.copy()
        self.chains = [get_async_chain(chain_id) for chain_id, _ in self.selected_chains]

    def select_chains(self, chains: List[str]) -> List[Tuple[str, str]]:
        """Update selected chains"""
        self._selected_chains = [(chain_id, chain_name) for chain_id, chain_name in self.supported_chains if chain_id in chains]
        
        # Create a mapping of existing chains by chain_id
        existing_chains = {chain.chain_id: chain for chain in self.chains}
        
        # Build new chains list, preserving existing instances where possible
        new_chains = []
        for chain_id, _ in self.selected_chains:
            if chain_id in existing_chains:
                # Preserve existing chain instance
                new_chains.append(existing_chains[chain_id])
            else:
                # Create new chain instance
                new_chains.append(get_async_chain(chain_id))
        
        self.chains = new_chains
        return self.selected_chains

    async def load_pools(self) -> List[LiquidityPool]:
        """Load pools from all selected chains concurrently"""
        all_pools = []
        for chain in self.chains:
            async with chain:
                pools = await chain.get_pools()
                all_pools.extend(pools)
        return all_pools


def state() -> 'AppState':
    """Get the singleton instance of AppState"""
    if not hasattr(state, "_instance"):
        state._instance = AppState()
    return state._instance