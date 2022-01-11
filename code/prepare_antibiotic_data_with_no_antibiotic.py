import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def prepare_ab_vs_no_ab_proportion(data_contact, data_antibiotic_profile, unit_list_per_hospital):
    
    df_ab = data_antibiotic_profile[['contactid', 'hid_proxy', 'nhsnunitname', 'patientid', 'No_antibiotic']].copy()
    print(df_ab.shape)

    # prepare ab vs no ab proportion data unitwise
    dict_proportion = {'type' : ['No antibiotic for both', 'One exposed to antibiotic another no antibiotic', 'Both are on antibiotic']}
    df_ab_vs_no_ab = pd.DataFrame(dict_proportion)
    for key, value in unit_list_per_hospital.items(): # key : hospitalid and value: corresponding unit_list
        for unit_name in value:
            print(str(key),': ', unit_name)
            df_subset = df_ab[(df_ab['hid_proxy'] == key) &
                                        (df_ab['nhsnunitname'] == unit_name)]
            df_subset = df_subset[['contactid','patientid', 'No_antibiotic']].copy()
            print('data_subset shape: ', df_subset.shape)
            df_merged = pd.merge(df_subset, df_subset, on='contactid')
            #print('merged data shape: ', data_merged.shape)
            #data_antibiotic_contact = data_merged.copy()
            df_contact = df_merged[df_merged['patientid_x'] != df_merged['patientid_y']].copy()
            both_no = len(df_contact[(df_contact['No_antibiotic_x'] == 1) & (df_contact['No_antibiotic_y'] == 1)])
            one_no = len(df_contact[(df_contact['No_antibiotic_x'] == 1) & (df_contact['No_antibiotic_y'] == 0)]) + len(df_contact[(df_contact['No_antibiotic_x'] == 0) & (df_contact['No_antibiotic_y'] == 1)])
            both_yes = len(df_contact[(df_contact['No_antibiotic_x'] == 0) & (df_contact['No_antibiotic_y'] == 0)])
            value = [both_no, one_no, both_yes]
            print(value)
            colname_value = str(key)+'_'+unit_name+'value'
            colname_percentage = str(key)+'_'+unit_name+'percentage'
            df_ab_vs_no_ab[colname_value] = value
            df_ab_vs_no_ab[colname_percentage] = df_ab_vs_no_ab[colname_value]/df_ab_vs_no_ab[colname_value].sum()
            #break
            #df_ab_vs_no_ab[count_colname] = freq
            #print(data_contact.head(10))
            #print(data_contact.shape)
    df_ab_vs_no_ab.to_csv('antibiotic_exposed_vs_no_antibiotic_proportion_hpro.csv', index=False)
    return df_ab_vs_no_ab


def prepare_patient_profile_with_antibiotic(contact_table, data_antibiotic_profile_daywise):
    df_contact = contact_table[['contactid', 'hid_proxy', 'nhsnunitname', 'patientid', 'admissionid', 'day_of_contact']].copy()
    df_antibiotic = data_antibiotic_profile_daywise[['patientid', 'admissionid', 'administrationdate', 'a', 'b', 'c', 'd']].copy()

    df_patient_with_antibiotic = pd.merge(df_contact, df_antibiotic, how='left',
        left_on=[ 'patientid', 'admissionid', 'day_of_contact'],
        right_on=['patientid', 'admissionid', 'administrationdate'])
    print(df_patient_with_antibiotic.head(5))

    df_patient_with_antibiotic.sort_values(['patientid', 'admissionid', 'day_of_contact'], inplace=True)
    print(df_patient_with_antibiotic.head(10))

    cols = ['a', 'b', 'c', 'd']
    df = df_patient_with_antibiotic.copy()
    #df = df_patient_with_antibiotic.groupby(['patientid', 'admissionid', 'day_of_contact'])[cols].ffill().fillna(0)
    df.update(df.groupby(['patientid', 'admissionid'])[cols].ffill().fillna(0))
    #df_patient_with_antibiotic.head(20)
    #print(df.head(20))

    df['No_antibiotic'] = 0
    df['No_antibiotic'].loc[(df['a']+df['b']+df['c']+df['d']) == 0] = 1
    print(df.head(50))

    data_groupby_hospital = df.groupby('hid_proxy')
    unit_list_per_hospital = data_groupby_hospital.apply(lambda x: x['nhsnunitname'].unique())
    unit_list_per_hospital = unit_list_per_hospital.to_dict()

    df_ab_vs_no_ab = prepare_ab_vs_no_ab_proportion(df_contact, df, unit_list_per_hospital)
    print(df_ab_vs_no_ab)


# read two input file: one holds the contact information of the patients and the other holds the antibiotic exposure information
data_antibiotic_profile_daywise = pd.read_csv('../data/daywise_count_profile.csv', delimiter=',', na_values=['\\N'])
print(data_antibiotic_profile_daywise.head(5))

contact_table = pd.read_csv('../data/contable_all_patient_cleaned.csv', delimiter=',', na_values=['\\N'])
#df_contact = contact_table.copy()
#print(contact_table.shape)
print(contact_table.head(5))

prepare_patient_profile_with_antibiotic(contact_table, data_antibiotic_profile_daywise)

# ended reading input

