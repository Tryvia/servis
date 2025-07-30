import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# Importar apenas as rotas essenciais
from src.routes.tickets_by_client_python import tickets_by_client_bp
from src.routes.tickets_minimal import tickets_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Registrar apenas os blueprints essenciais
app.register_blueprint(tickets_bp, url_prefix='/api')
app.register_blueprint(tickets_by_client_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'API Freshdesk funcionando',
                'status': 'healthy',
                'endpoints': [
                    '/health',
                    '/api/tickets/status',
                    '/api/tickets/client-by-empresa?cf_empresa=NOME',
                    '/api/tickets/client?email=EMAIL'
                ]
            })

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'message': 'API Freshdesk funcionando',
        'version': '2.0',
        'features': ['tickets_by_empresa', 'tickets_by_email']
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask (versão mínima)...")
    print("📡 Endpoints disponíveis:")
    print("   - GET /health - Verificação de saúde")
    print("   - GET /api/tickets/status - Status dos tickets")
    print("   - GET /api/tickets/client-by-empresa?cf_empresa=NOME - Tickets por empresa")
    print("   - GET /api/tickets/client?email=EMAIL - Tickets por email")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

