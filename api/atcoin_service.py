import requests
from typing import Dict, List
from config import ATCOIN_API_URL, ATCOIN_API_KEY

class ATCoinService:
    def __init__(self, binance_service):
        self.api_url = ATCOIN_API_URL
        self.api_key = ATCOIN_API_KEY
        self.binance_service = binance_service

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

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {"historical_data": historical_data}

            print(f"Enviando requisição para a API ATCoin em: {self.api_url}")
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins (4xx ou 5xx)

            result = response.json()
            return result.get("recommended_allocation", {})

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição à API ATCoin: {e}")
            return {}
        except Exception as e:
            print(f"Erro inesperado ao obter alocação da API ATCoin: {e}")
            return {}


