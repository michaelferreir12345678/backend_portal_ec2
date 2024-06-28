from flask import Blueprint, request, jsonify
from ..services.file_processing import processar_arquivo
from ..services.validation import validar_dados
from ..utils.data_loader import carregar_dados
from flask_login import login_required,current_user
from app.middlewares.auth_middleware import token_required


inconsistencies_bp = Blueprint('inconsistencies_bp', __name__)

@inconsistencies_bp.route('/processar_inconsistencia', methods=['POST'])
@token_required
def processar_arquivo_route(current_user):
    if request.method == 'POST':
        try:
            # Verifica se foram enviados arquivos na requisição
            if 'arquivos' not in request.files:
                return jsonify({"error": "Nenhum arquivo enviado"}), 400

            arquivos = request.files.getlist('arquivos')
            dados_totais = []
            nome_arquivo = None

            for arquivo in arquivos:
                # Verifica se o arquivo é texto ou com extensão .ret ou .rem
                if arquivo.filename.lower().endswith(('.txt', '.ret', '.rem')):
                    dados_processados, nome_arquivo = processar_arquivo(arquivo, arquivo.filename)
                    dados_totais.extend(dados_processados)

                else:
                    return jsonify({"error": f"Arquivo '{arquivo.filename}' não é um arquivo de texto válido (.txt, .ret, .rem)"}), 400

            # Se nenhum arquivo de texto for processado
            if nome_arquivo is None:
                return jsonify({"error": "Nenhum arquivo de texto processado"}), 400

            # Validar os dados do arquivo em relação aos dados JSON
            dados_json = carregar_dados()

            if not dados_json:
                return jsonify({"error": "Erro ao carregar dados JSON"}), 500

            nomes_inconsistentes = validar_dados(dados_totais, dados_json, nome_arquivo)

            return jsonify({
                'nome_arquivo': nome_arquivo,
                'nomes_inconsistentes': nomes_inconsistentes
            }), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Método não permitido"}), 405