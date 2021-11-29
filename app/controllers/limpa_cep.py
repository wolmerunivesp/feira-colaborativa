import re

def limpa_cep(cep):
    cep_limpo = re.sub('[^0-9]', "", cep)
    return cep_limpo