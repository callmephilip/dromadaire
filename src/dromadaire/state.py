import asyncio
from typing import List, Tuple
from sugar import get_async_chain
from sugar.pool import Pool

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
        self.chains = [get_async_chain(chain_id) for chain_id, _ in self.selected_chains]
        return self.selected_chains

    async def load_pools(self) -> List[Pool]:
        """Load pools from all selected chains concurrently"""
        pool_tasks = [chain.get_pools() for chain in self.chains]
        pools_results = await asyncio.gather(*pool_tasks)
        return [pool for pools in pools_results for pool in pools]


def state() -> 'AppState':
    """Get the singleton instance of AppState"""
    if not hasattr(state, "_instance"):
        state._instance = AppState()
    return state._instance