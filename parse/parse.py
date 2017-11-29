import re
from util.case import *


exit_action = ['exit', 'quit']
show_type = ['databases', 'tables', 'users']


def __exit(_):
    return {
        'type': 'exit',
    }


def __show(statement):
    kind = statement[1]
    if kind not in show_type:
        return None
    return {
        'type': 'show',
        'kind': kind,
    }


def __desc(statement):
    return{
        'type': 'desc',
        'table_name': statement[1],
    }


def __use(statement):
    db_name = statement[1]
    return {
        'type': 'use',
        'db_name': db_name,
    }


def __create(statement):
    kind = statement[1]
    if kind not in ['database', 'table', 'user']:
        return None
    if kind == 'database':
        return {
            'type': 'create',
            'kind': kind,
            'name': statement[2],
        }
    elif kind == 'table':
        result = pattern_map['create'].findall(" ".join(statement))
        tuple = result[0]
        table_name = tuple[0]
        fields = tuple[1].split(',')
        data = {
            'type': 'create',
            'kind': kind,
            'table_name': table_name,
            'fields': [],
        }
        for elem in fields:
            field = elem.strip().split(' ')
            field_name = field[0]
            field_type = field[1]
            field_keys = []
            for i in range(2, len(field)):
                field_keys.append(field[i])
            data['fields'].append({
                'field_name': field_name,
                'field_type': field_type,
                'field_keys': field_keys
            })
        return data
    elif kind == 'user':
        return {
            'type': 'create',
            'kind': 'user',
            'name': statement[2],
            'pwd': statement[4],
        }


def __drop(statement):
    kind = statement[1]
    if kind not in ['database', 'table']:
        return None
    name = statement[2]
    return {
        'type': 'drop',
        'kind': kind,
        'name': name,
    }


def __grant(statement):
    result = pattern_map['grant'].findall(" ".join(statement))
    tuple = result[0]
    print(tuple)
    return {
        'type': 'grant',
        'priv': tuple[0],
        'db': tuple[1],
        'user': tuple[2],
    }


def __revoke(statement):
    result = pattern_map['revoke'].findall(" ".join(statement))
    tuple = result[0]
    print(tuple)
    return {
        'type': 'revoke',
        'priv': tuple[0],
        'db': tuple[1],
        'user': tuple[2],
    }


def __insert(statement):
    result = pattern_map['insert'].findall(" ".join(statement))

    # 上面返回的结果是数组中套一个元祖，我们吧元祖摘出来操作
    tup = result[0]

    # 元组内的内容包括：要插入的表名，目标字段，字段的值
    if len(tup) == 3:
        table_name = tup[0]
        data = {
            'type': 'insert',
            'table_name': table_name,
            'kwargs': {},
        }

        # 取出插入的数据，封装为字典
        fields = tup[1].replace(' ', '').split(',')
        values = tup[2].replace(' ', '').split(',')
        if len(fields) != len(values):
            raise Exception('The number of fields is not equal to values')
        for i in range(0, len(fields)):
            field = fields[i]
            value = values[i]
            # 这里有个bug，就是当你输入insert into student（）values（）的时候，会出“”
            if field == '':
                continue
            if "'" in value or '"' in value:
                value = value.replace("'", "").replace('"', '')
            else:
                try:
                    value = int(value)
                except Exception:
                    raise Exception('The value %s should be put in quotes if it is not a number')
            data['kwargs'][field] = value
        return data
    return None


def __select(statement):
    result = pattern_map['select'].findall(" ".join(statement))
    tup = result[0]
    fields = tup[0].split(',')
    for i in range(0, len(fields)):
        fields[i] = fields[i].strip()
    return {
        'type': 'select',
        'fields': fields,
        'table_name': tup[1],
    }


def __update(statement):
    result = pattern_map['update'].findall(" ".join(statement))
    tup = result[0]
    tmp = re.split(" |,", tup[1])
    elems = []
    for elem in tmp:
        if elem == "":
            continue
        if "'" in elem or '"' in elem:
            elem = elem.replace("'", "").replace('"', '')
        elems.append(elem)
    if len(elems) % 3 != 0:
        raise Exception('Syntax error: set not matched!')
    data = {}
    for i in range(0, len(elems), 3):
        data[elems[i]] = elems[i + 2]
    return {
        'type': 'update',
        'table_name': tup[0],
        'data': data,
    }


def __delete(statement):
    result = pattern_map['delete'].findall(" ".join(statement))
    if len(result) != 1:
        raise Exception('Syntax error: check your delete statement!')
    return {
        'type': 'delete',
        'table_name': result[0],
    }

pattern_map = {
    'insert': re.compile(r'insert into (.*)\((.*)\) values\((.*)\)'),
    'create': re.compile(r'create table (.*)\((.*)\)'),
    'select': re.compile(r'select (.*) from (.*)'),
    'update': re.compile(r'update (.*) set (.*)'),
    'delete': re.compile(r'delete from (.*)'),
    'grant': re.compile(r'grant (.*) on (.*) to (.*)'),
    'revoke': re.compile(r'revoke (.*) on (.*) from (.*)'),
}


action_map = {
    'exit': __exit,
    'quit': __exit,
    'show': __show,
    'use': __use,
    'create': __create,
    'desc': __desc,
    'insert': __insert,
    'select': __select,
    'drop': __drop,
    'update': __update,
    'delete': __delete,
    'grant': __grant,
    'revoke': __revoke,
}

case_map = {
    'range': RangeCase,
    'in': InCase,
    'not_in': NotInCase,
    '=': IsCase,
    '!=': IsNotCase,
    '>': GreaterCase,
    '<': LessCase,
    '>=': GAECase,
    '<=': LAECase,
    'like': LikeCase,
}


def raise_exception(sql):
    raise Exception('Syntax Error for: %s' % sql)


def filter_space(list):
    ret = []
    for it in list:
        if it.strip() == '' or it.strip() == 'and':
            continue
        ret.append(it)
    return ret


def parse(sql):

    # 预处理，全部变成小写
    statement = sql.lower()

    # 首先以where为依据划分为简单句与复杂句
    if 'where' in statement:
        statement = statement.split('where')
    else:
        statement = statement.split('WHERE')

    # 处理简单句，即划分后的第一部分
    base_statement = filter_space(statement[0].split(' '))

    # 简单句包括exit，quit，show *，desc *， create *， drop *, insert into table（id）values（1）
    # 那么单指令的只有 exit， quit了， 检查是否符合这个标准
    if len(base_statement) < 2 and base_statement[0] not in exit_action:
        raise_exception(sql)

    action_type = base_statement[0]

    if action_type not in action_map:
        raise_exception(sql)

    action = action_map[action_type](base_statement)

    if action is None or 'type' not in action:
        raise_exception(sql)

    action['conditions'] = {}

    conditions = None

    if len(statement) == 2:
        conditions = filter_space(statement[1].split(' '))

    if conditions:
        for i in range(0, len(conditions), 3):
            field = conditions[i]
            symbol = conditions[i + 1]
            condition = conditions[i + 2]

            if symbol == 'range':
                condition_tmp = condition.replace('(', '').replace(')', '').split(',')
                start = condition_tmp[0].strip(' ')
                end = condition_tmp[1].strip(' ')
                case = case_map[symbol](start, end)

            elif symbol == 'in' or symbol == 'not_in':
                condition_tmp = condition.replace('(', '').replace(')', '').replace(' ', '').split(',')
                case = case_map[symbol](condition_tmp)

            else:
                case = case_map[symbol](condition)

            action['conditions'][field] = case

    return action
