# News-Simpler
Summarized News in Timeline  
요약된 문장으로 보는 뉴스 히스토리

![image](https://user-images.githubusercontent.com/75239607/120752867-4c647780-c545-11eb-9c89-438872e63318.png)

## About Team

Jung Min Yeo @jmin1117  
Will Gyuha Yi @1nsidewill  
Peter Bin Jino @bean-gno  


### Requirements

```
rhinoMorph
Transformers
konlpy
streamlit
bert-extractive-summarizer
```

### Installing / 설치

아래 사항들로 현 프로젝트에 관한 모듈들을 설치할 수 있습니다.

```
pip install transformers
pip install streamlit
pip install bert-extractive-summarizer
```

### NaverNewscrawler
```
Selenium Webdriver, BeautifulSoup 을 이용한 자동화 뉴스 크롤러.
원하는 키워드, 언론사, 기간을 입력 해 .xlsx (엑셀) 또는 .csv 로 저장한다.
```

### Similarity
```
Dataframe 정제 후 크롤링 된 모든 기사들을 Tokenizing. 
TF-IDF (vectorizer) 와 Cosine Similarity (OR linear Kernel) 등 으로 문서 유사도를 구현해
서로 유사한 기사들의 목록을 가져온다. 유사 기사 목록이 존재하지 않거나 적으면 중요하지 않은 issue라고 판단, 
유사한 기사가 많으면 많을 수록 HOT - TOPIC (issue) 라고 판단.
```
### Clustering
```
K-means 를 이용해 유사도를 측정한 dataset에 대해 군집화. 
높은 유사 점수를 가진 (핫이슈라고 판단이 되는) 유사한 기사들끼리 K-means clustering (군집화)를 통해 각 그룹으로 찢어짐.
이 후 각 그룹 내에서 제일 영양가 있는 기사를 하나씩 선별 (Counter 기반). 
최종 n개의 HOT-NEWS 만 남게 됨.
```

### Summarizing
```
Summarizer + KoBERT
Gensim Textrank
Lexrank
```

### Visualization
```
streamlit timeline
```


### Run Orders

왜 이렇게 동작하는지, 설명합니다

```
run newscrawler.py
run similarity.py
run clustering.py
```

### tests

```
예시
```

## Deployment / 배포

Add additional notes about how to deploy this on a live system / 라이브 시스템을 배포하는 방법


## Contributiong / 기여

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. / [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽고 이에 맞추어 pull request 를 해주세요.


## Demo 

https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1zTY1oyRhZga1Kupl8TOOv5KYBbrm_OthtgFOdeDmVY0&font=Default&lang=en&initial_zoom=2&height=950
