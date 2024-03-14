# Admixture

## Navigating the file structure
The `Admixture` package is broken down into several components:

### admixture.py
This file provides the main CLI functionality for the tool.

### loaders.py
This file implements several functions to load SNP data from a variety of sources, including 23andMe, Ancestry, and 1000Genomes.

### logger.py
This file initializes the log file.

### optimizer.py
This file contains the algorithm performing the optimization.

### models.py
This file manages loading the various admixture models. The main model we computed is based on the 1000Genomes project.

Our process for generating admixture models from the 1000 Genomes Project involves analyzing pruned Variant Call Format (VCF) files to explore the genetic diversity within populations and superpopulations. We start with an input file, `igsr_samples.tsv`, which lists each sample along with its associated population and superpopulation data, and a series of pruned VCF files named following the convention `1000G_chr#_pruned.vcf`, one for each chromosome. Our analysis has resulted in the creation of two key admixture models: `1000Genomes_pop.txt` and `1000Genomes_superpop.txt`, which detail the alternate allele frequency and catalog all rsIDs with their reference and alternate alleles for each SNP across populations and superpopulations.

### plot.py
This file handles visualization of admixture breakdown for an arbitrary number of input samples.

### models
This folder contain the different admixture models available.

### ps2-results
This folder contain the necessary files to reproduce the benchmarking results against the ADMIXTURE software used during PS2.

### sample-data
This folder contain multiple 23andme files that can be used to test the package.

### demo.ipynb
This is a Jupyter Notebook used as a usage demonstration and to obtain the main results on the report.

