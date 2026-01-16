import matplotlib.pyplot as plt

def plot_score_hist(df, bins=20):
    plt.figure()
    plt.hist(df["alignment_score"], bins=bins)
    plt.xlabel("Alignment score (cosine similarity)")
    plt.ylabel("Number of papers")
    plt.title("Distribution of thematic alignment scores")
    plt.show()

def plot_year_mean(df):
    year_mean = df.groupby("year")["alignment_score"].mean().sort_index()
    plt.figure()
    plt.plot(year_mean.index, year_mean.values, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Mean alignment score")
    plt.title("Mean alignment score by year")
    plt.show()