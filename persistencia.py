from pymongo import MongoClient
from datetime import datetime, timedelta

class TarefasDB:
    def __init__(self, host='localhost', port=27017, db_name='todolist'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.tarefas_collection = self.db['tarefas']

    def listar_tarefas_por_status(self, status):
        return list(self.tarefas_collection.find({'status': status}))

    def listar_tarefas_por_data_vencimento(self, data_vencimento):
        data_vencimento_completa = datetime.strptime(data_vencimento, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)      
        return list(self.tarefas_collection.find({'data_vencimento': {"$lte": data_vencimento_completa}}))
    
    def listar_tarefas(self):
        return list(self.tarefas_collection.find())

    def cadastrar_tarefa(self, descricao, data_vencimento, status="Pendente"):
        # Aqui, estamos definindo a hora para 23:59:59, representando o final do dia
        data_vencimento_completa = datetime.strptime(data_vencimento, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

        tarefa = {
            'descricao': descricao,
            'data_vencimento': data_vencimento_completa,
            'status': status
        }
        self.tarefas_collection.insert_one(tarefa)

    def editar_tarefa(self, tarefa_id, descricao=None, data_vencimento=None, status=None):
        update_data = {}
        if descricao:
            update_data['descricao'] = descricao
        if data_vencimento:
            # Aqui, estamos definindo a hora para 23:59:59, representando o final do dia
            data_vencimento_completa = datetime.strptime(data_vencimento, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            update_data['data_vencimento'] = data_vencimento_completa
        if status:
            update_data['status'] = status

        self.tarefas_collection.update_one({'_id': tarefa_id}, {'$set': update_data})

    def remover_tarefa(self, tarefa_id):
        self.tarefas_collection.delete_one({'_id': tarefa_id})
