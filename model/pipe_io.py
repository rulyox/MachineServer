import sys


def pipe_input():
    value = sys.stdin.readline()
    data = value.strip()
    return data


def pipe_output(data):
    sys.stdout.write(f'{data}\n')
    sys.stdout.flush()
