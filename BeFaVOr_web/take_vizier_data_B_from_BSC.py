# ==============================================================================
# !/usr/bin/env python
# -*- coding:utf-8 -*-

# Created by B. Mota 2016-02-16 to present...

# import packages

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import pyhdust.phc as phc
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
import csv
import os
# import pyraf
mpl.rcParams.update({'font.size': 18})
mpl.rcParams['lines.linewidth'] = 2
font = fm.FontProperties(size=17)
mpl.rc('xtick', labelsize=17)
mpl.rc('ytick', labelsize=17)
fontsize_label = 18  # 'x-large'

__version__ = "0.0.1"
__author__ = "Bruno Mota"

# ==============================================================================
# Parameters that must be defined
user = 'tangodown'
num_spa = 75
commum_folder = '/Users/' + user + '/Dropbox/1_Tese/1_Projeto/BeFaVOr_web/' +\
    'tables_vizier/'
folder_fig = '/Users/' + user +\
    '/Dropbox/1_Tese/1_Projeto/BeFaVOr_web/figures/'

if os.path.isdir(folder_fig) is False:
    os.mkdir(folder_fig)

print(num_spa * '=')
print('\nTake_VIZIER_data\n')
print(num_spa * '=')


# ==============================================================================
def create_txt_file(a, b, c, d, e, f, g, h, i, j, l, file_name):
    '''
    Create a txt file.

    :param x: array with n elements (array)
    :param y: array with n elements (array)
    :param file_name: file's name (string)
    :return: txt file
    '''

    with open(file_name, 'w') as k:
        # file.write(('%s\t & \t %s \t & \t %s \t & \t %s \t & \t  %s \t &' +
        #                ' \t  %s \t & \t  %s   \n')
        writer = csv.writer(k, delimiter='\t')
        writer.writerows(zip(a, b, c, d, e, f, g, h, i, j, l))

    return


# ==============================================================================
def create_txt_file_compl(a, b, c, d, e, f, g, h, file_name):
    '''
    Create a txt file.

    :param x: array with n elements (array)
    :param y: array with n elements (array)
    :param file_name: file's name (string)
    :return: txt file
    '''

    with open(file_name, 'w') as k:
        writer = csv.writer(k, delimiter='\t')
        writer.writerows(zip(a, b, c, d, e, f, g, h))

    return


# ==============================================================================
def main():

    # VIZIER whole catalog
    Vizier.ROW_LIMIT = -1
    cat = ['V/50', 'V/36B']
    catalogs = Vizier.get_catalogs(cat)
    catalog = catalogs[0]
    catalog_compl = catalogs[2]

    # Operating with the data
    data = catalog.as_array()
    data_compl = catalog_compl.as_array()

    # Print available data
    data.dtype
    data_compl.dtype

    # Filtering the SpType
    sptype = list(data['SpType'].data)
    sptype_compl = list(data_compl['SpType'].data)
    # indexes = np.where(conc_flux[0] > 0)

    indexes = []
    for i in range(len(sptype)):
        sptyp = sptype[i].decode('UTF-8')
        if len(sptyp) != 0:
            if sptyp[0] == 'B':
                if ('e' in sptyp) is False:
                    if ('I' in sptyp) is False:
                        if ('V' in sptyp) is True:
                            if ('Hg' in sptyp) is False:
                                if ('Mn' in sptyp) is False:
                                    if ('n' in sptyp) is False:
                                        indexes.append(i)

    indexes_compl = []
    for i in range(len(sptype_compl)):
        sptyp_compl = sptype_compl[i].decode('UTF-8')
        if len(sptyp_compl) != 0:
            if sptyp_compl[0] == 'B':
                if ('e' in sptyp_compl) is False:
                    if ('I' in sptyp_compl) is False:
                        if ('V' in sptyp_compl) is True:
                            if ('Hg' in sptyp_compl) is False:
                                if ('Mn' in sptyp_compl) is False:
                                    if ('n' in sptyp_compl) is False:
                                        indexes_compl.append(i)

# ==============================================================================
    # Selecting the data with the B stars
    selected_data = data[indexes]
    sptyp_selected = list(selected_data['SpType'])
    name_selected = selected_data['Name']
    hd_selected = selected_data['HD']
    plx = selected_data['Parallax']
    bmv = selected_data['B-V']
    err_bmv = selected_data['u_B-V']
    umb = selected_data['U-B']
    err_umb = selected_data['u_U-B']
    rmi = selected_data['R-I']
    vsini = selected_data['RotVel']
    err_vsini = selected_data['u_RotVel']
    companions = selected_data['MultCnt']

    selected_data_compl = data_compl[indexes_compl]
    sptyp_selected_compl = list(selected_data_compl['SpType'])
    hd_selected_compl = selected_data_compl['HD']
    plx_compl = selected_data_compl['Plx']
    bmv_compl = selected_data_compl['B-V']
    umb_compl = selected_data_compl['U-B']
    rmi_compl = selected_data_compl['R-I']
    vsini_compl = selected_data_compl['vsini']
    err_vsini_compl = selected_data_compl['u_vsini']


# ==============================================================================
    # Checking if there are IUE data
    customSimbad = Simbad()
    customSimbad.TIMEOUT = 2000  # sets the timeout to 2000s

    # see which fields are currently set
    customSimbad.get_votable_fields()

    # To set other fields
    customSimbad.add_votable_fields('measurements')


