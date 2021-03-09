import pandas as pd
import time

### Put you file names here for the script to work
files = ["DVS_2015-01-01.csv"]

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


if __name__ == '__main__':
    for file in files:
        clean_file(file)
