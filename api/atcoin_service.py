import json
import requests
from typing import Dict, List
from config import ATCOIN_API_URL, ATCOIN_API_KEY


from binance.client import Client


api_key="At0R6ebAME5rvFAFv2vfdniyamxdjIN3ouw9NcVU0jBuejrMRlpt2070wKwNGOil"
api_secret="KwXApzKS3L0pbmrjT93CuDPgQ63pOrKi49TfSnU9eCBrrFkfi07362PF8Ryx7rF3"

client = Client(api_key, api_secret)

# Get user account information
info = client.get_account()


# Get user ID
user_id = info['uid']
balances = client.get_asset_balance(asset='USDT')
amount = balances



class ATCoinService:
    def __init__(self, binance_service):
        self.api_url = ATCOIN_API_URL
        self.api_key = ATCOIN_API_KEY
        self.binance_service = binance_service
        #balance = binance_service.fetch_balance()

    def get_portfolio_allocation(self, portfolio_assets: Dict[str, str]) -> Dict[str, float]:
        """Obtém a alocação de portfólio da API ATCoin (Hugging Face Space)."""
        try:
            # Coletar dados históricos para cada ativo do portfólio
            historical_data = {}
            for asset_key, yf_ticker in portfolio_assets.items():
                klines = self.binance_service.get_historical_klines_for_atcoin(yf_ticker)
                if not klines:
                    print(f"Aviso: Não foi possível obter dados históricos para {yf_ticker}. Ignorando este ativo.")
                    continue
                historical_data[asset_key] = klines

            if not historical_data:
                print("Erro: Nenhum dado histórico disponível para enviar à API ATCoin.")
                return {}


            url = ATCOIN_API_URL
            api_key = ATCOIN_API_KEY
            payload = {
                "client_id": str(user_id),
                "amount": float(amount['free']),
                "aibank_transaction_token": "token123"
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }



            print(f"Enviando requisição para a API ATCoin em: {self.api_url}")
            print(json.dumps(payload, indent=2))

            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins (4xx ou 5xx)

            result = response.json()
            return result.get("recommended_allocation", {})

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição à API ATCoin: {e}")
            return {}
        except Exception as e:
            print(f"Erro inesperado ao obter alocação da API ATCoin: {e}")
            return {}


