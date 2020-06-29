import sys
import time

def read(f):
        while True:
                l = f.readline()
                if l:
                        #yield l
                        continue
                while True:
                        last_pos = f.tell()
                        l = f.readline()
                        if l:
                                yield l
                                continue
                        time.sleep(1)
                        f.seek(last_pos)

def main():
        args = sys.argv
        if len(args) < 2:
                print(f"Usage: {args[0]} filename")
                sys.exit(0)
        fname = args[1]
        with open(fname, "r") as f:
                for l in read(f):
                        print(l.strip())

if __name__ == "__main__":
        main()
