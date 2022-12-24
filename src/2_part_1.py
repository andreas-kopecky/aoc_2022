points = {"X": 1, "Y": 2, "Z": 3}
outcomes = {
    "AX": 3, "AY": 6, "AZ": 0,
    "BX": 0, "BY": 3, "BZ": 6,
    "CX": 6, "CY": 0, "CZ": 3
}

def map_line(line: str) -> str:
    return line.replace(" ", "").strip()

def outcome(game: str):
    return outcomes[game] + points[game[1]]

if __name__ == "__main__":
    with open("../data/2_input.txt", "r") as fh:
        games = list(map(map_line, fh.readlines()))
    print("Solution:", sum(map(outcome, games)))
