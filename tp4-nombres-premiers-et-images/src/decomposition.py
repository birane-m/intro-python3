import sys
from classes import NbPremier

if __name__ == "__main__":
    if len(sys.argv) == 2:
        N = int(sys.argv[1])
        nombres = NbPremier(N)
        nombres.decomposition(N)