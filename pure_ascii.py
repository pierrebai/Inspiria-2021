
import sys


def main(filenames):
    for fn in filenames:
        verify_pure_ascii(fn)


def verify_pure_ascii(fn):
    # Note: opening in binary mode reads a stream of bytes.
    #       read() returns a list of byte.
    data = open(fn, 'rb').read()

    zero_count = 0
    zero_offset = 0

    for i, d in enumerate(data):
        if d > 127:
            print(f"Error: the file '{fn}' is not pure ASCII at offset {i}.")
            # Note: don't bother mentioning potential other zero-bytes,
            #       being non-ASCII is the most important thing!
            return
        elif d == 0:
            zero_count += 1
            if zero_count == 1:
                zero_offset = i

    if zero_count:
        print(f"Warning: the file '{fn}' contains a zero byte at offset {zero_offset}, which may confuse C and C++ programmers.")
    if zero_count > 1:
        print(f"Warning: the file '{fn}' contains {zero_count} zero bytes.")


if __name__ == '__main__':
    main(sys.argv)