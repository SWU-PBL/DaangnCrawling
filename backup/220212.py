import numpy as np
import nltk
import pandas as pd

#크롤링한 데이터 불러오기
f = open('C:/Users/초코송이맘_카테고리추가.txt','r', encoding= 'utf-8')
x_data = f.readlines()
x_data = list(map(lambda s: s.strip(), x_data))

for line in x_data:
    print(line.rstrip())
f.close()


#불용어 제거
stopwords = []
f = open('C:/Users/stopwords.txt', 'r', encoding = 'utf-8')
lines = f.readlines()
for line in lines:
    line = line.strip()
    stopwords.append(line)
f.close()


nltk.download('punkt')
for i, document in enumerate(x_data):
    clean_words = [] 
    for word in nltk.tokenize.word_tokenize(document): 
        if word not in stopwords: #불용어 제거
            clean_words.append(word)
    
    x_data[i] = ' '.join(clean_words)
            
print('-------- 불용어 처리 완료 --------\n', x_data)

# list를 dataFrame으로 변환 
transdata = pd.DataFrame(x_data, columns=['파일명']) 
# 추출 경로, index 제거, 인코딩 설정 
transdata.to_csv('C:/Users/불용어처리 완료.csv', index=False, encoding='utf-8-sig')
