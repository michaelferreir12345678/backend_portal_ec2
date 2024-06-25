from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import json


app = Flask(__name__)
CORS(app) 

codigo_ocorrencia_descricao = {
    "00": "Crédito ou Débito Efetivado",
    "01": "Insuficiência de Fundos - Débito Não Efetuado",
    "02": "Crédito ou Débito Cancelado pelo Pagador/Credor",
    "03": "Débito Autorizado pela Agência - Efetuado",
    "AA": "Controle Inválido",
    "AB": "Tipo de Operação Inválido",
    "AC": "Tipo de Serviço Inválido",
    "AD": "Forma de Lançamento Inválida",
    "AE": "Tipo/Número de Inscrição Inválido",
    "AF": "Codigo de Convênio Inválido",
    "AG": "Agência/Conta Corrente/DV Inválido",
    "AH": "Nº Seqüencial do Registro no Lote Inválido",
    "AI": "Codigo de Segmento de Detalhe Inválido",
    "AJ": "Tipo de Movimento Inválido",
    "AK": "Codigo da Câmara de Compensação do Banco Favorecido/Depositário Inválido",
    "AL": "Codigo do Banco Favorecido, Instituição de Pagamento ou Depositário Inválido",
    "AM": "Agência Mantenedora da Conta Corrente do Favorecido Inválida",
    "AN": "Conta Corrente/DV/Conta de Pagamento do Favorecido Inválido",
    "AO": "Nome do Favorecido Não Informado",
    "AP": "Data Lançamento Inválido",
    "AQ": "Tipo/Quantidade da Moeda Inválido",
    "AR": "Valor do Lançamento Inválido",
    "AS": "Aviso ao Favorecido - Identificação Inválida",
    "AT": "Tipo/Número de Inscrição do Favorecido Inválido",
    "AU": "Logradouro do Favorecido Não Informado",
    "AV": "Nº do Local do Favorecido Não Informado",
    "AW": "Cidade do Favorecido Não Informada",
    "AX": "CEP/Complemento do Favorecido Inválido",
    "AY": "Sigla do Estado do Favorecido Inválida",
    "AZ": "Codigo/Nome do Banco Depositário Inválido",
    "BA": "Codigo/Nome da Agência Depositária Não Informado",
    "BB": "Seu Número Inválido",
    "BC": "Nosso Número Inválido",
    "BD": "Inclusão Efetuada com Sucesso",
    "BE": "Alteração Efetuada com Sucesso",
    "BF": "Exclusão Efetuada com Sucesso",
    "BG": "Agência/Conta Impedida Legalmente",
    "BH": "Empresa não pagou salário",
    "BI": "Falecimento do mutuário",
    "BJ": "Empresa não enviou remessa do mutuário",
    "BK": "Empresa não enviou remessa no vencimento",
    "BL": "Valor da parcela inválida",
    "BM": "Identificação do contrato inválida",
    "BN": "Operação de Consignação Incluída com Sucesso",
    "BO": "Operação de Consignação Alterada com Sucesso",
    "BP": "Operação de Consignação Excluída com Sucesso",
    "BQ": "Operação de Consignação Liquidada com Sucesso",
    "BR": "Reativação Efetuada com Sucesso",
    "BS": "Suspensão Efetuada com Sucesso",
    "CA": "Codigo de Barras - Codigo do Banco Inválido",
    "CB": "Codigo de Barras - Codigo da Moeda Inválido",
    "CC": "Codigo de Barras - Digito Verificador Geral Inválido",
    "CD": "Codigo de Barras - Valor do Título Inválido",
    "CE": "Codigo de Barras - Campo Livre Inválido",
    "CF": "Valor do Documento Inválido",
    "CG": "Valor do Abatimento Inválido",
    "CH": "Valor do Desconto Inválido",
    "CI": "Valor de Mora Inválido",
    "CJ": "Valor da Multa Inválido",
    "CK": "Valor do IR Inválido",
    "CL": "Valor do ISS Inválido",
    "CM": "Valor do IOF Inválido",
    "CN": "Valor de Outras Deduções Inválido",
    "CO": "Valor de Outros Acréscimos Inválido",
    "CP": "Valor do INSS Inválido",
    "HA": "Lote Não Aceito",
    "HB": "Inscrição da Empresa Inválida para o Contrato",
    "HC": "Convênio com a Empresa Inexistente/Inválido para o Contrato",
    "HD": "Agência/Conta Corrente da Empresa Inexistente/Inválido para o Contrato",
    "HE": "Tipo de Serviço Inválido para o Contrato",
    "HF": "Conta Corrente da Empresa com Saldo Insuficiente",
    "HG": "Lote de Serviço Fora de Seqüência",
    "HH": "Lote de Serviço Inválido",
    "HI": "Arquivo não aceito",
    "HJ": "Tipo de Registro Inválido",
    "HK": "Codigo Remessa / Retorno Inválido",
    "HL": "Versão de layout inválida",
    "HM": "Mutuário não identificado",
    "HN": "Tipo do beneficio não permite empréstimo",
    "HO": "Beneficio cessado/suspenso",
    "HP": "Beneficio possui representante legal",
    "HQ": "Beneficio é do tipo PA (Pensão alimentícia)",
    "HR": "Quantidade de contratos permitida excedida",
    "HS": "Beneficio não pertence ao Banco informado",
    "HT": "Início do desconto informado já ultrapassado",
    "HU": "Número da parcela inválida",
    "HV": "Quantidade de parcela inválida",
    "HW": "Margem consignável excedida para o mutuário dentro do prazo do contrato",
    "HX": "Empréstimo já cadastrado",
    "HY": "Empréstimo inexistente",
    "HZ": "Empréstimo já encerrado",
    "H1": "Arquivo sem trailer",
    "H2": "Mutuário sem crédito na competência",
    "H3": "Não descontado – outros motivos",
    "H4": "Retorno de Crédito não pago",
    "H5": "Cancelamento de empréstimo retroativo",
    "H6": "Outros Motivos de Glosa",
    "H7": "Margem consignável excedida para o mutuário acima do prazo do contrato",
    "H8": "Mutuário desligado do empregador",
    "H9": "Mutuário afastado por licença",
    "IA": "Primeiro nome do mutuário diferente do primeiro nome do movimento do censo ou diferente da base de",
    "IB": "Benefício suspenso/cessado pela APS ou Sisobi",
    "IC": "Benefício suspenso por dependência de cálculo",
    "ID": "Benefício suspenso/cessado pela inspetoria/auditoria",
    "IE": "Benefício bloqueado para empréstimo pelo beneficiário",
    "IF": "Benefício bloqueado para empréstimo por TBM",
    "IG": "Benefício está em fase de concessão de PA ou desdobramento",
    "IH": "Benefício cessado por óbito",
    "II": "Benefício cessado por fraude",
    "IJ": "Benefício cessado por concessão de outro benefício",
    "IK": "Benefício cessado: estatutário transferido para órgão de origem",
    "IL": "Empréstimo suspenso pela APS",
    "IM": "Empréstimo cancelado pelo banco",
    "IN": "Crédito transformado em PAB",
    "IO": "Término da consignação foi alterado",
    "IP": "Fim do empréstimo ocorreu durante período de suspensão ou concessão",
    "IQ": "Empréstimo suspenso pelo banco",
    "IR": "Não averbação de contrato – quantidade de parcelas/competências informadas ultrapassou a data limit",
    "TA": "Lote Não Aceito - Totais do Lote com Diferença",
    "YA": "Título Não Encontrado",
    "YB": "Identificador Registro Opcional Inválido",
    "YC": "Codigo Padrão Inválido",
    "YD": "Codigo de Ocorrência Inválido",
    "YE": "Complemento de Ocorrência Inválido",
    "YF": "Alegação já Informada Observação: As ocorrências iniciadas com 'ZA' tem caráter informativo para o c",
    "ZA": "Agência / Conta do Favorecido Substituída",
    "ZB": "Divergência entre o primeiro e último nome do beneficiário versus primeiro e último nome na Receita",
    "ZC": "Confirmação de Antecipação de Valor",
    "ZD": "Antecipação parcial de valor",
    "ZE": "Título bloqueado na base",
    "ZF": "Sistema em contingência – título valor maior que referência",
    "ZG": "Sistema em contingência – título vencido",
    "ZH": "Sistema em contingência – título indexado",
    "ZI": "Beneficiário divergente",
    "ZJ": "Limite de pagamentos parciais excedido",
    "ZK": "Boleto já liquidado",
}

