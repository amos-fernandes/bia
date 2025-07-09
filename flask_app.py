from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from portfolio_manager import PortfolioManager
from binance_service import BinanceService
from atcoin_service import ATCoinService
from config import PORTFOLIO_ASSETS, QUOTE_ASSET, YFINANCE_TO_BINANCE_MAP

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)  # Permitir CORS para todas as rotas

# Instanciar os serviços
portfolio_manager = PortfolioManager()

@app.route('/')
def serve_frontend():
    """Serve o frontend React."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/portfolio/balance', methods=['GET'])
def get_portfolio_balance():
    """Retorna o saldo atual do portfólio."""
    try:
        balances = portfolio_manager.binance.get_account_balance()
        if not balances:
            return jsonify({"error": "Não foi possível obter o saldo da conta"}), 500
        
        # Obter preços atuais
        asset_symbols = [YFINANCE_TO_BINANCE_MAP[yf_ticker] for yf_ticker in PORTFOLIO_ASSETS.values()]
        prices = portfolio_manager.binance.get_current_prices(asset_symbols)
        
        # Calcular valor total e alocações
        total_portfolio_value_usd = balances.get(QUOTE_ASSET, 0.0)
        current_allocations = {}
        
        for asset, binance_symbol in YFINANCE_TO_BINANCE_MAP.items():
            coin = binance_symbol.replace(QUOTE_ASSET, '')
            if coin in balances:
                qty = balances[coin]
                price = prices.get(binance_symbol, 0)
                value_usd = qty * price
                total_portfolio_value_usd += value_usd
                current_allocations[coin] = {
                    'quantity': qty,
                    'price': price,
                    'value_usd': value_usd
                }
        
        # Adicionar USDT
        current_allocations[QUOTE_ASSET] = {
            'quantity': balances.get(QUOTE_ASSET, 0.0),
            'price': 1.0,
            'value_usd': balances.get(QUOTE_ASSET, 0.0)
        }
        
        return jsonify({
            "total_value_usd": total_portfolio_value_usd,
            "allocations": current_allocations,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/allocation', methods=['GET'])
def get_ai_allocation():
    """Obtém a alocação recomendada pela IA."""
    try:
        target_allocation_weights = portfolio_manager.atcoin.get_portfolio_allocation(PORTFOLIO_ASSETS)
        if not target_allocation_weights:
            return jsonify({"error": "Não foi possível obter a alocação da IA"}), 500
        
        return jsonify({
            "recommended_allocation": target_allocation_weights,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/rebalance', methods=['POST'])
def rebalance_portfolio():
    """Executa o rebalanceamento do portfólio."""
    try:
        # Executar rebalanceamento em uma thread separada para não bloquear a resposta
        import threading
        
        def run_rebalance():
            portfolio_manager.rebalance_portfolio()
        
        thread = threading.Thread(target=run_rebalance)
        thread.start()
        
        return jsonify({
            "message": "Rebalanceamento iniciado",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/status', methods=['GET'])
def get_portfolio_status():
    """Retorna o status geral do portfólio."""
    try:
        # Obter saldo atual
        balances = portfolio_manager.binance.get_account_balance()
        
        # Obter alocação recomendada
        target_allocation = portfolio_manager.atcoin.get_portfolio_allocation(PORTFOLIO_ASSETS)
        
        # Obter preços atuais
        asset_symbols = [YFINANCE_TO_BINANCE_MAP[yf_ticker] for yf_ticker in PORTFOLIO_ASSETS.values()]
        prices = portfolio_manager.binance.get_current_prices(asset_symbols)
        
        return jsonify({
            "balances": balances,
            "target_allocation": target_allocation,
            "current_prices": prices,
            "portfolio_assets": PORTFOLIO_ASSETS,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

