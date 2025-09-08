from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️  python-dotenv não está instalado. Usando variáveis de ambiente do sistema.")

class MongoDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        try:
            # Conexão SEM autenticação (para desenvolvimento)
            self.host = os.getenv('MONGO_HOST', 'localhost')
            self.port = os.getenv('MONGO_PORT', '27017')
            self.database_name = os.getenv('MONGO_DATABASE', 'car_dealer_db')
            
            connection_string = f"mongodb://{self.host}:{self.port}/"
            print(f"🔗 Conectando sem autenticação: {connection_string}")
            
            # Conectar ao MongoDB
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Testar conexão
            self.client.admin.command('ping')
            print("✅ Conectado ao MongoDB com sucesso!")
            
            # Selecionar database
            self.db = self.client[self.database_name]
            
            # Criar a coleção se não existir
            if 'cars' not in self.db.list_collection_names():
                self.db.create_collection('cars')
                print("✅ Coleção 'cars' criada!")
            
            print(f"✅ Database '{self.database_name}' acessível!")
            
        except ConnectionFailure as e:
            print(f"❌ Erro de conexão com MongoDB: {e}")
            raise
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            raise
    
    def get_database(self):
        return self.db
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("🔌 Conexão com MongoDB fechada.")

# Singleton instance
mongodb_connection = MongoDBConnection()