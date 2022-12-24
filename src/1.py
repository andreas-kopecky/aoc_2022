if __name__ == "__main__":
    stack = []
    result = []
    with open("../data/1_input.txt", "r") as fh:
        for line in fh:
            if line == '\n':
                result.append(sum(stack))
                stack = []
            else:
                stack.append(int(line.strip()))
    result.append(sum(stack))
    result.sort()
    print("Solution Part 1:", result[-1])
    print("Solution Part 2:", sum(result[-1:-4:-1]))
