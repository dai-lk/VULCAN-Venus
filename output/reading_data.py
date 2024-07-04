#!usr/bin/env python
# _*_ coding:utf-8 _*_
# @Time: 2024/4/28 16:29
# @File: reading_data.py
# @Author: Longkang Dai

import numpy as np
import pickle

data_file_path = "./Nominal_Bkzz_SO2.vul"

with open(data_file_path, 'rb') as handle:
    read_data = pickle.load(handle)

altitude = read_data['atm']['zco'][1:] # (cm)
T = read_data['atm']['Tco'] # Temperature (K)
P = read_data['atm']['pco'] # Pressure (dyne/cm2)
density = read_data['atm']['M'] # Total atmospheric number density (cm-3)
k_all = read_data['variable']['k'] # reaction rate coefficient
Kzz_i = read_data['atm']['Kzz'] # Kzz (cm2/s) at the boundary of the neighbouring grids, its length = len(alt)-1
vulcan_spec = read_data['variable']['species'] # the list of the species name string

bins = read_data['variable']['bins'] # the bins of the actinic flux (nm), shaped in (n_bins)
sflux = read_data['variable']['aflux'] # the actinic flux (cm-2 s-1 nm-1), shaped in (n_alt, n_bins)

O2_mixing_ratio = read_data['variable']['ymix'][:,vulcan_spec.index('O2')] # an example for O2 mixing ratio
O2_number_density = read_data['variable']['y'][:,vulcan_spec.index('O2')] # an example for O2 number density

# a useful tool for reading the source and sink reactions of the selected species
def reac_rate(check_sp): # check_sp = 'O2' for example
    # the reaction index for all the forward reactions (in our Venus model they refer to all the involved reactions.
    # The reverse reactions auto-calculated by VULCAN are banned since we provide directly the coefficients for all.
    # Then, the model regards them as the 'forward reactions'.)
    R_indx = []
    for i in read_data['variable']['Rf']:
        R_indx.append(i) # all the index are odd numbers, e.g.: 1,3,5,7,9 ...

    sink_indx = []
    sink_reactant = []
    sink_count = []
    source_indx = []
    source_reactant = []
    source_count = []

    for i in range(len(R_indx)):
        reaction = read_data['variable']['Rf'][R_indx[i]] # reaction formula in str
        reaction = ''.join(reaction.split())
        left = reaction.split('->')[0].split('+')
        right = reaction.split('->')[1].split('+')
        count_left = left.count(check_sp)
        count_right = right.count(check_sp)
        count_sp = 0
        if count_left > count_right:
            count_sp = count_left - count_right
            sink_count.append(count_sp)
            sink_indx.append(R_indx[i])
            sink_reactant.append(left)
        elif count_left < count_right:
            count_sp = count_right - count_left
            source_count.append(count_sp)
            source_indx.append(R_indx[i])
            source_reactant.append(left)

    # calculate rate profiles
    sink_rate = [] # (n_reaction, nz)
    source_rate = [] # (n_reaction, nz)
    for i in range(len(sink_indx)):
        rate = k_all[sink_indx[i]]
        for reactant in sink_reactant[i]:
            if reactant == 'M':
                r_density = density
            else:
                r_density = read_data['variable']['y'][:, vulcan_spec.index(reactant)]
            rate = rate * r_density  # k*[A]*[B]...
        sink_rate.append(rate*sink_count[i])

    for i in range(len(source_indx)):
        rate = k_all[source_indx[i]]
        for reactant in source_reactant[i]:
            if reactant == 'M':
                r_density = density
            else:
                r_density = read_data['variable']['y'][:, vulcan_spec.index(reactant)]
            rate = rate * r_density  # k*[A]*[B]...
        source_rate.append(rate*source_count[i])

    sink_rate = np.array(sink_rate)
    source_rate = np.array(source_rate)
    sum_sink = sink_rate.copy().sum(axis=0)
    sum_source = source_rate.copy().sum(axis=0)

    contribution_sink = np.zeros(sink_rate.shape)
    for i in range(len(sink_rate)):
        contribution_sink[i] = sink_rate[i]/sum_sink
    contribution_source = np.zeros(source_rate.shape)
    for i in range(len(source_rate)):
        contribution_source[i] = source_rate[i]/sum_source

    # store output
    out = {}
    out['sink_indx'] = sink_indx # the collection of the sink reaction index for the check_sp, shaped in (n_reaction)
    out['source_indx'] = source_indx # the collection of the source reaction index for the check_sp
    out['sink_rate'] = sink_rate # the collection of the sink reaction rate profiles, shaped in (n_reaction, n_alt)
    out['source_rate'] = source_rate # the collection of the source reaction rate profiles
    out['sum_sink'] = sum_sink # the total sink rate profile of the selected species, (n_alt)
    out['sum_source'] = sum_source # the total source rate profile of the selected species
    out['contribution_sink'] = contribution_sink # the contribution of the corresponding reactions in 'sink_rate' to the total sink
    out['contribution_source'] = contribution_source # the contribution of the corresponding reactions in 'source_rate' to the total source
    return out


# other usages could refer to store.py
# Here shows the keys of the data:
print(read_data['atm'].keys())
print(read_data['variable'].keys())
print(read_data['parameter'].keys())