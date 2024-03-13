# Imports: standard library
import logging
from typing import Dict, Tuple, Callable

# Imports: third party
import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize


def cross_reference(
    sample: pd.DataFrame,
    model: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Combine the information of a model SNPs frequencies with an individual genotype
    in order to use it later on to compute the log-likelihood.

    :param sample: <pd.DataFrame> Sample genotyping.
    :param model: <pd.DataFrame> Reference populations SNPs frequencies.

    :return: <Tuple[pd.DataFrame, pd.DataFrame]>
    """
    df = sample.merge(model, left_on="rsid", right_on="rsid")
    df = df[
        np.logical_or(
            df.apply(lambda x: x.alt in x.genotype, axis=1),
            df.apply(lambda x: x.ref in x.genotype, axis=1),
        )
    ]
    df = df.reset_index(drop=True)
    columns = model.columns[3:]
    df["mutation"] = df.apply(lambda x: x.genotype.count(x.alt), axis=1)
    df["not_mutation"] = 2 - df["mutation"]
    return df[columns], df[["mutation", "not_mutation"]]


def score_admixture(
    df: pd.DataFrame,
    mutations: pd.DataFrame,
) -> Callable[[np.ndarray], float]:
    """
    Given a df with the sample genotype frequency for the given populaton
    and the mutations, return a function to compute the log-likelihood given
    an admixture proportion.

    :param df: <pd.DataFrame> Reference populations SNPs frequencies.
    :param mutations: <pd.DataFrame> DataFrame with the count of mutated
                                     and non mutated alleles in each SNP.

    :return: <function> Return afunction that given an admixture proportion
                        returns the log-likelihood.
    """

    def score_admixture_(admixture: np.ndarray) -> float:
        """
        Compute the log-likelihood given an admixture proportion.

        :param admixture: <np.ndarray> Admixture proportion.

        :returns: <float> log-likelihood.
        """
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


def estimate_ancestry(sample: pd.DataFrame, model: pd.DataFrame) -> Dict[str, float]:
    """
    Estimate the ancestry of sample given its genotype and a reference population SNP
    frequencies.

    :param sample: <pd.DataFrame> Sample genotyping.
    :param model: <pd.DataFrame> Reference populations SNPs frequencies.

    :return: <Dict[str, float]> Dictionary whose keys are population names and
                                values the corresponding admixture fraction.
    """
    df, mutations = cross_reference(sample, model)
    pops = list(df.columns)

    linear_constraint = LinearConstraint(np.ones(len(pops)), [1], [1])
    bounds = Bounds(0, 1)
    admixture = minimize(
        score_admixture(df, mutations),
        np.ones(len(pops)) / len(pops),
        constraints=[linear_constraint],
        bounds=bounds,
    ).x

    output_str = "Admixture proportions:"
    for pop, admix in zip(pops, admixture):
        output_str += f"\n\t{pop}: {admix*100:.3f}%"
    logging.info(output_str)
    return dict(zip(pops, admixture))
