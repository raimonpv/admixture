# Imports: standard library
import os
from typing import List, Tuple

# Imports: third party
import pandas as pd


def load_model(model: str) -> Tuple[pd.DataFrame, List[str]]:
    if model == "1000Genomes_superpopulation":
        alleles_path = "1000Genomes.alleles"
        freq_path = "1000Genomes_superpopulation.F"
        pops = ["EUR", "EAS", "AMR", "SAS", "AFR"]
    elif model == "1000Genomes_population":
        alleles_path = "1000Genomes.alleles"
        freq_path = "1000Genomes_population.F"
        pops = [
            "FIN",
            "GBR",
            "CHS",
            "PUR",
            "CDX",
            "CLM",
            "IBS",
            "KHV",
            "PEL",
            "PJL",
            "ACB",
            "GWD",
            "ESN",
            "BEB",
            "MSL",
            "ITU",
            "STU",
            "CEU",
            "YRI",
            "CHB",
            "JPT",
            "LWK",
            "MXL",
            "ASW",
            "TSI",
            "GIH",
        ]
    elif model == "K7b":
        alleles_path = "K7b.alleles"
        freq_path = "K7b.7.F"
        pops = [
            "South Asian",
            "West Asian",
            "Siberian",
            "African",
            "Southern",
            "Atlantic Baltic",
            "East Asian",
        ]
    else:
        raise ValueError(f"Unkown model {model}")
    model_path = os.path.dirname(os.path.realpath(__file__)) + "/models"
    alleles = pd.read_csv(
        os.path.join(model_path, alleles_path),
        delim_whitespace=True,
        header=None,
    )
    frequencies = pd.read_csv(
        os.path.join(model_path, freq_path),
        delim_whitespace=True,
        header=None,
    )
    if model == "1000Genomes_population":
        frequencies = frequencies.iloc[:, :-4]
    alleles.columns = ["rsid", "ref", "alt"]
    return pd.concat([alleles, frequencies], axis=1), pops


def twenty_three(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep="\t", comment="#", header=None, low_memory=False)
    df = df[[0, 3]]
    df.columns = ["rsid", "genotype"]
    return df
