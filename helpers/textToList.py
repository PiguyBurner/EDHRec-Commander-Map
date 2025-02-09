# helper where I input a copied list from EDHREC of popular commanders and
# generates a properly-formatted list for main as an option

import utils

import os

TEXT_FILE = os.path.dirname(os.path.abspath(__file__)) + "/raw_text.txt"

def createListFromText():
    my_file = open(TEXT_FILE, "r") 
    
    # reading the file 
    data = my_file.read() 
    
    data_into_list = data.replace('\n', '$').split("$")
    my_file.close()
    
    for i in range(len(data_into_list)):
        data_into_list[i] = utils.cleanName(data_into_list[i])

    # printing the data 
    return data_into_list

