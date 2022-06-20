from abc import ABC, abstractmethod
from typing import List

from pony.orm import Database, db_session

class DBAdapter(ABC):
    """DB Adapter"""
    @abstractmethod
    def get_all(self, columns: List[str], target: str):
        """Get all records from data structure for specified columns

        Args:
            columns (List[str]): Columns of table
            target: (str): Data structure
        """

class MYSQLAdapter(DBAdapter):
    """MySQLAdapter"""
    def __init__(self, conn: str, db_type: str):
        self.db_type = db_type
        self.db = Database()
        self.db.bind(provider=db_type, **conn)

    @db_session
    def get_all(self, columns: List[str], target: str):
        columns_format = ",".join(columns) if columns else "*"
        return self.db.select(f"select {columns_format} from {target}")
