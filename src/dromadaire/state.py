from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
    
class AppState:
    """Centralized state management for Dromadaire"""
    
    @property
    def supported_chains(self) -> List[Tuple[str, str]]:
        """List of all supported chains"""
        return [
            ('10', 'Optimism'),
            ('8453', 'Base'),
            ('130', 'Unichain'),
            ('1135', 'Lisk'),
        ]
    
    @property
    def default_chains(self) -> List[Tuple[str, str]]:
        """Default selected chains"""
        return [
            ('10', 'Optimism'),
            ('1135', 'Lisk'),
        ]
    
    def __init__(self):
        self.selected_chains: List[Tuple[str, str]] = self.default_chains.copy()
        