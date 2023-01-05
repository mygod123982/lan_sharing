import moment
import ntpath
import win32con
from win32 import win32file


def format_time(t):
    # update_timezones = moment.date(t).timezone("Asia/Shanghai")
    update_timezones = moment.date(t).timezone("utc-8")
    return update_timezones.strftime('%Y-%m-%d %H:%M:%S')


def get_file_base_time(file_name):
    f = win32file.CreateFile(
        file_name,
        win32file.GENERIC_READ,
        0,
        None,
        win32con.OPEN_EXISTING,
        0,
        None,
    )
    tuple_time = win32file.GetFileTime(f)
    return (format_time(t) for t in tuple_time)


def wrapper_to_file(file_name):
    __name, __ext = ntpath.basename(file_name).rsplit('.', 1)
    __c_t, __a_t, __w_t = get_file_base_time(file_name)
    result = {
        "name": __name,
        "type": __ext,
        "dir": file_name,
        "create_time": __c_t,
        "access_time": __a_t,
        "write_time": __w_t
    }
    return result


if __name__ == '__main__':
    main_file_name = "../main.py"
    c_t, a_t, w_t = get_file_base_time(main_file_name)
    print(f"文件：{main_file_name} 创建时间： {c_t}, 访问时间： {a_t}, 修改时间： {w_t}")
