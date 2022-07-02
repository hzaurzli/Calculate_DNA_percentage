import os

def rate(path,o):
    for i in os.listdir(path):
        with open(path + i, "r") as words:
            name = i.split('.')[0]
            word = words.readlines()
            rate = word[len(word) - 1:len(word)]
            rate = ''.join(rate)
            rate = rate.split(' ')[0]
            with open(o, "w") as f:
                line = name + ',' + rate + '\n'
                f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mapping rate")
    parser.add_argument("-p", "--path", required=True, type=str, help="log files path")
    parser.add_argument("-o", "--out", required=True, type=str, help="summary file")
    Args = parser.parse_args()

    rate(Args.path,Args.out)
