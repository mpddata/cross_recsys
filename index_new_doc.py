

## for ssh tunnel into EDW (Google cloud)
import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

import json
import time
import datetime

from elasticsearch import Elasticsearch
from elasticsearch import helpers


## set elasticsearch instance and endpoint
es = Elasticsearch('10.55.80.130')
es

## connect to EDW (with ssh tunnel)

mypkey = paramiko.RSAKey.from_private_key_file('google_cloud_ssh')

# MySQLdb.Connect(host="35.187.224.17", port=3306, user="tci_admin", passwd="TcIaDmIn2018", db="stg_tci")

sql_hostname = '35.187.224.17'
sql_username = 'tci_admin'
sql_password = 'TcIaDmIn2018'
sql_main_database = 'stg_tci'
sql_port = 3306
ssh_host = '10.55.86.2'
ssh_user = 'hafeez'
ssh_port = 22
sql_ip = '1.1.1.1.1'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    
## SQL to extract T-1 articles (pls change the timestamp on interval x hour)
    sql = '''
    select * ,  from_unixtime(created) as created_v2,  from_unixtime(changed) as changed_v2
    from articles_metadata 
    where created >= unix_timestamp(CURRENT_TIMESTAMP - interval 24 hour) and created <=unix_timestamp(CURRENT_TIMESTAMP)
    '''

## run the SQL queries
    data = pd.read_sql_query(sql, conn)
    




#### function to auto index the 
def start_es_index():

    global data
    df = data

    try:
	    ## change date format to string object - to ensure able to updload to es
	    data.insertDate = data.insertDate.astype('str')
	    data.created_v2 = data.created_v2.astype('str')
	    data.changed_v2 = data.changed_v2.astype('str')
    except:
	    pass
    
    
    # set index and doc_type name
    ES_INDEX = 'nstp'
    ES_TYPE =  'article'
#     ID_FIELD = df.index.values

#     df["id"] = df.index.values
    ## df["no_index"] = df["id"]+1

    tmp = df.to_json(orient = "records")
    df_json= json.loads(tmp)

    ## using bulk action (100x times)

    actions = [
      {
        "_index": ES_INDEX,
        "_type": ES_TYPE,
        "_id": i,
        "_source": df_json[i]
      }
      for i in range(0, len(df_json))
    ]

    ## start the process

    start = time.time()

    try:
        helpers.bulk(es, actions)
        print('es index complete!, total {} new docs indexed!'.format( len(data))  )
    except:
        print('process fail')

    end = time.time()
    duration = end -start
    duration  ## 136 sec to complete index 1 millions docs




### start main function ##########
start_es_index()


