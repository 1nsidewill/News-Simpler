from gensim.summarization.summarizer import summarize
# summarize에 입력 가능한 매개 변수는 다음과 같다.

# test_articles[i] (str) – 요약할 테스트.
# ratio (float, optional) – 요약에 대해 선택할 원본 텍스트의 문장 수 비율을 결정하는 0~1 사이 숫자.
# word_count (int or None, optional) – 출력에 포함할 단어 수. 두 파라미터가 모두 제공되는 경우 ratio는 무시된다.
# split (bool, optional) – True면 문장 list가 반환된다. False는 조인(join)된 문자열이 반환된다.

test_articles = []
li = ['IT','경제','사회','스포츠','연예','정치']
for i in li:
  dir = './data/test_article/'+i+'.txt'
  data = open(dir, 'r').read()
  # print('---',i,'---\n',data)
  test_articles.append(data)

for i in range(len(test_articles)):
  print(i,'.',li[i],'\n',summarize(test_articles[i], ratio=0.3))
  # print(summarize(text))
  # print(summarize(text, word_count=100))
  # print(summarize(text, ratio=0.3))
