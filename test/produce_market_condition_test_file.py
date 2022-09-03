import sys
import random


def main(argv):
    n = 100
    if len(argv) == 2:
        if argv[1].isdigit():
            n = int(argv[1])

    print("Time,Price")
    for n in range(0, n):
        price = random.random() % 0.500 + 1
        print(f"{n},{price:.04f}")


if __name__ == "__main__":
    main(sys.argv)
