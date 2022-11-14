from zipfile import ZipFile

import datetime

import os
from os.path import basename


def create_zip():

    day = str(datetime.date.today())
    filename = 'report-' + day + '.zip'
    with ZipFile(filename, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk('output'):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))


#create_zip()