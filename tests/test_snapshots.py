from unittest.mock import patch, AsyncMock
from dromadaire.app import DromadaireApp
from dromadaire.confiture import LiquidityPool, Token, Price, Amount, TokenBalance


def create_mock_pools():
    """Create a static list of mock LiquidityPools for testing"""
    # Create mock tokens
    eth_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x4200000000000000000000000000000000000006",
        symbol="WETH",
        decimals=18,
        listed=True
    )
    
    usdc_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        symbol="USDC",
        decimals=6,
        listed=True
    )
    
    op_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x4200000000000000000000000000000000000042",
        symbol="OP",
        decimals=18,
        listed=True
    )
    
    # Create mock prices
    eth_price = Price(token=eth_token, price=2500.0)
    usdc_price = Price(token=usdc_token, price=1.0)
    op_price = Price(token=op_token, price=2.5)
    
    # Create mock amounts
    eth_amount = Amount(token=eth_token, amount=1000000000000000000, price=eth_price)  # 1 WETH
    usdc_amount = Amount(token=usdc_token, amount=2500000000, price=usdc_price)  # 2500 USDC
    op_amount = Amount(token=op_token, amount=1000000000000000000, price=op_price)  # 1 OP
    
    # Create mock pools
    pools = [
        LiquidityPool(
            chain_id="10",
            chain_name="Optimism",
            lp="0x1234567890abcdef1234567890abcdef12345678",
            factory="0xF1046053aa5682b4F9a81b5481394DA16BE5FF5a",
            symbol="WETH/USDC",
            type=0,
            is_stable=False,
            is_cl=False,
            total_supply=1000000.0,
            decimals=18,
            token0=eth_token,
            reserve0=eth_amount,
            token1=usdc_token,
            reserve1=usdc_amount,
            token0_fees=Amount(token=eth_token, amount=0, price=eth_price),
            token1_fees=Amount(token=usdc_token, amount=0, price=usdc_price),
            pool_fee=0.003,
            gauge_total_supply=0.0,
            emissions=Amount(token=op_token, amount=0, price=op_price),
            emissions_token=op_token,
            weekly_emissions=Amount(token=op_token, amount=0, price=op_price),
            nfpm="0x0000000000000000000000000000000000000000",
            alm="0x0000000000000000000000000000000000000000"
        ),
        LiquidityPool(
            chain_id="10",
            chain_name="Optimism",
            lp="0xabcdef1234567890abcdef1234567890abcdef12",
            factory="0xF1046053aa5682b4F9a81b5481394DA16BE5FF5a",
            symbol="OP/USDC",
            type=0,
            is_stable=False,
            is_cl=False,
            total_supply=500000.0,
            decimals=18,
            token0=op_token,
            reserve0=op_amount,
            token1=usdc_token,
            reserve1=usdc_amount,
            token0_fees=Amount(token=op_token, amount=0, price=op_price),
            token1_fees=Amount(token=usdc_token, amount=0, price=usdc_price),
            pool_fee=0.003,
            gauge_total_supply=0.0,
            emissions=Amount(token=op_token, amount=0, price=op_price),
            emissions_token=op_token,
            weekly_emissions=Amount(token=op_token, amount=0, price=op_price),
            nfpm="0x0000000000000000000000000000000000000000",
            alm="0x0000000000000000000000000000000000000000"
        )
    ]
    
    return pools


def create_mock_wallet_address():
    """Create a consistent mock wallet address for testing"""
    return "0xac48b0f630f8c4c0c0b7a7f2c6e8f9b3a8d1a24"


def create_mock_balances():
    """Create a static list of mock TokenBalance objects for testing"""
    # Reuse the tokens from mock pools
    eth_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x4200000000000000000000000000000000000006",
        symbol="WETH",
        decimals=18,
        listed=True
    )
    
    usdc_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        symbol="USDC",
        decimals=6,
        listed=True
    )
    
    op_token = Token(
        chain_id="10",
        chain_name="Optimism",
        token_address="0x4200000000000000000000000000000000000042",
        symbol="OP",
        decimals=18,
        listed=True
    )
    
    # Create mock token balances
    balances = [
        TokenBalance(
            token=eth_token,
            balance=1.5,
            price_stable=2500.0
        ),
        TokenBalance(
            token=usdc_token,
            balance=1000.0,
            price_stable=1.0
        ),
        TokenBalance(
            token=op_token,
            balance=500.0,
            price_stable=2.5
        )
    ]
    
    return balances


@patch('dromadaire.state.AppState.load_pools', new_callable=AsyncMock)
@patch('dromadaire.state.AppState.wallet_address', new_callable=lambda: create_mock_wallet_address())
@patch('dromadaire.state.AppState.get_balances', new_callable=AsyncMock)
def test_app_snapshot(mock_get_balances, mock_wallet_address, mock_load_pools, snap_compare):
    """Test that the app matches the expected snapshot."""
    mock_load_pools.return_value = create_mock_pools()
    mock_get_balances.return_value = create_mock_balances()
    assert snap_compare(DromadaireApp(), terminal_size=(80, 24))

@patch('dromadaire.state.AppState.load_pools', new_callable=AsyncMock)
@patch('dromadaire.state.AppState.wallet_address', new_callable=lambda: create_mock_wallet_address())
@patch('dromadaire.state.AppState.get_balances', new_callable=AsyncMock)
def test_pools_navigate(mock_get_balances, mock_wallet_address, mock_load_pools, snap_compare):
    mock_load_pools.return_value = create_mock_pools()
    mock_get_balances.return_value = create_mock_balances()
    assert snap_compare(DromadaireApp(), press=["arrow_down"])

@patch('dromadaire.state.AppState.load_pools', new_callable=AsyncMock)
@patch('dromadaire.state.AppState.wallet_address', new_callable=lambda: create_mock_wallet_address())
@patch('dromadaire.state.AppState.get_balances', new_callable=AsyncMock)
def test_chain_selection_snapshot(mock_get_balances, mock_wallet_address, mock_load_pools, snap_compare):
    """Test the chain selection modal matches the expected snapshot."""
    mock_load_pools.return_value = create_mock_pools()
    mock_get_balances.return_value = create_mock_balances()
    assert snap_compare(DromadaireApp(), press=["c"])

@patch('dromadaire.state.AppState.load_pools', new_callable=AsyncMock)
@patch('dromadaire.state.AppState.wallet_address', new_callable=lambda: create_mock_wallet_address())
@patch('dromadaire.state.AppState.get_balances', new_callable=AsyncMock)
def test_chain_selection_with_add_base(mock_get_balances, mock_wallet_address, mock_load_pools, snap_compare):
    """Test chain selection: show chain selector and add Base added."""
    mock_load_pools.return_value = create_mock_pools()
    mock_get_balances.return_value = create_mock_balances()
    assert snap_compare(DromadaireApp(), press=["c", "space", "enter"])

@patch('dromadaire.state.AppState.load_pools', new_callable=AsyncMock)
@patch('dromadaire.state.AppState.wallet_address', new_callable=lambda: create_mock_wallet_address())
@patch('dromadaire.state.AppState.get_balances', new_callable=AsyncMock)
def test_wallet_screen_snapshot(mock_get_balances, mock_wallet_address, mock_load_pools, snap_compare):
    """Test the wallet screen matches the expected snapshot."""
    assert snap_compare(DromadaireApp(), press=["w", "esc"])