from accounts import Account, get_share_price
import gradio as gr
from datetime import datetime

account = None

def create_account(user_id: str):
    global account
    account = Account(user_id)
    return f"Account created for user '{user_id}'. Balance: $0.00"

def deposit(amount: float):
    try:
        if account is None:
            return "Please create an account first."
        account.deposit(amount)
        return f"Deposited ${amount:.2f}. New balance: ${account.cash_balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw(amount: float):
    try:
        if account is None:
            return "Please create an account first."
        account.withdraw(amount)
        return f"Withdrew ${amount:.2f}. New balance: ${account.cash_balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares(symbol: str, quantity: int):
    try:
        if account is None:
            return "Please create an account first."
        symbol = symbol.upper()
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol} at ${get_share_price(symbol):.2f} each."
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares(symbol: str, quantity: int):
    try:
        if account is None:
            return "Please create an account first."
        symbol = symbol.upper()
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol} at ${get_share_price(symbol):.2f} each."
    except Exception as e:
        return f"Error: {str(e)}"

def show_holdings():
    if account is None:
        return "Please create an account first."
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings."
    result = "Holdings:\n"
    for symbol, qty in holdings.items():
        price = get_share_price(symbol)
        value = price * qty
        result += f"{symbol}: {qty} shares @ ${price:.2f} = ${value:.2f}\n"
    return result.strip()

def show_portfolio_value():
    if account is None:
        return "Please create an account first."
    val = account.get_portfolio_value()
    return f"Total portfolio value: ${val:.2f}"

def show_profit_loss():
    if account is None:
        return "Please create an account first."
    pl = account.get_profit_loss()
    color = "green" if pl >= 0 else "red"
    sign = "+" if pl >= 0 else ""
    return f'<span style="color:{color};">Profit/Loss: {sign}${pl:.2f}</span>'

def list_transactions():
    if account is None:
        return "Please create an account first."
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions yet."
    lines = []
    for t in transactions:
        ts = t['timestamp']
        ttype = t['type'].capitalize()
        if ttype == "Deposit" or ttype == "Withdraw":
            amt = f"${t['amount']:.2f}"
            lines.append(f"{ts}: {ttype} {amt}")
        elif ttype == "Buy" or ttype == "Sell":
            sym = t['symbol']
            qty = t['quantity']
            amt = f"${t['amount']:.2f}"
            lines.append(f"{ts}: {ttype} {qty} shares of {sym} for {amt}")
    return "\n".join(lines)


with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Account Management Demo")
    with gr.Row():
        with gr.Column():
            user_id_input = gr.Textbox(label="User ID", value="user123")
            create_btn = gr.Button("Create Account")
            create_output = gr.Textbox(label="Status", interactive=False)

        with gr.Column():
            deposit_amount = gr.Number(label="Deposit Amount", value=0, precision=2)
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Status", interactive=False)

            withdraw_amount = gr.Number(label="Withdraw Amount", value=0, precision=2)
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Status", interactive=False)
    
    with gr.Row():
        with gr.Column():
            symbol_buy = gr.Textbox(label="Symbol to Buy", value="AAPL", max_lines=1)
            qty_buy = gr.Number(label="Quantity to Buy", value=0, precision=0)
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Status", interactive=False)

            symbol_sell = gr.Textbox(label="Symbol to Sell", value="AAPL", max_lines=1)
            qty_sell = gr.Number(label="Quantity to Sell", value=0, precision=0)
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Status", interactive=False)
    
    with gr.Row():
        holdings_btn = gr.Button("Show Holdings")
        holdings_output = gr.Textbox(label="Holdings", interactive=False)

        port_val_btn = gr.Button("Portfolio Value")
        port_val_output = gr.HTML(label="Portfolio Value")

        pl_btn = gr.Button("Show Profit/Loss")
        pl_output = gr.HTML(label="Profit/Loss")

    with gr.Row():
        transactions_btn = gr.Button("List Transactions")
        transactions_output = gr.Textbox(label="Transactions", interactive=False)

    # Callbacks
    create_btn.click(create_account, inputs=user_id_input, outputs=create_output)
    deposit_btn.click(deposit, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(buy_shares, inputs=[symbol_buy, qty_buy], outputs=buy_output)
    sell_btn.click(sell_shares, inputs=[symbol_sell, qty_sell], outputs=sell_output)
    holdings_btn.click(show_holdings, outputs=holdings_output)
    port_val_btn.click(show_portfolio_value, outputs=port_val_output)
    pl_btn.click(show_profit_loss, outputs=pl_output)
    transactions_btn.click(list_transactions, outputs=transactions_output)
    
if __name__ == "__main__":
    demo.launch()