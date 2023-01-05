import webview
import sys
import getopt
import psutil
import subprocess
import os
import re
import threading
from backgroundend.app import server
from backgroundend.models import Models
from queue import Queue

window = None
child = None
q = Queue()


class Api(Models):
    def __init__(self):
        self.db = None
        super(Api, self).__init__()

    def close_win(e):
        global child
        window.destroy()
        child.join()
        exit()

    def min_win(e):
        window.minimize()

    def open_file_dialog(self):
        file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
        try:
            file_path, = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
        except:
            print('cacel')
            return

        def run_add():
            _file_share = self.add_file_db(file_path)
            self.init_initial_data()

        if len(self.file_share_list) == 0:
            self.thread_wrapper_run(run_add)
        else:
            current_file_share = None
            for file_share in self.file_share_list:
                if file_share["name"] in file_path:
                    current_file_share = file_share
                    break
            if current_file_share:
                return current_file_share
            else:
                self.thread_wrapper_run(run_add)


def main():
    is_dev = get_is_dev()
    if is_dev:
        global window
        global child
        url, pid = start_window_dev()
        # url = "http://127.0.0.1:5173/#/"
        child = threading.Thread(target=server, daemon=True)
        child.start()
        api = Api()
        window = webview.create_window("lan_sharing", url=url + "#/index", js_api=api, frameless=True)
        webview.start(debug=True)
        kill(pid)
    else:
        start_window_pro()


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


def kill(proc_pid):
    os.system("taskkill /t /f /pid %s" % proc_pid)
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def start_window_dev():
    rules = r"http:\/\/127\.0\.0\.1:\d+\/"
    line_str = ''
    runlog = subprocess.Popen("cd frontend && yarn dev", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    for line in iter(runlog.stdout.readline, b''):
        line_str = line.decode('utf-8')
        if 'Local' in line_str:
            print(line_str)
            runlog.stdout.close()
            break
    print('for 循环结束')
    url = re.findall(rules, line_str.replace("\x1b[1m", '').replace("\x1b[22m", ''))[0]

    return url, runlog.pid


def start_window_pro():
    global window
    global child
    api = Api()
    child = threading.Thread(target=server, daemon=True, args=(True,))
    child.start()
    url = 'http://127.0.0.1:5001'
    window = webview.create_window("lan_sharing", url=url + "#/index", js_api=api, frameless=True)
    webview.start(debug=True)


if __name__ == '__main__':
    main()
    # api = Api()
