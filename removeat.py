from typing import List


class MyString(str):
    def __sub__(self, other: str) -> str:
        return self.split(other)[0]

# main()
def main() -> None:
    with open("requirements.txt", "r") as f:
        lines : List[str] = f.readlines()

    target : str = "@"

    with open("requirements.txt", "w") as f:
        f.writelines([MyString(line) - target + "\n" if target in line else line for line in lines])

# Main()
if __name__ == "__main__":
    main()