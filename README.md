# Admixture

`Admixture` is a Python-based command-line interface designed to compute genetic admixture from SNP data. This tool simplifies the process of determining the proportionate ancestry in individuals from multiple source populations using genotype data from one of several consumer genotyping companies. Additionally, the software provides a detailed visualization functionality of ancestry breakdown. Several models are supported, and guidance is provided for users to define their own models.

Companion code to the Final project for CSE 284 (WI24) authored by Raimon Padrós I Valls (A59025488) and Lucas Patel (A13041630); Group 21.

## Getting Started

### Prerequisites

`Admixture` is written in Python and requires several dependencies. A premade conda environment is provided for convenience, or packages can be installed manually. If installing conda for the first time, we suggest using [Miniconda](https://docs.anaconda.com/free/miniconda/) as a lightweight installer.

### Installation

Follow these steps to install `Admixture`:

1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/AdmixtureAnalysisTool.git
    ```
2. Next, configure the conda environment and other dependencies as follows:
    ```bash
    make setup
    ```

### Usage
Usage may vary depending on use case. An example usage is provided below:
```python
python admixture.py -m k7b -i ./sample-data/1.txt -o ./results
```

## Contributing
We welcome contributions from the community. If you're interested in improving `Admixture`, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch and open a pull request.

## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file in the project repository.

## Acknowledgments

Special thanks to the many contributors and the broader community of geneticists and bioinformaticians whose insights and feedback have made the development of `Admixture` possible.

Credit is given to the following authors:
* []()
