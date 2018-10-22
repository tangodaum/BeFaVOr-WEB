# 1) Esta rotina deve ser rodada em ipython3

# ==============================================================================
# Importing modules
import numpy as np
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import tarfile
from astroquery.simbad import Simbad
import csv
import os
from glob import glob
import math


# ==============================================================================
def read_txt(list_name, folder):
    '''
    Read a given list of star names.

    :param list_name: name o txt file containing the list (string)
    :param folder: list's folder (string)
    :return: column of the list read
    '''

    list_name = folder + list_name

    f = open(list_name)
    lines = f.read().splitlines()

    return lines


# ==============================================================================
def create_list_files(list_name, folder, folder_table):
    '''
    Creates a list of the files inside a given folder.

    :param list_name: list's name (string)
    :param folder: files' folder (string)
    :return: creates a txt file, with the files' paths
    '''

    a = open(folder_table + list_name + ".txt", "w")
    for path, subdirs, files in os.walk(folder):
        for filename in files:
            f = os.path.join(path, filename)
            a.write(str(f) + os.linesep)
    return


# ==============================================================================
def create_txt_file(data_list, file_name):
    '''
    Create a txt file.

    :param data_list: list of data to be saved (array)
    :param file_name: txt file's name (string)
    :return: txt file
    '''

    with open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(zip(data_list))
    return


# ==============================================================================
def read_simbad_data(star_name):
    '''
    Query SIMBAD for a given star parallax, vsini, bump and references.

    :param star_name: star's name (string)
    :return: txt file with star's parallax, vsini, bump, the respective
    errors and references for vsini and E(B-V)
    '''

    customSimbad = Simbad()
    # customSimbad.list_votable_fields() #  to list all avaiable fields
    customSimbad.get_votable_fields()
    customSimbad.add_votable_fields('plx', 'plx_error', 'rot', 'sptype')
    customSimbad.get_votable_fields()
    result_table = customSimbad.query_object(star_name)
    # star = result_table['MAIN_ID']
    star = np.copy(star_name)
    plx = result_table['PLX_VALUE'][0]
    plx_error = result_table['PLX_ERROR'][0]
    vsini = result_table['ROT_Vsini'][0]
    vsini_err = result_table['ROT_err'].item()
    rot_bibcode = result_table['ROT_bibcode']
    sptype = result_table['SP_TYPE']
    sptype_ref = sptype.item()
    bump = True
    ebmv_ref = 0.0

    return star.item(), plx, plx_error, vsini, vsini_err, bump,\
        rot_bibcode.item(), ebmv_ref, sptype_ref


# ==============================================================================
def unzip(zip_file, outdir):
    '''
    Unzip a given file into the specified output directory.

    :param zip_file: name of file to be unziped (string)
    :param outdir: directory of the file (string)
    :return: unziped file
    '''

    import zipfile
    zf = zipfile.ZipFile(zip_file, "r")
    zf.extractall(outdir)
    return


# ==============================================================================
def selecting_data(star_name):
    '''
    Search the INES website for a specified star.

    :param star_name: name of the star (string)
    :return: request of the star name in INES page
    '''

    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()

    # now Chrome will run in a virtual display.
    # you will not see the browser.

    # Starting the searching
    if os.path.isdir('iue/' + star_name) is False:
        os.mkdir('iue/' + star_name)

        folder_data = 'iue/' + star_name

        # Define global Chrome properties
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": folder_data}
        options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(chrome_options=options)
        # browser = webdriver.Firefox(firefox_profile=fp)

        # Define web source
        ines_site = "http://sdc.cab.inta-csic.es/cgi-ines/IUEdbsMY"

        # Openning it
        browser.get(ines_site)
        # browser.maximize_window()

        # Selecting all data
        mySelect = Select(browser.find_element_by_name("limit"))
        mySelect.select_by_value("all")
        time.sleep(3)

        # Selecting some stars
        browser.find_element_by_name("object").send_keys(star_name)
        browser.find_element_by_name(".submit").click()
        # time.sleep(3)

        # Taking the data
        try:
            browser.find_element_by_name("markRebin").click()
            browser.find_element_by_name(".submitNH").click()
            time.sleep(10)
        except:
            print('There is no data for this star!')
        # browser.close()

        # Unzip files
        outdir = os.getcwd()
        os.chdir(folder_data)
        file_list = glob('*')
        if len(file_list) != 0:
            # print(file_list)
            fname = str(file_list[0])
            # print(fname)
            tar = tarfile.open(fname, "r:gz")
            tar.extractall()
            tar.close()
            os.system('rm *.gz')
        os.chdir(outdir)
        browser.close()

    return


