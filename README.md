# Generative models for nonB-DNA structures generation
## Description

This repository contains code and data for the paper [Deep Generative models for generating DNA secondary structure sequences](https://github.com/powidla/Secondary-structures-generation).

Omics data for Z-DNA stored in [folder](https://github.com/powidla/Secondary-structures-generation/tree/main/data/DeepZ_data/hg19_features/sparse).

Experiments with deep learning models are stored in [notebooks](https://github.com/powidla/Secondary-structures-generation/tree/main/notebooks).

[Z-DNA BERT](https://github.com/mitiau/Z-DNABERT/blob/main/ZDNA-prediction.ipynb) predictions for synthetic data are stored at the [folder](https://github.com/powidla/Secondary-structures-generation/tree/main/zdna_bert).

## Content
**Data_preprocessing** folder consists of three notebooks: 
- **data_prep.ipynb** - script to convert original data and extract features into csv.
- **data_prep_conditional.ipynb** - script to convert original data and extract features with timepoint condition.
- **datatata_prep.ipynb** - script to handle json and sql initial commits.

**data_csvs** folder consists of three files: 

- **df_data (1).csv** - original preprocessed dataset.
- **df_data_tp=-2.csv** - dataset with timepoints two points behind.
- **df_data_tp=-3.csv** - dataset with timepoints three points behind.
It was used to train models in first place.  

**ml_code** folder contains saved model and notebooks for experiments.
**figures** folder has results of classification and feature importance results.




