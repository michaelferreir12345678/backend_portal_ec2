from flask import Blueprint, request, jsonify
from ..services.file_processing import processar_arquivo, encontrar_erros
from flask_login import login_required


errors_bp = Blueprint('errors_bp', __name__)

@errors_bp.route('/processar_erros', methods=['POST'])
@login_required
def processar_erros():
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
    
            nomes_erros = encontrar_erros(dados_totais)
            
            return jsonify({
                'erros': nomes_erros 
            }), 200
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Método não permitido"}), 405