from abc import ABC, abstractmethod
from typing import Any, List, Optional

import pandas as pd
import pymysql.cursors
from sqlalchemy import create_engine, Table, MetaData, inspect, select, insert
from pymongo import MongoClient

from anonimization_script.exceptions import BDTypeNotValid


class DBAdapter(ABC):
    """DB Adapter"""
    @abstractmethod
    def get_all(self, columns: List[str], target: str, index_column: Optional[str]="id"):
        """Get all records from data structure for specified columns

        Args:
            columns (List[str]): Columns of table
            target: (str): Data structure
        """
        pass
    
    @abstractmethod
    def copy_database(self, database: str, tables: List[str]) -> bool:
        """Copy database into another.

        Args:
            database (str): name of database to copy
            tables (List[str]) Table list to change
        Return:
            (bool): Indicate if new database was created
        """
        pass

    @abstractmethod
    def update_target(dataframe, target, index_column: Optional[str]="id"):
        """Massive update to DB

        Args:
            target (str): table to update
            records (List[dict]):records whose we will use to update DB
            index_column (Optional[str], optional): Primary field
            
            . Defaults to "id".
        """
        pass


class DBRelationalAdapter(DBAdapter):
    @abstractmethod
    def delete_all_index(self, target: str):
        """Delete all index from database

        Args:
            target (str): Target database
        """
        pass

    @abstractmethod
    def create_all_index(self, indexs: list):
        """Create indexs in fake database

        Args:
            indexs (list): Index list to create indexs in database
        """
        pass

    @abstractmethod
    def get_indexs(self, target: str):
        """Get indexs from target database

        Args:
            target (str): Target database
        """

def get_data_format(data: Any):
    """Transform data to format with '

    Args:
        data (Any): Data to be formatted

    Returns:
        Any: Data formatted
    """
    
    if type(data) == str:
        return f"'{data}'" if type(data) == str else data
    elif data == None:
        return 'null'
    else:
        return data

