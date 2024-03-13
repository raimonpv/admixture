# Imports: standard library
import os
from typing import Optional

# Imports: third party
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def generate_admixture_plot(data: pd.DataFrame, output_path: Optional[str] = None):
    """
    Generate an admixture plot from the given data.
    The function generates a stacked bar chart where each bar represents a sample
    and the segments of the bar represent the contributions from different populations.

    :param data: <pd.DataFrame> Pandas DataFrame where each row represents the
                                proportional contribution of each population to the
                                samples in the index.
    :param output_path: <str> Folder where to save the resulting figure.
    """
    # Set seaborn style for better aesthetics
    sns.set(style="whitegrid")

    _fig, ax = plt.subplots(figsize=(10, 3))

    data.plot.bar(stacked=True, ax=ax, width=1)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")
    ax.set_xticklabels(data.index)

    plt.tight_layout()
    plt.show()
    if output_path is not None:
        plt.savefig(os.path.join(output_path, "ancestry.pdf"))
