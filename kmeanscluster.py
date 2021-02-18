
k-means를 위해 'sim' column (유사한 기사들 번호) 만 가져와 새로운 dataframe을 만든다


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def filterkmeans (originaldf, n):
    newser = pd.Series(originaldf['sim'])
    # Series를 데이터 프레임으로 바꾸며, 번호를 전부 찢어준다.
    newdf = pd.DataFrame(newser.str.split(',',9).tolist(), \
                                 columns = ['1','2','3','4','5','6','7','8','9'])
    # 모든 value 'int'화
    newdf = newdf.apply(pd.to_numeric) 
    # drop.na 가 아닌 최소값에 맞춰 불필요한 컬럼을 제거한다.
    newdf = newdf.drop(['6','7','8','9'], axis = 1)
    # kmeans 구간을 n개로 지정
    kmeans = KMeans(int(n))
    kmeans_label = kmeans.fit_predict(newdf)
    newdf['kmeans_label'] = kmeans_label
    
    return newdf

# checking function if it works
# print(filterkmeans (newdf, 12)['kmeans_label'].unique())


# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

def getnumlist(originaldf, n):
### 다중 리스트 생성 (n개)
### 후에 numlist [index 0~7] 로 접근 가능
    numlist = []
    for i in range(int(n)):
        numlist.append([])
# Kmeans label 번호 정렬
    label_order = []
    for i in filterkmeans(originaldf,n)['kmeans_label'].unique():
        label_order.append (i)


# label 순으로 1,2,3,4 랭크에 해당되는 숫자들만 list에 append 
    for label_number,sort_number in zip(label_order,range(int(n))):
        certaindf = filterkmeans(originaldf,n)[filterkmeans(originaldf,n)['kmeans_label'] == label_number]
        for a in certaindf['1']:
            numlist[sort_number].append(a)
        for b in certaindf['2']:
            numlist[sort_number].append(b)
        for c in certaindf['3']:
            numlist[sort_number].append(c)
        for d in certaindf['4']:
            numlist[sort_number].append(d)
            
    return numlist
# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
def listcount (originaldf, n):
    datelist = []
    summarylist = []
    for i in range(int(n)):
        vocab = Counter(getnumlist(originaldf, n)[i])
        samplelist = list(vocab.most_common(1)[0]) # list와 [0]은 tuple 진입을 위해서
        date = bts['date'][int(samplelist[0])]
        datelist.append(date)
        summary = bts['summary'][int(samplelist[0])]
        summarylist.append(summary)
    return datelist
