## Extractive 컬럼에 있는 인덱스 3개로 해당 문장 추출 후 데이터프레임 화


summary_list = []
for j in range(og_train.shape[0]):  
    new_list=[]
    for i in train_df['extractive'][j]:
        new_list.append(train_df['article_original'][j][i])
    print(new_list)
    summary_list.append(new_list)

### pandas - series 로 변환
sentence_df = pd.Series (summary_list)

### 원본 데이터프레임에 Summary 컬럼 (sentence_df) 를 merge (추가)
final_df = pd.concat ([train_df, sentence_df], axis= 1)


# 데이터 지정
article_data = final_df ['article_original']
article_target = final_df [0]


### CountVectorizer TFIDF 등에 Fit 하려면 'lower~' 를 피하기 위해 str화 해주어야 한다.
article_data = article_data.astype(str)
article_target = article_target.astype(str)
