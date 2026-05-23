import sys
from agent import run_agent

if __name__ == "__main__":
    command = sys.argv[1]
    result = run_agent(command)
    print(result)