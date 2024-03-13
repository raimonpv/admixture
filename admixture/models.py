# Imports: standard library
import os
import typing
from typing import List, Optional
from collections import Counter

# Imports: third party
import pandas as pd
from tqdm import tqdm

# pylint: disable=too-many-branches


def generate_1000genomes_model(
    input_folder: str,
    output_folder: str,
    chromosomes: Optional[List[int]] = None,
):
    """
    Given the 1000 Geneomes pruned VCF files, generate an admixture model.
    The input folder should contain the 'igsr_samples.tsv' with the population and
    superpopulation of each sample and one vcf file per chromosome with the following
    naming convention '1000G_chr{chrom}_pruned.vcf'. An admixture model for the 1000G
    populations ('1000Genomes_pop.txt') and another one for the superpopulations
    ('1000Genomes_superpop.txt') will be generated in the ouput_folder.
    The files contain all the rsids, the reference and the alternate alleles, as well
    as the alternate allele frequency for each population for each SNP is provided.

    :param input_folder: <str> Path to folder with pruned .vcf files.
    :param output_folder: <str> Path to folder to store resulting models.
    :param chromosomes: <List[str]> List of chromosomes to use to create the model.
                                    If None, all chromosomes will be used. Default: None
    """
    if chromosomes is None:
        chromosomes = list(range(1, 23))

    file_name = os.path.join(input_folder, "1000G_chr{chrom}_pruned.vcf")
    sample_pop_df = pd.read_csv(
        os.path.join(input_folder, "igsr_samples.tsv"),
        sep="\t",
    )

    keys = sample_pop_df["Sample name"]
    values = sample_pop_df["Population code"]
    sample_pop = dict(zip(keys, values))
    pops = values.dropna().unique()[:-1]

    values = sample_pop_df["Superpopulation code"]
    sample_superpop = dict(zip(keys, values))
    superpops = values.dropna().unique()[:-1]

    alleles = []
    pop_freq = []
    superpop_freq = []

    for chrom in chromosomes:
        print(f"Extracting stats for snps in chromosome {chrom}...")
        with open(
            file_name.replace("{chrom}", str(chrom)),
            "r",
            encoding="utf-8",
        ) as file:
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

    alleles = pd.DataFrame(alleles, columns=["rsid", "ref", "alt"])
    frequencies = pd.DataFrame(superpop_freq, columns=superpops)
    df = pd.concat([alleles, frequencies], axis=1)
    df.to_csv(
        os.path.join(output_folder, "1000Genomes_superpop.txt"),
        sep=" ",
        index=False,
    )
    frequencies = pd.DataFrame(pop_freq, columns=pops)
    df = pd.concat([alleles, frequencies], axis=1)
    df.to_csv(
        os.path.join(output_folder, "1000Genomes_pop.txt"),
        sep=" ",
        index=False,
    )
