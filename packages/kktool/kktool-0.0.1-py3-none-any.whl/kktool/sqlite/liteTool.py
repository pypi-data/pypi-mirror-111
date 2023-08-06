import sqlite3


class KSqlite:

    def __init__(self, file):

        self.db = sqlite3.connect(file)
        # 设置查询结果为字典格式（原先为元组）
        self.db.row_factory = _dict_factory
        self.cur = self.db.cursor()

    def execute_script(self, file):
        """
        执行对应的脚本
        :param conn: 数据库连接
        :param file: sql文件
        :return:
        """
        with open(file, 'r', True, 'UTF-8') as f:
            sql = f.read()
            self.db.executescript(sql)

    def insert_single(self, table, item):
        """
        插入dict数据到对应的表里
        :param conn: DB连接
        :param table: 表名
        :param item: dict数据（单条）
        :return:
        """

        sql = _get_insert_sql(table, item)
        try:
            self.cur.execute(sql, tuple(item.values()))
            self.db.commit()
        except Exception as e:
            print('插入错误', item, sql, e)
            self.db.rollback()


def _dict_factory(cursor, row):
    """
    If returning a tuple doesn’t suffice and you want name-based access to columns,
    you should consider setting row_factory to the highly-optimized sqlite3.
    Row type. Row provides both index-based and case-insensitive name-based
    access to columns with almost no memory overhead.
    It will probably be better than your own custom dictionary-based approach or even a db_row based solution
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _get_insert_sql(table, data):
    """
    生成插入的sql
    :param table: 表名
    :param data: 要插入的数据
    :return:
    """
    # 列的字段
    keys = ', '.join(data.keys())
    # 行字段
    values = ', '.join(['?'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    return sql
