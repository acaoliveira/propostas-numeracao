import os

# Nome do arquivo que armazenará o último número
CONTROLE_ARQUIVO = "ultimo_numero.txt"

def obter_proximo_numero():
    # Verifica se o arquivo existe
    if os.path.exists(CONTROLE_ARQUIVO):
        with open(CONTROLE_ARQUIVO, "r") as f:
            try:
                ultimo_numero = int(f.read().strip())
            except ValueError:
                ultimo_numero = 0
    else:
        ultimo_numero = 0

    proximo_numero = ultimo_numero + 1

    # Salva o próximo número no arquivo
    with open(CONTROLE_ARQUIVO, "w") as f:
        f.write(str(proximo_numero))

    return f"PC{proximo_numero:05d}"  # Exemplo: PC00001, PC00002...

# Exemplo de uso
if __name__ == "__main__":
    numero_proposta = obter_proximo_numero()
    print(f"Próximo número de proposta: {numero_proposta}")
