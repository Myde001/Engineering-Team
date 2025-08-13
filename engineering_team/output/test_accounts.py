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

import unittest

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('user123')

    def test_deposit_positive_amount(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.cash_balance, 100.0)
        self.assertEqual(self.account.initial_deposit, 100.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'deposit')

    def test_deposit_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    def test_withdraw_positive_amount(self):
        self.account.deposit(200)
        self.account.withdraw(50)
        self.assertEqual(self.account.cash_balance, 150)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'withdraw')

    def test_withdraw_more_than_balance_raises(self):
        self.account.deposit(50)
        with self.assertRaises(ValueError):
            self.account.withdraw(100)

    def test_withdraw_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-20)

    def test_buy_shares_success(self):
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 5)  # 5 * 150 = 750
        self.assertAlmostEqual(self.account.cash_balance, 250)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(self.account.transactions[-1]['type'], 'buy')

    def test_buy_shares_insufficient_funds_raises(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 1)

    def test_buy_shares_negative_quantity_raises(self):
        self.account.deposit(1000)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -1)

    def test_buy_shares_invalid_symbol_raises(self):
        self.account.deposit(1000)
        with self.assertRaises(ValueError):
            self.account.buy_shares('INVALID', 1)

    def test_sell_shares_success(self):
        self.account.deposit(1000)
        self.account.buy_shares('TSLA', 1)  # 700
        self.account.sell_shares('TSLA', 1)  # sell 1 share
        self.assertEqual(self.account.cash_balance, 1000)  # back to original
        self.assertNotIn('TSLA', self.account.holdings)
        self.assertEqual(self.account.transactions[-1]['type'], 'sell')

    def test_sell_shares_insufficient_quantity_raises(self):
        self.account.deposit(1000)
        self.account.buy_shares('TSLA', 1)
        with self.assertRaises(ValueError):
            self.account.sell_shares('TSLA', 2)

    def test_sell_shares_negative_quantity_raises(self):
        self.account.deposit(1000)
        self.account.buy_shares('TSLA', 1)
        with self.assertRaises(ValueError):
            self.account.sell_shares('TSLA', -1)

    def test_get_holdings(self):
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 2, 'TSLA': 1})

    def test_get_portfolio_value(self):
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 2)  # 300
        expected_value = self.account.cash_balance + 2*150
        self.assertEqual(self.account.get_portfolio_value(), expected_value)

    def test_get_profit_loss(self):
        self.account.deposit(2000)
        with self.assertRaises(ValueError):
            self.account.buy_shares('GOOGL', 1)  # too expensive
        self.account.buy_shares('AAPL', 10)  # 1500
        self.account.withdraw(200)  # withdraw 200
        profit_loss_before = self.account.get_profit_loss()
        self.account.sell_shares('AAPL', 10)  # get back 1500
        profit_loss_after = self.account.get_profit_loss()
        self.assertTrue(profit_loss_after >= profit_loss_before)

    def test_get_transactions(self):
        self.account.deposit(500)
        self.account.withdraw(100)
        self.account.deposit(200)
        txns = self.account.get_transactions()
        self.assertEqual(len(txns), 3)
        self.assertEqual(txns[0]['type'], 'deposit')
        self.assertEqual(txns[1]['type'], 'withdraw')
        self.assertEqual(txns[2]['type'], 'deposit')

class TestGetSharePrice(unittest.TestCase):
    def test_known_symbols(self):
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('TSLA'), 700.00)
        self.assertEqual(get_share_price('GOOGL'), 2800.00)

    def test_invalid_symbol_raises(self):
        with self.assertRaises(ValueError):
            get_share_price('INVALID')

if __name__ == '__main__':
    unittest.main()