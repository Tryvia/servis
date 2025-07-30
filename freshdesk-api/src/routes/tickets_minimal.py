from flask import Blueprint, jsonify
from flask_cors import cross_origin

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets/status', methods=['GET'])
@cross_origin()
def get_tickets_status():
    """Endpoint de status dos tickets"""
    return jsonify({
        'status': 'active',
        'message': 'Serviço de tickets funcionando',
        'endpoints': [
            '/api/tickets/client-by-empresa?cf_empresa=NOME',
            '/api/tickets/client?email=EMAIL'
        ]
    })

@tickets_bp.route('/tickets/test', methods=['GET'])
@cross_origin()
def test_tickets():
    """Endpoint de teste para verificar se a rota está funcionando"""
    return jsonify({
        'message': 'Rota de tickets funcionando corretamente',
        'test': True
    })
