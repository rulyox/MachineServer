from flask import Flask, request, jsonify
from child_controller import create_child, write_child, read_child, enable_child, disable_child, check_available

# server app
app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    epoch = data['epoch']

    # request type check
    if type(epoch) is not int:
        response = {'error': 'Epoch should be an integer'}
        return jsonify(response)

    try:
        # create child process
        create_child()

        # send to child
        write_child(epoch)

        # receive from child
        while True:
            result = read_child()

            if result.startswith('MESSAGE'):
                enable_child()

                # parse result
                result = result.replace('MESSAGE', '')
                key = result.split(':')[0]
                value = result.split(':')[1]

                response = {key: value}
                return jsonify(response)

    except Exception as e:
        disable_child()

        response = {'error': str(e)}
        return jsonify(response)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    if not check_available():
        response = {'error': 'Child process is not available'}
        return jsonify(response)

    data = request.get_json()
    index = data['index']

    # request type check
    if type(index) is not int:
        response = {'error': 'Index should be an integer'}
        return jsonify(response)

    try:
        # send to child
        write_child(index)

        # receive from child
        result = read_child()

        response = {'result': result}
        return jsonify(response)

    except Exception as e:
        disable_child()

        response = {'error': str(e)}
        return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
