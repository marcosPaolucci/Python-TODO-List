from tarefas import TarefasManager

def exibir_menu():
    print("1. Cadastrar Tarefa")
    print("2. Listar Tarefas (Visualização/Edição/Remoção)")
    print("3. Sair")

def main():
    tarefas_manager = TarefasManager()   # Cria uma instância da classe TarefasManager

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção pelo numero: ")

        if escolha == '1':
            tarefas_manager.cadastrar_tarefa()
        elif escolha == '2':
            tarefas_manager.listar_tarefas()
        elif escolha == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Verifica se este script está sendo executado como o programa principal para então executar a função main()
if __name__ == "__main__":
    main()
