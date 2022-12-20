import numpy as np

class Connection:
    def __init__(self, conn):
        self.connection = conn
    
    def get_data_from_table(self, query):
        return np.array(self.connection.execute(query).fetchall())

    def execute_query(self, query):
        self.connection.execute(query)