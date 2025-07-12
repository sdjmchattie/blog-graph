from dotenv import load_dotenv

load_dotenv()

from graph import graph

if __name__ == "__main__":
    graph.invoke()
