import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import pyhdust.phc as phc
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
import csv
import os
import re

# VIZIER whole catalog
Vizier.ROW_LIMIT = -1
cat = ['J/ApJ/722/605/table3', 'J/ApJ/722/605/table4', 'J/ApJ/573/359/table1',
       'J/AJ/144/130/table2']
catalogs = Vizier.get_catalogs(cat)
catalog = catalogs[0]
catalog_2 = catalogs[1]
catalog_3 = catalogs[2]
catalog_4 = catalogs[3]

# Operating with the data
data = catalog.as_array()
data_2 = catalog_2.as_array()
data_3 = catalog_3.as_array()
data_4 = catalog_4.as_array()

# Print available data
data.dtype
data_2.dtype
data_3.dtype
data_4.dtype

# Taking data
vsini = data['vsini'].data
vsini_err = data['e_vsini'].data
vcrit = data['Vc'].data
logM = data['logM'].data
Teff = data['Teff'].data
Teff_err = data['e_Teff'].data
logg = data['log_g_'].data
logg_e = data['e_log_g_'].data

vsini_2 = data_2['vsini'].data
vsini_err_2 = data_2['e_vsini'].data
vcrit_2 = data_2['Vc'].data
logM_2 = data_2['logM'].data
Teff_2 = data_2['Teff'].data
Teff_err_2 = data_2['e_Teff'].data
logg_2 = data_2['log_g_'].data
logg_e_2 = data_2['e_log_g_'].data

sptype_3 = data_3['SpType'].data
vsini_3 = data_3['vsini'].data

sptype_4 = data_4['SpT'].data
Teff_4 = data_4['Teff'].data
vsini_4 = data_4['__vsini_'].data
vsini_err_4 = data_4['e__vsini_'].data

# First Plotting
# plt.scatter(logM, vsini, color='blue', alpha=0.5)
# plt.scatter(logM_2, vsini_2, color='red', alpha=0.5)
# plt.xlabel(r'$\log M / M_\odot$')
# plt.ylabel(r'$v \sin i [km / s]$')
# plt.yscale('log')
# plt.show()

# Second Plotting
sptype_4 = list(sptype_4)
sptype_4_dic = list(set(sptype_4))
sptype_4_dic = [b'B0O9V', b'B0V', b'B0Ve', b'B0.2V', b'B0.5IVn', b'B1IV',
                b'B1V:', b'B1V', b'B1.5Ve', b'B1.5V', b'B2V', b'B2IV',
                b'B2.5V', b'B2Ve', b'B2IV-V', b'B3Vn', b'B3IV/V', b'B3V',
                b'B3Ve', b'B3IV', b'B4V', b'B4Ve', b'B4', b'B4IV', b'B5IV/V',
                b'B5V', b'B6V', b'B6Vn',
                b'B2/B3IV', b'O8/O9', b'O9V', b'B1/B2V', b'B2/B3Ve',
                b'B2/B3V', b'B3/B4V', b'B4/B5V']

# sptype_4_dic = dict((x, sptype_4.count(x)) for x in sptype_4)
# sptype_3_dic = list(sptype_3_dic.values())
for i in range(len(vsini_4)):
    if vsini_4[i] < 0:
        vsini_4[i] = 0.
    sptype_4[i] = sptype_4[i].decode('UTF-8')


for i in range(len(sptype_4_dic)):
    sptype_4_dic[i] = sptype_4_dic[i].decode('UTF-8')

sptype_4_hist = []
vsini_4_hist = []
sptype_4_hist_2 = []
for i in range(len(vsini_4)):
    indx = np.where(sptype_4[i] == np.array(sptype_4_dic))
    indx = indx[0][0]
    # print(indx)
    pattern = r'B(.*)B(.*?).*'
    match = re.match(pattern, sptype_4_dic[indx], flags=0)
    pattern2 = r'O(.*)O(.*?).*'
    match2 = re.match(pattern2, sptype_4_dic[indx], flags=0)
    if match is None and match2 is None:
        sptype_4_hist.append(indx)
        vsini_4_hist.append(vsini_4[i])
        # sptype_4_hist_2.append(sptype_4_dic[indx])


sptype_4_hist_2 = []
for i in range(len(sptype_4_dic)):
    pattern = r'B(.*)B(.*?).*'
    match = re.match(pattern, sptype_4_dic[i], flags=0)
    pattern2 = r'O(.*)O(.*?).*'
    match2 = re.match(pattern2, sptype_4_dic[indx], flags=0)
    if match is None and match2 is None:
        sptype_4_hist_2.append(sptype_4_dic[i])

sptype_4_hist_2 = list(set(sptype_4_hist_2))

# Second Plot
plt.clf()
fig, ax = plt.subplots()
sptype_4_hist = np.array(sptype_4_hist)

ax.scatter(sptype_4_hist, vsini_4_hist, alpha=0.5)
# ax.hist2d(sptype_4_hist, vsini_4_hist, alpha=0.5)
xticks = list(np.arange(len(sptype_4_hist_2)))
xticks_labels = list(sptype_4_hist_2)
# plt.bar(range(len(xticks)), xticks, align='center')
# plt.xticks(range(len(t12)), t11, size='small')
# plt.xticks(len(range(xticks)), xticks_labels, rotation=45)
plt.xticks(xticks, xticks_labels, rotation=45)
plt.ylabel(r'$v \sin i [km / s]$')
plt.show()


# Third Plotting
# plt.scatter(Teff_4, vsini_4, color='red', alpha=0.5)
# plt.xlabel(r'$T_{eff} [K]$')
# plt.ylabel(r'$v \sin i [km / s]$')
# # plt.yscale('log')
# plt.show()