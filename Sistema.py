import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    port=3308,
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)

autentico = False

def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite seu e-mail: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            print('E-mail ou senha errada')
    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome: ')
        senha = input('Digite seu e-mail: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('Usuario já cadastrado')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('INSERT INTO cadastros(nome, senha, nivel) VALUES(%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print('Usuario cadastrado')
            except:
                print('Erro ao inserir os dados')
    return autenticado, usuarioMaster

def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingrediantes do produto: ')
    grupo = input('Digite o grupo pertencente deste produto: ')
    preco = float(input('Digite o preco do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO produtos (nome, ingredientes, grupo, preco) values (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado')
    except:
        print('Print erro na inserção dos produtos')

def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos")
            produtosCadastrados = cursor.fetchall()
    except:
        print('erro ao conectao ao banco')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('nenhum produto cadastrado')

while not autentico:
    decisao = int(input('Digite 1 para logar e 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar ao BD')

    autentico, usuarioSupremo = logarCadastrar()

if autentico == True:
    print('autenticado')

    decisaoUsuario = 1

    while decisaoUsuario != 0:
        decisaoUsuario = int(input('Digite 0 para sair 1 para cadastrar produtos 2 para listar produtos cadastrados'))

        if decisaoUsuario == 1:
            cadastrarProdutos()
        elif decisaoUsuario == 2:
            listarProdutos()

