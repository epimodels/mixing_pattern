# mixing_pattern.github.io

# Mixing Matrices from Hospital Data

This is the codebase for generating a visualization dashboard of mixing matrices calculated from different hospital units in DASON dataset. There are a number of variables which were used to draw these matrices namely patient's age, Elixhauser Commorbidity Index and antibiotic category. The dataset contains information from 24 hospitals and total number of units is 299. There are two dropdowns to choose a hospital and a unit within that hospital. The dashboard is dynamically updated using the selection from the user.

The dashboard is hosted here: http://go.wsu.edu/hospitalmatrix

## Necessary libraries

Python libraries used for this project.

* python version 3.6
* Pandas and Numpy  for data preparation
* Bokeh for visualization

## Input files

There are a number of input files which are uploaded in the data folder of this repository. They are pre-calculated and ready to use for generating the mixing matrices.

* age_mixing_hospital_unitwise_proxyhid.csv
* antibiotic_rank_mixing_hospital_unitwise_proxyhid.csv
* elix_score_mixing_hospital_unitwise_proxyhid.csv
* antibiotic_exposed_vs_no_antibiotic_proportion_proxyhid.csv

## Run the file

The main file is the *mixing_matrices_main.py*.

There are a number of other supporting files for data preparation and plot generation.

The main file takes input from two patient level data file to calculate matrices which could not be added to the repository due to privacy and ethical concern. The calculated csv files in the data folder can be used to run and test the program. To run the file, type in the command line:

`python mixing_matrices_main.py

This will generate a standalone HTML file which shows the plots.
