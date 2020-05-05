#!/usr/bin/python3.7
import sys

if __name__ == "__main__":
    block_size = int(sys.argv[1])
    msg = sys.argv[2]

    out = msg
    l = len(msg.encode("utf-8"))
    if l % block_size != 0:
        x = block_size - l % block_size
        # else:
        #     print(out)

        for i in range(x):
            out += "\\" + str(hex(x))

    print(out)
