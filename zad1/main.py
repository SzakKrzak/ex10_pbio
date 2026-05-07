import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import StringIO


def main() -> None:
    with open("GDS2490.soft", encoding="utf-8") as file:
        lines = file.readlines()

    start = next(i for i, line in enumerate(lines) if line.startswith("!dataset_table_begin")) + 1
    end = next(i for i, line in enumerate(lines) if line.startswith("!dataset_table_end"))

    table = "".join(
        line for line in lines[start:end]
        if not line.startswith(("#","^"))
    )

    df = pd.read_csv(StringIO(table), sep="\t")
    non_smokers = [
        "GSM114084",
        "GSM114085",
        "GSM114086",
        "GSM114087",
        "GSM114088",
    ]

    smokers = [
        "GSM114078",
        "GSM114079",
        "GSM114080",
        "GSM114081",
        "GSM114082",
        "GSM114083",
    ]

    df = df.melt([
        "gene",
        "sample",
        "expression",
        "group",

    ]
    )

    print(df[smokers])


if __name__ == "__main__":
    main()