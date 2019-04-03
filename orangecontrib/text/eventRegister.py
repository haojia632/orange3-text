# API Key : 26b3731d-2aaa-41fb-a6d4-823fe91b2fa7
# Result: articles
                # count
                # page
                # pages
                # results []
                # totalResults

from eventregistry import *
import json
import csv
import pickle
from Orange import data
from orangecontrib.text import Corpus

def json2csv(path):

    articles = pickle.load(open('tradewar.txt', 'rb'))
    results = articles['results']

    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    csvfile = open(path+'.csv', 'w', newline='') # python3下
    writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_ALL)
    flag = True
    count = 0
    for result in results:
        # if count > 3000:
        #     break
        count += 1
        if flag:
            # 获取属性列表
            keys = ['title','date','time','dataType','author','url','dateCrawl','timeCrawl','sentiment','location','body']
            # keys = list(result.keys())
            print (keys)
            writer.writerow(keys) # 将属性列表写入csv中
            flag = False
        # 读取json数据的每一行，将values数据一次一行的写入csv中
        
        ## author
        author =''
        if len(result['authors'])==0:
            author = 'None'
        else:
            author = result['authors'][0]['name']

        ## location
        location = ''
        score = 0
        if len(result['concepts'])!=0:
            for concept in result['concepts']:
                if concept['type'] == 'loc' and concept['score']>score: 
                    location = concept['label']['eng']
                    score = concept['score']

        values = [result['title'],result['date'],result['time'],result['dataType'],author,
                result['url'],result['dateCrawl'],result['timeCrawl'],result['sentiment'],location,result['body']]
        # writer.writerow(list(result.values()))
        writer.writerow(values)
    csvfile.close()

def RequestArticles():
    er = EventRegistry(apiKey='26b3731d-2aaa-41fb-a6d4-823fe91b2fa7')
    # search for the phrase "Barack Obama" - both words have to appear together
    q = QueryArticles(keywords = "Trade war")
    articles = {}
    results = []
    for i in range(1,223):
        q.setRequestedResult(RequestArticlesInfo(
            page = i,
            returnInfo = ReturnInfo(
            articleInfo = ArticleInfoFlags(duplicateList = True, 
                                            concepts = True, 
                                            categories = True, 
                                            location = True,
                                            socialScore=True,
                                            sentiment= True,
                                            dates= True))))
        res = er.execQuery(q)
        articles = res['articles']
        results = results + articles['results']
    articles['results'] = results
    pickle.dump(articles,open('tradewar.txt', 'wb') ) 

def processResponse():
    '''
        author:
            isAgency
            name
            type
            uri
        body:
        dataType:
        date
        datetime
        eventUri
        isDuplicate
        lang
        sim
        source
            dataType
            title
            uri
        time
        title
        uri
        rul
        wgt

    '''
    res = pickle.load(open('tradewar.txt', 'rb'))
    articles = res
    print(articles['totalResults'])
    print(articles['count'])
    print(articles['pages'])
    print(articles['page'])
    article = articles['results'][0]
    print('author   ',article['authors'][0]['name'])
    print('dataType ',article['dataType'])
    print('dataTime ',article['dateTime'])
    print('eventUri ',article['eventUri'])
    print('lang     ',article['lang'])
    print('sim      ',article['sim'])
    articleResultss = articles['results'] + articles['results']
    print(articleResultss)


class eventRegistryAPI:
    """
        封装event registry 接口
    """
    metas = [
        (data.StringVariable('题目'), lambda doc: getattr(doc, 'title')),
        (data.StringVariable('内容'), lambda doc: getattr(doc, 'body')),
        (data.StringVariable('作者'), lambda doc: getattr(doc, 'author')),
        (data.StringVariable('连接'), lambda doc: getattr(doc, 'url')),
        (data.StringVariable('日期'), lambda doc: getattr(doc, 'date')),
        (data.StringVariable('时间'), lambda doc: getattr(doc, 'time')),
    ]

    attributes = []
    class_vars = []

    def __init__(self, on_error=None):
        super().__init__()
        self.on_error = on_error or (lambda x: x)


    def search(self, apikey, query, articles_per_query=100):
        """ Searches for articles."""

        er = EventRegistry(apiKey = apikey)
        q = QueryArticles(keywords = query)
        articles = {}
        results = []
        
        q.setRequestedResult(RequestArticlesInfo(
            page = 1,
            count = articles_per_query,
            returnInfo = ReturnInfo(
            articleInfo = ArticleInfoFlags(duplicateList = True, 
                                            concepts = True, 
                                            categories = True, 
                                            location = True,
                                            socialScore=True,
                                            sentiment= True,
                                            dates= True))))
        res = er.execQuery(q)
        articles = res['articles']
        results = articles['results']
        simplized_results = []
        for result in results:
            simplized_result = {}
            author =''
            if len(result['authors'])==0:
                author = 'None'
            else:
                author = result['authors'][0]['name']

            simplized_result['title'] = result['title']
            simplized_result['date'] = result['date']
            simplized_result['time'] = result['date']
            simplized_result['dataType'] = result['date']
            simplized_result['author'] = result['date']
            simplized_result['url'] = result['date']
            simplized_result['dateCrawl'] = result['date']
            simplized_result['timeCrawl'] = result['date']
            simplized_result['sentiment'] = result['date']
            simplized_result['body'] = result['date']

            simplized_results += simplized_result

        return Corpus.from_documents(simplized_results, 'EventRegistry', self.attributes,
                                     self.class_vars, self.metas, title_indices=[-1])


if __name__ == '__main__':
    # RequestArticles()
    # processResponse()
    json2csv('tradeware')
    