# ==============================================================================
def mark_all_checkboxes(site):
    browser = webdriver.Chrome()
    browser.get(site)
    name = 'check[]'
    a = browser.find_elements_by_name(name)
    for i in range(len(a)):
        a[i].click()
    return


# ==============================================================================
def retrieve_ebmv_value(star_name):
    '''
    Search the INES website for a specified star's E(B-V) value.

    :param star_name: stars's name (string)
    :return: E(B-V) value
    '''

    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Define global Chrome properties
    browser = webdriver.Chrome()

    # Define web source
    irsa_site = "http://irsa.ipac.caltech.edu/applications/DUST/"

    # Openning it
    browser.get(irsa_site)
    # wait = WebDriverWait(browser, 180)
    # wait.until(EC.title_contains("title"))

    # Selecting some stars
    browser.find_element_by_name("locstr").send_keys(star_name)
    browser.find_element_by_class_name("tdsubmit").click()

    time.sleep(30)
    ebmv = browser.find_element_by_class_name("tdwhiteleft")
    ebmv = float(ebmv.text)
    browser.close()

    return ebmv


# ==============================================================================
def main():

    num_spa = 75
    print(num_spa * '=')
    print('Selection of Beacon stars\n')
    print(num_spa * '=')
    # table_of_stars = 'selected_Ae_stars.txt'
    # table_of_stars = 'oe_stars.txt'
    table_of_stars = 'be_beacon_stars.txt'

# ------------------------------------------------------------------------------
    stars = read_txt(list_name=table_of_stars,
                     folder='tables_vizier/')

    for i in range(len(stars)):
        star = 'HD' + str(stars[i])
        # star = str(stars[i])

        # Starting the searching
        if os.path.isdir('iue/' + star) is False:

            # Saving data from the INES database
            print(num_spa * '=')
            print('\nStar: %s' % star)
            print('\nSaving data from INES database... %d of %d' %
                  (i + 1, len(stars)))

            selecting_data(star_name=star)

        val = read_simbad_data(star_name=star)
        table_file = 'tables/' + star + '.txt'
        if math.isfinite(val[1]) is True and\
           math.isfinite(val[2]) is True\
           and math.isfinite(val[3]) is True:

            if math.isfinite(val[3]) is True and\
               math.isfinite(val[4]) is False:
                val = list(val)
                val[4] = 0.0
                val = tuple(val)
                create_txt_file(data_list=val, file_name=table_file)
            else:
                create_txt_file(data_list=val, file_name=table_file)
        else:
            print('This Star was excluded!')

    # Creating list of files
    create_list_files(list_name='selected_beacon_stars_with_iue',
                      folder='tables_vizier/',
                      folder_table='tables/')

    table_final = 'tables_vizier/' + 'selected_beacon_stars_with_iue.txt'
    table_final_2 = 'tables_vizier/'

    files = open(table_final)
    # files = files.readlines()
    files = files.read().splitlines()
    final_table = open(table_final_2 + 'list_beacon_stars.txt', "a+")

    for i in range(len(files)):
        print(files[i])
        files_2 = open('tables/' + str(files[i]) + '.txt')
        # files_2 = open(str(files[i]) + '.txt')
        # lines = files_2.readlines()
        lines = files_2.read().splitlines()
        star = lines[0][:]
        a = star.split()

        if len(a) >= 2:
            short_star_name = a[0] + a[1]
        else:
            short_star_name = np.copy(a)

        final_table.writelines(('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n')
                               % (short_star_name, lines[1][:-1],
                                  lines[2][:-1], lines[3][:-1],
                                  lines[4][:-1], lines[7][:-1],
                                  'nan', lines[5][:-1]))
    final_table.close()
    print(num_spa * '=')
    print('\nFinished\n')

# ==============================================================================
if __name__ == '__main__':
    main()
