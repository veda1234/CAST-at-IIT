import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use('seaborn-ticks')
#matplotlib.use('TkAgg')


def dispersivity_graphs():
    df = pd.read_csv('groundwater/static/fig1_plots.csv', sep=";", na_filter=True)
    df_mod = df.drop(["Reference"], axis=1)  # removing reference from the analysis

    x = df["Alpha_T"].values  # making numpy array
    x1 = df["Alpha_TV"].values
    x, x1 = x[~np.isnan(x)], x1[~np.isnan(x1)]  # removing the nan from the array
    x = np.delete(x, x.argmin())  # removed the lowest value an outlier in our data

    n1 = x.size  # nr. of data in the plot
    n2 = x1.size
    sns.set_style("ticks")
    sns.distplot(x, kde=False, color='red', hist_kws={"linewidth": 3, "color": "r", "alpha": 0.9})
    sns.distplot(x1, kde=False, color='blue', hist_kws={"linewidth": 3, "color": "b", "alpha": 0.9})
    plt.yscale("log")
    plt.xlim((0, 0.006))
    plt.xlabel(r"Transverse dispersivity data, (m)")
    plt.ylabel("Count")
    plt.text(0.003, 30, "Over 90% value are below 0.0013 m")
    plt.text(0.003, 20, r"Total number of $\alpha_T$ data = " + str(n1))
    plt.text(0.003, 15, r"Total number of $\alpha_{TV}$ data = " + str(n2))
    plt.legend([r"Trans. Dispers., $\alpha_T$", r"Trans. Vertical Dispers., $\alpha_{TV}$"])
    plt.savefig("groundwater/static/DispersivityPlots/ticks")
    plt.clf()

    # subplot 2
    df2 = pd.read_csv('groundwater/static/fig1_plots.csv', sep=";", na_filter=True)
    df2_mod = df2.drop(["Reference"], axis=1)
    sns.boxplot(data=df2_mod, showfliers=False, showmeans=True)
    plt.ylabel("Dispersivity (m)")
    plt.text(-0.5, 0.00075, " the median rather than the mean is a better central value")
    plt.tight_layout()
    plt.savefig("groundwater/static/DispersivityPlots/box")
    plt.clf()

    # subplot 3
    df3 = pd.read_csv('groundwater/static/fig1_plots.csv', sep=";", na_filter=True)
    x_at = df3["Alpha_T"].values  # making tablular data to array.
    x_atv = df3["Alpha_TV"].values
    fig, ax = plt.subplots()
    ax1 = plt.plot(x_at, 'o', x_atv, "*")
    # ax1 =plt.plot(x_atv, '*', c="b")
    plt.xlabel("Randomized data order")
    plt.ylabel(r"Dispersivity (m)")
    plt.ylim((0, 0.015))
    plt.legend([r"Trans. Dispers., $\alpha_T$", r"Trans. Vertical Dispers., $\alpha_{TV}$"], loc=2)
    ax2 = plt.axes([0.55, 0.35, 0.35, 0.35])
    ax2.plot(x_at, 'o', x_atv, "*")
    plt.ylim((0, 0.001))
    plt.savefig("groundwater/static/DispersivityPlots/scatter")
    plt.clf()
    dfs4 = pd.read_csv('groundwater/static/fig1_plots.csv', delimiter=";")  # importing data for plot 2
    dfs4_mod1 = dfs4.drop(["Reference"], axis=1)  # removing not required columns and columns with only few data
    dfs4_mod1.columns = [r'$\alpha_T$', r'$\alpha_{Tv}$']  # renaming columns to get alpha symbol for the plot
    data = dfs4_mod1.describe()  # The table below will occupy the empty space right bottom of figure 1 in MS.
    return data
