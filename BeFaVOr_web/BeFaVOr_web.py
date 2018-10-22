# 1) Esta rotina deve ser rodada em ipython3

# ==============================================================================
# Importing modules
import numpy as np
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys
import re
import datetime
import random
import time
import requests
import math
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import tarfile
from astroquery.simbad import Simbad
import csv
import os
from glob import glob
import pyhdust.phc as phc
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==============================================================================
def show_page_code(url):
    '''
    Shows the page code of a certain webpage.

    :param url: page url (string)
    :return: page code
    '''

    html = urlopen(url)
    bsObj = BeautifulSoup(html.read())
    return bsObj


# ==============================================================================
def getTitle(url):
    '''
    Gets the title of a certain webpage.

    :param url: page url (string)
    :return: page title
    '''

    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title


# ==============================================================================
def there_is_a_title(url):
    '''
    Prints the title of a certain webpage.

    :param url: page url (string)
    :return: page title
    '''

    title = getTitle(url)
    if title is None:
        print("Title could not be found")
    else:
        print(title)
    return title


# ==============================================================================
def example_try():
    '''
    Ela funciona assim ...
    '''

    while True:
        try:
            x = int(raw_input("Please enter a number: "))
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return


# ==============================================================================
def get_attribute(url, atr, typ):
    '''
    Lists all text in a webpage that satisfacts a specified attribute.

    :param url: page url (string)
    :param atr: attribute (string)
    :param typ: tag (string)
    :return: text containing specified attribute
    '''

    bsOBJ = show_page_code(url)
    namelist = bsOBJ.findAll(typ, {"class": atr})
    names = []
    for name in namelist:
        nome = name.get_text()
        names.append(nome)

    return names


# ==============================================================================
def get_attribute_2(url, atr):
    '''Lista todos os textos que satisfazem um dado atributo
       ulr: page (ex: 'http://www.pythonscraping.com/pages/warandpeace.html')
       atr: example "text"
    '''

    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    allText = bsObj.findAll(id=atr)
    print(allText[0].get_text())

    return


# =================================================================================
def find_regular_expression(url, typ, atr, expr):
    '''Busca uma certa expressao dentro do codigo e lista
    todas as suas ocorrencias'''

    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    array = bsObj.findAll(typ, {atr: re.compile(expr)})
    for lista in array:
        print(lista["src"])
    return lista


# ==============================================================================
random.seed(datetime.datetime.now())


def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id": "bodyContent"}).\
        findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


# ==============================================================================
def get_Link(articleUrl):
    links = getLinks("/wiki/Kevin_Bacon")
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)


# ==============================================================================
def file_submission():
    files = {'uploadFile': open('../files/Python-logo.png', 'rb')}
    r = requests.post("http://pythonscraping.com/pages/processing2.php",
                      files=files)
    print(r.text)
    return


# ==============================================================================
def simple_form():
    params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
    r = requests.post("http://pythonscraping.com/files/processing.php",
                      data=params)
    print(r.text)
    return


# ==============================================================================
def file_submission2():
    files = {'uploadFile': open('../files/python.png', 'rb')}
    r = requests.post("http://pythonscraping.com/pages/processing2.php",
                      files=files)
    print(r.text)

    return


# ==============================================================================
def iue_submission(star_name):
    '''
    Search in the IUE database for a certain star name.

    :param star_name: name of the star (string)
    :return: request of star name in IUE page
    '''

    ines_site = "http://sdc.cab.inta-csic.es/cgi-ines/IUEdbsMY"
    params = {'object': star_name}
    r = requests.post(ines_site, data=params)
    print(r.text)

    return r


# ==============================================================================
def read_txt(list_name, folder):
    '''
    Read a given list of star names.

    :param list_name: name o txt file containing the list (string)
    :param folder: list's folder (string)
    :return: column of the list read
    '''

    list_name = folder + list_name

    cols = np.genfromtxt(list_name, unpack=True, comments='#',
                         delimiter='\t')

    return cols