# ==============================================================================
    # Selecting the stars with IUE data
    data = data[indexes]
    obs_iue_date = []
    stars = []
    indexes = []
    print('selected stars: %d' % len(hd_selected))
    for i in range(len(hd_selected)):
        try:
            star = "HD " + str(hd_selected[i])
            result_table = customSimbad.query_object(star)
            obs_date = result_table['IUE_ObsDate']
            if len(obs_date.item()) != 0:
                print(num_spa * '-')
                print('\n' + star)
                print('%0.2f perc. concluded' % (100 * i / len(hd_selected)))
                print(obs_date)
                obs_iue_date.append(obs_date.item())
                stars.append(star)
                indexes.append(i)
        except:
            pass

    data_compl = data_compl[indexes_compl]
    obs_iue_date_compl = []
    stars_compl = []
    indexes_compl = []
    print('selected stars compl: %d' % len(hd_selected_compl))
    for i in range(len(hd_selected_compl)):
        try:
            star = "HD " + str(hd_selected_compl[i])
            result_table = customSimbad.query_object(star)
            obs_date = result_table['IUE_ObsDate']
            if len(obs_date.item()) != 0:
                print(num_spa * '-')
                print('\n' + star)
                print('%0.2f perc. concluded' % (100 * i / len(hd_selected)))
                print(obs_date)
                obs_iue_date_compl.append(obs_date.item())
                stars_compl.append(star)
                indexes_compl.append(i)
        except:
            pass

# ==============================================================================
    # Selecting the data with the B stars in IUE database

    selected_data = data[indexes]
    sptyp_selected = list(selected_data['SpType'])
    name_selected = selected_data['Name']
    hd_selected = selected_data['HD']
    plx = selected_data['Parallax']
    bmv = selected_data['B-V']
    err_bmv = selected_data['u_B-V']
    umb = selected_data['U-B']
    err_umb = selected_data['u_U-B']
    rmi = selected_data['R-I']
    vsini = selected_data['RotVel']
    err_vsini = selected_data['u_RotVel']
    companions = selected_data['MultCnt']

    selected_data_compl = data_compl[indexes_compl]
    sptyp_selected_compl = list(selected_data_compl['SpType'])
    hd_selected_compl = selected_data_compl['HD']
    plx_compl = selected_data_compl['Plx']
    bmv_compl = selected_data_compl['B-V']
    umb_compl = selected_data_compl['U-B']
    rmi_compl = selected_data_compl['R-I']
    vsini_compl = selected_data_compl['vsini']
    err_vsini_compl = selected_data_compl['u_vsini']


# ==============================================================================
    # Plotting correlations

    # Plot B-V vs U-B
    plt.clf()
    plt.scatter(bmv, umb, label='V/50', marker='o')
    plt.scatter(bmv_compl, umb_compl, label='V/36B', color='red', marker='o')
    plt.xlabel(r'(B-V) [mag]')
    plt.ylabel(r'(U-B) [mag]')
    plt.legend()
    plt.savefig(folder_fig + 'bmvVSumb.png')

# ------------------------------------------------------------------------------
    # Plot R-I vs U-B
    plt.clf()
    plt.scatter(rmi, umb, label='V/50', marker='o')
    plt.scatter(rmi_compl, umb_compl, label='V/36B', color='red', marker='o')
    plt.xlabel(r'(R-I) [mag]')
    plt.ylabel(r'(U-B) [mag]')
    plt.legend()
    plt.savefig(folder_fig + 'rmiVSumb.png')

# ------------------------------------------------------------------------------
    # Plot B-V vs R-I
    plt.clf()
    plt.scatter(bmv, rmi, label='V/50', marker='o')
    plt.scatter(bmv_compl, rmi_compl, label='V/36B', color='red', marker='o')
    plt.xlabel(r'(B-V) [mag]')
    plt.ylabel(r'(R-I) [mag]')
    plt.legend()
    plt.savefig(folder_fig + 'bmvVSrmi.png')

# ------------------------------------------------------------------------------
    # Plot B-V vs vsini
    plt.clf()
    plt.scatter(bmv, vsini, label='V/50', marker='o')
    plt.scatter(bmv_compl, vsini_compl, label='V/36B', color='red', marker='o')
    plt.xlabel(r'(B-V) [mag]')
    plt.ylabel(r'$v \sin i$ [km/s]')
    plt.legend()
    plt.savefig(folder_fig + 'bmvVSvsini.png')

# ==============================================================================

    create_txt_file(a=hd_selected, b=bmv, c=umb, d=rmi, e=vsini,
                    f=err_bmv, g=err_umb, h=err_vsini, i=companions.data,
                    j=obs_iue_date, l=sptyp_selected,
                    file_name=commum_folder + 'selected_b_bsc_stars.txt')

    create_txt_file_compl(a=hd_selected_compl, b=bmv_compl, c=umb_compl,
                          d=rmi_compl, e=vsini_compl, f=err_vsini_compl,
                          g=obs_iue_date_compl, h=sptyp_selected_compl,
                          file_name=commum_folder +
                          'selected_b_bsc_stars_compl.txt')

# ==============================================================================
    # example
    if False:
        R = np.array((data['Vc'] * 1e5) ** 2 /
                     10 ** data['logg'] / phc.Rsun.cgs)
        L = phc.sigma.cgs * np.array(data['Teff'], dtype=float)**4 * 4 *\
            np.pi * (R * phc.Rsun.cgs)**2 * phc.Lsun.cgs
        M = np.array((data['Vc'] * 1e5)**2 * (R * phc.Rsun.cgs) /
                     phc.G.cgs / phc.Msun.cgs)

# ==============================================================================
if __name__ == '__main__':
    main()
