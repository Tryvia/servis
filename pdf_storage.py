from flask import Blueprint, request, jsonify, send_file, url_for
import os
import uuid
import base64
from datetime import datetime, timedelta
import hashlib
from ..models.user import db
from ..models.pdf_file import PdfFile

pdf_storage_bp = Blueprint('pdf_storage', __name__)

# Diretório para armazenar os PDFs
PDF_STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdf_storage')

# Garantir que o diretório existe
os.makedirs(PDF_STORAGE_DIR, exist_ok=True)

        # Criar registro na base de dados
        pdf_file = PdfFile(
            id=file_id,
            original_filename=filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_size=len(pdf_bytes),
            file_hash=file_hash
        )
        
        db.session.add(pdf_file)
        db.session.commit()

@pdf_storage_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Recebe um PDF em base64 e armazena no servidor
    """
    try:
        data = request.get_json()
        
        if not data or 'pdf_data' not in data:
            return jsonify({'error': 'PDF data is required'}), 400
        
        pdf_base64 = data['pdf_data']
        filename = data.get('filename', 'relatorio_visita.pdf')
        
        # Remover prefixo data:application/pdf;base64, se existir
        if pdf_base64.startswith('data:application/pdf;base64,'):
            pdf_base64 = pdf_base64.split(',')[1]
        
        # Decodificar base64
        try:
            pdf_bytes = base64.b64decode(pdf_base64)
        except Exception as e:
            return jsonify({'error': 'Invalid base64 data'}), 400
        
        # Gerar ID único para o arquivo
        file_id = str(uuid.uuid4())
        file_extension = '.pdf'
        stored_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(PDF_STORAGE_DIR, stored_filename)
        
        # Salvar arquivo
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)
        
        # Gerar hash para verificação de integridade
        file_hash = hashlib.md5(pdf_bytes).hexdigest()
        
        # Criar registro na base de dados
        pdf_file = PdfFile(
            id=file_id,
            original_filename=filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_size=len(pdf_bytes),
            file_hash=file_hash
        )
        
        db.session.add(pdf_file)
        db.session.commit()
        
        # Gerar URL de download
        download_url = url_for('pdf_storage.download_pdf', file_id=file_id, _external=True)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'download_url': download_url,
            'filename': filename,
            'file_size': len(pdf_bytes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_storage_bp.route('/download/<file_id>')
def download_pdf(file_id):
    """
    Permite download do PDF pelo ID
    """
    try:        pdf_file = PdfFile.query.filter_by(id=file_id, is_active=True).first()
        
        if not pdf_file:
            return jsonify({"error": "File not found"}), 404
        
        if not os.path.exists(pdf_file.file_path):
            return jsonify({"error": "File not found on disk"}), 404
        
        # Incrementar contador de downloads
        pdf_file.increment_download_count()
        
        # Retornar arquivo para download
        return send_file(
            pdf_file.file_path,
            as_attachment=True,
            download_name=pdf_file.original_filename,
            mimetype=\'application/pdf\'  
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_storage_bp.route('/info/<file_id>')
def get_pdf_info(file_id):
    """
    Retorna informações sobre um PDF armazenado
    """
    try:
        pdf_file = PdfFile.query.filter_by(id=file_id, is_active=True).first()
        
        if not pdf_file:
            return jsonify({"error": "File not found"}), 404
        
        file_info = pdf_file.to_dict()
        # Remover informações sensíveis
        file_info.pop("file_path", None)
        
        return jsonify({
            "success": True,
            "file_info": file_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_storage_bp.route('/cleanup', methods=['POST'])
def cleanup_old_files():
    """
    Remove arquivos antigos (mais de 7 dias)
    """
    try:
        deleted_count = 0
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        # Buscar arquivos antigos
        old_files = PdfFile.query.filter(
            PdfFile.upload_time < cutoff_date,
            PdfFile.is_active == True
        ).all()
        
        for pdf_file in old_files:
            # Remover arquivo do disco
            if os.path.exists(pdf_file.file_path):
                os.remove(pdf_file.file_path)
            
            # Marcar como inativo na base de dados
            pdf_file.is_active = False
            deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'deleted_files': deleted_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_storage_bp.route('/list')
def list_pdfs():
    """
    Lista todos os PDFs armazenados (para debug/admin)
    """
    try:
        pdf_files = PdfFile.query.filter_by(is_active=True).all()
        
        files_info = []
        for pdf_file in pdf_files:
            info = pdf_file.to_dict()
            info.pop(\'file_path\', None)  # Remover caminho por segurança
            return jsonify({
            'success': True,
            'files': files_info,
            'total_files': len(files_info)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

