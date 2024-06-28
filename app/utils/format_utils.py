
def formatar_valor_moeda_real(valor):
    valor_formatado = "{:0,.2f}".format(int(valor)/100)
    return f'R$ {valor_formatado}'

def padronizar_cpfs(cpfs):
    for cpf in cpfs:
        cpf['CPF'] = cpf['CPF'].zfill(11) 

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
