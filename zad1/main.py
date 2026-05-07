import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main() -> None:

    table = []
    ap = False
    try:
        with open('GDS2490.soft') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("^"):
                    continue
                if line.startswith("!dataset_table_begin"):
                    ap = True
                if line.startswith("!dataset_table_end"):
                    ap = False
                if ap:
                    table.append(line)
    except:
        pass


if __name__ == "__main__":
    main()