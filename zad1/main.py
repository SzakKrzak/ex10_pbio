import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


df = pd.read_csv('GDS2490.soft')
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='gene', y='expression')
plt.title('Rozkład')
plt.show()