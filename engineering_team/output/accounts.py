from datetime import datetime
from typing import Dict, List, Union

def get_share_price(symbol: str) -> float:
    if symbol == 'AAPL':
        return 150.00
    elif symbol == 'TSLA':
        return 700.00
    elif symbol == 'GOOGL':
        return 2800.00
    else:
        raise ValueError('Unsupported symbol')

class Account:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.cash_balance = 0.0
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = 0.0

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive.')
        self.cash_balance += amount
        self.initial_deposit += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive.')
        if self.cash_balance - amount < 0:
            raise ValueError('Cannot withdraw more than the available balance.')
        self.cash_balance -= amount
        self.transactions.append({
            'type': 'withdraw',
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be a positive integer.')
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.cash_balance:
            raise ValueError('Insufficient funds to buy shares.')
        self.cash_balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'amount': total_cost,
            'timestamp': datetime.now().isoformat()
        })

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be a positive integer.')
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError('Insufficient shares to sell.')
        price = get_share_price(symbol)
        total_proceeds = price * quantity
        self.cash_balance += total_proceeds
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'amount': total_proceeds,
            'timestamp': datetime.now().isoformat()
        })

    def get_holdings(self) -> Dict[str, int]:
        return {symbol: quantity for symbol, quantity in self.holdings.items() if quantity > 0}

    def get_portfolio_value(self) -> float:
        total_value = self.cash_balance
        for symbol, quantity in self.holdings.items():
            total_value += quantity * get_share_price(symbol)
        return total_value

    def get_profit_loss(self) -> float:
        net_deposits = self.initial_deposit - sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'withdraw')
        return self.get_portfolio_value() - net_deposits

    def get_transactions(self) -> List[Dict[str, Union[str, float, int]]]:
        return self.transactions.copy()