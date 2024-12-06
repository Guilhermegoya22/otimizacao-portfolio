import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular o indicador MACD
def calculate_macd(data, short_window=12, long_window=26):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = data['Close'].ewm(span=9).mean()
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    signals['macd'] = signals['short_mavg'] - signals['long_mavg']
    signals['macd_signal'] = signals['macd'].ewm(span=9).mean()
    signals['macd_diff'] = signals['macd'] - signals['macd_signal']
    return signals

# Função para gerar sinais de compra e venda
def generate_signals(data):
    signals = calculate_macd(data)
    buy_signals = pd.DataFrame(index=data.index)
    buy_signals['Buy'] = 0
    buy_signals['Sell'] = 0
    buy_signals['Buy'][signals['macd_diff'] > 0] = 1
    buy_signals['Sell'][signals['macd_diff'] < 0] = 1
    return buy_signals

# Função para calcular o saldo
def calculate_balance(signals, initial_balance=1000):
    balance = initial_balance
    balance_history = []
    for i in range(len(signals)):
        if signals['Buy'].iloc[i] == 1:
            balance += balance * 0.01  # Aumento de 1% no saldo
        elif signals['Sell'].iloc[i] == 1:
            balance -= balance * 0.01  # Diminuição de 1% no saldo
        balance_history.append(balance)
    return balance_history

# Função principal
def main():
    ticker = 'AAPL'  # Substitua pelo ticker desejado
    start_date = '2022-01-01'
    end_date = '2024-01-01'
    
    # Obter dados históricos
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Gerar sinais de compra e venda
    signals = generate_signals(data)
    
    # Calcular o saldo
    balance_history = calculate_balance(signals)
    
    # Plotar gráfico do saldo total pelo tempo
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, balance_history, label='Saldo Total')
    plt.title('Saldo Total ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Saldo')
    plt.legend()
    plt.show()

if _name_ == "_main_":
    main()
