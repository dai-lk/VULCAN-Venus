# ============================================================================= 
# Modifications of the chemical network:
# ============================================================================= 

import vulcan_cfg
import numpy as np

kb = 1.38064852E-16    #Boltzmann constant (erg K^-1)

def modify(k):
    reac_to_indx  = {}
    reaction_list = []
    f_network = open(vulcan_cfg.network,'r')
    for line in f_network.readlines():
        if not line.strip():
            continue
        elif line.startswith('#'):
            continue
        else:
            index = int(line.split()[0])
            reaction = line.split('[')[1].split(']')[0].split()
            reaction = ' '.join(reaction)
            reaction_list.append(reaction)
            reac_to_indx[reaction] = index
    f_network.close()

    Tco = np.loadtxt(vulcan_cfg.atm_file,skiprows=2)[:,1]
    Pco = np.loadtxt(vulcan_cfg.atm_file,skiprows=2)[:,0]
    density = Pco/(kb*Tco)

    # =========== S2O2 + M -> SO + SO + M ===============
    # Zhang et al. (2010)
    if 'S2O2 + M -> SO + SO + M' in reaction_list:
        k[reac_to_indx['S2O2 + M -> SO + SO + M']] = k[reac_to_indx['SO + SO + M -> S2O2 + M']]/k[reac_to_indx['S2O2 + M -> SO + SO + M']]
        for i in range(len(k[reac_to_indx['S2O2 + M -> SO + SO + M']])):
            if k[reac_to_indx['S2O2 + M -> SO + SO + M']][i] <= 1E-37:
                k[reac_to_indx['S2O2 + M -> SO + SO + M']][i] = 1E-37
    else:
        print('Modifying S2O2 + M -> SO + SO + M is not in the network')

    # =========== S2 + M -> S + S + M ===================
    # Bierson and Zhang (2020)
    if 'S2 + M -> S + S + M' in reaction_list:
        k[reac_to_indx['S2 + M -> S + S + M']] = k[reac_to_indx['S + S + M -> S2 + M']]/k[reac_to_indx['S2 + M -> S + S + M']]
        for i in range(len(k[reac_to_indx['S2 + M -> S + S + M']])):
            if k[reac_to_indx['S2 + M -> S + S + M']][i] <= 1E-37:
                k[reac_to_indx['S2 + M -> S + S + M']][i] = 1E-37
    else:
        print('Modifying S2 + M -> S + S + M is not in the network')

    # =========== S4 + M -> S2 + S2 + M =================
    # Bierson and Zhang (2020)
    if 'S4 + M -> S2 + S2 + M' in reaction_list:
        k[reac_to_indx['S4 + M -> S2 + S2 + M']] = k[reac_to_indx['S2 + S2 + M -> S4 + M']]/k[reac_to_indx['S4 + M -> S2 + S2 + M']]
        for i in range(len(k[reac_to_indx['S4 + M -> S2 + S2 + M']])):
            if k[reac_to_indx['S4 + M -> S2 + S2 + M']][i] <= 1E-37:
                k[reac_to_indx['S4 + M -> S2 + S2 + M']][i] = 1E-37
    else:
        print('Modifying S4 + M -> S2 + S2 + M is not in the network')

    # =========== S6 + M -> S3 + S3 + M =================
    # Bierson and Zhang (2020)
    if 'S6 + M -> S3 + S3 + M' in reaction_list:
        k[reac_to_indx['S6 + M -> S3 + S3 + M']] = k[reac_to_indx['S3 + S3 + M -> S6 + M']]/k[reac_to_indx['S6 + M -> S3 + S3 + M']]
        for i in range(len(k[reac_to_indx['S6 + M -> S3 + S3 + M']])):
            if k[reac_to_indx['S6 + M -> S3 + S3 + M']][i] <= 1E-37:
                k[reac_to_indx['S6 + M -> S3 + S3 + M']][i] = 1E-37
    else:
        print('Modifying S6 + M -> S3 + S3 + M is not in the network')

    # =========== S8 + M -> S4 + S4 + M =================
    # Bierson and Zhang (2020)
    if 'S8 + M -> S4 + S4 + M' in reaction_list:
        k[reac_to_indx['S8 + M -> S4 + S4 + M']] = k[reac_to_indx['S4 + S4 + M -> S8 + M']]/k[reac_to_indx['S8 + M -> S4 + S4 + M']]
        for i in range(len(k[reac_to_indx['S8 + M -> S4 + S4 + M']])):
            if k[reac_to_indx['S8 + M -> S4 + S4 + M']][i] <= 1E-37:
                k[reac_to_indx['S8 + M -> S4 + S4 + M']][i] = 1E-37
    else:
        print('Modifying S8 + M -> S4 + S4 + M is not in the network')

    # =========== COCl + N2 -> CO + Cl + N2 =============
    # Bierson and Zhang (2020)
    if 'COCl + N2 -> CO + Cl + N2' in reaction_list:
        k[reac_to_indx['COCl + N2 -> CO + Cl + N2']] = k[reac_to_indx['Cl + CO + N2 -> COCl + N2']]/k[reac_to_indx['COCl + N2 -> CO + Cl + N2']]
        # Mills (1998) modification:
        '''for i in range(len(Tco)):
            if Tco[i] >= 298:
                k[reac_to_indx['COCl + N2 -> CO + Cl + N2']] = k[reac_to_indx['COCl + N2 -> CO + Cl + N2']]/(7.5*np.exp(500/298-500/Tco[i]))
            else:
                k[reac_to_indx['COCl + N2 -> CO + Cl + N2']] = k[reac_to_indx['COCl + N2 -> CO + Cl + N2']] /(7.5*np.exp(500/Tco[i]-500/298))
        '''
    else:
        print('Modifying COCl + N2 -> CO + Cl + N2 is not in the network')

    # =========== COCl + CO2 -> CO + Cl + CO2 ===========
    # Bierson and Zhang (2020)
    if 'COCl + CO2 -> CO + Cl + CO2' in reaction_list:
        k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']] = k[reac_to_indx['Cl + CO + CO2 -> COCl + CO2']]/k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']]
        # Mills (1998) modification:
        '''for i in range(len(Tco)):
            if Tco[i] >= 298:
                k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']] = k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']]/(7.5*np.exp(500/298-500/Tco[i]))
            else:
                k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']] = k[reac_to_indx['COCl + CO2 -> CO + Cl + CO2']] /(7.5*np.exp(500/Tco[i]-500/298))
        '''
    else:
        print('Modifying COCl + CO2 -> CO + Cl + CO2 is not in the network')

    # =========== O + O2 + M -> O3 + M ==================
    # Mills (1998)
    if 'O + O2 + M -> O3 + M' in reaction_list:
        k[reac_to_indx['O + O2 + M -> O3 + M']] = np.zeros(len(Tco))
    else:
        print('Modifying O + O2 + M -> O3 + M is not in the network')

    # =========== COCl + O2 + M -> ClCO3 + M ============
    # Yung and Demore (1982)
    if 'COCl + O2 + M -> ClCO3 + M' in reaction_list:
        k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']] = k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']]/(1E17+0.05*density)
        # Mills (1998), Bierson and Zhang (2020) modification:
        '''for i in range(len(Tco)):
            if Tco[i] >= 298:
                k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']] = k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']]*2*np.exp(200/298-200/Tco[i])
            else:
                k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']] = k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']]*2*np.exp(200/Tco[i]-200/298)
        '''
    else:
        print('Modifying COCl + O2 + M -> ClCO3 + M is not in the network')

    # ============ COCl + Cl2 -> COCl2 + Cl =============
    # Mills (1998)
    if 'COCl + Cl2 -> COCl2 + Cl' in reaction_list:
        k[reac_to_indx['COCl + Cl2 -> COCl2 + Cl']] = k[reac_to_indx['COCl + Cl2 -> COCl2 + Cl']]*((107*1.01325E6/(760.*Tco*1.38E-16))+density)*k[reac_to_indx['COCl + O2 + M -> ClCO3 + M']]
    else:
        print('Modifying COCl + Cl2 -> COCl2 + Cl is not in the network')

    print('========================= Modifying Chemical Network Accomplished ======================')

    return k

