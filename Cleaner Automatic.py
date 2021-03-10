import pandas as pd
import time
import glob, os
import lzma, urllib
import urllib.request



def clean_file(filepath):

    ### Open the file, start timer and clear/declare variables
    start = time.time()
    df = pd.read_csv(filepath)
    f = open("clean_{}.xml".format(filepath.split(".", 1)[0]), "a",encoding='utf-8')
    clean_string = ""
    counter = 0

    ## Remove unnecesary columns and write <Root> to the xml file
    df.drop(df.columns[0], axis=1, inplace=True) 
    df.drop(df.columns[-1], axis=1, inplace=True)
    f.write("<Root>"+"\n")


    ## Itterate through all the rows and clean them up
    for row_index in range(len(df)):

        ### Select the text from the df
        raw_text = df.iloc[row_index].values[0]
        cleaned = ""

        ## Check if certain flaws are in the text and removes them
        if " <?xml" in raw_text:
            cleaned = raw_text.split(""" <?xml""", 1)[0]
            cleaned = cleaned.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
        else:
            cleaned = raw_text.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
            cleaned = cleaned.split("""    <ns0:PutReisInformatieBoodschapIn""", 1)[0]

        ## Add the ezt to a string to later write to the file
        clean_string += cleaned + "\n"

        ## If the script has itterated through 50 lines the data will be writen to the file. This is for preformance enhancment
        if counter % 50 == 0:
            f.write(clean_string)
            clean_string = ""

        counter += 1

    ## End the file and timer
    f.write("</Root>")
    f.close()
    end = time.time()

    print("Converted {} to a clean XML file in: {} seconds...".format(filepath, end - start))

def download_files(url):

    ## Create a filename for the new file
    file_name = url.split('/')[5]
    coutner = 0

    ## Download the file
    urllib.request.urlretrieve(url, file_name)

    ## Unzip the file using lzma, and write it to a .csv
    with lzma.open(file_name, mode='rt') as file:
        f = open(file_name.replace('.xz', ''), "w")
        for line in file:
            f.write(line)
            coutner += 1

            if(coutner % 10000 == 0):
                print("wrote 10000 lines") 
        f.close

    ## Remove the .xz file
    os.remove(file_name)
        

if __name__ == '__main__':

    urls = []

    for url in urls:
        download_files(url)

    for file in glob.glob("*.csv"):
        clean_file(file)
        os.remove(file) #This can be commented out if you do not want to remove the files after converting them


