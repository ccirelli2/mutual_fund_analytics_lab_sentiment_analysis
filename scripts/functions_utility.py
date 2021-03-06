# -*- coding: utf-8 -*-
"""
Description:
    Useful functions used throughout program to read and write data
    and create directories.
"""

###############################################################################
# Set up logging parameters
###############################################################################
import logging
from datetime import datetime
today = datetime.today().strftime("%d_%m%Y")
logging.basicConfig(level=logging.INFO)


###############################################################################
# Import Libraries
###############################################################################
import mysql.connector
import pandas as pd
from tqdm import tqdm
import re
import inspect
from collections import Counter
import os
import sys


############################################################################### 
# Declare Path Variables                                                           
############################################################################### 
dir_base = r'/home/cc2/Desktop/repositories/mutual_fund_analytics_lab_sentiment_analysis'
dir_data = os.path.join(dir_base, 'data')                                          
dir_scripts = os.path.join(dir_base, 'scripts')         

###############################################################################
# Import Project Modules
###############################################################################
from functions_decorators import *



###############################################################################
# Function
###############################################################################


def create_pkey(df, colname, pk_name, table_name, write2file, dir_output,
        project_folder):
    """
    Function to create sentence primary key, which is a function of the accession number
    and count of sentence.
    """
    # Create Primary Key Object.  Initialize = 1
    pkey = [1]
    count = 1
    # Iterate Column values as pair
    for val1, val2 in zip(df[colname].values.tolist(),
                          df[colname].values.tolist()[1:]):
        # If Value 2 == Value 1, Increase Count and append to pkey list.
        if val2 == val1:
            count += 1
            pkey.append(count)
        # When Value 2 != Value 1 then reset count & append.
        else:
            count = 1
            pkey.append(count)
    # Add Primary Key To DataFrame (accession_num + sent key)
    df[pk_name] = [str(x) + '-' + str(y) for x, y in zip(
        df[colname].values, pkey)]
    
    if write2file:
        filename = f'{table_name}_add_pkey.csv'
        write2csv(df, dir_output, project_folder, filename)

    # Logging
    logging.info(f'Primary key created for => {table_name}')
    # Return df
    return df



@my_timeit
def load_file(path2file, name, delimiter):
    """
    Generic function load Excel and CSV files.

    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    directory : TYPE
        DESCRIPTION.
    project_folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    Dataframe

    """
    logging.info(f'---- loading file => {name}')
    
    if '.csv' in path2file:
        data = pd.read_csv(path2file, delimiter)
    elif '.xlsx' in path2file:
        data = pd.read_excel(path2file)
    else:
        logging.warning('This function can only load Excel of CSV files')
    
    logging.info(f'---- returning dataframe with dimensions => {data.shape}')
    
    # Return
    return data


def write2csv(dataframe, dir_output, project_folder=None, filename=''):
    """
    Generic function write dataframe to csv.

    Parameters
    ----------
    dataframe : TYPE
        DESCRIPTION.
    dir_output : TYPE
        DESCRIPTION.
    filename : TYPE
        DESCRIPTION.
    project_folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    if project_folder:
        path=os.path.join(dir_output, project_folder, filename)
    else:
        path=os.path.join(dir_output, filename) 
 
    dataframe.to_csv(path, sep="|")
    logging.info(f'---- {filename} writen to directory {dir_output}')


def write2excel(dataframe, dir_output, project_folder=None, filename=''):
    """
    Generic function write dataframe to csv.

    Parameters
    ----------
    dataframe : TYPE
        DESCRIPTION.
    dir_output : TYPE
        DESCRIPTION.
    filename : TYPE
        DESCRIPTION.
    project_folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    if project_folder:
        path = os.path.join(dir_output, project_folder, filename)
    else:
        path = os.path.join(dir_output, filename)
 
    dataframe.to_excel(path)
    logging.info(f'---- {filename} writen to directory {dir_output}')


def create_project_folder(dir_output, name):
    """
    Generic function to create a project folder in the output directory.

    Parameters
    ----------
    dir_output : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    path : TYPE
        DESCRIPTION.

    """
    logging.info(f'Creating project folder => {name}')
    path = os.path.join(dir_output, name)

    try:
        os.mkdir(path)
        logging.info(f'---- Project folder created => {path}\n\n')

    except FileExistsError as err:
        logging.warning(f'---- {name} directory already exists\n\n')
    
    return name            


@my_timeit
def chunk_csv_file(data, num_chunks, filename_output, dir_output, write2file):
    """
    Function to create and write to file equal size chunks of csv file.

    Args:
        num_chunks:
        path2file:
        dir_output:
        project_folder:
        write2file:
    Return :
    ----------------
    n number of equal size chunks
    """
    
    # Calculate Size of Chunks
    remainder = (data.shape[0] % num_chunks)
    chunk_size = int((data.shape[0] - remainder) / num_chunks)
    logging.info(f'---- creating {num_chunks} chunks of size ~ {chunk_size}')
    # Iterate Range & Get Chunks
    count = 0
    for i in tqdm(range(num_chunks)):
        if count < num_chunks-1: 
            chunk = data.sample(chunk_size)
            logging.info(f'---- data dimension pre chunk => {data.shape}')
            data = data.drop(axis=0, index=chunk.index)
            logging.info(f'---- data dimension post chunk => {data.shape}')
            # Write Chunk to output directory
            filename = f'{filename_output}_{i}.csv'
            path2file = os.path.join(dir_output, filename)
            chunk.to_csv(path2file)
            # Increase Count
            count += 1
        # So that we don't have to worry about the remainder, just append
        # Remaining rows
        else:
            filename = f'{filename_output}_{i}.csv'
            data.to_csv(os.path.join(dir_output, filename))




#### END









