#데이터 가져오기
columns = ['media','date','title','article_original','url']
news_crawled_df = pd.read_csv('./crawled_news/news_df_210205_v02.csv')
news_crawled_df


#gensim summary (전체 문서 부분만)
from gensim.summarization.summarizer import summarize

summary_list = []
for i in range(65):
    summary_list.append(summarize(news_crawled_df.article_original[i],ratio=0.3))
summary_list


#gensim에서 요약이 아예 안나오는 것
print(news_crawled_df.article_original[12])
summarize(news_crawled_df.article_original[12])



#okt로 형태소 기사 분석
from konlpy.tag import Okt
pos_tagger = Okt()

articles = news_crawled_df.article_original

# def tokenize(doc):
#     return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

#t = tokenize(articles[0])

article_morphed = pos_tagger.morphs(articles[0])


#불용어 처리
stopwords2 = pd.read_csv('./불용어리스트2.txt',header=None)
sw = stopwords2[0]

morphed = []
for word in article_morphed:
    if word not in sw:
        morphed.append(word)
#print(morphed)


#카운터
from collections import Counter
vocab = Counter(morphed)
print(vocab)
