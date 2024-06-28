import os
import json

def carregar_dados():
    try:
        json_path = os.path.join(os.path.dirname(__file__), "../../dados.json")
        if not os.path.isfile(json_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8-sig') as file:
            dados = json.load(file)
        
        return dados
    except Exception as e:
        print(f"Erro ao carregar os dados: {str(e)}")
        return None
