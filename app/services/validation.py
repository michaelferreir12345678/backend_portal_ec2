from ..utils.format_utils import padronizar_cpfs

def validar_dados(arquivo, dados_json, nome_arquivo):
    try:
        # Padroniza os CPFs no arquivo e no JSON
        padronizar_cpfs(arquivo)
        padronizar_cpfs(dados_json)

        nomes_nao_encontrados = []

        # Verifica cada CPF do arquivo em relação aos dados do JSON
        for registro in arquivo:
            cpf_arquivo = registro['CPF']
            encontrado = False

            for item_json in dados_json:
                if item_json['CPF'] == cpf_arquivo:
                    encontrado = True
                    break
            
            if not encontrado:
                nomes_nao_encontrados.append(registro)
        return nomes_nao_encontrados
    
    except Exception as e:
        print(f"Erro ao validar os dados: {str(e)}")
        return []
