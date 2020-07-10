import sys

if __name__ == '__main__':
    while True:
        data = sys.stdin.readline()
        text = data.strip()

        result = 'result is ' + text

        sys.stdout.write(f'{result}\n')
        sys.stdout.flush()
