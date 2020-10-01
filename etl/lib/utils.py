from hashlib import md5
import functools


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


class EtlValidationMixin:
    '''Classe filha deve ser o atributo "KEY_COLUMNS" e "ETL_COLUMNS" na forma de tupla contendo strings'''
    
    def __repr__(self):
        keys = self.get_key_columns_tuple()
        values = self.get_key_columns_values()
        args = ', '.join(f'{x[0]}={x[1]!r}' for x in zip(keys, values))
        return "{}({})".format(str(type(self).__name__), args)
    
    @classmethod
    def get_key_columns_tuple(cls):
        assert cls.KEY_COLUMNS
        return cls.KEY_COLUMNS
    
    @classmethod
    def get_etl_columns_tuple(cls):
        assert cls.ETL_COLUMNS
        return cls.ETL_COLUMNS
    
    def get_key_columns_values(self):
        return tuple(rgetattr(self, c) for c in self.get_key_columns_tuple())
    
    @classmethod
    def get_key_columns_hash__from_values(cls, values):
        hash_obj = md5()
        for value in values:
            hash_obj.update(str(value).encode('utf-8', errors='ignore'))
        return hash_obj.digest()
    
    def get_key_columns_hash(self):
        return self.get_key_columns_hash__from_values(self.get_key_columns_values())
    
    def get_etl_columns_values(self):
        return tuple(rgetattr(self, c) for c in self.get_etl_columns_tuple())
    
    def get_etl_columns_hash(self):
        hash_obj = md5()
        for value in self.get_etl_columns_values():
            hash_obj.update(str(value).encode('utf-8', errors='ignore'))
        return hash_obj.digest()
    
    @classmethod
    def dict_etl_from_values_list(cls, values):
        return dict(zip(cls.get_etl_columns_tuple(), values))
    
    @classmethod
    def keys_values_from_values_dict(cls, values_dict):
        keys = cls.get_key_columns_tuple()
        return tuple([values_dict[k] for k in keys])