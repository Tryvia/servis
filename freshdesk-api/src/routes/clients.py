import os
import json
import subprocess
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.client import Client, db

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/clients', methods=['GET'])
@cross_origin()
def get_clients():
    """Listar todos os clientes"""
    try:
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients])
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@clients_bp.route('/clients', methods=['POST'])
@cross_origin()
def create_client():
    """Criar novo cliente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        cf_empresa = data.get('cf_empresa', '').strip()
        
        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        if not cf_empresa:
            return jsonify({'error': 'Campo cf_empresa é obrigatório'}), 400
        
        # Verificar se cf_empresa já existe
        existing_client = Client.query.filter_by(cf_empresa=cf_empresa).first()
        if existing_client:
            return jsonify({'error': 'cf_empresa já existe'}), 400
        
        client = Client(
            name=name,
            email=email if email else None,
            cf_empresa=cf_empresa
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify(client.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@cross_origin()
def get_client(client_id):
    """Obter cliente por ID"""
    try:
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict())
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
@cross_origin()
def update_client(client_id):
    """Atualizar cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        cf_empresa = data.get('cf_empresa', '').strip()
        
        if name:
            client.name = name
        
        if email:
            client.email = email
        
        if cf_empresa:
            # Verificar se cf_empresa já existe em outro cliente
            existing_client = Client.query.filter(
                Client.cf_empresa == cf_empresa,
                Client.id != client_id
            ).first()
            if existing_client:
                return jsonify({'error': 'cf_empresa já existe'}), 400
            client.cf_empresa = cf_empresa
        
        db.session.commit()
        return jsonify(client.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@clients_bp.route('/clients/<int:client_id>', methods=['DELETE'])
@cross_origin()
def delete_client(client_id):
    """Deletar cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Cliente deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@clients_bp.route('/tickets/client-by-empresa', methods=['GET'])
@cross_origin()
def get_tickets_by_cf_empresa():
    """Buscar tickets por cf_empresa"""
    try:
        # Obter cf_empresa dos parâmetros da query
        cf_empresa = request.args.get('cf_empresa')
        if not cf_empresa:
            return jsonify({'error': 'cf_empresa é obrigatório'}), 400
        
        # Get the project root directory (onde o script PowerShell está localizado)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        script_path = os.path.join(project_root, 'freshdesk_export_tickets_by_cf_empresa.ps1')
        json_path = os.path.join(project_root, f'tickets_empresa_{cf_empresa.replace(" ", "_").replace("/", "_")}.json')
        
        # Verificar se PowerShell está disponível
        try:
            subprocess.run(['pwsh', '--version'], capture_output=True, check=True)
            powershell_cmd = 'pwsh'
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['powershell', '--version'], capture_output=True, check=True)
                powershell_cmd = 'powershell'
            except (subprocess.CalledProcessError, FileNotFoundError):
                return jsonify({'error': 'PowerShell não encontrado. Instale PowerShell Core ou Windows PowerShell.'}), 500
        
        # Executar o script PowerShell com parâmetro cf_empresa
        result = subprocess.run(
            [powershell_cmd, '-ExecutionPolicy', 'Bypass', '-File', script_path, cf_empresa],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': f'Erro ao executar script PowerShell: {result.stderr}',
                'stdout': result.stdout
            }), 500
        
        # Ler o arquivo JSON gerado
        if not os.path.exists(json_path):
            return jsonify({'error': 'Arquivo JSON não foi gerado pelo script PowerShell'}), 500
        
        with open(json_path, 'r', encoding='utf-8') as f:
            tickets_data = json.load(f)
        
        # Limpar o arquivo temporário
        try:
            os.remove(json_path)
        except:
            pass  # Ignorar erros de limpeza
        
        # Retornar os dados dos tickets
        return jsonify(tickets_data)
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout ao executar script PowerShell (5 minutos)'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

