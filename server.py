from subprocess import Popen, PIPE, STDOUT
from flask import Flask, request, jsonify

PYTHON = 'python.exe'
EXE = 'test.py'

# child process
child = Popen([PYTHON, EXE], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

# server app
app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    text = data['text']

    # send to child
    child.stdin.write(f'{text}\n'.encode())
    child.stdin.flush()

    # receive from child
    output = child.stdout.readline()
    result = output.decode().strip()

    response = {
        'result': result
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
