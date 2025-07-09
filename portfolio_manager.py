# bia/portfolio_manager.py
import time
from typing import Dict

from config import PORTFOLIO_ASSETS, QUOTE_ASSET, YFINANCE_TO_BINANCE_MAP, MIN_ORDER_VALUE_USD
from binance_service import BinanceService
from atcoin_service import ATCoinService

class PortfolioManager:
    def __init__(self):
        self.binance = BinanceService()
        self.atcoin = ATCoinService(self.binance)

    def rebalance_portfolio(self):
        """
        Executa um ciclo completo de rebalanceamento do portfólio.
        """
        print("\n" + "="*50)
        print(f"INICIANDO CICLO DE REBALANCEAMENTO - {datetime.now().isoformat()}")
        print("="*50)

        # 1. Obter estado atual da conta Binance
        balances = self.binance.get_account_balance()
        if not balances:
            print("Não foi possível obter o saldo da conta. Abortando ciclo.")
            return

        asset_symbols = [YFINANCE_TO_BINANCE_MAP[yf_ticker] for yf_ticker in PORTFOLIO_ASSETS.values()]
        prices = self.binance.get_current_prices(asset_symbols + [f"{a}/{QUOTE_ASSET}" for a in balances.keys() if a != QUOTE_ASSET])

        # Calcular o valor total do portfólio em USDT
        total_portfolio_value_usd = balances.get(QUOTE_ASSET, 0.0)
        current_allocations = {QUOTE_ASSET: balances.get(QUOTE_ASSET, 0.0)}

        for asset, binance_symbol in YFINANCE_TO_BINANCE_MAP.items():
            coin = binance_symbol.replace(QUOTE_ASSET, '')
            if coin in balances:
                qty = balances[coin]
                price = prices.get(binance_symbol, 0)
                value_usd = qty * price
                total_portfolio_value_usd += value_usd
                current_allocations[coin] = value_usd

        print(f"Valor Total do Portfólio: ${total_portfolio_value_usd:,.2f}")
        print(f"Alocação Atual (Valor em USD): {current_allocations}")

        # 2. Obter alocação alvo da API ATCoin
        print("\n--- Consultando a IA ATCoin para nova alocação... ---")
        target_allocation_weights = self.atcoin.get_portfolio_allocation(PORTFOLIO_ASSETS)
        if not target_allocation_weights:
            print("Não foi possível obter a alocação da IA. Abortando ciclo.")
            return

        print(f"Alocação Alvo da IA: {target_allocation_weights}")

        # 3. Calcular ordens necessárias para rebalancear
        print("\n--- Calculando ordens de rebalanceamento... ---")
        orders_to_execute = {'buy': [], 'sell': []}

        for asset_key, weight in target_allocation_weights.items():
            yf_ticker = PORTFOLIO_ASSETS[asset_key]
            binance_symbol = YFINANCE_TO_BINANCE_MAP[yf_ticker]
            coin = binance_symbol.replace(QUOTE_ASSET, '')

            target_value = total_portfolio_value_usd * weight
            current_value = current_allocations.get(coin, 0.0)
            difference = target_value - current_value

            price = prices.get(binance_symbol)
            if not price: continue

            if difference > MIN_ORDER_VALUE_USD: # COMPRAR
                quantity_to_buy = difference / price
                orders_to_execute['buy'].append({'symbol': binance_symbol, 'qty': quantity_to_buy, 'value': difference})
            elif difference < -MIN_ORDER_VALUE_USD: # VENDER
                quantity_to_sell = abs(difference) / price
                orders_to_execute['sell'].append({'symbol': binance_symbol, 'qty': quantity_to_sell, 'value': abs(difference)})

        print(f"Ordens a Executar: {orders_to_execute}")

        # 4. Executar Ordens (PRIMEIRO VENDER, DEPOIS COMPRAR)
        print("\n--- Executando ordens na Binance... ---")
        # Vender
        for order in orders_to_execute['sell']:
            # Obter precisão do ativo para a ordem
            market_info = self.binance.client.market(order['symbol'])
            qty_to_sell_precise = self.binance.client.amount_to_precision(order['symbol'], order['qty'])
            print(f"  VENDENDO {qty_to_sell_precise} de {order['symbol']}...")
            self.binance.create_market_order(order['symbol'], 'sell', qty_to_sell_precise)
            time.sleep(1) # Pequena pausa entre ordens

        # Aguardar um pouco para o saldo USDT ser atualizado
        if orders_to_execute['sell']: time.sleep(5)

        # Comprar
        for order in orders_to_execute['buy']:
            market_info = self.binance.client.market(order['symbol'])
            qty_to_buy_precise = self.binance.client.amount_to_precision(order['symbol'], order['qty'])
            print(f"  COMPRANDO {qty_to_buy_precise} de {order['symbol']}...")
            self.binance.create_market_order(order['symbol'], 'buy', qty_to_buy_precise)
            time.sleep(1)

        print("\nCiclo de Rebalanceamento Concluído.")
        print("="*50 + "\n")
