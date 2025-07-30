import os
import json
import subprocess
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

tickets_by_client_bp = Blueprint('tickets_by_client', __name__)

@tickets_by_client_bp.route('/tickets/client', methods=['GET'])
@cross_origin()
def get_tickets_by_client():
    try:
        # Obter email do cliente dos parâmetros da query
        client_email = request.args.get('email')
        if not client_email:
            return jsonify({'error': 'Email do cliente é obrigatório'}), 400
        
        # Get the project root directory (where the PowerShell script is located)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        script_path = os.path.join(project_root, 'freshdesk_export_tickets_by_client.ps1')
        json_path = os.path.join(project_root, f'tickets_cliente_{client_email.replace("@", "_").replace(".", "_")}.json')
        
        # Check if PowerShell is available
        try:
            subprocess.run(['pwsh', '--version'], capture_output=True, check=True)
            powershell_cmd = 'pwsh'
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['powershell', '--version'], capture_output=True, check=True)
                powershell_cmd = 'powershell'
            except (subprocess.CalledProcessError, FileNotFoundError):
                return jsonify({'error': 'PowerShell não encontrado. Instale PowerShell Core ou Windows PowerShell.'}), 500
        
        # Execute the PowerShell script with client email parameter
        result = subprocess.run(
            [powershell_cmd, '-ExecutionPolicy', 'Bypass', '-File', script_path, client_email],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': f'Erro ao executar script PowerShell: {result.stderr}',
                'stdout': result.stdout
            }), 500
        
        # Read the generated JSON file
        if not os.path.exists(json_path):
            return jsonify({'error': 'Arquivo JSON não foi gerado pelo script PowerShell'}), 500
        
        with open(json_path, 'r', encoding='utf-8') as f:
            tickets_data = json.load(f)
        
        # Clean up the temporary file
        try:
            os.remove(json_path)
        except:
            pass  # Ignore cleanup errors
        
        # Return the tickets data
        return jsonify(tickets_data)
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout ao executar script PowerShell (5 minutos)'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

