import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import nltk
import time
from tqdm import tqdm_notebook

import pandas as pd
import numpy as np

------------------------------------
#url 가져오는 함수 - 기사 list에서 뽑아온다.

def get_url():
   # link_list=[]
    for a in bs_obj.find_all('a', href=True):
        naver = 'news.naver.com/main/'
        if naver in a['href']:
            #print(a['href'])
            link_list.append(a['href'])
            #link_list_total.append(link_list)
            
#날짜 가져오는 함수
def get_date():
  #  date_list=[]
    for span in bs_obj.findAll('span',{'class':'info'}):
        if '2020' in span.text:
            date_list.append(span.text)
   # date_list_total.append(date_list)

#list page에서 언론사 가져오는 함수
def get_media():
 #   media_list=[]
    for a in bs_obj.findAll('a',{'class':'info press'}):
        a1 = a.text.split('언')[0]
        media_list.append(a1)
#    media_list_total.append(media_list)

#정민's 타이틀 가져오기
def get_title(bs):
    title=''
    if bs.find('h3',{'id':'articleTitle'}):
        title = bs.find('h3',{'id':'articleTitle'})
    elif bs.find('h2',{'class':'end_tit'}):
        title = bs.find('h2',{'class':'end_tit'})
    else:
        pass
    title = re.sub(r'[^A-Za-z0-9가-힣 ]','',title.text)  #cleaning
    return title

#정민's content 가져오는 함수
def get_content(bs):
    article_obj =bs.find_all('div')[0]   # type: ResultSet

    if article_obj.find('div',{'id':'articleBodyContents'}):
        article_obj = article_obj.find('div',{'id':'articleBodyContents'})
    elif article_obj.find('div',{'class': 'article_body'}):
        article_obj = article_obj.find('div',{'id':'articeBody'})

    # cleaning (tag)
    for e in range(len(article_obj.find_all('em'))):
        article_obj.em.extract()
        article_obj.img.extract()
    for i in range(len(article_obj.find_all('a'))):
        article_obj.a.extract()
    if article_obj.find('script'):
        article_obj.script.extract()
    if article_obj.find('strong'):
        article_obj.strong.extract()
    
    # cleaning (text)
    article_obj = BeautifulSoup(re.split('\w\w\w 기자',article_obj.prettify())[0], 'lxml')
    article = clear_content(article_obj.text)
    
    return article

#정제 함수
def clear_content(text):
    remove_special = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]', '', text)
    remove_flash_error = re.sub('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0', '', remove_special)
    remove_strip = remove_flash_error.strip().replace('   ', '') # 공백 에러 삭제
    remove_dphase = re.sub('if deployPhase(.*)displayRMCPlayer', '', remove_strip)
   
    cleared_t = re.sub('[\t]',' ',remove_dphase)
    cleared_n = re.split('\n',cleared_t)
    cleared_content = ' '.join([ s for s in cleared_n if len(s)>80 ])

    return cleared_content

#받은 url로 request하는 함수
def url_go(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    result = requests.get(url, headers=headers)
    bs = BeautifulSoup(result.text,'lxml')
    #time.sleep(0.5)
    return (bs)
    
#정민's title, content, url 가져오는 함수
def news_parsing(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    res = requests.post(url, headers=headers)
    bs_obj_n = BeautifulSoup(res.text, 'lxml')

    news = []
#    news.append(get_media(bs_obj_n))     # media
 #   news.append(get_date(bs_obj_n))      # date
    news.append(get_title(bs_obj_n))     # title
    news.append(get_content(bs_obj_n))   # content
    news.append(url)                     # url
    
    return news



#------------------Main-------------------

path = './chromedriver.exe'
driver = webdriver.Chrome(path)

start_url = 'https://search.naver.com/search.naver?where=news&query=%EB%B0%A9%ED%83%84%EC%86%8C%EB%85%84%EB%8B%A8%20%7C%20BTS&sm=tab_opt&sort=2&photo=0&field=1&reporter_article=&pd=3&ds=2020.01.01&de=2020.05.31&docid=&nso=so%3Ada%2Cp%3Afrom20200101to20200531%2Ca%3At&mynews=1&refresh_start=0&related=0'
driver.get(start_url)


#selenium 4대 언론사 체크하여 관련 기사만 뽑아내는 driver명령
driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[5]/a').click()
driver.find_element_by_xpath('//*[@id="ca_1032"]').click()
driver.find_element_by_xpath('//*[@id="ca_1025"]').click()
driver.find_element_by_xpath('//*[@id="ca_1028"]').click()
driver.find_element_by_xpath('//*[@id="ca_1023"]').click()  #조선
driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[5]/div/span/span[1]/button/span/strong').click()


#----selenium으로 page당 동적으로 url가져오는 구문------

link_list = []
date_list = []
media_list = []
#처음 한 번은 for문 전에 가져와야한다.
result = driver.page_source
bs_obj = BeautifulSoup(result,'lxml')
get_url()
get_date()
get_media()
#page들을 도는 for문
for i in range(1,25):

    url = 'https://search.naver.com/search.naver?&where=news&query=%EB%B0%A9%ED%83%84%EC%86%8C%EB%85%84%EB%8B%A8%20%7C%20BTS&sm=tab_pge&sort=2&photo=0&field=1&reporter_article=&pd=3&ds=2020.01.01&de=2020.05.31&docid=&nso=so:da,p:from20200101to20200531,a:t&mynews=1&start='+str(i)+'1&refresh_start=0'
    driver.get(url)
    result = driver.page_source
    bs_obj = BeautifulSoup(result,"lxml")

    get_url()
    get_date()
    get_media()
    
    time.sleep(0.5)
    
    
#타이틀과 본문을 news_data로 가져오기
news_data = []
for i in tqdm_notebook(link_list):
    news_data.append(news_parsing(i))
news_data


#news_data에 미디어와 날짜 추가
for i in range(len(news_data)):
    news_data[i].insert(0,date_list[i])
    news_data[i].insert(0, media_list[i])
news_data 


#dataframe에 넣기
columns = ['media','date','title','article-original','url']
news_df = pd.DataFrame(news_data,columns=columns)
news_df


