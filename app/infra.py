#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from random import random
import pandas as pd
import logging
import datetime
import time
import glob
import re

MOCK = {'id':1,'N':0,'n':0}

def input_serialize(txt_line):
    title_regex = re.compile('Event\s*(.*?)\s*[0-9]{2}:')
    time_regex = re.compile('([0-9]{2}:[0-9]{2}:[0-9]{2};[0-9]{2})')
    reconcile_regex = re.compile('Duration\s*(.*?)\s*[0-9]{10}')

    times = time_regex.findall(txt_line)
    title = title_regex.findall(txt_line)
    reconcile = reconcile_regex.findall(txt_line)

    input_splited = txt_line.split(';')
    input_dict = {}
    input_dict['start_time'] = times[0]
    input_dict['end_time'] = times[1]
    input_dict['title'] = title[0]
    input_dict['duration'] = times[2] if len(times)==3 else times[3]
    input_dict['reconcile_key'] = reconcile[0]

    return input_dict

def log_init(log_file_name):                                                                 
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-4.4s]  %(message)s")
    rootLogger = logging.getLogger()                                            
                                                                                
    fileHandler = logging.FileHandler("log_file_name.log")                              
    fileHandler.setFormatter(logFormatter)                                      
    fileHandler.setLevel(level=logging.DEBUG)      
    rootLogger.addHandler(fileHandler)                                          
                                                                                
    consoleHandler = logging.StreamHandler()                                    
    consoleHandler.setFormatter(logFormatter)                                   
    consoleHandler.setLevel(level=logging.WARNING)      
    rootLogger.addHandler(consoleHandler)                                       
    rootLogger.setLevel(level=logging.DEBUG)      

def list_to_sql(conn,l):
    c = conn.cursor()
    c.execute('''Create TABLE if not exists server("sites")''')
    for item in l:
        c.execute("INSERT INTO server(sites) VALUES(?)", (item,))
    conn.commit()

def sql_to_list(conn):
    c = conn.cursor()
    c.execute('''Create TABLE if not exists server("sites")''')
    c.execute("SELECT * FROM server")
    rows = c.fetchall()
    return [r[0] for r in rows]

def watchdog(table_name,connection):

    txts_list  = glob.glob('*.txt')
    txts_list.sort()

    try:
        files_read = sql_to_list(connection)
        files_not_read =  list(set(txts_list) - set(files_read))
        files_not_read.sort()
        if len(files_not_read)>0:

            logging.warning('Novo arquivo encontrado: '+str(txts_list))
            return files_not_read
        return None #WRONG
    except:
        return txts_list


def register_inputs(txts_files_list,conn_files,conn_lines):
    keys = ['start_time', 'end_time', 'title', 'duration', 'reconcile_key']
    files_completed = []
    try:
        result = pd.read_sql('SELECT * FROM lines',conn_lines,index_col = 'index') 
    except:
        result = pd.DataFrame(columns = keys)

    for txt_name in txts_files_list:
        file_object  = open(txt_name, "r")
        logging.warning('Analisando dados relativos ao arquivo: '+str(txt_name))

        # Read the file reversed allows the search to be interrupted as soon as
        # there is repeatedinformation:
        for txt_line in reversed(list(file_object)):
        
            # Test if all data was analised:
            if '----' in txt_line:
                files_completed.append(file_object.name)
                break

            # Create new strutured data from line:
            new_input = input_serialize(txt_line)

            # if data (line) are already in db -> finish this file and start next one.
            if any(result['start_time']==new_input['start_time']):
                files_completed.append(file_object.name)
                break
            else:
                # If data not in db -> put the new input in db
                result = result.append([new_input])
                logging.warning('\t└>Lendo linha: '+txt_line[0:50]+"... ")

    ## Now we need to save our progress to future consultations:
    result.to_sql('lines', con=conn_lines, if_exists="replace")
    list_to_sql(conn_files,files_completed)
    logging.warning('Leitura de dados terminada!')
    logging.warning('WATCHDOG ATIVADO')
    #files_completed.to_sql('files', con=conn_files)
    return result

def api_corte_MOCK1(start_time,end_time,duration,path):
    # Essa função e um mock da api de corte, gostaria de ter feito ela
    # direitinho no django mas nao deu... De toda maneira vou tentar explicar a
    # logica:

    # Teste se o video tem a duração mínima necessaria:
    duration = duration[:-3]
    duration = duration.split(':')
    duration = [int(i) for i in duration]
    d = datetime.time(duration[0],duration[1],duration[2])
    if d<datetime.time(second=30):
        return None 
    else:
        # Aqui entraria algo com datajson = requests ...
        # Para simular isso eu defeni uma variavel global "MOCK"
        datajson = {'id':MOCK['id']}
        MOCK['id']+=1
        MOCK['N'] = (random()*10)+5 #Numero de tentativas necessarias
        MOCK['n'] = 0
        return datajson

# PROGRAM START: #

# Initial Verification:
# pd.read_sql('SELECT * FROM test',conn,index_col = 'index')
# Try import database:

# If we dont have a db we'll need to start from the beginig:
## First we need a list of file's name:

## Now we will interact in each file to read the inputs:

def main():
    # INITIAL CONFIGURATIONS:
    
    # configuring the logger:
    log_init('debug.log')
    logging.warning('Inicializando Aplicação de Infraestrutura-GLOBO')
    
    # acessing/creating db:
    conn_l = sqlite3.connect('lines_read.db')
    conn_f = sqlite3.connect('files_read.db')
    
    logging.warning('WATVCHDOG ATIVADO')
    try:
        while True:
            new_files = watchdog('files',conn_f)
            if  new_files == None:
                time.sleep(1)
                logging.info('Nenhum novo arquivo encontrado')
            else:
                inputs_df = register_inputs(new_files,conn_f,conn_l)
                for inp in inputs_df.iterrows():
                    data = api_corte_MOCK1(inp[1]['start_time'],
                                           inp[1]['end_time'],
                                           inp[1]['duration'],
                                           path = '/.')
                    if data != None:
                        logging.warning('REQUISIÇÃO ENVIADA PARA API DE CORTE')
                        result = api_corte_MOCK2(data['id'])

                
    except KeyboardInterrupt:
        logging.critical('!!! Aplicação de Infraestrutura foi encerrada !!!')


if __name__ == '__main__':
    main()
