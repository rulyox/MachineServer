from subprocess import Popen, PIPE, STDOUT
from flask import Flask, request, jsonify
from config import PYTHON_PATH, MODEL_PATH

# child process
child = None

# server app
app = Flask(__name__)


def write_child(data):
    global child

    child.stdin.write(f'{data}\n'.encode())
    child.stdin.flush()


def read_child():
    global child

    value = child.stdout.readline()
    data = value.decode().strip()

    return data


@app.route('/train', methods=['POST'])
def train():
    global child

    # create child process
    command = [PYTHON_PATH, MODEL_PATH]
    child = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    # receive from child
    while True:
        result = read_child()

        if result.startswith('accuracy:'):
            response = {
                'result': result
            }
            return jsonify(response)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    global child

    data = request.get_json()
    text = data['index']

    # send to child
    write_child(text)

    # receive from child
    result = read_child()

    response = {
        'result': result
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