'''
Here are all the download links for every Month. You can copy the month you need and fill "urls" with it.
I wont do a whole year at once bcs you would need more than 365 GB free space


def create_2013():
    urls_2013_11 = [
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-09.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-10.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-11.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-12.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-14.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-15.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-16.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-17.csv.xz',
        'https://trein.fwrite.org/dumps/2013-11/DVS_2013-11-18.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-19.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-20.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-21.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-22.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-23.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-24.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-25.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-26.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-27.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-28.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-29.csv.xz',
        'https://trein.fwrite.org/AMS-RPi/2013-11/DVS_2013-11-30.csv.xz',   
    ]
    urls_2013_12 = []
    for day in range(30):
        urls_2013_12.append('https://trein.fwrite.org/AMS-RPi/2013-12/DVS_2013-12-{}}.csv.xz'.format(day+1))

def create_2014():

    urls_2014_01 = []
    for day in range(30):
        urls_2014_01.append('https://trein.fwrite.org/AMS-RPi/2014-01/DVS_2014-01-{}}.csv.xz'.format(day+1))

    urls_2014_02 = []
    for day in range(27):
        urls_2014_02.append('https://trein.fwrite.org/AMS-RPi/2014-02/DVS_2014-02-{}}.csv.xz'.format(day+1))

    urls_2014_03 = []
    for day in range(30):
        urls_2014_03.append('https://trein.fwrite.org/AMS-RPi/2014-03/DVS_2014-03-{}}.csv.xz'.format(day+1))

    urls_2014_04 = []
    for day in range(29):
        urls_2014_04.append('https://trein.fwrite.org/AMS-RPi/2014-04/DVS_2014-04-{}}.csv.xz'.format(day+1))

    urls_2014_05 = []
    for day in range(30):
        urls_2014_05.append('https://trein.fwrite.org/AMS-RPi/2014-05/DVS_2014-05-{}}.csv.xz'.format(day+1))

    urls_2014_06 = []
    for day in range(29):
        urls_2014_06.append('https://trein.fwrite.org/AMS-RPi/2014-06/DVS_2014-06-{}}.csv.xz'.format(day+1))

    urls_2014_07 = []
    for day in range(30):
        urls_2014_07.append('https://trein.fwrite.org/AMS-RPi/2014-07/DVS_2014-07-{}}.csv.xz'.format(day+1))

    urls_2014_08 = []
    for day in range(30):
        urls_2014_08.append('https://trein.fwrite.org/AMS-RPi/2014-08/DVS_2014-08-{}}.csv.xz'.format(day+1))

    urls_2014_09 = []
    for day in range(29):
        urls_2014_09.append('https://trein.fwrite.org/AMS-RPi/2014-09/DVS_2014-09-{}}.csv.xz'.format(day+1))

    urls_2014_10 = []
    for day in range(30):
        urls_2014_10.append('https://trein.fwrite.org/AMS-RPi/2014-10/DVS_2014-10-{}}.csv.xz'.format(day+1))

    urls_2014_11 = []
    for day in range(29):
        urls_2014_11.append('https://trein.fwrite.org/AMS-RPi/2014-11/DVS_2014-11-{}}.csv.xz'.format(day+1))

    urls_2014_12 = []
    for day in range(30):
        urls_2014_12.append('https://trein.fwrite.org/AMS-RPi/2014-12/DVS_2014-12-{}}.csv.xz'.format(day+1))

def create_2015():

    urls_2015_01 = []
    for day in range(30):
        urls_2015_01.append('https://trein.fwrite.org/AMS-RPi/2015-01/DVS_2015-01-{}}.csv.xz'.format(day+1))

    urls_2015_02 = []
    for day in range(27):
        urls_2015_02.append('https://trein.fwrite.org/AMS-RPi/2015-02/DVS_2015-02-{}}.csv.xz'.format(day+1))

    urls_2015_03 = []
    for day in range(28):
        urls_2015_03.append('https://trein.fwrite.org/DT-HP/2015-03/DVS_2015-03-{}}.csv.xz'.format(day+1))

    urls_2015_04 = []
    for day in range(29):
        urls_2015_04.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-04/DVS_2015-04-{}}.csv.xz'.format(day+1))

    urls_2015_05 = []
    for day in range(30):
        urls_2015_05.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-05/DVS_2015-05-{}}.csv.xz'.format(day+1))

    urls_2015_06 = []
    for day in range(29):
        urls_2015_06.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-06/DVS_2015-06-{}}.csv.xz'.format(day+1))

    urls_2015_07 = []
    for day in range(30):
        urls_2015_07.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-07/DVS_2015-07-{}}.csv.xz'.format(day+1))

    urls_2015_08 = []
    for day in range(30):
        urls_2015_08.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-08/DVS_2015-08-{}}.csv.xz'.format(day+1))

    urls_2015_09 = []
    for day in range(29):
        urls_2015_09.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-09/DVS_2015-09-{}}.csv.xz'.format(day+1))

    urls_2015_10 = []
    for day in range(30):
        urls_2015_10.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-10/DVS_2015-10-{}}.csv.xz'.format(day+1))

    urls_2015_11 = []
    for day in range(29):
        urls_2015_11.append('https://trein.fwrite.org/DT-RPi-archive/2015-11/DVS_2015-11-{}}.csv.xz'.format(day+1))

    urls_2015_12 = []
    for day in range(30):
        urls_2015_12.append('https://trein.fwrite.org/AMS-Aurora-archive/2015-12/DVS_2015-12-{}}.csv.xz'.format(day+1))

def create_2016():

    urls_2016_01 = []
    for day in range(30):
        urls_2016_01.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-01/DVS_2016-01-{}}.csv.xz'.format(day+1))

    urls_2016_02 = []
    for day in range(28):
        urls_2016_02.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-02/DVS_2016-02-{}}.csv.xz'.format(day+1))

    urls_2016_03 = []
    for day in range(30):
        urls_2016_03.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-03/DVS_2016-03-{}}.csv.xz'.format(day+1))

    urls_2016_04 = []
    for day in range(29):
        urls_2016_04.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-04/DVS_2016-04-{}}.csv.xz'.format(day+1))

    urls_2016_05 = []
    for day in range(30):
        urls_2016_05.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-05/DVS_2016-05-{}}.csv.xz'.format(day+1))

    urls_2016_06 = []
    for day in range(29):
        urls_2016_06.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-06/DVS_2016-06-{}}.csv.xz'.format(day+1))

    urls_2016_07 = []
    for day in range(30):
        urls_2016_07.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-07/DVS_2016-07-{}}.csv.xz'.format(day+1))

    urls_2016_08 = []
    for day in range(30):
        urls_2016_08.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-08/DVS_2016-08-{}}.csv.xz'.format(day+1))

    urls_2016_09 = []
    for day in range(29):
        urls_2016_09.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-09/DVS_2016-09-{}}.csv.xz'.format(day+1))

    urls_2016_10 = []
    for day in range(30):
        urls_2016_10.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-10/DVS_2016-10-{}}.csv.xz'.format(day+1))

    urls_2016_11 = []
    for day in range(29):
        urls_2016_11.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-11/DVS_2016-11-{}}.csv.xz'.format(day+1))

    urls_2016_12 = []
    for day in range(30):
        urls_2016_12.append('https://trein.fwrite.org/AMS-Aurora-archive/2016-12/DVS_2016-12-{}}.csv.xz'.format(day+1))

'''