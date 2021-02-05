import os
import sys
import warnings
import numpy as np
import pandas as pd
import json

import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set(style='white', context='notebook', palette='deep')

warnings.filterwarnings(action='ignore')

#데이터 가져오기
with open('./data_news/train.jsonl', 'r',encoding='utf-8') as json_file:
    json_list = list(json_file)

trains = []
for json_str in json_list:
    line = json.loads(json_str)
    trains.append(line)
    
train_df = pd.DataFrame(trains)
train_df.head()


#dataframe에 extractive 숫자 답안을 본래 문장으로 추가
ext_ans = []
for i in range(len(train_df)):
    temp =[]
    for num in train_df.extractive[i]:
        temp.append(train_df.article_original[i][num])
    ext_ans.append(temp)
train_df['ext_ans'] = ext_ans


# 기사를 리스트가 아닌 한 문단의 스트링으로 만드는 함수
def article_strfy(corpus_list,article_no):
    article = ''
    for sent in corpus_list[article_no]:
        article += str(sent)
        article += ' '
    return article, article_no   #합쳐진 기사와 answer을 리턴한다.
    

#gensim summarization
from gensim.summarization import summarize
from gensim.summarization import summarize_corpus
article, _ = article_strfy(train_df['article_original'],1)
print(article)
print()
print(summarize(article,.6))
print()
print(train_df['ext_ans'][no])


####  LEXRANK

from lexrankr import LexRank
lexrank = LexRank()

article, no = article_strfy(train_df.article_original,5)
              
lexrank.summarize(article)
summaries = lexrank.probe(0.2)  #3을 넣으면 3문장 요약

print(article)
print(summaries)
print(train_df['ext_ans'][no])


#인터넷 기사 summarize
from lexrankr import LexRank
lexrank = LexRank()
lexrank.summarize('잉글랜드 프로축구 프리미어리그(EPL) 토트넘홋스퍼가 ‘에이스’ 손흥민(29)에게 큰 기대를 보인다. 또 다른 ‘주포’ 해리 케인(28)이 부상으로 쓰러졌기 때문이다. 토트넘은 내달 1일 오전 4시 15분(이하 한국시간) 브라이턴 안방에서 브라이턴과 2020∼2021 EPL 21라운드 경기를 치른다. 직전 라운드에서 패배를 경험했던 토트넘은 이날 경기서 필승을 정조준한다. 토트넘은 지난 29일 리버풀과의 EPL 20라운드 경기에서 1-3으로 패배했다. 손흥민은 전반 3분 득점에 성공했지만 비디오판독시스템(VAR) 결과 오프사이드로 판정돼 취소되는 아픔을 겪었다. 리그 득점 1위인 리버풀의 모하메드 살라 또한 골망을 흔들었지만 공격 시작점에서 호베르투 피르미누의 핸드볼 파울이 확인돼 골이 선언되지 않았다. 손흥민과 공동 2위였던 케인 역시 전반에 부상 아웃되며 득점 3위권 순위는 그대로 유지됐다. 여전히 살라를 한 골 차로 뒤쫓고 있는 손흥민이 브라이턴전 득점으로 팀을 위기에서 구하고 득점 선두를 정조준한다. 토트넘과 손흥민 모두에게 긍정적인 것은 브라이턴이 강등에서 자유롭지 못한 객관적인 ‘한 수 아래’ 팀이라는 점이다. 매 시즌 리그 생존을 위해 분투하는 팀인 만큼, 누가 봐도 토트넘이 걱정할만한 상대는 아니다. 하지만 EPL에서 방심은 금물이다. 토트넘은 2019∼2020시즌 브라이턴의 홈에서 0-3 패배를 당하는 수모를 겪은 바 있다. 토트넘이 케인의 공백이라는 악재를 딛고 브라이턴전 승리를 따내며 도약의 기반을 마련할 수 있을지 시선이 집중된다. 손흥민이 브라이턴전에서 토트넘에 승점 3점을 가져다주는 동시에 득점 1위로 치고 나갈 수 있을까. 토트넘과 손흥민 모두에게 중요한 한 판이 될 브라이턴 원정이다.')
summaries = lexrank.probe(0.2)

print('잉글랜드 프로축구 프리미어리그(EPL) 토트넘홋스퍼가 ‘에이스’ 손흥민(29)에게 큰 기대를 보인다. 또 다른 ‘주포’ 해리 케인(28)이 부상으로 쓰러졌기 때문이다. 토트넘은 내달 1일 오전 4시 15분(이하 한국시간) 브라이턴 안방에서 브라이턴과 2020∼2021 EPL 21라운드 경기를 치른다. 직전 라운드에서 패배를 경험했던 토트넘은 이날 경기서 필승을 정조준한다. 토트넘은 지난 29일 리버풀과의 EPL 20라운드 경기에서 1-3으로 패배했다. 손흥민은 전반 3분 득점에 성공했지만 비디오판독시스템(VAR) 결과 오프사이드로 판정돼 취소되는 아픔을 겪었다. 리그 득점 1위인 리버풀의 모하메드 살라 또한 골망을 흔들었지만 공격 시작점에서 호베르투 피르미누의 핸드볼 파울이 확인돼 골이 선언되지 않았다. 손흥민과 공동 2위였던 케인 역시 전반에 부상 아웃되며 득점 3위권 순위는 그대로 유지됐다. 여전히 살라를 한 골 차로 뒤쫓고 있는 손흥민이 브라이턴전 득점으로 팀을 위기에서 구하고 득점 선두를 정조준한다. 토트넘과 손흥민 모두에게 긍정적인 것은 브라이턴이 강등에서 자유롭지 못한 객관적인 ‘한 수 아래’ 팀이라는 점이다. 매 시즌 리그 생존을 위해 분투하는 팀인 만큼, 누가 봐도 토트넘이 걱정할만한 상대는 아니다. 하지만 EPL에서 방심은 금물이다. 토트넘은 2019∼2020시즌 브라이턴의 홈에서 0-3 패배를 당하는 수모를 겪은 바 있다. 토트넘이 케인의 공백이라는 악재를 딛고 브라이턴전 승리를 따내며 도약의 기반을 마련할 수 있을지 시선이 집중된다. 손흥민이 브라이턴전에서 토트넘에 승점 3점을 가져다주는 동시에 득점 1위로 치고 나갈 수 있을까. 토트넘과 손흥민 모두에게 중요한 한 판이 될 브라이턴 원정이다.\n')
for summary in summaries:
    print(summary)
© 2021 GitHub, Inc.
