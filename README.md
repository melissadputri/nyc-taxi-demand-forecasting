[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Yi0Zbe2y)
# MAST30034 Project 1 README.md
- Name: Melissa Putri
- Student ID: 1389438

# Project Title: The Battle of NYC Online Taxis: Forecasting Demand for Uber vs. Lyft

**Research Goal:** This research aims to forecast the demand for Uber vs. Lyft in NYC to analyze how Lyft is able to compete with Uber in terms of ride demands.

**Timeline:** The timeline for the research is June 2023 - May 2024, the most recent data available 12 months back.

## Project Structure
The project is organized into several directories to manage data, scripts, and analysis:

- **data/landing:** Directory to store data from upstream. 
- **data/raw:** Data after basic transformations are stored here.
- **data/curated:** Preprocessed, cleaned, and prepared data for analysis is stored here.
- **scripts:** Python scripts for initialising and downloading datasets.
- **notebooks:** Jupyter notebooks used for preprocessing, analysis, and modeling.
- **plots:** Image files of plots produced during data analysis and modeling through Jupyter notebooks.
- **report:** Zip file containing report file written in LaTeX format.

## Setup and Requirements
To run this project, ensure that the necessary Python packages are installed. You can install the required packages by running:

pip install -r requirements.txt

Python ver 3.11.5 was used in building this code.

## Pipeline

To run the pipeline please visit the 'scripts' directory and run '__init__.py' to initialize and download raw data.
Then, please visit the 'notebooks' directory and run these files in order:
1. 'data_preprocessing_1.ipynb': This loads initial data from the landing page and performs basic cleaning methods, including handling missing data, data types conversions, and ensuring data are within valid range. The final data is exported to the raw folder.
2. 'data_preprocessing_2.ipynb': This continues the data preprocessing procedure by standardizing, removing outliers, feature engineering, and aggregating external datasets. This notebook will output two versions of cleaned data, one without standardizing used for exploratory data analysis and another with standardizing for model training, both to the curated folder.
3. 'exploratory_data_analysis.ipynb': This notebook samples cleaned data and produces various plots used to infer correlations and features.
4. 'ML_data_prep.ipynb': This notebook further prepares the cleaned data to ensure that it is in the correct format to feed into the model. This step includes encoding categorical features, one-hot encoding, as well as aggregating these features using the VectorAssembler.
5. 'ML_training_eval.ipynb': This notebook trains the models as well as evaluate its performance by producing diagnostic statistics as well as plots.