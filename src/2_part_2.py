points = {"A": 1, "B": 2, "C": 3}

outcomes = {
    "AA": 3, "AB": 6, "AC": 0,
    "BA": 0, "BB": 3, "BC": 6,
    "CA": 6, "CB": 0, "CC": 3
}

strategies = {
    "AX": "AC", "AY": "AA", "AZ": "AB",
    "BX": "BA", "BY": "BB", "BZ": "BC",
    "CX": "CB", "CY": "CC", "CZ": "CA"
}

def map_line(line: str) -> str:
    return line.replace(" ", "").strip()

def outcome(game: str):
    strategy = strategies[game]
    return outcomes[strategy] + points[strategy[1]]

if __name__ == "__main__":
    with open("../data/2_input.txt", "r") as fh:
        games = list(map(map_line, fh.readlines()))
    print("Solution:", sum(map(outcome, games)))
