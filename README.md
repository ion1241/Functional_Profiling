# Functional profiling for eDNA-based monitoring in coastal environments

Code and data for the article:

> **Towards functional profiling for eDNA-based monitoring in coastal environments: a comparison of three approaches**  
> Ion L. Abad-Recio

This repository contains scripts and processed data used to compare three methods for profiling microbial functional communities in estuarine and coastal sediments from the Basque coast (Bay of Biscay):

- Functional prediction from 16S metabarcoding data with Tax4Fun2
- Functional gene detection using GeoChip microarrays
- Direct functional annotation of shotgun metagenomes

The study evaluates whether the three approaches produce concordant functional profiles and whether they can distinguish samples with “Good” and “Bad” environmental status based on a physicochemical Pressure Index (PI).

## Repository structure

```
.
├── README.md
├── metadata.csv
├── SWARM_OTUs_curated.fasta
├── SWARM_table_filtered.tsv
├── Tax4Fun_KEGGs.csv
├── MG_2017_ORFKOs.txt
├── KofamKoalaOut.csv
├── Python_scripts/
│   ├── ibatches.py
│   └── retrieve_fasta_from_GIDs.py
└── R_scripts/
    ├── Tax4Fun_prediction.R
    └── Find_sig_cats_functions.R
```

## Workflow

### 1. 16S metabarcoding and Tax4Fun2

The 16S metabarcoding workflow generates representative sequence variants (SVs), applies abundance and quality filters, and predicts KEGG Ortholog (KO) abundances with Tax4Fun2.

The main R entry point is [`R_scripts/Tax4Fun_prediction.R`](R_scripts/Tax4Fun_prediction.R). It:

1. Runs `runRefBlast()` against a Tax4Fun2 reference database.
2. Runs `makeFunctionalPrediction()` using the filtered SV table.
3. Normalizes predictions by 16S copy number and sets the minimum reference identity to 97%.

Before running this script, edit `setwd()` and `REFPATH` and provide the Tax4Fun2 reference database.

```bash
Rscript R_scripts/Tax4Fun_prediction.R
```

### 2. GeoChip microarray processing

GeoChip GenBank gene identifiers are converted into KEGG Ortholog identifiers through:

1. [`Python_scripts/retrieve_fasta_from_GIDs.py`](Python_scripts/retrieve_fasta_from_GIDs.py), which retrieves protein FASTA sequences using Entrez.
2. [`Python_scripts/ibatches.py`](Python_scripts/ibatches.py), which batches Gene/GenBank IDs for API requests.
3. KofamKOALA, which assigns KEGG Orthologs to protein sequences.

The Python script is designed to process `GeochipGenbankIDList.txt` and write `GeoID.fasta`:

```bash
cd Python_scripts
python retrieve_fasta_from_GIDs.py
```

Before running it, set an appropriate NCBI Entrez contact email and ensure that `GeochipGenbankIDList.txt` is available in the working directory.

Only the highest-scoring KOfamKOALA annotation is retained. Repeated GenBank identifiers assigned to the same KO are combined, and KOs detected in fewer than six of the eight samples are removed.

### 3. Statistical comparison

[`R_scripts/Find_sig_cats_functions.R`](R_scripts/Find_sig_cats_functions.R) contains helper functions for:

- Comparing KO categories between “Good” and “Bad” samples using Wilcoxon rank-sum tests.
- Testing relationships with continuous variables using Kendall rank correlations.

```r
source("R_scripts/Find_sig_cats_functions.R")
```

In the manuscript, the abundance of each KO was compared across environmental-status groups using Wilcoxon rank-sum tests. Non-metric multidimensional scaling (NMDS), Bray-Curtis distances, Mantel tests and envfit were used to compare community profiles and environmental variables.

## Data

| File | Description |
|---|---|
| `metadata.csv` | Sample metadata, including station, environment, estuary, sampling date, pressure-index values and physicochemical measurements. |
| `SWARM_OTUs_curated.fasta` | Curated representative SWARM sequence variants derived from 16S metabarcoding data. |
| `SWARM_table_filtered.tsv` | Filtered SWARM abundance table used for functional prediction. |
| `Tax4Fun_KEGGs.csv` | Processed KEGG Ortholog abundance table generated or used by the Tax4Fun2 workflow. |
| `MG_2017_ORFKOs.txt` | Shotgun metagenome-derived KEGG Ortholog data. |
| `KofamKoalaOut.csv` | KofamKOALA GeoChip protein-to-KEGG Ortholog annotations. |

The repository includes processed or intermediate data used in the functional-profile comparison. Raw sequencing reads and complete pipeline-specific intermediate outputs may need to be obtained separately.

## Methods summary

The study analysed eight estuarine and coastal sediment samples from the Basque coast. Four samples were classified as “Bad” and four as “Good” based on their five-year average physicochemical Pressure Index (PI5yAvg), with a cutoff of 2.5.

After prevalence filtering, the datasets contained:

- 8,589 unique KOs from Tax4Fun2
- 12,161 unique KOs from shotgun metagenomes
- 1,468 unique KOs from GeoChip

Tax4Fun2 and metagenomics showed substantial KO occurrence overlap and significantly concordant abundance patterns among shared KOs. GeoChip profiles showed lower functional richness and little concordance with the sequencing-based datasets.

In total, 229 KOs were concordantly overrepresented in samples with “Bad” status by both Tax4Fun2 and metagenomics. These KOs were enriched for functions including methanogenesis, reductive acetyl-CoA metabolism, citrate-cycle pathways and dissimilatory sulfate reduction.

## Requirements

### R

The scripts use:

- `Tax4Fun2`
- `vegan`
- `ggplot2`

### Python

- Python 2.7 or Python 3 for utility compatibility
- `Biopython`

### External tools and resources

- Tax4Fun2 reference database
- VSEARCH
- Cutadapt
- SWARM
- LULU
- SqueezeMeta
- KofamKOALA
- Kofam database or HMM profiles
- NCBI Entrez access
- NCBI, SILVA or equivalent data dependencies required by the upstream pipeline

Exact package versions and the external database configuration should be documented before repeating the complete analysis on a fresh system.

## Running the available scripts

Run the Tax4Fun2 prediction workflow from the repository root after editing the paths in the R script:

```bash
Rscript R_scripts/Tax4Fun_prediction.R
```

Run the GenBank-ID/FASTA retrieval utility from `Python_scripts/` after configuring Entrez and providing the identifier list:

```bash
cd Python_scripts
python retrieve_fasta_from_GIDs.py
```

The scripts and files currently included represent a processed analysis repository rather than a complete, one-command reproducibility pipeline.

## Citation

If you use this code or data, please cite:

> Abad-Recio, I. L., et al. (2024). **Towards functional profiling for eDNA-based monitoring in coastal environments: a comparison of three approaches**. *Environmental DNA*, 5, e504. https://doi.org/10.1002/edn3.504

Please also cite the relevant upstream tools and databases used in the workflows, including Tax4Fun2, SWARM, VSEARCH, SqueezeMeta and KofamKOALA.

## Contact

Ion L. Abad-Recio  
GitHub: https://github.com/ion1241