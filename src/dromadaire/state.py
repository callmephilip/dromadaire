from typing import List, Tuple, Optional
from dromadaire.confiture import get_async_chain, get_chain, normalize_address, LiquidityPool


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
    def wallet_address(self) -> Optional[str]:
        """Get the wallet address from the first selected chain's account"""
        try:
            with get_chain("10") as chain:
                account = chain.account
                return account.address
        except Exception:
            return None

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
    
    def filter_pools(self, pools: List[LiquidityPool], query: str) -> List[LiquidityPool]:
        if not query or not query.strip():
            return pools
        
        query = query.strip().lower()
        try:
            normalized_query = normalize_address(query) if query.startswith('0x') else None
        except Exception:
            normalized_query = None
        
        filtered_pools = []
        
        for pool in pools:
            # Check for exact matches on pool address (if pool has address/lp attribute)
            if hasattr(pool, 'address') and normalized_query:
                if normalize_address(pool.address).lower() == normalized_query.lower():
                    filtered_pools.append(pool)
                    continue
            elif hasattr(pool, 'lp') and normalized_query:
                if normalize_address(pool.lp).lower() == normalized_query.lower():
                    filtered_pools.append(pool)
                    continue
            
            # Check for exact matches on pool name (if pool has name attribute)
            if hasattr(pool, 'name') and pool.name:
                if query == pool.name.lower():
                    filtered_pools.append(pool)
                    continue
            
            # Check token addresses
            if normalized_query:
                token0_addr = getattr(pool.token0, 'address', None)
                token1_addr = getattr(pool.token1, 'address', None)
                
                if token0_addr and normalize_address(token0_addr).lower() == normalized_query.lower():
                    filtered_pools.append(pool)
                    continue
                elif token1_addr and normalize_address(token1_addr).lower() == normalized_query.lower():
                    filtered_pools.append(pool)
                    continue
            
            # Fuzzy match on token names/symbols
            token0_symbol = getattr(pool.token0, 'symbol', '').lower()
            token1_symbol = getattr(pool.token1, 'symbol', '').lower()
            token0_name = getattr(pool.token0, 'name', '').lower()
            token1_name = getattr(pool.token1, 'name', '').lower()
            
            if (query in token0_symbol or query in token1_symbol or 
                query in token0_name or query in token1_name):
                filtered_pools.append(pool)
                continue
            
            # Fuzzy match on chain name
            chain_name = getattr(pool, 'chain_name', '').lower()
            if query in chain_name:
                filtered_pools.append(pool)
                continue
            
            # Fuzzy match on pool name (if exists)
            if hasattr(pool, 'name') and pool.name:
                if query in pool.name.lower():
                    filtered_pools.append(pool)
                    continue
        
        return filtered_pools
        


def state() -> 'AppState':
    """Get the singleton instance of AppState"""
    if not hasattr(state, "_instance"):
        state._instance = AppState()
    return state._instance