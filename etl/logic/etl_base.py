import sys
from pathlib import Path
sys.path.append(str((Path(__file__).parent/"..").resolve()))

from typing import Dict

from sqlalchemy import inspect

from lib.db import get_or_create_and_maybe_update


# def 


def sync(
        source_session, source_table,
        target_session, target_table,
        foreign_keys: Dict[str,type] = None,
        dry_run=False
    ):
    
    if foreign_keys is None:
        foreign_keys = {}
    
    for source_record in source_session.query(source_table).all():
        
        print(source_record)
        
        # read key values
        key_values = source_record.get_key_columns_values()
        key_values_dict = dict(zip(target_table.get_key_columns_tuple(), key_values))
        
        # read all values to extract
        etl_values = source_record.get_etl_columns_values()
        etl_values_dict = dict(zip(target_table.get_etl_columns_tuple(), etl_values))
        
        # remove ETL keys from etl_values_dict
        only_values_dict = etl_values_dict.copy()
        for key in key_values_dict.keys():
            del only_values_dict[key]
        
        # process Foreign Keys
        etl_columns = target_table.get_etl_columns_tuple()
        etl_fks = [c for c in etl_columns if '.' in c]
        
        # foreign keys - get or create, or update
        for fk_attr, fk_table in foreign_keys.items():
            fk_keys = fk_table.get_key_columns_tuple()
            
            fk_prefix = f'{fk_attr}.'
            if set(fk_keys).issubset([c.split(fk_prefix)[-1] for c in etl_fks]):
                
                # fk keys values extract
                fk_keys_dict = {}
                for fk_key in fk_keys:
                    source_table_attr = fk_prefix + fk_key
                    fk_keys_dict[fk_key] = etl_values_dict[source_table_attr]
                
                # fk other columns values extract
                fk_etl_columns = fk_table.get_etl_columns_tuple()
                fk_etl_values = {}
                for fk_etl_column in fk_etl_columns:
                    if fk_etl_column in [c.split(fk_prefix)[-1] for c in etl_fks]:
                        fk_value_attr = fk_etl_column.split(fk_prefix)[-1]
                        source_table_attr = fk_prefix + fk_etl_column
                        fk_etl_values[fk_value_attr] = etl_values_dict[source_table_attr]
                
                # remove keys from fk etl values
                for fk_key in fk_keys_dict.keys():
                    del fk_etl_values[fk_key]
                
                # fk instance create
                fk_instance = get_or_create_and_maybe_update(target_session, fk_table, fk_keys_dict, fk_etl_values)
                
                # inject fk id on target table values
                fk_source_table_attr = f'{fk_attr}_id'
                if fk_attr in [c.split('.')[0] for c in key_values_dict]: # fk in keys?
                    for key in key_values_dict.copy():
                        test_key = key.split('.')[0]
                        if test_key == fk_attr:
                            del key_values_dict[key]
                    
                    key_values_dict[fk_source_table_attr] = fk_instance.id
                
                else:
                    only_values_dict[fk_source_table_attr] = fk_instance.id
        
        # print(key_values_dict); break
        
        # remove fk values from etl values
        for etl_fk in etl_fks:
            if etl_fk in only_values_dict:
                del only_values_dict[etl_fk]
        
        # print(only_values_dict); break
        
        # target_record - create, or update
        target_record = get_or_create_and_maybe_update(target_session, target_table, key_values_dict, only_values_dict)
        
        # print(target_record)
