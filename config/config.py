# bia/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis de um arquivo .env

# --- Configuração da API ATCoin ---
ATCOIN_API_URL = os.environ.get("ATCOIN_API_URL", "http://127.0.0.1:8000") # Mude para a URL do seu HF Space
ATCOIN_API_KEY = os.environ.get("ATCOIN_API_KEY", "default_secret_key_for_bia")

# --- Configuração da API Binance ---
# CUIDADO: NUNCA coloque chaves diretamente no código. Use variáveis de ambiente.
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

# --- Configuração do Portfólio ---
# Os tickers aqui devem corresponder aos usados na API ATCoin
PORTFOLIO_ASSETS = {
    'eth': 'ETH-USD', # Chave amigável : ticker yfinance (para buscar dados para a API ATCoin)
    'btc': 'BTC-USD',
    'ada': 'ADA-USD',
    'sol': 'SOL-USD'
}
# Mapeamento do ticker yfinance para o par de trading da Binance (ex: 'ETHUSDT')
YFINANCE_TO_BINANCE_MAP = {
    'ETH-USD': 'ETHUSDT',
    'BTC-USD': 'BTCUSDT',
    'ADA-USD': 'ADAUSDT',
    'SOL-USD': 'SOLUSDT'
}
QUOTE_ASSET = "USDT" # O ativo base para medir o valor e para negociação
REBALANCE_INTERVAL_SECONDS = 3600 # Rebalancear a cada 1 hora
MIN_ORDER_VALUE_USD = 11.0 # Valor mínimo para uma ordem na Binance (geralmente ~$10)
