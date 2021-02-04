'''
naver_news_crawler.ipynb
version. 1.0
update. 2021/02/04
'''

import re
import pandas as pd
import numpy as np
from tqdm import tqdm_notebook   # 진행 상황을 bar로 시각화

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests  
from bs4 import BeautifulSoup


# ================ method ===================

# ------------------------------
# load_url : 페이지 번호로 url 가져옴
# ------------------------------
def load_url(cont_num):
    search_key = 'BTS | 방탄소년단'
    sort_num = '2' #0:관련된 순, 1:최신순, 2:오래된순
    start_date = '2020.09.01'
    end_date = '2020.12.31'
    cont_num = str(cont_num)  #페이지 별 첫번째 뉴스 번호 (페이지당 10건)
    url='https://search.naver.com/search.naver?&where=news&query='+search_key\
    +'&sm=tab_pge&sort='+sort_num+'&photo=0&field=1&reporter_article=&pd=3&ds='+start_date+'&de='+end_date+'&docid=&nso=so:da,p:from'\
    + start_date.replace('.','')+'to'+end_date.replace('.','')+',a:t&mynews=1&start='+cont_num+'&refresh_start=0'
    return url
    
# ------------------------------
# 뉴스 내용 정제
# ------------------------------
def clear_content(text):
    remove_special = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]', '', text)
    remove_flash_error = re.sub('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0', '', remove_special)
    remove_strip = remove_flash_error.strip().replace('   ', '') # 공백 에러 삭제
    remove_dphase = re.sub('if deployPhase(.*)displayRMCPlayer', '', remove_strip)
   
    cleared_t = re.sub('[\t]',' ',remove_dphase)
    cleared_n = re.split('\n',cleared_t)
    cleared_content = ' '.join([ s for s in cleared_n if len(s)>80 ])

    return cleared_content


# ------------------------------
# media (언론사)
# ------------------------------
def get_media(bs):
    media = bs.find('div', {'class':'press_logo'}).find('img')['alt']
    return media

# ------------------------------
# date (기사 입력일), type: str
# ------------------------------
def get_date(bs):
    date = bs.find('span',{'class':['t11','author']})
    date = '-'.join(re.findall('\d+',date.text)[:3]) 
    return date
    
# ------------------------------    
# title
# ------------------------------
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

# ------------------------------
# content
# ------------------------------
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

# ------------------------------
# news parsing
# ------------------------------
def news_parsing(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    res = requests.post(url, headers=headers)
    bs_obj_n = BeautifulSoup(res.text, 'lxml')

    news = []
    news.append(get_media(bs_obj_n))     # media
    news.append(get_date(bs_obj_n))      # date
    news.append(get_title(bs_obj_n))     # title
    news.append(get_content(bs_obj_n))   # content
    news.append(url)                     # url
    
    return news
    
# ===========================================


# ================= main ====================
# - webdriver open
path = './lib/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(load_url(1))             # 검색 조건 지정된 1 페이지 접속
time.sleep(0.5)

# ------------------------------
# 검색 조건: 언론사 선택
# ------------------------------
media_list = {'경향':'//*[@id="ca_1032"]', '중앙':'//*[@id="ca_1025"]','한겨례':'//*[@id="ca_1028"]','조선':'//*[@id="ca_1023"]'}

# - btn: 출처
driver.find_element(By.XPATH, '//*[@id="snb"]/div/ul/li[5]/a').click() 

# - check box: 언론사 선택
for s in media_list:
    element = driver.find_element(By.XPATH, media_list[s])
    driver.execute_script("arguments[0].click();", element)
    print(s)
    time.sleep(0.5)
    
# - btn: 확인
driver.find_element(By.XPATH, '//*[@id="snb"]/div/ul/li[5]/div/span/span[1]/button').click()
print('확인')    

# ------------------------------
# 웹페이지 순서대로, 뉴스 url 가져오기
# ------------------------------
start_con = 1
end_con = 32
link_list =[]
naver = 'news.naver.com/main/'

for i in range(start_con,end_con,10):
    driver.get(load_url(i))
    # - 페이지(html) parsing
    page_html = driver.page_source    # type: str
    bs_obj = BeautifulSoup(page_html, 'lxml')
    # - 페이지 내 '네이버뉴스' 링크(10개) 가져오기
    lis = [ a['href'] for a in bs_obj.find_all('a', href=True) if naver in a['href'] ]
    link_list.extend(lis)
    time.sleep(0.5)
    
# print(len(link_list))
# print(link_list)


# - webdriver quit
# driver.quit()


news_data = []
for i in tqdm_notebook(link_list):
    news_data.append(news_parsing(i))
    
# news_data 확인하기
col_name = ['media','date','title','article_original','url']
news_df = pd.DataFrame(news_data,columns = col_name)
# news_df
