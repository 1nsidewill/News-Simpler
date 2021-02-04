from transformers import *
from summarizer import Summarizer



# Load model, model config and tokenizer via Transformers
custom_config = AutoConfig.from_pretrained('monologg/kobert')
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained('monologg/kobert')
custom_model = AutoModel.from_pretrained('monologg/kobert', config=custom_config)

summarize_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
summarize_model2 = Summarizer()  



# txt 파일로 저장돼 있는 뉴스 원문 불러오기
test_articles = []
li = ['IT','경제','사회','스포츠','연예','정치']
for i in li:
  dir = './data/'+i+'.txt'
  data = open(dir, 'r', encoding = 'utf-8').read()
  # print(i,'\n',data)
  test_articles.append(data)



# 요약 
for i in range(len(test_articles)):
  print(i,'.',li[i],'\n',summarize_model2(test_articles[i], ratio=0.2))
