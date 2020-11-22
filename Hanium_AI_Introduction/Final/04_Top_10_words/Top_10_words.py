from konlpy.tag import Mecab
from collections import Counter
import konlpy
import kss
import pandas as pd
mecab = Mecab()

# 문장 단위로 토큰화
def sentences_tokenize(orig_text, stop_text):
    sent_text = kss.split_sentences(orig_text)
    stop_words = stop_text.split()
    
    sentences = []
    
    for i in sent_text:
        sentence = mecab.morphs(i) # 단어 토큰화
        result = []
        
        for word in sentence:
            if word not in stop_words: # 단어 토큰화 된 결과에 대해서 불용어를 제거
                if len(word) > 1: # 단어 길이가 1 이하인 경우에 대해서 추가로 단어를 제거
                    result.append(word)
        sentences.append(result)
    #print(sentences)
    return sentences
    
# 상위 10개 단어
def top_10_words(orig_text, stop_text):
    words = sum(sentences_tokenize(orig_text, stop_text), []) # 단어들을 하나의 리스트로 만들기
    frequency = Counter(words)
    # Counter 모듈을 이용하면 단어의 모든 빈도를 쉽게 계산 가능
    vocab_size = 10 
    vocab = frequency.most_common(vocab_size) # 등장 빈도수 상위 10개 단어만 저장
    
    word = [] # 단어 리스트
    freq = [] # 빈도수 리스트
    
    print(f'< 상위 {vocab_size}개 단어와 빈도수 >\n')
    i = 0
    for (w, f) in vocab:
        i = i+1
        print(f'{i}. {w} \t({f} 회)')
        word.append(w)
        freq.append(f)
        
    return vocab

def run():
    #USER_PATH = f'/mnt/c/Users/ehdal/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset/test.txt' # 경로
    #STOPWORDS_PATH = f'/mnt/c/Users/ehdal/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset/stop_words.txt' # 경로
    USER_PATH = '../07_Saramin_dataset/testset/test.txt'  # 경로
    STOPWORDS_PATH = '../07_Saramin_dataset/testset/stop_words.txt'  # 경로
    # 원본 텍스트 데이터
    origin_text = konlpy.utils.read_txt(USER_PATH , encoding='UTF-8')  # txt 파일 읽음
    stopwords_text = konlpy.utils.read_txt(STOPWORDS_PATH , encoding='UTF-8')  # 불용어 파일

    print(f'<원본 텍스트>')
    print(origin_text, '\n')

    # 불용어 제거
    sentences_tokenize(origin_text, stopwords_text)
    # 상위 10개 단어 추출
    top_10_words(origin_text, stopwords_text)
    
run()