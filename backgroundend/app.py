from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from backgroundend.models import Models
from engineio.async_drivers import eventlet
import sys
import os


def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)


is_share = True
models = Models()
template_folder = source_path('dist')
static_folder = source_path('dist\\assets')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():  # 定义根目录处理器
    return render_template("index.html")


@app.route('/download')
def download():
    _id = request.args.get('id', '')
    dir_info = models.get_file_dir(_id)
    print(dir_info)
    return send_file(dir_info["dir"])


@socketio.on('notice_web', namespace='/ws_sharing')
def select_file_result():
    if not is_share:
        result = []
    else:
        result = models.get_now_data()
    emit('select_file_result', {"data": result}, namespace="/ws_sharing")


@socketio.on('change_share', namespace='/ws_sharing')
def change_share_status(val):
    print("change_share_status: ", val)
    global is_share
    is_share = val
    emit("change_share", {'data': is_share}, broadcast=True)


# update_file_status
@socketio.on('update_file_status', namespace='/ws_sharing')
def update_file_status(kwarg):
    print(type(kwarg), kwarg)
    _id, is_del = kwarg['id'], kwarg['is_del']
    if is_del:
        models.thread_wrapper_run(models.del_file_db, {"_id": _id})
    else:
        models.thread_wrapper_run(models.update_file_status, {"_id": _id})
        # models.update_file_status(_id)

@socketio.on('connect', namespace='/ws_sharing')
def test_connect(message):
    if is_share:
        reset_data = models.init_front_data()
    else:
        reset_data = []
        print(reset_data)
    emit('ws_connect', {"data": reset_data})


@socketio.on('disconnect', namespace='/ws_sharing')
def test_disconnect():
    print('Client disconnected')


def server(is_dev):
    socketio.run(app, host="0.0.0.0", port="5001")  # 启动服务


if __name__ == '__main__':
    # socketio.init_app(app, async_mode="eventlet", host="0.0.0.0", port="5001")
    socketio.run(app, host="0.0.0.0", port="5001")  # 启动服务
