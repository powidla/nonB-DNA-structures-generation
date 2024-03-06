# Generative models for nonB-DNA structures generation
## Description

This repository contains code and data for the paper [Deep Generative models for generating DNA secondary structure sequences](https://github.com/powidla/Secondary-structures-generation).

Omics data for Z-DNA stored in [folder](https://github.com/powidla/Secondary-structures-generation/tree/main/data/DeepZ_data/hg19_features/sparse).

Experiments with deep learning models are stored in [notebooks](https://github.com/powidla/Secondary-structures-generation/tree/main/notebooks).

[Z-DNA BERT](https://github.com/mitiau/Z-DNABERT/blob/main/ZDNA-prediction.ipynb) predictions for synthetic data are stored at the [folder](https://github.com/powidla/Secondary-structures-generation/tree/main/zdna_bert).

## Content
**data** folder contains fasta and bed files for training purposes: 
- both folders have stored data for mouse and human.
- preprocessed fasta files are available.
- In addition, data in format for [DeepZ](https://github.com/Nazar1997/DeepZ) are availabe in this folder.

**notebooks** folder contains conducted experiments with training models and evaluation of synthetic data: 

- **Detection.ipynb** - notebook for discriminative analysis of synthetic data.
- **seq_analysis.ipynb** - notebook for evaluating novelty and diversity and other results.
- **full_zdna_vqvae.ipynb**, **full_zdna_diff.ipynb**, **full_zdna_wgan.ipynb** - notebooks with training processes and generation of synthetic data.
It was used to train models in first place.  

**saved_models** folder contains saved model and notebooks for experiments.

**figures** folder has results of classification and feature importance results.





