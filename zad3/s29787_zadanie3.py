import gzip

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def parse_fastq(filename):
    """Generator odczytujący plik FASTQ (zwraca listę jakości)."""
    qual_list = []
    with gzip.open(filename, 'rt') as f:
        while True:
            header = f.readline().strip()
            if not header:
                break
            seq = f.readline().strip()
            f.readline()
            qual = f.readline().strip()
            qual_list.append(qual)
    return qual_list


def pred_score_33(str_values):
    pred_list = []
    for char in str_values:
        pred_list.append(ord(char) - 33)
    return pred_list


def transform(mtrix):
    transf = []
    max_len = max(len(row) for row in mtrix)

    for i in range(max_len):
        lisr = []
        for j in range(len(mtrix)):
            if i < len(mtrix[j]):
                lisr.append(mtrix[j][i])
        transf.append(lisr)
    return transf


import numpy as np


def quality(qual_list):
    reading_scores = []
    for q in qual_list:
        reading_scores.append(pred_score_33(q))
    trasf = transform(reading_scores)

    mean = []  # p50 to w rzeczywistości mediana
    p10 = []
    p25 = []
    p75 = []
    p90 = []

    for item in trasf:
        if len(item) > 0:
            r10, r25, r50, r75, r90 = np.percentile(item, (10, 25, 50, 75, 90))
            p10.append(r10)
            p25.append(r25)
            mean.append(r50)
            p75.append(r75)
            p90.append(r90)
        else:
            p10.append(0)
            p25.append(0)
            mean.append(0)
            p75.append(0)
            p90.append(0)

    print("\n" + "=" * 65)
    print(
        f"{'Element':<9} | {'10% (p10)':<9} | {'25% (p25)':<9} | {'50% (Med)':<9} | {'75% (p75)':<9} | {'90% (p90)':<9}")
    print("-" * 65)
    for i in range(len(trasf)):
        print(f"Item {i:<4} | {p10[i]:<9.2f} | {p25[i]:<9.2f} | {mean[i]:<9.2f} | {p75[i]:<9.2f} | {p90[i]:<9.2f}")
    print("=" * 65 + "\n")

    return mean, trasf


def scoring_graph_BASE33(mean, data):
    nt = [i for i in range(len(mean))]

    colors = ('#ed7272', '#ecfa82', '#82fa8c', '#ff5c33', 'yellow')

    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    plt.title(f'SCORING GRAPH, length {len(mean)} bp', size=20, font='arial', color='#636057')
    # line plot foe mean
    plt.plot(nt, mean, c=colors[3], linewidth=1)
    # box plot for list of the quality probability at all the position of reads
    sns.boxplot(data, showfliers=False, width=0.4, color=colors[4], linewidth=0.3)
    ranges = [i for i in range(0, len(mean), 5)]  # set x at the range interval of 5
    ax.grid(1)
    ax.margins(0)
    ax.axhspan(0, 20, facecolor=colors[0], alpha=0.5)  # set back color 0-20
    ax.axhspan(20, 28, facecolor=colors[1], alpha=0.5)  # set back color 20-28
    ax.axhspan(28, 42, facecolor=colors[2], alpha=0.5)  # set back color 28-42
    ax.set_xticks(ranges)
    ax.set_xticklabels(ranges)
    plt.xlim(0, len(nt))
    plt.ylim(0, 42)

    # set the lable..
    plt.xlabel('Nucleotides (bp)', font='arial', fontsize=12, color='#636057')
    plt.ylabel('Phred Score (Q)', font='arial', fontsize=12, color='#636057')
    plt.savefig("per_base_quality.png")


def main():
    filename = "sample_data.fastq.gz"
    fastq_dict = parse_fastq(filename)
    print(len(fastq_dict))
    qscore = quality(fastq_dict)
    scoring_graph_BASE33(qscore[0], qscore[1])


if __name__ == "__main__":
    main()
