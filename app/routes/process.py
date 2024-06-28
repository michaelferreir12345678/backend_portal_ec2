from flask import Blueprint, request, jsonify
from ..services.file_processing import processar_arquivo
from flask_login import login_required, current_user
from app.middlewares.auth_middleware import token_required



process_bp = Blueprint('process_bp', __name__)

@process_bp.route('/processar_arquivo', methods=['POST'])
@token_required
def process_arquivo(current_user):
    if 'arquivos' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    arquivos = request.files.getlist('arquivos')
    dados_totais = []

    try:
        for arquivo in arquivos:
            if arquivo.filename.lower().endswith(('.txt', '.ret', '.rem')):
                dados_processados, nome_arquivo = processar_arquivo(arquivo, arquivo.filename)
                dados_totais.extend(dados_processados)
            else:
                return jsonify({"error": f"Arquivo '{arquivo.filename}' não é um arquivo de texto válido (.txt, .ret, .rem)"}), 400

        if not dados_totais:
            return jsonify({"error": "Nenhum arquivo de texto processado"}), 400

        return jsonify({
            'dados totais': dados_totais,
            'total': len(dados_totais)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
