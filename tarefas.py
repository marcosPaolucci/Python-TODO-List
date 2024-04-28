from persistencia import TarefasDB
from datetime import datetime

class TarefasManager:
    def __init__(self):
        # cria um atributo chamado db que terá acesso a funções de TarefasDB
        self.db = TarefasDB()

    def cadastrar_tarefa(self):
        while True:
            descricao = input("Descrição da tarefa: ")
            if descricao.strip():  # Verifica se a descrição não está vazia
                break
            else:
                print("Erro: Descrição da tarefa não pode ser vazia. Por favor, insira uma descrição.")
            
        # Verificar se a data fornecida está no formato correto (YYYY-MM-DD) e não é anterior a data atual
        while True:
            data_vencimento = input("Data de vencimento (formato YYYY-MM-DD): ")
            try:
                data_vencimento_obj = datetime.strptime(data_vencimento, "%Y-%m-%d")
                data_atual = datetime.now().date()
                if data_vencimento_obj.date() < data_atual:
                    print("Erro: A data de vencimento não pode ser anterior à data atual.")
                else:
                    break
            except ValueError:
                print("Erro: Formato de data inválido. Por favor, insira a data no formato YYYY-MM-DD.")

        self.db.cadastrar_tarefa(descricao, data_vencimento)

    def listar_tarefas(self):
        filtro = input("Deseja filtrar os documentos por status (S), por data máxima de vencimento (D) ou qualquer tecla para exibir todos? ").upper()  
        if filtro == 'S':
            status = input("Informe o status Pendente , Em andamento ou Concluída: ").capitalize()
            while status not in {"Pendente", "Em andamento", "Concluída"}:
                status = input("Status inválido. Por favor, informe Pendente, Em andamento, Concluída: ").capitalize()
            tarefas = self.db.listar_tarefas_por_status(status)
        elif filtro == 'D':
            while True:
                data_vencimento = input("Informe a data de vencimento (formato YYYY-MM-DD): ")
                try:
                    # Tenta converter a entrada em uma data usando o formato especificado
                    datetime.strptime(data_vencimento, "%Y-%m-%d")
                    
                    # Executa a função quando a data é válida
                    tarefas = self.db.listar_tarefas_por_data_vencimento(data_vencimento)
                    
                    break
                except ValueError:
                # Se ocorrer um ValueError, significa que a data não está no formato correto
                    print("Formato de data inválido. Por favor, insira no formato correto.")
        else:
            tarefas = self.db.listar_tarefas()

        if not tarefas:
            print("Nenhuma tarefa encontrada.")
            return

        for i, tarefa in enumerate(tarefas, start=1):
            tarefa['num_tarefa'] = i
        
        # Pedir o número da tarefa para editar/remover:
        while True:
            for tarefa in tarefas:
                print(f"{tarefa['num_tarefa']}. {tarefa['descricao']} (Vencimento: {tarefa['data_vencimento']}, Status: {tarefa['status']})")
            opcao = input("Selecione o número da tarefa para editar ou remover, ou pressione Enter para voltar ao menu principal: ")
            if not opcao:  # Verifica se a opção está vazia (usuário pressionou Enter)
                return
            if opcao.isdigit():  # Verifica se a entrada é composta apenas por dígitos
                num_tarefa = int(opcao)
                tarefa = next((tarefa for tarefa in tarefas if tarefa['num_tarefa'] == num_tarefa), None)
                if tarefa:
                    acao = input("Deseja editar ou remover esta tarefa? (E para editar, R para remover, ou qualquer tecla para voltar a seleção): ").upper()
                    if acao == 'E':
                        self.editar_tarefa(tarefa['_id'])
                        return
                    elif acao == 'R':
                        self.remover_tarefa(tarefa['_id'])
                        return                  
                else:
                    print("Tarefa não encontrada. Tente novamente!")
            else:
                print("Por favor, digite um número válido!")

    def editar_tarefa(self, tarefa_id):
        descricao = input("Nova descrição (deixe em branco para manter a mesma): ")
        while True:
            data_vencimento = input("Nova data de vencimento (formato YYYY-MM-DD, deixe em branco para manter a mesma): ")
            #condiciona se o campo estiver vazio vai sair o while pois vai manter o valor
            if not data_vencimento:  
                break
            # Verificar se a data fornecida está no formato correto (YYYY-MM-DD) e não é anterior a data atual
            try: 
                data_vencimento_obj = datetime.strptime(data_vencimento, "%Y-%m-%d")
                data_atual = datetime.now().date()
                if data_vencimento_obj.date() < data_atual:
                    print("Erro: A data de vencimento não pode ser anterior à data atual.")
                else:
                    break
            except ValueError:
                print("Erro: Formato de data inválido. Por favor, insira a data no formato YYYY-MM-DD.")

        novo_status = input("Novo status (Pendente, Em andamento ou Concluída, deixe em branco para manter o mesmo): ").capitalize()
        while novo_status not in {"", "Pendente", "Em andamento", "Concluída"}:
            print("Status inválido. Por favor, informe Pendente, Em andamento, Concluída ou deixe em branco para manter o mesmo.")
            novo_status = input("Novo status (Pendente, Em andamento ou Concluída, deixe em branco para manter o mesmo): ")

        #if novo_status == "":
            #novo_status = None

        self.db.editar_tarefa(tarefa_id, descricao, data_vencimento, novo_status)
        print("Tarefa editada com sucesso.")
      
    def remover_tarefa(self, tarefa_id):
        self.db.remover_tarefa(tarefa_id)
        print("Tarefa removida com sucesso.")
        
