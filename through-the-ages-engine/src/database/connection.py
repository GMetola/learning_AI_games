from pymongo import MongoClient
import logging

class DatabaseConnection:
    def __init__(self, host='localhost', port=27182, database_name='through_the_ages'):
        """Inicializa la conexión a MongoDB

        Args:
            host (str): Dirección del servidor MongoDB
            port (int): Puerto del servidor MongoDB
            database_name (str): Nombre de la base de datos
        """
        self.host = host
        self.port = port
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self) -> bool:
        """Establece conexión con MongoDB"""
        try:
            # Conecta a MongoDB en el puerto especificado
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[self.database_name]

            # Verifica la conexión
            self.client.admin.command('ping')
            logging.info(f"Conexión exitosa a MongoDB en {self.host}:{self.port}")
            return True

        except Exception as e:
            logging.error(f"Error conectando a MongoDB: {e}")
            return False

    def get_collection(self, collection_name: str):
        """Obtiene una colección de la base de datos

        Args:
            collection_name (str): Nombre de la colección

        Returns:
            Collection: Objeto de colección de MongoDB
        """
        if self.db is None:
            raise ConnectionError("Base de datos no conectada")
        return self.db[collection_name]

    def close(self):
        """Cierra la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada")