from subprocess import Popen, PIPE, STDOUT
from config import PYTHON_PATH, MODEL_PATH

# child process
child = None
is_available = False


def create_child():
    global child

    command = [PYTHON_PATH, MODEL_PATH]
    child = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)


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

    is_available = False


def check_available():
    global is_available

    return is_available
