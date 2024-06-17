import os


class MyString(str):
    def __sub__(self, other: str) -> str:
        return self.split(other)[0]

with open("requirements.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

target = "@"

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.writelines([MyString(line) - target + "\n" if target in line else line for line in lines])