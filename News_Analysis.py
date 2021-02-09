import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


-----정제 과정-----
#뉴스 데이터 불러오기
columns = ['media','date','title','article_original','url']
news_crawled_df = pd.read_csv('./crawled_news/news_df_210205_v02.csv')

# N/A처리
news_crawled_df.isna().sum()

news_crawled_df.dropna(inplace=True)
news_crawled_df.info()

# 인덱스 리셋
news_crawled_df.reset_index(inplace=True)
news_crawled_df.drop('index',inplace=True,axis=1)


#불용어 import
stopwords2 = pd.read_csv('./불용어리스트2.txt',header=None)
stopwords = list(stopwords2[0])


#okt 형태소 토크나이징
from konlpy.tag import Okt
okt = Okt()

articles = news_crawled_df.article_original

articles_morphed = []
for article in articles:
    morph = okt.morphs(article)
    
    stopped = ''
    for word in morph:
        if word not in stopwords:
            stopped += word
            stopped += ' '
            
    articles_morphed.append(stopped)
    

#형태소 분해된 컬럼 추가
news_crawled_df['article_morphed'] = articles_morphed
#날짜 칼럼 추가
news_crawled_df['date_pd']=pd.to_datetime(news_crawled_df['date'])



-----분석 과정-----
###함수###

# 날짜 그룹별 tfidf 변환 함수
def tfidfy(period_no):
    tfidf = TfidfVectorizer(lowercase=False)
    #그룹에 있는 아티클 가져오기
    article_group = [news_crawled_df.article_original[i] for i in date_grouped[period_no]]

    art_group_tfidf = tfidf.fit_transform(article_group)
    return art_group_tfidf

# 그룹 내에서 유사도 높은 기사의 index 가져오는 함수
def get_similar_art_index(article_index):
    # 그룹 안의 첫 번째 기사와 나머지 기사간의 similarity 비교
    sim_pair = cosine_similarity(art_group_tfidf[article_index],art_group_tfidf)
    # 인덱스 내림차순으로 소트
    sorted_index = sim_pair.argsort()[:,::-1]
    # 자기자신은 빼기
    sorted_index = sorted_index[:,1:]
    print(sorted_index)

    # #유사도가 큰 순으로 group을 추출해 재정렬
    # group = pd.Series(date_grouped[0])
    # art_sorted_indices = group[sorted_index.reshape(-1)]
    # print(art_sorted_indices)

    #유사도가 큰 순으로 유사도 값을 재정렬하되 자기 자신은 제외
    art_sim_value = np.sort(sim_pair.reshape(-1))[::-1]
    art_sim_value = art_sim_value[1:]
    print(art_sim_value)

    # 유사도가 0.3보다 높은 인덱스만 뽑아오기.
    index_high = []
    for num,value in enumerate(art_sim_value):
        if value>=0.3:
            index_high.append(sorted_index[:,num].tolist())
            
    return index_high
    
    
### Main ###

#기사 날짜 14일마다 그룹화
date_grouped = []
date_range = pd.date_range(start='2020-01-01', end='2020-12-31',periods=26)
L = len(date_range)
R = len(news_crawled_df)

for i, date in enumerate(date_range):
    index_group = []
    if i< L-1:
        for j in range(R):
            if date_range[i] < news_crawled_df.date_pd[j] <= date_range[i+1]:
                index_group.append(j)
        date_grouped.append(index_group)

--------------#2021-02-09
