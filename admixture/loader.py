# Imports: standard library
import os
from typing import Dict, List, Optional

# Imports: third party
import pandas as pd


def load_model(model: str) -> pd.DataFrame:
    """
    Loads the model file with the frequencies and the mutations
    at each SNP.

    :param model: <str> Name of the model. Choices: 1000Genomes_superpopulation,
                         1000Genomes_pop.txt, K1000Genomes_chr21_population, 7b.

    :returns: <pd.DataFrame> Pandas Dataframe with the frequencies,
                             the mutations and the rsid for each SNP.
    """
    if model == "1000Genomes_superpopulation":
        model_name = "1000Genomes_superpop.txt"
    elif model == "1000Genomes_population":
        model_name = "1000Genomes_pop.txt"
    elif model == "1000Genomes_chr21_population":
        model_name = "1000Genomes_chr21_pop.txt"
    elif model == "K7b":
        model_name = "K7b.txt"
    else:
        raise ValueError(
            f"Unknown model {model}. Expected 1000Genomes_superpopulation,"
            "1000Genomes_population or K7b",
        )
    model_path = os.path.dirname(os.path.realpath(__file__)) + "/models"
    model_df = pd.read_csv(
        os.path.join(model_path, model_name),
        delim_whitespace=True,
    )
    if model == "1000Genomes_chr21_population":
        model_df = model_df[["rsid", "ref", "alt", "ASW", "CEU", "GWD", "PEL", "PUR"]]
    return model_df


def twenty_three(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Loads and parses a 23andMe genotype file.

    :param file_path: <str> Full path to the 23andMe file.

    :return: <Dict[str, pd.DataFrame]> Pandas dataframe with the rsid and the genotype
                            for each SNP. Key is the file name.
    """
    df = pd.read_csv(file_path, sep="\t", comment="#", header=None, low_memory=False)
    df = df[[0, 3]]
    df.columns = ["rsid", "genotype"]
    return {os.path.split(file_path)[-1]: df}


def ancestry(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Loads and parses an AncestryDNA genotype file.

    :param file_path: <str> Full path to the AncestryDNA file.

    :return: <Dict[str, pd.DataFrame]> Pandas dataframe with the rsid and the genotype
                            for each SNP. Key is the file name.
    """
    df = pd.read_csv(file_path, sep="\t", comment="#", header=None, low_memory=False)
    df = df[[0, 4]]
    df.columns = ["rsid", "genotype"]
    return {os.path.split(file_path)[-1]: df}


def _convert_genotypes(ref, alt, genotypes):
    genotype_map = {"0": ref, "1": alt, ".": "N"}
    # Convert genotype strings using the map
    mapped_genotypes = genotypes.apply(
        lambda genotype: "".join(
            genotype_map.get(allele, "N")
            for allele in genotype.replace("|", "/").split("/")
        ),
    )
    return mapped_genotypes


def vcf(file_path: str, ids: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """
    Loads and parses a vcf file.

    :param file_path: <str> Full path to the vcf file.
    :param ids: <List[str]> If provided, just the ids provided will be parsed.
                            Default: None.

    :return: <Dict[str, pd.DataFrame]> Dict whose keys are the sample id and the values
                                       a Pandas dataframe with the rsid and the genotype
                                       for each SNP of the sample id.
    """
    vcf_data = pd.read_csv(file_path, sep="\t", skiprows=5, header=None, comment="#")
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#CHROM"):
                line = line[1:]
                if line.endswith("\n"):
                    line = line[:-2]
                columns = line.split("\t")
    sample_columns = columns[9:]
    if ids is not None:
        sample_columns = [id for id in sample_columns if id in ids]
    sample_data: Dict[str, pd.DataFrame] = {sample: [] for sample in sample_columns}

    # Correct header processing
    vcf_data.columns = columns

    for _, row in vcf_data.iterrows():
        rsid = row["ID"]
        ref, alt = row["REF"], row["ALT"]
        genotypes = row[sample_columns]
        # Use _convert_genotypes function
        converted_genotypes = _convert_genotypes(ref, alt, genotypes)

        # Accumulate data in a list of dicts for DataFrame conversion
        for sample in sample_columns:
            sample_data[sample].append(
                {"rsid": rsid, "genotype": converted_genotypes[sample]},
            )

    # Convert each list of dicts to a DataFrame
    for sample in sample_columns:
        sample_data[sample] = pd.DataFrame(sample_data[sample])

    return sample_data
