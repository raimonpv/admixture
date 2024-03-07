# Imports: standard library
import sys
import logging
import argparse
import datetime
from typing import Dict, Tuple

# Imports: third party
import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize

# Imports: first party
from loader import load_model, twenty_three
from logger import load_config


def cross_reference(
    sample: pd.DataFrame,
    alleles: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = sample.merge(alleles, left_on="rsid", right_on="rsid")
    df = df[
        np.logical_or(
            df.apply(lambda x: x.alt in x.genotype, axis=1),
            df.apply(lambda x: x.ref in x.genotype, axis=1),
        )
    ]
    df = df.reset_index(drop=True)
    columns = alleles.columns[3:]
    df["mutation"] = df.apply(lambda x: x.genotype.count(x.alt), axis=1)
    df["not_mutation"] = 2 - df["mutation"]
    return df[columns], df[["mutation", "not_mutation"]]


def score_admixture(df: pd.DataFrame, mutations: pd.DataFrame):
    def score_admixture_(admixture: np.ndarray):
        score = -np.dot(
            mutations["mutation"],
            np.log(np.matmul(df, admixture) + 1e-100),
        )
        score -= np.dot(
            mutations["not_mutation"],
            np.log(np.matmul(1 - df, admixture) + 1e-100),
        )
        return score

    return score_admixture_


def estimate_ancestry(file_path: str, model: str) -> Dict[str, float]:
    logging.info(f"Loading admixture {model} model...")
    sample = twenty_three(file_path)
    alleles, pops = load_model(model)
    df, mutations = cross_reference(sample, alleles)
    logging.info("Admixture module loaded!")

    logging.info("Estimating sample ancestry...")
    linear_constraint = LinearConstraint(np.ones(len(pops)), [1], [1])
    bounds = Bounds(0, 1)
    admixture = minimize(
        score_admixture(df, mutations),
        np.ones(len(pops)) / len(pops),
        constraints=[linear_constraint],
        bounds=bounds,
    ).x
    logging.info("Ancestry estimated!")

    output_str = f"{file_path}:"
    for pop, admix in zip(pops, admixture):
        output_str += f"\n\t{pop}: {admix*100:.3f}%"
    logging.info(output_str)
    return dict(zip(pops, admixture))


def setup_log_file(args: argparse.Namespace):
    now_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    load_config(
        log_dir=args.output,
        log_file_basename="log-" + now_string,
    )
    command_line = f"\n{' '.join(sys.argv)}".replace(" --", "\n\t--")
    logging.info(f"Command line was: {command_line}")


def parse_args() -> argparse.Namespace:
    # Create an ArgumentParser object for handling command-line arguments
    parser = argparse.ArgumentParser(
        description="Admixture CLI for processing SNP files and assigning ancestry.",
    )

    # Define the command-line arguments that the script accepts
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        required=True,
        help="The model to use for performing admixture.",
        choices=["K7b", "1000Genomes_population", "1000Genomes_superpopulation"],
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Path to the input SNP file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Path where the output visualization will be saved.",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    setup_log_file(args)
    _ = estimate_ancestry(args.input, args.model)


if __name__ == "__main__":
    main()
