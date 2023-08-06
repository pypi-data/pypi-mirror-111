from typing import List, Dict, Optional, Tuple, Union, Any, NewType

from .m_dao import MDao

# 数据库类型定义
VARCHAR = NewType('VARCHAR', str)
DATETIME = NewType('DATETIME', str)
INT = NewType('INT', int)
TINYINT = NewType('TINYINT', int)

class MBaseT():
    ...


class MBaseSelectExprT():
    '''
    TODO: 查询sql中字段(select_expr)部分
    '''
    def get_select_expr(self):
        pass


class MBaseWhereT():
    '''
    TODO: 查询sql中的where部分， 实现parse_where_sql和get_where_params功能和query_fields
    '''
    def get_where_str(self):
        pass


def parse_where_sql(params):
    '''
    [
        {
            field_name,
            query_type, # like: 字符串匹配, =: 全等, in: 范围, null: 匹配null
            value,
        }
    ]
    '''
    wherelist = []

    for item in params:
        field_name = item.get('field_name')
        query_type = item.get('query_type')
        value = item.get('value')

        if query_type == 'like':
            wherelist.append(f'{field_name} like "%{str(value)}%"')

        elif query_type == '=':
            wherelist.append(f'{field_name} = \'{str(value)}\'')

        elif query_type == 'in':
            if type(value) != list:
                value = [value]

            value = ', '.join([f'\'{str(v)}\'' for v in value])
            wherelist.append(f'{field_name} in ({value})')

        elif query_type == 'null':
            wherelist.append(f'{field_name} is null')

    return ' and '.join(wherelist)


def normallize_insert_value(inst, k, v):
    assert isinstance(inst, MBaseT)

    ann = inst.__annotations__
    typ = ann.get(k)

    if typ == VARCHAR:
        return f'\'{v}\''
    elif typ == DATETIME:
        return 'null' if not v else f'\'{v}\''
    elif typ in [INT, TINYINT]:
        return str(v)
    elif v == None:
        return 'null'

    return f'\'{str(v)}\''


class MBase():
    db_config = None
    table_name = None
    query_fields = {}
    field_names = []

    def __init__(self):
        self._db = MDao(self.db_config)

    def get_where_params(self, mt: Any) -> List[Any]:
        fields = self.query_fields
        params = []

        for field_name in self.field_names:
            if hasattr(mt, field_name) and field_name in fields:
                item = fields[field_name]
                item['value'] = getattr(mt, field_name)

                if type(item['value']) == list:
                    item['query_type'] = 'in'

                params.append(item)

        return params

    async def list(self, mt: Any, limit=True) -> Optional[List[Any]]:
        params = self.get_where_params(mt)

        if limit and len(params) < 1:
            return []

        sql = f'''
        select * from {self.table_name} where {parse_where_sql(params) or ' 1=1'};
        '''

        return await self._db.query(sql)

    async def insert(self, mt: Any):
        return await self.insert_b([mt])

    async def insert_b(self, mts: List[Any]):
        sql = ''

        for mt in mts:
            ks = ', '.join([field_name for field_name in self.field_names if hasattr(mt, field_name)])
            vs = ', '.join([normallize_insert_value(mt, field_name, getattr(mt, field_name)) for field_name in self.field_names if hasattr(mt, field_name)])

            sql += f'''
            insert into {self.table_name} ({ks}) values ({vs});
            '''

        return await self._db.dml(sql)

    async def update(self, mt: Any, where_mt: Any):
        return await self.update_b([(mt, where_mt)])

    async def update_b(self, args: List[Tuple[Any, Any]]): # mt: Any, where_mt: Any
        sql = ''

        for mt, where_mt in args:
            ks = ', '.join([f'{field_name} = {normallize_insert_value(mt, field_name, getattr(mt, field_name))}' for field_name in self.field_names if hasattr(mt, field_name)])

            params = self.get_where_params(where_mt)

            where_str = '1 = 1'

            if len(params) > 0:
                where_str = parse_where_sql(params)

            sql += f'''
            update {self.table_name}
            set {ks}
            where {where_str};
            '''

        return await self._db.dml(sql)

    async def delete(self, mt: Any):
        params = self.get_where_params(mt)

        if len(params) < 1:
            return

        sql = f'''
        delete from {self.table_name} where {parse_where_sql(params)};
        '''

        return await self._db.dml(sql)