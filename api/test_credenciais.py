import ccxt


import os

binance = ccxt.binance({
    'apiKey': os.getenv("BINANCE_API_KEY"),
    'secret': os.getenv("BINANCE_SECRET_KEY"),
    'enableRateLimit': True,
    'options': {
        'adjustForTimeDifference': True
    }
})

try:
    # Apenas carrega os pares públicos
    binance.load_markets(True)
    print("Mercados públicos carregados com sucesso!")

    # Teste de chamada autenticada
    balance = binance.fetch_balance()
    print("Saldo da conta Binance:")
    #print(balance)
except Exception as e:
    print("Erro durante conexão com Binance:", e)
