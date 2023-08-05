import textwrap


def menu():

    menu = """\n
    ================== EXTRATO ==================\n
    [d]\tDepositar
    [s]\tSacar
    [e]\tGerar Extrato
    [c]\tCriar Nova Conta
    [l]\tListar Contas
    [u]\tCriar Novo Usuário
    [q]\tSair
    = > """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    LIMITE_DEPOSITO = 1
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\nDepósito concluído! Seu saldo atual é: R$ {:.2f}".format(saldo))
    elif valor < LIMITE_DEPOSITO:
        print("\nSó é possivel depositar valores a partir de R$ 1,00. \nPor favor tente novamente com um valor permitido.")
    else:
        print("\nValor Invalido! \nNão foi possivel completar a operação, por favor tente novamente!")

    return saldo, extrato



def sacar(*, saldo, valor, extrato, limite, numero_saques,limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nSaldo insuficiente.")

    elif excedeu_limite:
        print("\nValor de saque excedeu o limite permitido de R$ {:.2f}. \nTente novamente com um valor dentro do limite.".format(limite)) 

    elif excedeu_saques:
        print("\nLimite de saques diarios atingido. \nTente novamente amanhã.")

    elif valor > 0:
            saldo -= valor
            numero_saques += 1
            extrato += f"Saque: R$ {valor:.2f}\n"
            print("\nSaque concluído! Seu saldo atual é: R$ {:.2f}".format(saldo)) 

    else:
        print("\nValor Invalido. Não foi possivel completar a operação, por favor tente novamente!")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================== EXTRATO ==================\n")
    print("Não existe registro de transações.\n" if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print("\n=============================================")

def criar_usuario(usuarios):
    cpf = input("Informe somente os números do seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nEsse CPF já está cadastrado em outro usuario!")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, não foi possivel concluír o processo de criação de conta")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.   ")


main()