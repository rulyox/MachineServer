from subprocess import Popen, PIPE, STDOUT
from flask import Flask, request, jsonify
from config import PYTHON_PATH, MODEL_PATH

# child process
child = None
is_available = False

# server app
app = Flask(__name__)


def write_child(data):
    global child

    if hasattr(child, 'stdin'):
        child.stdin.write(f'{data}\n'.encode())
        child.stdin.flush()


def read_child():
    global child
    global is_available

    if hasattr(child, 'stdout'):
        value = child.stdout.readline()
        data = value.decode().strip()

        return data

    else:
        disable_child()
        raise Exception('Child process error')


def enable_child():
    global is_available

    is_available = True


def disable_child():
    global is_available

    is_available = True


@app.route('/train', methods=['POST'])
def train():
    global child

    try:
        # create child process
        command = [PYTHON_PATH, MODEL_PATH]
        child = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        # receive from child
        while True:
            result = read_child()

            if result.startswith('accuracy:'):
                enable_child()
                response = {'result': result}
                return jsonify(response)

    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    global is_available

    if not is_available:
        response = {'error': 'Child process is not available'}
        return jsonify(response)

    data = request.get_json()
    text = data['index']

    try:
        # send to child
        write_child(text)

        # receive from child
        result = read_child()

        response = {'result': result}
        return jsonify(response)

    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
