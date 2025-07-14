# bia/binance_service.py
import ccxt
from typing import Dict, List

from config import BINANCE_API_KEY, BINANCE_API_SECRET, YFINANCE_TO_BINANCE_MAP

from dotenv import load_dotenv
load_dotenv()

import os
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


class BinanceService:
    def __init__(self):
        if not BINANCE_API_KEY or not BINANCE_API_SECRET:
            raise ValueError("Chaves da API Binance não encontradas nas variáveis de ambiente.")
        self.client = ccxt.binance({
            'apiKey': BINANCE_API_KEY,
            'secret': BINANCE_API_SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot', # Negociação Spot
                'adjustForTimeDifference': True,
            },
        })
        try:
            self.client.load_markets(True)
            print("Cliente Binance inicializado e mercados carregados.")
        except Exception as e:
            print(f"Erro ao carregar mercados da Binance: {e}")


    def get_account_balance(self) -> Dict[str, float]:
        """Busca o saldo de todos os ativos na conta spot."""
        try:
            balance = self.client.fetch_balance()
            # Filtrar apenas saldos maiores que zero e retornar dict {asset: free_amount}
            free_balances = {
                asset: amount
                for asset, amount in balance['total'].items()
                if amount > 0
            }

            return free_balances
        except Exception as e:
            print(f"Erro ao buscar saldo da Binance: {e}")
            return {}

    def get_current_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Busca os preços atuais para uma lista de símbolos da Binance (ex: ['ETHUSDT', 'BTCUSDT'])."""
        try:
            tickers = self.client.fetch_tickers(symbols)
            return {symbol: ticker['last'] for symbol, ticker in tickers.items()}
        except Exception as e:
            print(f"Erro ao buscar preços atuais da Binance: {e}")
            return {}

    def get_historical_klines_for_atcoin(self, yf_ticker: str, interval: str = '1h', limit: int = 200) -> List[Dict]:
        """Busca candles históricos para um ticker yfinance, convertendo-o para o formato da Binance."""
        try:
            binance_symbol = YFINANCE_TO_BINANCE_MAP.get(yf_ticker)
            if not binance_symbol:
                raise ValueError(f"Símbolo {yf_ticker} não encontrado no mapa YFINANCE_TO_BINANCE_MAP.")

            # ccxt fetch_ohlcv retorna [timestamp, open, high, low, close, volume]
            klines = self.client.fetch_ohlcv(binance_symbol, timeframe=interval, limit=limit)

            # Converter para o formato que a API ATCoin espera (dicionário por candle)
            klines_dict_list = [
                {"timestamp": k[0], "open": k[1], "high": k[2], "low": k[3], "close": k[4], "volume": k[5]}
                for k in klines
            ]
            return klines_dict_list
        except Exception as e:
            print(f"Erro ao buscar klines históricos para {yf_ticker} ({binance_symbol}): {e}")
            return []

    def create_market_order(self, symbol: str, side: str, amount: float):
        """Cria uma ordem de mercado ('buy' ou 'sell')."""
        try:
            print(f"Criando ordem de mercado: {side.upper()} {amount} {symbol}...")
            order = self.client.create_market_order(symbol, side, amount)
            print("Ordem criada com sucesso:")
            print(order)
            return order
        except Exception as e:
            print(f"ERRO ao criar ordem de mercado para {symbol}: {e}")
            return None
