import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys


def plot_intervals(input_tsv, main_cols):
    df = pd.read_csv(input_tsv)
    index_column = 'Interval'
    value_column = 'Percentage'
    all_composers = [c for c in df.columns if c != index_column]
    sub_cols = [c for c in all_composers if c not in main_cols]
    main_df = df[[index_column] + main_cols]
    main_df = pd.melt(main_df, id_vars=index_column, var_name='Composer', value_name=value_column)
    sub_df = df[[index_column] + sub_cols]
    sub_df = pd.melt(sub_df, id_vars=index_column, var_name='Test Piece', value_name=value_column)
    f, axes = plt.subplots(2, 1)
    ax = sns.barplot(x=index_column, y=value_column, hue='Composer', data=main_df, ax=axes[0])
    ax = sns.barplot(x=index_column, y=value_column, hue='Test Piece', data=sub_df, ax=axes[1])
    plt.show()

if __name__ == '__main__':
    input_tsv = sys.argv[1]
    main_plot = ['Josquin', 'La Rue']
    plot_intervals(input_tsv, main_plot)