import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def generate_admixture_plot(data):
    """
    Generate an admixture plot from the given data.

    Args:
    - data: A 2D numpy array of shape (N, M) where N is the number of samples
            and M is the number of distinct populations. Each element represents
            the proportional contribution of each population to the samples.

    The function generates a stacked bar chart where each bar represents a sample
    and the segments of the bar represent the contributions from different populations.
    """
    # Set seaborn style for better aesthetics
    sns.set(style="whitegrid")

    # Number of samples and populations
    num_samples, num_populations = data.shape

    # Sort samples by the first population's contribution for visual clarity
    # This can be adjusted based on the desired sorting criteria
    sorted_indices = np.argsort(data[:, 0])
    sorted_data = data[sorted_indices]

    # Create figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each population's contribution per sample as a stacked bar
    bottoms = np.zeros(num_samples)
    for i in range(num_populations):
        ax.bar(range(num_samples), sorted_data[:, i], bottom=bottoms, edgecolor='white')
        bottoms += sorted_data[:, i]

    # Customize the plot to make it more informative
    ax.set_xlabel('Sample')
    ax.set_ylabel('Population Contribution')
    ax.set_title('Admixture Plot')
    ax.set_xticks([])  # Remove x-axis tick marks for clarity

    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
# Create a dummy data array for demonstration purposes
N, M = 50, 5  # 50 samples, 5 distinct populations
np.random.seed(42)  # For reproducible results
data = np.random.dirichlet(alpha=[1]*M, size=N)  # Generate random proportions

generate_admixture_plot(data)

# Specify the output file path and name
output_file = "admixture_plot.png"
generate_admixture_plot(data, output_file)
