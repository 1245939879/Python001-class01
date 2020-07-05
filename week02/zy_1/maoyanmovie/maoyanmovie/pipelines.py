from itemadapter import ItemAdapter
import pandas as pd 
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
dic_info ={'title':[],'movie_type':[],'time':[]}
path='./scrapy-xpath.csv'


class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        conn = pymysql.connect(host = '127.0.0.1',
                                port = 3306,
                                user = 'root',
                                password = '123456',
                                database = 'test',
                                charset = 'utf8'
                                )

        cur=conn.cursor()

        result=[]
        values=(item['title'],item['movie_type'],item['time'])

        try:
            cur.execute('insert into film.film_name(title,movie_type,c_time) '+' values(%s,%s,%s)',values)
            # cur.execute('select * from film.film_name')
            result.append(cur.fetchall())
            cur.close()
            conn.commit()

            print(result)

        except Exception as a:
            print(a)

        conn.close()
        return item