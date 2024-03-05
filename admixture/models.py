# Imports: standard library
import os
import typing
from collections import Counter

# Imports: third party
import pandas as pd
from tqdm import tqdm

# pylint: disable=too-many-branches


def k7b():
    return [
        "South Asian",
        "West Asian",
        "Siberian",
        "African",
        "Southern",
        "Atlantic Baltic",
        "East Asian",
    ]


def generate_1000genomes_model(input_folder: str, output_folder: str):
    """
    Given the 1000 Geneomes pruned VCF files, generate an admixture model.
    The input folder should contain the 'igsr_samples.tsv' with the population and
    superpopulation of each sample and one vcf file per chromosome with the following
    naming convention '1000G_chr{chrom}_pruned.vcf'. An admixture model for the 1000G
    populations ('1000Genomes_population.T') and another one for the superpopulations
    ('1000Genomes_superpopulation.T') will be generated in the ouput_folder.
    Additionally, a file called '1000Genomes.alleles' containing all the rsids,
    the reference and the alternate alleles for each SNP is also generated.
    In '1000Genomes_population.T' the alternate allele frequency for each population for
    each SNP is provided.
    In '1000Genomes_superpopulation.T' the alternate allele frequency for each
    superpopulation for each SNP is provided.

    :param input_folder: <str> Path to folder with pruned .vcf files.
    :param output_folder: <str> Path to folder to store resulting models.
    """
    file_name = os.path.join(input_folder, "1000G_chr{chrom}_pruned.vcf")
    sample_pop_df = pd.read_csv(
        os.path.join(input_folder, "igsr_samples.tsv"),
        sep="\t",
    )

    keys = sample_pop_df["Sample name"]
    values = sample_pop_df["Population code"]
    sample_pop = dict(zip(keys, values))
    pops = values.dropna().unique()

    values = sample_pop_df["Superpopulation code"]
    sample_superpop = dict(zip(keys, values))
    superpops = values.dropna().unique()

    alleles = []
    pop_freq = []
    superpop_freq = []

    for chrom in range(1, 23):
        print(f"Extracting stats for snps in chromosome {chrom}...")
        with open(file_name.replace("{chrom}", str(chrom)), "r") as file:
            parse = False
            for line in tqdm(file):
                if line.startswith("#CHROM"):
                    if line.endswith("\n"):
                        line = line[:-2]
                    columns = line.split("\t")
                    parse = True
                elif parse:
                    pop_counter: typing.Counter[int] = Counter()
                    superpop_counter: typing.Counter[int] = Counter()
                    n_pop_counter: typing.Counter[int] = Counter()
                    n_superpop_counter: typing.Counter[int] = Counter()
                    if line.endswith("\n"):
                        line = line[:-2]
                    row = line.split("\t")
                    ref = row[3]
                    alt = row[4]
                    if len(ref) > 1 or len(alt) > 1:
                        continue
                    alleles.append(row[2:5])

                    for i, subject in enumerate(columns[9:]):
                        genotype = row[i + 9]
                        if len(genotype) == 3:
                            genotype = sum(int(el) for el in genotype.split("|"))
                            pop_counter[sample_pop[subject]] += genotype
                            superpop_counter[sample_superpop[subject]] += genotype
                            n_pop_counter[sample_pop[subject]] += 2
                            n_superpop_counter[sample_superpop[subject]] += 2

                    row = []
                    for pop in pops:
                        if n_pop_counter[pop] == 0:
                            row.append(0)
                        else:
                            row.append(pop_counter[pop] / n_pop_counter[pop])
                    pop_freq.append(row)

                    row = []
                    for pop in superpops:
                        if n_superpop_counter[pop] == 0:
                            row.append(0)
                        else:
                            row.append(superpop_counter[pop] / n_superpop_counter[pop])
                    superpop_freq.append(row)

    df = pd.DataFrame(superpop_freq)
    df.to_csv(
        os.path.join(output_folder, "1000Genomes_superpopulation.T"),
        sep=" ",
        index=False,
        header=False,
    )
    df = pd.DataFrame(pop_freq)
    df.to_csv(
        os.path.join(output_folder, "1000Genomes_population.T"),
        sep=" ",
        index=False,
        header=False,
    )
    df = pd.DataFrame(alleles)
    df.to_csv(
        os.path.join(output_folder, "1000Genomes.alleles"),
        sep=" ",
        index=False,
        header=False,
    )
