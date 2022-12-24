def solve():
    with open("../data/6_input.txt", "r") as fh:
        content = fh.read()

    def search_forward(content, n=4):
        for i, window in ((j, content[j:j+n]) for j in range(len(content))):
            if len(set(window)) == n:
                return i + n

    return search_forward(content, 4), search_forward(content, 14)

if __name__ == "__main__":
    print(solve())
