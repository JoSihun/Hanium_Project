# https://www.oracle.com/technetwork/java/javase/downloads/jdk13-downloads-5672538.html Java JDK 설치필요
# Jpype 1.7.0 설치
# konlpy 설치
########################################################################################################################
def regular_expression(text):
    text = text.replace('.', '')  # 정규 표현식을 위해 '온점'을 제거하는 작업
    text = text.replace(',', '')  # 정규 표현식을 위해 '쉼표'를 제거하는 작업
    text = text.replace('(', '')  # 정규 표현식을 위해 '('를 제거하는 작업
    text = text.replace(')', '')  # 정규 표현식을 위해 ')'를 제거하는 작업
    text = text.replace('[', '')  # 정규 표현식을 위해 '['를 제거하는 작업
    text = text.replace(']', '')  # 정규 표현식을 위해 ']'를 제거하는 작업
    text = text.replace('\'', '')  # 정규 표현식을 위해 '작은 따옴표'를 제거하는 작업
    text = text.replace('\"', '')  # 정규 표현식을 위해 '큰 따옴표'를 제거하는 작업
    text = text.replace('\n', '')  # 정규 표현식을 위해 '\n'를 제거하는 작업

    return text
########################################################################################################################
# NLTK 사용법 : https://datascienceschool.net/view-notebook/8895b16a141749a9bb381007d52721c1/
# Okt() 사용법: https://devtimes.com/bigdata/2019/04/18/konlpy/
from konlpy.tag import Okt
import nltk
okt = Okt()

def extract_top_10(user_path, count=20, often=10):
    origin_text = open(user_path, 'r', encoding='UTF-8').read()
    text = regular_expression(origin_text)
    print(f'사용자 자소서:\n{origin_text}')

    tokens = []
    morpheme_tokens = okt.pos(text)
    for token in morpheme_tokens:
        if token[1] == 'Josa':      # 조사를 제외한 품사 모두 포함
            continue
        tokens.append(token[0])
    # print(morpheme_tokens)        # 각 토큰의 품사를 보고 싶다면 주석해제
    # tokens = okt.nouns(text)      # 명사를 기준으로 토큰화 할 경우 주석해제

    print(f'==========================================================================================================')
    frequency_dic = nltk.Text(tokens)
    frequency = frequency_dic.vocab().most_common(count)
    print(f'빈도수가 높은(자주 사용한) 상위 {count}개 단어입니다.')
    for i, token in enumerate(frequency):
        if i % 10 == 0: print()
        print(f'{token[0]}({token[1]})', end=' ')

    print(f'\n========================================================================================================')
    idx_tokens = [token[1] for token in frequency].index(often - 1)
    frequency = frequency_dic.vocab().most_common(idx_tokens)
    print(f'빈도수가 {often}회 이상 출현한 상위 {idx_tokens}개 단어입니다.')
    for i, token in enumerate(frequency):
        if i % 10 == 0: print()
        print(f'{token[0]}({token[1]})', end=' ')
    # show_graph(frequency_dic, count)        # 그래프를 보고 싶다면 주석해제
########################################################################################################################
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc

def show_graph(frequency_dic, count):
    font_fname = 'c:/windows/fonts/gulim.ttc'
    font_name = font_manager.FontProperties(fname=font_fname).get_name()
    rc('font', family=font_name)

    frequency_dic.plot(count)
    plt.show()
########################################################################################################################
def run():
    # 백엔드 연결후 user_path 수정할 것,
    user_path = f'../07_Saramin_dataset/user/answer/test.txt'
    extract_top_10(user_path, count=20, often=10)   # count는 상위 몇개인지, often은 몇회이상 출현한 단어인지

run()
