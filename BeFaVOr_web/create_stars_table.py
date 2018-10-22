# This routine creates the latex table of the selected stars
import numpy as np
from astroquery.simbad import Simbad
from tabulate import tabulate


# ==============================================================================
def read_txt(list_name, folder):
    '''Read a given list_name (string)
       ex. bn_stars.txt'''

    file_data = folder + list_name
    # file = open(file_data, 'w')

    typ = (0, 1, 2, 3, 4, 5, 6, 7)

    print(file_data)
    a = np.genfromtxt(file_data, usecols=typ, unpack=True,
                      delimiter='\t', comments='#',
                      dtype={'names': ('star', 'plx', 'sig_plx', 'vsini',
                             'sig_vsini', 'pre_ebmv', 'incl', 'bump'),
                             'formats': ('S16', 'f2', 'f2', 'f4',
                                         'f4', 'f4', 'f4', 'S8')})

    stars, plx, sig_plx, vsini_true, sig_vsini, pre_ebmv, incl0, bump0 =\
        a['star'], a['plx'], a['sig_plx'], a['vsini'], a['sig_vsini'],\
        a['pre_ebmv'], a['incl'], a['bump']

    # file.close()
    return stars, plx, sig_plx, vsini_true, sig_vsini, pre_ebmv, incl0, bump0


