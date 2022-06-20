"""Module to do generic logic for cases"""

import pandas as pd

from cases import Case
from cases.rules import RuleFactory
from anonimization_script.utils import tranform_to_rules, prepare_to_array


class CompliancerCase(Case):

    def __init__(self, meta, mapper):
        self._meta = meta
        self._mapper = mapper

    def start(self):
        # TODO: Refactorizar esto en funcion
        # TODO: Convertir este modulo en algo mas portable    
        # TODO: Definir mapper a nivel global y no por case object o al menos agregar el nombre del case a object case    
        global_context = {}
        global_context["mapper"] = self._mapper

        rules = self._meta.get_rules()
        steps = rules.keys()
        
        for step in steps:
            adapter = self._meta.get_db_for(step)
            database_rule = rules[step]
            
            for table in database_rule:
                table_rules = database_rule[table]
                columns = [column for column in database_rule[table]]
            
                records = [dict(zip(columns, prepare_to_array(record))) for record in adapter.get_all(columns=columns, table=table)]

                df_org = pd.DataFrame(records)
                df_fake = df_org.copy()
                
                rules_functions = tranform_to_rules(RuleFactory, table_rules)
                
                for i in range(len(df_fake)):

                    row = df_fake.loc[i]

                    for key in rules_functions.keys():
                        global_context["current_value"] = row[key]
                        rule_parts = table_rules[key].split(":")
                        
                        if len(rule_parts) > 0:
                            if rule_parts[0] == "inheritance":
                                global_context["route"] = rule_parts[1]
                            elif rule_parts[0] == "template":
                                global_context["template"] = rule_parts[1]

                        row[key] = rules_functions[key](**global_context)()
                        
                        if row[key] != None:
                            print(table, key, global_context["current_value"], row[key])
                            row_to_save = f"{step}.{table}.{key}"
                            mapi = { global_context["current_value"]: row[key] }

                            self._mapper.add_map(row_to_save, mapi)
                            row_dict = row.to_dict()
                            global_context["row"] = row_dict
                    