# ==============================================================================
def untar(fname):
    '''
    Decompact a tar file.

    :param fname: name o file to be decompacted (string)
    :return: decompacted file
    '''

    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print("Extracted in Current Directory")
    else:
        print("Not a tar.gz file: '%s '" % sys.argv[0])


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
def read_simbad_coodr(star_name):
    '''
    Query SIMBAD for the coordinates of a given star.

    :param star_name: star's name (string)
    :return: right ascencion and declination coordinates
    '''

    customSimbad = Simbad()
    customSimbad.get_votable_fields()
    result_table = customSimbad.query_object(star_name)

    ra = result_table['RA'][0]
    dec = result_table['DEC'][0]

    return ra, dec


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
def plot_gal(ra_val, dec_val, folder_fig):
    """
    Plot in "Galatic Coordinates" (i.e., Mollweide projection).

    :param ra_val: right ascencion in RADIANS (float)
    :param dec_val: declination in RADIANS (float)
    :param folder_fig: name of the folder for the figure (string)
    :return: saved images
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="mollweide")
    ax.set_xticklabels(['14h', '16h', '18h', '20h', '22h', '0h', '2h', '4h',
                        '6h', '8h', '10h'])

    for i in range(len(ra_val)):
        dec = dec_val[i].replace(' ', ':')
        ra = ra_val[i].replace(' ', ':')

        # list of floats (degrees fraction)
        dec = [phc.dec2degf(dec)]
        ra = [phc.ra2degf(ra)]

        # arrays of floats (radians)
        dec = np.array(dec) * np.pi / 180
        ra = np.array(ra) * np.pi / 180

        ax.scatter(ra, dec)
    plt.savefig(folder_fig + 'galatic_distribution.png')

    return


# ==============================================================================
def selecting_data(star_name, commum_folder):
    '''
    Search the INES website for a specified star.

    :param star_name: name of the star (string)
    :param commum_folder: name of the folder where the routine is located
    :return: request of the star name in INES page
    '''

    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()

    # now Chrome will run in a virtual display.
    # you will not see the browser.

    # Creating the path
    a = star_name.split()

    # short_star_name = a[0][0] + a[1][0:3]
    short_star_name = a[0] + a[1]

    # Starting the searching
    if os.path.isdir(commum_folder + 'iue/' + short_star_name) is False:
        os.mkdir(commum_folder + 'iue/' + short_star_name)

        folder_data = commum_folder + 'iue/' + short_star_name

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
        # time.sleep(3)

        # Selecting all data
        mySelect = Select(browser.find_element_by_name("limit"))
        mySelect.select_by_value("all")
        # time.sleep(3)

        # Selecting some stars
        browser.find_element_by_name("object").send_keys(star_name)
        browser.find_element_by_name(".submit").click()
        # time.sleep(3)

        # Taking the data
        browser.find_element_by_name("markRebin").click()
        browser.find_element_by_name(".submitNH").click()
        time.sleep(20)
        # browser.close()

        # Unzip files
        outdir = os.getcwd()
        # print(short_star_name)
        # new_path = outdir + '/iue/' + short_star_name + '/'
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
        # try:
        #    # Unzip files
        #    outdir = os.getcwd()
        #    new_path = outdir + '/iue/' + short_star_name + '/'
        #    os.chdir(new_path)
        #    file_list = glob('*')
        #    fname = str(file_list[0])
        #    print(fname)
        #    tar = tarfile.open(fname, "r:gz")
        #    tar.extractall()
        #    tar.close()
        #    os.system('rm *.gz')
        #    os.chdir(outdir)
        # except:
        #    pass #

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
def prepear_col(cols):
    if np.size(cols) == 1:
        col = [cols]
    else:
        col = cols
    return col


# ==============================================================================
def sptype_from_simbad(star_name):
    '''
    query sptype from SIMBAD
    '''

    customSimbad = Simbad()
    customSimbad.get_votable_fields()
    customSimbad.add_votable_fields('plx', 'plx_error', 'rot', 'sptype',
                                    'measurements')

    # print(customSimbad.get_votable_fields())
    result_table = customSimbad.query_object(star_name)

    sptype = result_table['SP_TYPE']
    sptype = sptype.item()

    return sptype


# ==============================================================================
def main():

    num_spa = 75
    print(num_spa * '=')
    print('\nBeFaVOr_Web\n')
    print(num_spa * '=')
# ------------------------------------------------------------------------------

    # Defining folders
    # user = input('Who is using? (bmota or artur): ')
    user = 'tangodown'
    # user = 'bmota'
    # commum_folder = '/Users/' + user + '/Dropbox/1_Tese/1_Projeto/BeFaVOr_web/'
    # commum_folder_2 = '/Users/' + user + '/Dropbox/1_Tese/1_Projeto/BeFaVOr/'
    commum_folder = '/Users/' + user + '/Dropbox/1_Tese/1_Projeto/BeFaVOr_web/'
    commum_folder_2 = '/Users/' + user + '/Dropbox/1_Tese/1_Projeto/BeFaVOr/'

    folder_tables = commum_folder + 'tables/'
    folder_tables_2 = commum_folder_2 + 'emcee/' + 'tables/'

    folder_figures = commum_folder + 'figures/'

    table_final = folder_tables + 'list.txt'
    table_final_2 = folder_tables_2 + 'list_final.txt'
# ------------------------------------------------------------------------------

    # Saving the input for the routine Befavour.py
    if os.path.isfile(table_final_2) is True:
        os.system('rm ' + table_final_2)

    if os.path.isfile(folder_figures) is False:
        os.system('rm -r ' + folder_figures)

    if os.path.isfile(folder_figures) is False:
        os.system('mkdir ' + folder_figures)

    if os.path.isfile(table_final) is True:
        os.system('rm ' + table_final)

    os.system('rm -r' + folder_tables)
    if os.path.isdir(commum_folder + 'tables/') is False:
        os.mkdir(commum_folder + 'tables/')
# ------------------------------------------------------------------------------

    # Would you like to run one or a list of stars?
    # option = input('\nRun one or more stars: (1 or more) ')
    option = 'more'
    if option == '1':
        # Saving data from the INES database
        star = input('\nPlease, put the star name: ')
        print('\nSaving data from INES database...')
        selecting_data(star_name=star, commum_folder=commum_folder)

        # Saving SIMBAD stellar data to a table
        print('\nSaving data (plx, vsini) from SIMBAD database...')
        table_file = commum_folder + 'tables/' + star + '.txt'
        folder_tables = commum_folder + 'tables/'
        val = read_simbad_data(star_name=star)

        # Check if there are bump files
        folder_star = commum_folder + 'iue/' + star
        bump = glob(folder_star + 'L*')

        if len(bump) is 0:
            start_time = time.time()
            val = list(val)
            ebmv_bump = retrieve_ebmv_value(star_name=star)
            print(ebmv_bump)
            val[7] = ebmv_bump
            val[5] = False
            val = tuple(val)
            print("--- %s seconds ---" % (time.time() - start_time))

        # Saving the table
        create_txt_file(data_list=val, file_name=table_file)
# ------------------------------------------------------------------------------

    if option == 'more':
        cols = read_txt(list_name='selected_bn_stars.txt',
                        folder=commum_folder + 'tables_vizier/')

        cols_2 = read_txt(list_name='selected_bn_stars_compl.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_3 = read_txt(list_name='selected_be_stars.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_4 = read_txt(list_name='selected_be_bsc_stars.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_5 = read_txt(list_name='selected_be_bsc_stars_compl.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_6 = read_txt(list_name='selected_b_bsc_stars.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_7 = read_txt(list_name='selected_b_bsc_stars_compl.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_8 = read_txt(list_name='selected_oe_stars.txt',
                          folder=commum_folder + 'tables_vizier/')

        cols_9 = read_txt(list_name='selected_oe_stars_compl.txt',
                          folder=commum_folder + 'tables_vizier/')

        # print(cols[0], cols_2[0], cols_3[0],
        #       cols_4[0], cols_5[0], cols_6[0],
        #       cols_7[0], cols_8[0], cols_9[0])

        # print(cols_5[0])
        print(len(cols_5))
        cols = prepear_col(cols[0])
        cols_2 = prepear_col(cols_2[0])
        cols_3 = prepear_col(cols_3[0])
        cols_4 = prepear_col(cols_4[0])
        cols_5 = prepear_col(cols_5[0])
        cols_6 = prepear_col(cols_6[0])
        cols_7 = prepear_col(cols_7[0])
        cols_8 = prepear_col(cols_8[0])
        cols_9 = prepear_col(cols_9[0])

        # stars = np.concatenate((cols[0], cols_2[0],
        #                         cols_3[0], cols_4[0],
        #                         cols_5[0], cols_6[0],
        #                         cols_7[0], cols_8[0],
        #                         cols_9[0]), axis=0)

        print(type(cols_5))
        # print(cols, cols_2, cols_3,
        #       cols_4, cols_5, cols_6,
        #       cols_7, cols_8, cols_9)

        stars = np.concatenate((cols, cols_2,
                                cols_3, cols_4,
                                cols_5, cols_6,
                                cols_7, cols_8,
                                cols_9), axis=0)

# ------------------------------------------------------------------------------

# sptypes = []
# for i in range(len(star_arr)):
#     sptypes.append(sptype_from_simbad(star_arr[i]))

        for i in range(len(stars)):
            star = str(stars[i])
            star = "HD " + star[:-2]
            # print(i, star)
            a = star.split()
            star_2 = a[0] + a[1]

            # Starting the searching
            if os.path.isdir(commum_folder + 'iue/' + star_2) is False:

                # Saving data from the INES database
                print(num_spa * '=')
                print('\nStar: %s' % star)
                print('\nSaving data from INES database... %d of %d' %
                      (i + 1, len(stars)))

                selecting_data(star_name=star, commum_folder=commum_folder)

                # Saving SIMBAD stellar data to a table
                print('\nSaving data from SIMBAD database... star: %s\n'
                      % (star))
                table_file = commum_folder + 'tables/' + star + '.txt'
                val = read_simbad_data(star_name=star)

                # Check if there are bump files
                folder_star = commum_folder + 'iue/' + star_2 + '/'

                bump = glob(folder_star + 'L*')

                if len(bump) is 0:
                    start_time = time.time()
                    val = list(val)
                    ebmv_bump = retrieve_ebmv_value(star_name=star)
                    print(ebmv_bump)
                    val[7] = ebmv_bump
                    val[5] = False
                    val = tuple(val)
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print(val)
                # nan and "--" Filters
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
# ------------------------------------------------------------------------------

        # Plotting galatic distribution
        ra_val_arr = []
        dec_val_arr = []
        for i in range(len(stars)):
            star = str(stars[i])
            star = "HD " + star[:-2]
            ra, dec = read_simbad_coodr(star_name=star)
            ra_val_arr.append(ra)
            dec_val_arr.append(dec)

        plot_gal(ra_val=ra_val_arr, dec_val=dec_val_arr,
                 folder_fig=folder_figures)

# ------------------------------------------------------------------------------

    # Creating list of files
    create_list_files(list_name='list', folder=folder_tables,
                      folder_table=folder_tables)

    table_final = folder_tables + 'list.txt'
    table_final_2 = folder_tables_2 + 'list_final.txt'

    files = open(table_final)
    files = files.readlines()
    final_table = open(table_final_2, "a+")

    for i in range(len(files)):
        files_2 = open(files[i][:-1])
        print(files[i][:-1])
        lines = files_2.readlines()

        # if len(lines) == 8:
        # print('estou aqui')
        star = lines[0][:-1]
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
    return


# ==============================================================================
if __name__ == '__main__':
    main()