def carregar_dados():
    try:
        json_path = os.path.join(os.path.dirname(__file__), "dados.json")
        if not os.path.isfile(json_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8-sig') as file:
            dados = json.load(file)
        
        return dados
    except Exception as e:
        print(f"Erro ao carregar os dados: {str(e)}")
        return None

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    cpf = cpf.strip().zfill(11)

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador1 = 0
    else:
        digito_verificador1 = 11 - resto

    # Verifica se o primeiro dígito verificador é válido
    if int(cpf[9]) != digito_verificador1:
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador2 = 0
    else:
        digito_verificador2 = 11 - resto

    # Verifica se o segundo dígito verificador é válido
    if int(cpf[10]) != digito_verificador2:
        return False

    # Se passou por todas as validações, o CPF é válido
    return True

def processar_arquivo(arquivo, nome_arquivo):    
    linhas = arquivo.readlines()  
    
    if linhas and "PENSAO" in linhas[0].decode('latin1'):
        salto = 3  
    else:
        salto = 2  

    linhas = linhas[2:-2] 
    dados = []

    for i in range(0, len(linhas), salto): 
        linha1 = linhas[i].decode('latin1')
        if i+1 < len(linhas):
            linha2 = linhas[i+1].decode('latin1')
        else:
            
            linha2 = ""

        cpf = linha2[21:32].strip() 

        # Verifica se o CPF é válido
        # if validar_cpf(cpf):
        dados_linha = {
            "Codigo do Banco": linha1[0:3].strip(),
            "Lote de Servico": linha1[3:7].strip(),
            "Tipo de Registro": linha1[7:8].strip(),
            "N Sequencial do Registro no Lote": linha1[8:13].strip(),
            "Codigo de Segmento do Reg. Detalhe": linha1[13:14].strip(),
            "Tipo de Movimento": linha1[14:15].strip(),
            "Codigo da Instrucao p/ Movimento": linha1[15:17].strip(),
            "Codigo da Camara Centralizadora": linha1[17:20].strip(),
            "Codigo do Banco do Favorecido": linha1[20:23].strip(),
            "Ag. Mantenedora da Cta do Favor.": linha1[23:28].strip(),
            "Digito Verificador da Agencia": linha1[28:29].strip(),
            "Numero da Conta Corrente": linha1[29:41].strip(),
            "Digito Verificador da Conta": linha1[41:42].strip(),
            "Digito Verificador da AG/Conta": linha1[42:43].strip(),
            "Nome do Favorecido": linha1[43:73].strip(),
            "CPF": cpf,
            "N do Docum. atribuido p/ Empresa": linha1[73:93].strip(),
            "Data do Pagamento": linha1[93:101].strip(),
            "Tipo da Moeda": linha1[101:104].strip(),
            "Quantidade da Moeda": linha1[104:119].strip(),
            "Valor do Pagamento": linha1[119:134].strip(),
            "N do Docum. Atribuido pelo Banco": linha1[134:154].strip(),
            "Empresa": linha1[73:76].strip(),
            "Matricula funcionario": linha1[80:90].strip(),
            "Data Real da Efetivacao Pagto": linha1[154:162].strip(),
            "Valor Real da Efetivacao do Pagto": linha1[162:177].strip(),
            "Outras Informacoes": linha1[177:217].strip(),
            "Compl. Tipo Serviço": linha1[217:219].strip(),
            "Codigo finalidade da TED": linha1[219:224].strip(),
            "Compl. Finalidade de Pagamento": linha1[224:226].strip(),
            "Uso Exclusivo FEBRABAN/CNAB": linha1[226:229].strip(),
            "Aviso ao Favorecido": linha1[229:230].strip(),
            "Codigos das Ocorrencias p/ Retorno": linha1[230:240].strip(),
            "Outras Informacoes (segunda linha)": linha2[177:217].strip()  # Adiciona dados da segunda linha
        }
        dados.append(dados_linha)
    return dados, nome_arquivo

def formatar_valor_moeda_real(valor):
    valor_formatado = "{:0,.2f}".format(int(valor)/100)
    return f'R$ {valor_formatado}'

def encontrar_erros(dados):
    erros = []
    for item in dados:
        if "Codigos das Ocorrencias p/ Retorno" in item and item["Codigos das Ocorrencias p/ Retorno"] != "BD":
            codigo_ocorrencia = item["Codigos das Ocorrencias p/ Retorno"]
            descricao_ocorrencia = codigo_ocorrencia_descricao.get(codigo_ocorrencia, "Descrição não encontrada")
            erro = {
                "Nome do Favorecido_arquivo": item.get("Nome do Favorecido", ""),
                "CPF_arquivo": item.get("CPF", ""),
                "Agencia_arquivo": item.get("Ag. Mantenedora da Cta do Favor.", ""),
                "Numero da Conta Corrente_arquivo": f'{item.get("Numero da Conta Corrente", "")} - {item.get("Digito Verificador da Conta", "")}',
                "Matricula funcionario_arquivo": item.get("Matricula funcionario", ""),
                "Valor do Pagamento": formatar_valor_moeda_real(item.get("Valor do Pagamento", 0)),
                "Codigo da Ocorrência": codigo_ocorrencia,
                "Descrição da Ocorrência": descricao_ocorrencia,
                "Arquivo": item.get("Arquivo", "")
            }
            erros.append(erro)
    return erros

def encontrar_quantidade_erros(dados):
    count = 0
    for item in dados:
        if "Empresa" in item and item["Codigos das Ocorrencias p/ Retorno"] != "BD":
            count += 1
    return count

def padronizar_cpfs(cpfs):
    for cpf in cpfs:
        cpf['CPF'] = cpf['CPF'].zfill(11) 

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

@app.route('/')
def home():
    return '<p>Home Page API</p>'

@app.route('/testes_arquivo', methods=['POST'])
def testando_arquivo():
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

            return jsonify({
                'dados totais': dados_totais,
                'nome_arquivo': nome_arquivo,
                'total': len(dados_totais)
            }), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Método não permitido"}), 405

@app.route('/processar_arquivo', methods=['POST'])
def processar_arquivo_route():
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

@app.route('/processar_erros', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)