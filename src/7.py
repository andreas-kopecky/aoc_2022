from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import List

@dataclass
class File:
    name: str
    size: int


class Directory:
    def __init__(self, name: str, parent: Directory = None):
        self.name: str = name
        self.parent: Directory = parent
        self.children: List[Directory] = []
        self.files: List[File] = []

    def child_directory(self, name: str) -> Directory:
        child = self.__class__(name=name, parent=self)
        self.children.append(child)
        return child

    def size(self) -> int:
        size = sum(map(lambda f: f.size, self.files))
        for directory in self.children:
            size += directory.size()
        return size

    def add_file(self, file: File):
        self.files.append(file)

    def __str__(self):
        return f"directory: {self.name}, size: {self.size()}"


class Shell:
    def __init__(self):
        self.stack: deque[Directory] = deque()
        self.directories: List[Directory] = []

    def parse_command(self, line: str):
        _, *command = line.split()
        match command:
            case ["cd", ".."]:
                self.stack.popleft()
            case ["cd", directory]:
                if len(self.stack) == 0:
                    directory = Directory(name=directory)
                else:
                    directory = self.stack[0].child_directory(name=directory)
                self.stack.appendleft(directory)
                self.directories.append(directory)
            case ["ls"]:
                pass

    def parse_output(self, line: str):
        output = line.split()
        match output:
            case ["dir", _]:
                pass
            case [size, name]:
                file = File(name, int(size))
                self.stack[0].add_file(file)


def solve():
    with open("../data/7_input.txt", "r") as fh:
        lines = fh.readlines()

    shell = Shell()
    for line in lines:
        line = line.strip()
        if line.startswith("$"):
            shell.parse_command(line)
        else:
            shell.parse_output(line)

    sizes = [d.size() for d in shell.directories]
    part_1 = sum(s for s in sizes if s <= 100000)

    root = shell.directories[0]
    required = 30000000 - (70000000 - root.size())
    mapping = [s for s in sizes if s >= required]
    part_2 = min(mapping)
    return part_1, part_2

if __name__ == "__main__":
    print(solve())