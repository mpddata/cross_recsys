
# 1. Install python package dependencies  

```
pip install -r requirement.txt
```

# 2. Index new document into elasticsearch 

Run the python script to start index

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

# 3. Successful indexed

es index complete!, total 420 (or x amount)  new docs indexed!



# 4. Test on Elasticsearch API query , find most similar articles

http://10.55.80.130:9200/nstp/article/_search?q=created_v2:[2019-01-01+TO+2019-01-24]+AND+title:najib+AND+site_name:bharian

parameter
created_v2: [start-to-end]
title: najib ( or any text/query)
site_name:  nst ( portal name)


```
{
    "took": 3,
    "timed_out": false,
    "_shards": {
        "total": 5,
        "successful": 5,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": 26,
        "max_score": 10.449777,
        "hits": [
            {
                "_index": "nstp",
                "_type": "article",
                "_id": "210985",
                "_score": 10.449777,
                "_source": {
                    "articleID": 520179,
                    "site_name": "bharian",
                    "title": "Mohamad Sabu dikritik Najib",
                    "url": "https://www.bharian.com.my/berita/politik/2019/01/520179/mohamad-sabu-dikritik-najib",
                    "created": 1547537566,
                    "changed": 1547537566,
                    "field_article_author_id": 54730,
                    "field_article_author_name": "Oleh Idris Musa",
                    "field_article_author_email": null,
                    "field_article_topic": "{\"tid\": 132, \"name\": \"Politik\"}",
                    "field_tags": "[{\"tid\": 5288, \"name\": \"Najib\"}, {\"tid\": 28646, \"name\": \"mohamad\"}, {\"tid\": 37312, \"name\": \"Sabu\"}, {\"tid\": 7712, \"name\": \"helikopter\"}, {\"tid\": 97190, \"name\": \"Cameron19\"}]",
                    "field_article_images_url": "https://assets.bharian.com.my/images/articles/15sabuviral2_1547537555.jpg",
                    "field_article_images_caption": "Catatan Najib (kiri) dan Mohamad Sabu di laman rasmi Facebook masing-masing.",
                    "field_article_videos": "",
                    "field_article_lead": "KUALA LUMPUR: Rentetan isu duit minyak, Menteri Pertahanan, Mohamad Sabu, turut menjadi sasaran kritikan bekas Perdana Menteri, Datuk Seri Najib Razak, hari ini. ",
                    "insertDate": "2019-01-15 15:33:03",
                    "created_v2": "2019-01-15 07:32:46",
                    "changed_v2": "2019-01-15 07:32:46"
                }
            }, 
```






