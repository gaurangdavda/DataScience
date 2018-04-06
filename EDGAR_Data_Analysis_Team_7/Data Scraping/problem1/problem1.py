import re
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
import os
import zipfile
import logging
import time
import datetime

def generateURL(cik, accession):
  # create the url with the given cik and accession number
    logging.debug('Entered function generateURL')
    cik = cik.lstrip('0')
    mid_acc = re.sub(r'[-]', r'', accession)
    url = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' + mid_acc + '/' + accession + '/-index.htm'
    logging.debug('Hitting the URL {} of CIK {} & Accession Number {}'.format(url, cik, accession))
    try:
        page_open = urllib.request.urlopen(url)
        if page_open.code == 200:
            logging.debug("URL is valid")
            extract10QURL(url)
    except:
        logging.error("Invalid URL {}: Please re-validate".format(url))
        print("Invalid URL {}: Please re-validate".format(url))



def extract10QURL(url):
    final_url = ""
    logging.debug('In the function : get_final_url')
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    all_tables = soup.find('table', class_='tableFile')
    tr = all_tables.find_all('tr')
    for row in tr:
        final_url = row.findNext("a").attrs['href']
        break
    next_url = "https://www.sec.gov" + final_url
    logging.debug("Final URL {}:".format(next_url))
    print(next_url)
    get_soup(next_url)
    return (next_url)


def get_soup(url):
    try:
        logging.debug('In the function : get_soup')
        htmlpage = urllib.request.urlopen(url)
        page = BeautifulSoup(htmlpage, "html.parser")
        find_tables(page)
    except:
        return None


def find_tables(page):
    logging.debug('In the function : find_all_tables')
    all_divtables = page.find_all('table')
    folder_name = foldername(page)
    write_to_csv(page, all_divtables,folder_name)
    return 0


def foldername(page):
    logging.info('Entered function createCompanyFolder')
    all_p_tags=page.find_all('p')
    for tags in all_p_tags:
        p_tag=tags
        tags=tags.text.replace("\n"," ")
        if tags == '(Exact name of registrant as specified in its charter)':
            prev_tag=p_tag.find_previous_sibling('p')
            prev_tag=prev_tag.text.replace("\n"," ")
            company_name=prev_tag.replace(" ","_")
            logging.info('Folder name {} '.format(company_name))
            break
    return company_name



def zip_dir(path_dir, path_file_zip=''):
    if not path_file_zip:
        logging.debug('In a function : zip_dir')
        path_file_zip = os.path.join(
            os.path.dirname(path_dir), os.path.basename(path_dir) + '.zip')
    with zipfile.ZipFile(path_file_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path_dir):
            for file_or_dir in files + dirs:
                zip_file.write(
                    os.path.join(root, file_or_dir),
                    os.path.relpath(os.path.join(root, file_or_dir),
                                    os.path.join(path_dir, os.path.pardir)))


def assure_path_exists(path):
    logging.debug('In a function : assure_path_exists')
    if not os.path.exists(path):
        os.makedirs(path)


def if_exists(param):
    setflag = "false"
    datatabletags = ["background", "bgcolor", "background-color"]
    for x in datatabletags:
        if x in param:
            setflag = "true"
    return setflag

def checkheadertag(param):
    logging.debug('In a function : checkheadertag')
    setflag="false"
    datatabletags=["center","bold"]
    for x in datatabletags:
        if x in param:
            setflag="true"
    return setflag


def extract_Table(table):
    logging.debug('In a function : printtable')
    printtable = [] 
    printtrs = table.find_all('tr')
    for tr in printtrs:
        data=[]
        pdata=[]
        printtds=tr.find_all('td')
        for elem in printtds:
            x=elem.text;
            x=re.sub(r"['()]","",str(x))
            x=re.sub(r"[$]"," ",str(x))
            if(len(x)>1):
                x=re.sub(r"[—]","",str(x))
                pdata.append(x)
        data=([elem.encode('utf-8') for elem in pdata])
        printtable.append([elem.decode('utf-8').strip() for elem in data])
    return printtable

def write_to_csv(page, all_divtables,company_name):
    logging.debug('In a function : find_all_datatables')
    count = 0
    allheaders=[]
    for table in all_divtables:
        logging.debug(len(all_divtables))
        datasets = []
        trs = table.find_all('tr')
        for tr in trs:
            if if_exists(str(tr.get('style'))) == "true" or if_exists(str(tr)) == "true":
                logging.debug('Checking data tables at Row Level')
                datasets=extract_Table(tr.find_parent('table'))
                count=count+1
                break
            else:
                tds = tr.find_all('td')
                for td in tds:
                    if if_exists(str(td.get('style'))) == "true" or if_exists(str(td)) == "true":
                        logging.debug('Checking data tables at Column Level')
                        datasets=extract_Table(td.find_parent('table'))
                        count=count+1
                        break
            if not len(datasets) == 0:
                break
        #***************************** create a directory *************************************
        if not len(datasets) == 0:
            logging.debug('Total Number of data tables to be created {}'.format(len(datasets)))
            count += 1
            ptag=table.find_previous('p');
            while ptag is not None and checkheadertag(ptag.get('style'))=="false" and len(ptag.text)<=1:
                ptag=ptag.find_previous('p')
                if checkheadertag(ptag.get('style'))=="true" and len(ptag.text)>=2:
                    global name
                    name=re.sub(r"[^A-Za-z0-9]+","",ptag.text)
                    if name in allheaders:
                        hrcount+=1
                        hrname=name+"_"+str(hrcount)
                        allheaders.append(hrname)
                    else:
                        hrname=name
                        allheaders.append(hrname)
                        break
            folder_name = foldername(page)
            logging.debug('folder created with folder Name{}'.format(folder_name))
            path = str(os.getcwd()) + "/" + folder_name
            logging.debug('Path for csv creation {}'.format(path))
            assure_path_exists(path)
            if(len(allheaders)==0):
                filename=folder_name+"-"+str(count)
            else:
                filename=allheaders.pop()
            csvname=filename+".csv"
            logging.debug('file creation Name{}'.format(csvname))
            csvpath = path + "/" + csvname
            logging.debug('CSV Path for the file creation {}'.format(csvpath))
            with open(csvpath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(datasets)
            zip_dir(path)


def main():
    sys_args = sys.argv[1:]
    cik = ''
    accession = ''
    counter = 0
    if len(sys_args) == 0:
        cik = '0000051143'
        accession = '0000051143-13-000007'
    for arg in sys_args:
        if counter == 0:
            cik = str(arg)
        else:
            accession = str(arg)
        counter += 1
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    logfilename = 'Edgar_log_files_'+ cik + '_' + st + '.txt' 
    logging.basicConfig(filename=logfilename, level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Program execution begins.')
    logging.debug('**************************')
    logging.debug('Generating the URL with CIK Number {} and Accession number {}'.format(cik, accession))
    generateURL(cik, accession)


if __name__ == '__main__':
    main()
