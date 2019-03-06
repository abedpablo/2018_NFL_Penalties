import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce

os.chdir("/Users/abedpablo/Documents/Scripts/NFLpenalties/")
files = glob.glob("*.xlsx")
data = []
for xlsx in files:
    df = pd.read_excel(xlsx)
    basexlsx = os.path.basename(xlsx)
    base = os.path.splitext(basexlsx)[0]
    df[base] = df['Count-A']/df['Games']
    df = df.drop(df.columns[1:12], axis = 1)
    df = df.rename(columns={'Name': 'Team'})
    data.append(df)

penalty = reduce(lambda x, y: pd.merge(x, y, on = 'Team'), data)
penalty = penalty.set_index('Team')
penalties = list(penalty)[1:]
means = penalty.mean(axis=0)
stnd = penalty.std(axis=0)

distrib = penalty.apply(lambda x: ((x-means)/stnd), axis = 1)
sns.set(rc={'figure.figsize':(8.5,7.7)})
ax = sns.heatmap(distrib, cmap="YlGnBu", xticklabels=True, yticklabels=True, linewidths=0, cbar_kws={'label': 'Standard Score'})
ax.set_xticklabels(ax.get_xticklabels(), ha='right', fontsize = '8', rotation = '50')
ax.set(xlabel='Penalty Type')
ax.set_title("How Each Team Draws a Penalty Relative to Other Teams \n 2018 Season \n", fontsize = '18', weight='bold')
plt.tight_layout()
plt.show()