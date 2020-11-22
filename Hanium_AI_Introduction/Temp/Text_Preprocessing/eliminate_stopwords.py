#!/usr/bin/env python
# coding: utf-8

from konlpy.tag import Mecab
import konlpy
mecab = Mecab()

def eliminate_stopwords(orig_text, stop_text):
    word_tokens = mecab.morphs(orig_text)  # 형태소 추출
    stop_words = stop_text.split()
    
    result = []
    for w in word_tokens:
        if w not in stop_words:
            if len(w) > 1: # 1개 이하의 단어도 추가로 제거
                result.append(w)
                
    print(f'<불용어 제거>')
    print(result)
    return result

def run():
    #USER_PATH = f'/mnt/c/Users/ehdal/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset/test.txt' # 경로
    #STOPWORDS_PATH = f'/mnt/c/Users/ehdal/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset/stop_words.txt' # 경로
    USER_PATH = '../../Final/07_Saramin_dataset/testset/test.txt'  # 경로
    STOPWORDS_PATH = '../../Final/07_Saramin_dataset/testset/stop_words.txt'  # 경로
    # 원본 텍스트 데이터
    origin_text = konlpy.utils.read_txt(USER_PATH , encoding='UTF-8')  # txt 파일 읽음
    stopwords_text = konlpy.utils.read_txt(STOPWORDS_PATH , encoding='UTF-8')  # 불용어 파일

    print(f'<원본 텍스트>')
    print(origin_text, '\n')

    # 불용어 제거
    eliminate_stopwords(origin_text, stopwords_text)
    
run()