class MYSQLAdapter(DBRelationalAdapter):
    """MySQLAdapter"""
    def __init__(self, conn: dict, db_type: str):
        self.dbtype = db_type
        self.db_pymsql = pymysql.connect(**conn, autocommit=True)
        connection_url = f"mysql+pymysql://{conn['user']}:{conn['password']}@{conn['host']}:{conn['port']}/{conn['db']}"
        self.db_sqlalchemy = create_engine(connection_url)
        self.db_sqlalchemy._metadata = MetaData(bind=self.db_sqlalchemy)
        self.db_sqlalchemy._metadata.reflect(self.db_sqlalchemy)

        with self.db_pymsql.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {conn['db']}_fake")
            cursor.execute(f"CREATE DATABASE {conn['db']}_fake")

        connection_url_fake = f"mysql+pymysql://{conn['user']}:{conn['password']}@{conn['host']}:{conn['port']}/{conn['db']}_fake"
        self.db_fake_sqlalchemy = create_engine(connection_url_fake)
        self.db_fake_sqlalchemy._metadata = MetaData(bind=self.db_fake_sqlalchemy)
        self.db_fake_sqlalchemy._metadata.reflect(self.db_fake_sqlalchemy)

    def get_all(self, columns: List[str], target: str, index_column: Optional[str]="id"):
        columns_with_id = columns.copy()
        columns_with_id.append(index_column)
    
        sql=f"SELECT * FROM {target}"
        
        return pd.read_sql(sql, self.db_sqlalchemy)

    def copy_database(self, database: str, tables: List[str]) -> bool:
        
        table_names = inspect(self.db_sqlalchemy).get_table_names()
        
        for table_name in table_names:
            
            table_org = Table(table_name, self.db_sqlalchemy._metadata)
            table_dest = Table(table_name, self.db_fake_sqlalchemy._metadata)

            for column in table_org.columns:
                table_dest.append_column(column.copy())
            
            table_dest.create()

            if not table_name in tables:     
                with self.db_sqlalchemy.connect() as con:
                    query = select(table_org)
                    result = con.execute(query)
                    with self.db_fake_sqlalchemy.connect() as con_fake:
                        con_fake.execute(
                            insert(table_dest),
                            result.mappings().all()
                        )
            
    def get_indexs(self, target):
        with self.db_sqlalchemy.connect() as con:
            result = con.execute(f"SHOW INDEX FROM {target};")
            indexs = result.mappings().all()
        
        return indexs

    def delete_all_index(self, target: str):
        with self.db_sqlalchemy.connect() as con:
            result = con.execute(f"SHOW INDEX FROM {target};")
            indexs = result.mappings().all()

            for index in indexs:
                con.execute(f"ALTER TABLE {index['Table']} DROP INDEX {index['Key_name']}")
            
        return indexs

    def create_all_index(self, indexs: list):
        
        with self.db_sqlalchemy.connect() as con:
            for index in indexs:
                if index['Key_name'] == 'PRIMARY':
                    con.execute(f"""ALTER TABLE {index['Table']}_fake ADD PRIMARY KEY ({index['Column_name']})""")
                else:
                    con.execute(
                        f"""ALTER TABLE {index['Table']}_fake ADD {'UNIQUE' if index['Non_unique'] == 0 else ''} INDEX {index["Key_name"]} ({index['Column_name']});
                        """
                    )

    def update_target(self, dataframe: pd.DataFrame, target: str, index_column: Optional[str]="id"):
        dataframe.to_sql(target, self.db_fake_sqlalchemy, index=False, if_exists="append")

        """
        command = "UPDATE {} SET {} WHERE {} IN ({});"
        case_format = "(CASE {} END)"
        when_format = "WHEN {} THEN {}"
        whens = {}
        ids = [str(record[index_column]) for record in records]
        ids_for_where = ",".join(ids)
        
        cases = {}
        
        columns = records[0].keys()
        
        for column in columns:
            if column != index_column:
                whens[column]={}  
            for record in records:
                if column != index_column:
                    whens[column][record[index_column]] = record[column]
        
        cond = []
        for column in columns:
            if column != index_column:
                for _id in whens[column].keys():
                    replace_value = whens[column][_id]
                    when_value = when_format.format(f"{index_column}={str(_id)}", get_data_format(replace_value))
                    cond.append(when_value)

                cases[column] = " ".join(cond)
                cond = []
        
        global_cases = [f"{column}={case_format.format(when)}" for column, when in cases.items()]
        cases_string = ",".join(global_cases)

        command = command.format(target, cases_string, index_column, ids_for_where)

        with self.db_sqlalchemy.connect() as con:
            try:
                con.execute(command)
            except Exception as e:
                raise Exception(str(e.__dict__['orig']))
        """
            
            
class MONGODBAdapter(DBAdapter):
    """MONGODBAdapter"""

    def __init__(self, conn: dict, db_type: str):
        self.dbtype = db_type
        self.db = conn.pop("db")
        self.db_fake = f"{self.db}_fake"

        self.db_pymongo = MongoClient(**conn)

    def copy_database(self, database: str, tables: List[str]) -> bool:
        pass
    
    def get_all(self, columns: List[str], target: str, index_column: Optional[str]="id"):
        return pd.DataFrame(list(self.db_pymongo[self.db][target].find()))

    def update_target(self, dataframe, target, index_column: Optional[str] = "id"):
        self.db_pymongo[self.db_fake][target].delete_many({})
        self.db_pymongo[self.db_fake][target].insert_many(dataframe.to_dict(orient="records"))
        
class DBFactory:

    DB_ADAPTERS = {
        "mysql": MYSQLAdapter,
        "mongodb": MONGODBAdapter
    }

    @classmethod
    def get_db(cls, dbtype: str) -> DBAdapter:
        """Get Adapter for DB Type

        Args:
            dbtype (str): dbtype

        Raises:
            BDTypeNotValid: DBType is not defined

        Returns:
            DBAdapter: DB Adapter
        """
        try:
            return cls.DB_ADAPTERS[dbtype]
        except KeyError:
            raise BDTypeNotValid(f"DB type '{dbtype}'is not a valid type, please use this instead {','.join(cls.DB_ADAPTERS.keys())}")