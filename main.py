import os

# Função para criar a pasta
def criar_pasta(nome_aluno, ano_escolar):
    base_dir = "fotos"
    ano_dir = os.path.join(base_dir, str(ano_escolar))
    
    # Cria a pasta do ano escolar, se não existir
    os.makedirs(ano_dir, exist_ok=True)
    
    pessoa_dir = os.path.join(ano_dir, nome_aluno)
    
    # Cria a pasta da pessoa
    os.makedirs(pessoa_dir, exist_ok=True)
    
    return pessoa_dir  # Retorna o caminho da pasta da pessoa

# Função para salvar um arquivo na pasta da pessoa
def salvar_arquivo(pasta, nome_arquivo, conteudo):
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(conteudo)
    print(f"Arquivo '{nome_arquivo}' salvo em '{pasta}'.")

# Solicita ao usuário o nome da pessoa e o ano escolar
nome_da_pessoa = input("Digite o nome do Aluno: ")
ano_escolar = input("Digite o ano escolar: ")

# Chama a função para criar a pasta
pasta_da_pessoa = criar_pasta(nome_da_pessoa, ano_escolar)

# Solicita o nome do arquivo e o conteúdo a ser salvo
nome_arquivo = input("Digite o nome do arquivo (ex: foto.txt): ")
conteudo = input("Digite o conteúdo do arquivo: ")

# Chama a função para salvar o arquivo
salvar_arquivo(pasta_da_pessoa, nome_arquivo, conteudo)
