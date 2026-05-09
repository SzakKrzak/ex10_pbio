import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import StringIO


def main() -> None:
    # 1. Wczytywanie danych
    with open("GDS2490.soft", encoding="utf-8") as file:
        lines = file.readlines()

    start = next(i for i, line in enumerate(lines) if line.startswith("!dataset_table_begin")) + 1
    end = next(i for i, line in enumerate(lines) if line.startswith("!dataset_table_end"))

    table = "".join(
        line for line in lines[start:end]
        if not line.startswith(("#", "^"))
    )

    df = pd.read_csv(StringIO(table), sep="\t")

    # 2. Definiowanie grup
    non_smokers = [
        "GSM114084", "GSM114085", "GSM114086", "GSM114087", "GSM114088"
    ]
    smokers = [
        "GSM114078", "GSM114079", "GSM114080", "GSM114081", "GSM114082", "GSM114083"
    ]

    # 3. Obliczenia
    df['mean_non_smoker'] = df[non_smokers].mean(axis=1)
    df['mean_smoker'] = df[smokers].mean(axis=1)

    df_grouped = df.groupby('IDENTIFIER', as_index=False).agg({
        'mean_non_smoker': 'mean',
        'mean_smoker': 'mean',
        **{col: 'mean' for col in non_smokers + smokers}
    })

    df_grouped['abs_diff'] = (df_grouped['mean_smoker'] - df_grouped['mean_non_smoker']).abs()

    # 4. Wybór Top 10
    df_grouped = df_grouped[df_grouped['IDENTIFIER'] != '--Control']
    top_10_df = df_grouped.sort_values(by='abs_diff', ascending=False).head(10)

    print("=== ANALIZA EKSPRESJI GENÓW ===")
    print(f"Wczytano dane: {len(df_grouped)} genów, 11 próbek")
    print("Grupy: non-smoker (5), smoker (6)\n")
    print("Top 10 genów z największą różnicą ekspresji:")
    print(f"{'Gene':<15} {'Non-smoker':<12} {'Smoker':<10} {'Difference'}")

    for _, row in top_10_df.iterrows():
        gene = row['IDENTIFIER']
        ns = row['mean_non_smoker']
        s = row['mean_smoker']
        diff = s - ns
        sign = "+" if diff > 0 else ""
        print(f"{gene:<15} {ns:<12.1f} {s:<10.1f} {sign}{diff:.1f}")

    print("\nZapisano wykresy:")
    print("- boxplot_top10_genes.png")
    print("- violinplot_top10_genes.png")
    print("- heatmap_top10_genes.png")

    df_long = top_10_df.melt(
        id_vars=['IDENTIFIER'],
        value_vars=non_smokers + smokers,
        var_name='SAMPLE',
        value_name='EXPRESSION'
    )
    df_long = df_long.rename(columns={'IDENTIFIER': 'GENE'})
    df_long['GROUP'] = df_long['SAMPLE'].apply(lambda x: 'SMOKER' if x in smokers else 'NON-SMOKER')

    # --- WYKRES 1: BOXPLOT ---
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_long, x="GENE", y="EXPRESSION", hue="GROUP", palette="Set2")
    plt.title("Boxplot: Porównanie ekspresji dla top 10 genów")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("boxplot_top10_genes.png", dpi=300)
    plt.close()

    # --- WYKRES 2: VIOLINPLOT ---
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df_long, x="GENE", y="EXPRESSION", hue="GROUP", split=True, palette="Set2", inner="quartile")
    plt.title("Violinplot: Rozkład gęstości ekspresji top 10 genów")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("violinplot_top10_genes.png", dpi=300)
    plt.close()

    # --- WYKRES 3: HEATMAP ---
    plt.figure(figsize=(12, 8))
    heatmap_data = top_10_df.set_index('IDENTIFIER')[non_smokers + smokers]

    sns.heatmap(heatmap_data, cmap="viridis", annot=False, cbar_kws={'label': 'Poziom ekspresji'})

    plt.axvline(x=len(non_smokers), color='white', linewidth=3)

    plt.title("Heatmap: Ekspresja w poszczególnych próbkach (Lewa: Non-Smoker | Prawa: Smoker)")
    plt.xlabel("Próbki (Samples)")
    plt.ylabel("Geny (Genes)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("heatmap_top10_genes.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    main()