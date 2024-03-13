# Imports: standard library
import os
import sys
import logging
import argparse
import datetime

# Imports: third party
import pandas as pd

# Imports: first party
from plot import generate_admixture_plot
from loader import vcf, ancestry, load_model, twenty_three
from logger import load_config
from optimizer import estimate_ancestry


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
        choices=[
            "K7b",
            "1000Genomes_chr21_population",
            "1000Genomes_population",
            "1000Genomes_superpopulation",
        ],
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        type=str,
        required=True,
        help="Path to the input SNP file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Path where the output visualization and the log file will be saved.",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    setup_log_file(args)

    logging.info(f"Loading {len(args.input)} samples...")
    data_dict = {}
    for sample_file in args.input:
        # hacky
        if "Ancestry" in sample_file:
            sample_data = ancestry(sample_file)
        if "vcf" in sample_file:
            sample_data = vcf(sample_file)
        else:
            sample_data = twenty_three(sample_file)
        data_dict.update(sample_data)
    logging.info("Samples loaded!")

    logging.info(f"Loading admixture {args.model} model...")
    model = load_model(args.model)
    logging.info("Admixture model loaded!")

    ancestries = {}
    for sample_id, sample in data_dict.items():
        logging.info(f"Estimating sample {sample_id} ancestry...")
        ancestries[sample_id] = estimate_ancestry(sample, model)

    if args.output:
        data = pd.DataFrame.from_dict(ancestries, orient="index").round(3)
        data.index.name = "id"
        ancestries_path = os.path.join(args.output, "ancestries.csv")
        data.to_csv(ancestries_path)
        logging.info("Saved ancestry predictions to: {ancestries_path}")
        logging.info(f"Saving visualization to: {args.output}/ancestry.pdf")
        generate_admixture_plot(data, args.output)


if __name__ == "__main__":
    main()
