import sqlite3
import hashlib
import time
from backgroundend.file_make import wrapper_to_file
import sys
import os
import getopt


def get_is_dev():
    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "DP", longopts=["development", "production"])
        print(opts)
        for opt, arg in opts:
            if opt in ('-dev', '--development'):
                print(f'is dev')
                return True
            else:
                return False
    except getopt.GetoptError as e:
        print(str(e))


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)


class Models:
    # 初始化 数据库
    def __init__(self):
        is_dev = get_is_dev()
        if is_dev:
            self.db_path = source_path('share.db')
        else:
            self.db_path = 'c://tmp/share.db'
        self.file_share_list = None
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)

        def run_init():
            self.__init_db()
            self.init_initial_data()

        self.thread_wrapper_run(run_init)

    def init_front_data(self):
        return self.file_share_list

    # 多线程隔离所以要重新请求连接
    def thread_wrapper_run(self, fn, arg=None):
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.db.row_factory = dict_factory
        self.db.execute('pragma foreign_keys = 1')
        if arg:
            print(arg)
            fn(**arg)
        else:
            fn()
        self.db.close()
        self.db = None

    def add_file_db(self, _dir):
        cursor = self.db.cursor()
        cursor.execute("select * from dirList where dir = ?", (_dir,))
        current_result = cursor.fetchone()
        if current_result:
            return current_result
        else:
            _id = hashlib.md5((str(time.time()) + _dir).encode('utf-8')).hexdigest()
            cursor.execute("insert into dirList(dir, id) VALUES (?, ?)", (_dir, _id))
            file_share_l = list(wrapper_to_file(_dir).values())
            file_share_l[2] = _id
            cursor.execute("insert into fileShareList(name,type,dir_id,create_time,access_time, write_time) "
                           "values (?, ? ,?, ?, ?, ?)", tuple(file_share_l))
            self.db.commit()
            cursor.close()
            return _dir, _id

    def del_file_db(self, _id):
        cursor = self.db.cursor()
        cursor.execute("delete from dirList where id = ?", (_id,))
        print('del --', _id)
        self.db.commit()
        cursor.close()

    def get_now_data(self):
        def get_result():
            self.init_initial_data()

        self.thread_wrapper_run(get_result)
        return self.init_front_data()

    def update_file_status(self, _id):
        cursor = self.db.cursor()
        cursor.execute("update fileShareList set is_pause ="
                       " abs(is_pause -1) where id=?", (_id,))
        self.db.commit()
        cursor.close()

    def __get_all_db(self):
        cursor = self.db.cursor()
        cursor.execute("select * from fileShareList")
        all_share_files = cursor.fetchall()
        cursor.close()
        return all_share_files

    def init_initial_data(self):
        cursor = self.db.cursor()
        cursor.execute("select * from fileShareList")
        self.file_share_list = cursor.fetchall()
        cursor.close()

    def __init_db(self):
        cursor = self.db.cursor()
        cursor.execute("create table if not exists dirList(dir varchar(255) unique, id varchar(20) unique,"
                       "  primary key(id))")
        cursor.execute("create table if not exists fileShareList("
                       "id integer not null primary key autoincrement,"
                       "name varchar(255),"
                       "type varchar(20),"
                       "dir_id varchar(20),"
                       "create_time date,"
                       "access_time date,"
                       "write_time date,"
                       "is_pause tinyint(1) default 0,"
                       "foreign key(dir_id) references dirList(id) on delete cascade,"
                       "unique(dir_id)"
                       ")")
        self.db.commit()
        cursor.close()

    def get_file_dir(self, _id):
        result = None

        def run():
            nonlocal result
            cursor = self.db.cursor()
            cursor.execute("select * from dirList where id = ?", (_id,))
            result = cursor.fetchone()
            cursor.close()

        self.thread_wrapper_run(run)
        return result
