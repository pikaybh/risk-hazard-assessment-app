# Internal Modules
...
# External Modules
from typing import List
import argparse
import logging

# Arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('--file', '-F', default="requirements.txt", type=..., help='')
parser.add_argument('--target', '-T', default='@', type=..., help='')
args = parser.parse_args()

# Root 
logger_name = "utils.removeat"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)


class MyString(str):
    def __sub__(self, other: str) -> str:
        return self.split(other)[0]

def rmrear(file_name : str, target : str) -> None:
    with open(file_name, "r") as f:
        lines : List[str] = f.readlines()
    with open(file_name, "w") as f:
        f.writelines([MyString(line) - target + "\n" if target in line else line for line in lines])

# main()
def main() -> None:
    rmrear(args.file, args.target)
    logger.debug(f"Trop '{args.target}' from {args.file} successfully.")

# Main()
if __name__ == "__main__":
    main()