# ==============================================================================
def read_simbad_data(star_name):
    '''
    SIMBAD query
    '''

    customSimbad = Simbad()
    # customSimbad.list_votable_fields() #  to list all avaiable fields
    customSimbad.get_votable_fields()
    customSimbad.add_votable_fields('plx', 'plx_error', 'rot', 'sptype',
                                    'measurements')

    # print(customSimbad.get_votable_fields())
    result_table = customSimbad.query_object(star_name)
    # star = result_table['MAIN_ID']
    star = np.copy(star_name)
    print(star)
    # print(result_table.keys())
    main_id = result_table['MAIN_ID'].item()
    plx = result_table['PLX_VALUE'][0]
    plx_error = result_table['PLX_ERROR'][0]
    vsini = result_table['ROT_Vsini'][0]
    vsini_err = result_table['ROT_err'].item()
    sptype = result_table['SP_TYPE']
    sptype = sptype.item()
    sptype_qual = result_table['SP_QUAL']
    sptype = sptype.decode('UTF-8')
    rot_bibcode = result_table['ROT_bibcode']
    dec = result_table['DEC'].item()
    ra = result_table['RA'].item()

    iras_f12 = result_table['IRAS_f12'].item()
    iras_e12 = result_table['IRAS_e12'].item()
    iras_f25 = result_table['IRAS_f25'].item()
    iras_e25 = result_table['IRAS_e25'].item()
    iras_f60 = result_table['IRAS_f60'].item()
    iras_e60 = result_table['IRAS_e60'].item()
    iras_f100 = result_table['IRAS_f100'].item()
    iras_e100 = result_table['IRAS_e100'].item()

    JP11_U_360 = result_table['JP11_U_360'].item()  # 3600 AA
    JP11_B_450 = result_table['JP11_B_450'].item()  # 4500 AA
    JP11_V_555 = result_table['JP11_V_555'].item()  # 5550 AA
    JP11_R_670 = result_table['JP11_R_670'].item()  # 6700 AA
    JP11_I_870 = result_table['JP11_I_870'].item()  # 8700 AA
    JP11_J_1200 = result_table['JP11_J_1200'].item()  # 12000 AA
    JP11_K_2200 = result_table['JP11_K_2200'].item()  # 22000 AA
    JP11_L_3500 = result_table['JP11_L_3500'].item()  # 35000 AA
    JP11_M_5000 = result_table['JP11_M_5000'].item()  # 50000 AA
    JP11_N_9000 = result_table['JP11_N_9000'].item()  # 90000 AA
    JP11_H_16200 = result_table['JP11_H_16200'].item()  # 162000 AA

    ROT_upVsini_1 = result_table['ROT_upVsini_1'].item()
    ROT_Vsini_1 = result_table['ROT_Vsini_1'].item()
    ROT_err_1 = result_table['ROT_err_1'].item()
    ROT_bibcode_1 = result_table['ROT_bibcode_1'].item()
    RVel_Rvel = result_table['RVel_Rvel'].item()
    RVel_bibcode = result_table['RVel_bibcode'].item()

    TD1_m2740 = result_table['TD1_m2740'].item()  # 27400 AA
    TD1_se_m2740 = result_table['TD1_se_m2740'].item()  # sigma
    TD1_m2365 = result_table['TD1_m2365'].item()  # 23650 AA
    TD1_se_m2365 = result_table['TD1_se_m2365'].item()  # sigma
    TD1_m1965 = result_table['TD1_m1965'].item()  # 19650 AA
    TD1_se_m1965 = result_table['TD1_se_m1965'].item()  # sigma
    TD1_m1565 = result_table['TD1_m1565'].item()  # 15650 AA
    TD1_se_m1565 = result_table['TD1_se_m1565'].item()  # sigma

    UBV_V = result_table['UBV_V'].item()
    UBV_B_V = result_table['UBV_B_V'].item()
    UBV_U_B = result_table['UBV_U_B'].item()
    UBV_bibcode = result_table['UBV_bibcode'].item()

    uvby_b_y = result_table['uvby_b_y'].item()
    uvby1_b_y = result_table['uvby1_b_y'].item()
    uvby1_m1 = result_table['uvby1_m1'].item()
    uvby1_bibcode = result_table['uvby1_bibcode'].item()

    simbad_data = [iras_f12, iras_e12, iras_f25, iras_e25, iras_f60, iras_e60,
                   iras_f100, iras_e100, JP11_U_360, JP11_B_450, JP11_V_555,
                   JP11_R_670, JP11_I_870, JP11_J_1200, JP11_K_2200,
                   JP11_L_3500, JP11_M_5000, JP11_N_9000, JP11_H_16200,
                   ROT_upVsini_1, ROT_Vsini_1, ROT_err_1, ROT_bibcode_1,
                   RVel_Rvel, RVel_bibcode, TD1_m2740, TD1_se_m2740, TD1_m2365,
                   TD1_se_m2365, TD1_m1965, TD1_se_m1965, TD1_m1565,
                   TD1_se_m1565, UBV_V, UBV_B_V, UBV_U_B, UBV_bibcode,
                   uvby_b_y, uvby1_b_y, uvby1_m1, uvby1_bibcode]

    return main_id, star.item(), plx, plx_error, vsini, vsini_err, sptype, ra,\
        dec, rot_bibcode.item(), simbad_data


# ==============================================================================

# list_name = 'list_final.txt'
list_name = 'list_iue.txt'
commum_folder = '/Users/tangodown/Dropbox/2_Artigos/tex_aara/Bemcee'
folder = commum_folder + '/tables/'

stars, plx, sig_plx, vsini_true, sig_vsini, pre_ebmv, inc0, bump0 = \
    read_txt(list_name=list_name, folder=folder)


results = []
for i in range(len(stars)):
    star = stars[i]
    print(star)
    star = star.decode('UTF-8')
    out = read_simbad_data(star_name=star)
    results.append(out)

# Making latex table
table = list(results)
# table = [[table[0][0:9]],["eggs",451],["bacon",0]]


new_table = []
for i in range(len(table)):
    new_table.append(table[i][0:10])

headers = ["main ID", "Star", "$\pi$ (mas)", "$\sigma_\pi$ (mas)",
           "v $\sin$i (km/s)", "$\sigma_{v $\sin$i}$ (mas)",
           "sptype", "ra", "dec", "rot_bibcode"]

print(tabulate(new_table, headers, tablefmt="latex"))
