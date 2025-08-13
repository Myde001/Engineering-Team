```markdown
# Design for accounts.py module

## Overview
The `accounts.py` module will contain a single main class `Account` that manages the trading simulation platform user account. It supports account creation, fund management (deposit/withdrawal), recording trades (buy/sell shares), portfolio valuation, profit and loss calculation, query of holdings and transaction history, and enforces business rules to prevent invalid operations.

The module also includes a standalone function `get_share_price(symbol: str) -> float` which returns current prices for supported symbols (`AAPL`, `TSLA`, `GOOGL`) with fixed test values.

---

## Module Components

### Function

#### get_share_price(symbol: str) -> float
- Returns the current price of the share symbol requested.
- Test implementation with fixed prices:
  - AAPL: $150.00
  - TSLA: $700.00
  - GOOGL: $2800.00
- Raises a ValueError if an unsupported symbol is requested.

---

### Class: Account

#### Constructor
```python
def __init__(self, user_id: str)
```
- Initializes a new account for the given user ID.
- Starts with zero balance, zero stock holdings, and no transactions.
- Records initial deposit amount as zero (to track profit/loss relative to deposits).

#### Deposit Method
```python
def deposit(self, amount: float) -> None
```
- Adds funds to the cash balance.
- Record this as a transaction of type "deposit".
- Rejects negative or zero deposit amounts with ValueError.

#### Withdraw Method
```python
def withdraw(self, amount: float) -> None
```
- Subtracts funds from the cash balance.
- Ensure balance does not go negative after withdrawal.
- Records transaction of type "withdraw".
- Reject negative or zero amounts or withdrawals causing negative balance.

#### Buy Shares Method
```python
def buy_shares(self, symbol: str, quantity: int) -> None
```
- Allows purchase of shares of `symbol` with positive integer `quantity`.
- Uses `get_share_price(symbol)` to get current price.
- Checks if user has sufficient cash balance to buy `quantity * price`.
- Updates cash balance and holdings accordingly.
- Records transaction of type "buy".
- Raises ValueError if invalid quantity, unsupported symbol, or insufficient cash.

#### Sell Shares Method
```python
def sell_shares(self, symbol: str, quantity: int) -> None
```
- Allows selling of shares of `symbol` for positive integer `quantity`.
- Checks if user holds at least `quantity` shares.
- Uses `get_share_price(symbol)` to get current price.
- Increases cash balance by `quantity * price`.
- Updates holdings accordingly.
- Records transaction of type "sell".
- Raises ValueError if invalid quantity, unsupported symbol, or insufficient shares.

#### Get Holdings Method
```python
def get_holdings(self) -> Dict[str, int]
```
- Returns a dictionary mapping symbols to quantities currently held.
- Symbols with zero holdings should be excluded.

#### Get Portfolio Value Method
```python
def get_portfolio_value(self) -> float
```
- Calculates total value = cash balance + sum over all holdings of (quantity * current share price).
- Uses `get_share_price` for current market prices.

#### Get Profit/Loss Method
```python
def get_profit_loss(self) -> float
```
- Returns the profit or loss as:
  (Current portfolio value) - (Total net deposits)
- Net deposits = sum of all deposits minus sum of all withdrawals.
- Profit/loss reflects trading outcome and cash flow.

#### Get Transaction History Method
```python
def get_transactions(self) -> List[Dict]
```
- Returns a chronological list of all transactions.
- Each transaction is a dictionary with keys:
  - `type`: one of "deposit", "withdraw", "buy", "sell"
  - `symbol`: stock symbol if applicable, else None
  - `quantity`: for buy/sell transactions, else None
  - `amount`: amount of money deposited/withdrawn or total cost/proceeds for trade
  - `timestamp`: datetime of transaction (ISO format string preferred)
- History allows tracking complete account activity over time.

---

## Data Structures Inside Account Class

- `self.cash_balance: float` — available funds for trading.
- `self.holdings: Dict[str, int]` — maps symbols to share quantities.
- `self.transactions: List[Dict]` — logs every deposit, withdrawal, buy, and sell with details and timestamps.
- `self.initial_deposit: float` — tracks total deposits minus withdrawals to calculate profit/loss baseline.

---

## Validation and Errors

- All monetary amounts must be positive where applicable.
- Buying shares requires sufficient cash balance.
- Selling shares requires sufficient share quantity.
- Withdrawal cannot cause negative cash balance.
- Unsupported symbols cause ValueError on buy/sell.
- Quantity of shares must be positive integers.
- Deposits and withdrawals reject zero or negative amounts.

---

## Example Usage (not part of the module, for illustration only)

```python
acct = Account("user123")
acct.deposit(10000)
acct.buy_shares("AAPL", 50)
acct.sell_shares("AAPL", 10)
portfolio_value = acct.get_portfolio_value()
profit_loss = acct.get_profit_loss()
transactions = acct.get_transactions()
```

---

This detailed design gives a clear, self-contained, testable, and extensible Python module structure named `accounts.py` with a single class `Account` plus `get_share_price` helper, ready for implementation.