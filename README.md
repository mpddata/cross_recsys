
# 1. Install python package dependencies  

```
pip install -r requirement.txt
```

# 2. Index new document into elasticsearch 

```
python index_new_doc.py
```

Default SQL query was T-1 (changed accordingly)

```
## SQL to extract T-1 articles (pls change the timestamp on interval x hour)
    sql = '''
    select * ,  from_unixtime(created) as created_v2,  from_unixtime(changed) as changed_v2
    from articles_metadata 
    where created >= unix_timestamp(CURRENT_TIMESTAMP - interval 24 hour) and created <=unix_timestamp(CURRENT_TIMESTAMP)
    '''
```
