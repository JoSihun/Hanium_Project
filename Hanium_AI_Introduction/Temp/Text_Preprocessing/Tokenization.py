#!/usr/bin/env python
# coding: utf-8


from konlpy.tag import Mecab
import konlpy
mecab = Mecab()

def text_morphs(text):
    morphs = mecab.morphs(text) # 형태소 추출
    print(f'<형태소 추출>')
    print(morphs)
    return morphs


def text_pos(text):
    pos = mecab.pos(text) # 품사 태깅
    print(f'<품사 태깅>')
    print(pos)
    return pos


def text_nouns(text):
    nouns = mecab.nouns(text) # 명사 추출
    print(f'<명사 추출>')
    print(nouns)
    return nouns


def run():
    #USER_PATH = f'/mnt/c/Users/ehdal/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset/test.txt' # 경로
    USER_PATH = '../../Final/07_Saramin_dataset/testset/test.txt'
    # 원본 텍스트 데이터
    origin_text = konlpy.utils.read_txt(USER_PATH, encoding='UTF-8')  # txt 파일 읽음
    str = "산업 내 수직적 통합, 전략적 제휴, Globalization을 추진하기 위하여 대상회사, 관련회사, Industry 전체의 정확한 가치를 산정하고 평가하는 능력"
    print(f'<원본 텍스트>')
    print(str, '\n')
    
    text_morphs(str) # 형태소 추출
    #text_pos(origin_text) # 품사 태깅
    text_nouns(str) # 명사 추출
    
run()
    

