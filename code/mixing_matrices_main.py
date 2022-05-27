import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.models import LinearColorMapper, ColorBar, FixedTicker
from bokeh.palettes import brewer, Viridis5
from bokeh.plotting import figure, show, output_file
from bokeh.models import Slider, HoverTool, Select, CustomJS, ColumnDataSource, FactorRange, NumeralTickFormatter
from bokeh.layouts import widgetbox, row, column

from data_preparation_for_mixing_matrices import *
from plot_specification_mixing_matrices_normalized import *
from generate_mixing_matrices import *

output_file('../output_file/dason_mixing_matrices_proxy_hid_git.html')

def main():
    print('Hello there! We will be preparing some mixing matrices from DASON! Hold on tight! \N{grinning face}')

    # we have two main input files: (1) contact_table and (2) daywise_count_profile
    # contact_table has the information about which patients visited the same unit at a specific day
    # and daywise_count_profile has the antibiotic exposure information of the patients
    # the count_profile holds the cumulative count of each type of antibiotic for the patients on a daily basis

    # reading and processing the patient level data
    # these two lines are commented out because these data tables are not publicly available
    """
    contact_table = '../../data/contable_all_patient_cleaned.csv'
    antibiotic_profile = '../../data/daywise_count_profile.csv'
    """

    # clean the data, get the hospital and unit list
    # commenting out this step as well
    # data_contact, unit_list_per_hospital, data_antibiotic = process_data(contact_table, antibiotic_profile)

    # data is cleaned, now compute the mixing matrices by variables of interest
    """
    we can skip this step if we already have the calculated values; 
    as I have already calculated the values, I'll go to the plotting part
    """
    #prepare_mixing_matrices(data_contact, unit_list_per_hospital, data_antibiotic)

    # mixing matrices computation done, now prepare the plots
    
    hospitals_list = data_contact.hid_proxy.unique()
    hospitals_list.sort()
    print(hospitals_list)
    #exit(1)
    # data preparation functions compute and saves the mixing matrices as csv file
    # reading the csv files generated from the data preparation functions
    data_age_mixing = pd.read_csv('../data/age_mixing_hospital_unitwise_proxyhid.csv', delimiter=',')
    print('data_age_mixing shape:', data_age_mixing.shape)
    print(data_age_mixing.columns)
    data_elix_score_mixing = pd.read_csv('../data/elix_score_mixing_hospital_unitwise_proxyhid.csv', delimiter=',')
    print('data_elix_score_mixing shape: ', data_elix_score_mixing.shape)
    print(data_elix_score_mixing.columns)
    data_antibiotic_rank_mixing = pd.read_csv('../data/antibiotic_rank_mixing_hospital_unitwise_proxyhid.csv', delimiter=',')
    #data_antibiotic_rank_mixing = pd.read_csv('../data/antibiotic_rank_frequency_with_no_antibiotic_and_nan.csv', delimiter=',')
    print('data_antibiotic_rank_mixing shape: ', data_antibiotic_rank_mixing.shape)
    print(data_antibiotic_rank_mixing.head(5))
    print(data_antibiotic_rank_mixing.columns)
    data_no_antibiotic_ratio = pd.read_csv('../data/antibiotic_exposed_vs_no_antibiotic_proportion_proxyhid.csv', delimiter=',')
    data_no_antibiotic_ratio.fillna(0, inplace=True)
    print(data_no_antibiotic_ratio.head(5))
    
    layout = plot_and_manage_javascript_calling(data_age_mixing, data_elix_score_mixing, data_antibiotic_rank_mixing, data_no_antibiotic_ratio,
                                                hospitals_list, unit_list_per_hospital)
    show(layout)


if __name__ == "__main__":
    main()
