# 참고 : https://excelsior-cjh.tistory.com/93
# 참고 : https://korbillgates.tistory.com/171
# 참고 : https://m.blog.naver.com/myincizor/221643594756 //코사인 유사도
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk

StopWord_Path = '../../Final/07_Saramin_dataset/testset/stop_words.txt'
class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.okt = Okt()
        self.stopwords = open(f'{StopWord_Path}', 'r', encoding='utf-8').read().split('\n')   # 불용어

    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence is not '':
                nouns.append(' '.join([noun for noun in self.okt.nouns(str(sentence))
                                if noun not in self.stopwords and len(noun) > 1])) # 키워드로 추출할 글자개수 정해줄수있음(현재 2개이상)
        return nouns

class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()
        self.sentences = self.sent_tokenize.text2sentences(text)
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)

# 코사인 유사도
def cosine_similarity(v1, v2):
    prod = np.dot(v1, v2)
    len1 = np.sqrt(np.dot(v1, v1))
    len2 = np.sqrt(np.dot(v2, v2))
    return prod / (len1 * len2)

def keyword_load(x):
    return {0 : ['정직','도전','근성','열정','창의'], #CJ
            1 : ['창의','도전','전문','신뢰','화합','글로벌 역량'], #DB
            2 : ['지식','도전','의지','창의','용기','정직','사명감','책임감','성실','협동',], #KCC
            3 : ['도전','존중','소통','기본','원칙'], #KT
            4 : ['열정','도전','창의','혁신','고객','경쟁'], #LG
            5 : ['긍정','기본','윤리','창의','변화','혁신','전문','열정','노력'], #LS
            6 : ['패기','자발','의욕','실행','역량','팀워크'], #SK
            7 : ['열정','패기','도전','유연','창의','용기','경험'], #넥슨
            8 : ['열정','책임','일류','도전','자신감','혁신','변화'], #넷마블
            9 : ['협력','행복','전문','정직','신뢰','도전','창의','열정'], #농협
            10 : ['도전','열정','자율','책임','신념'], #대우건설
            11 : ['책임감','노력','리드','소통','몰입','협력','공감'], #동원
            12 : ['존중','배려','팀워크','열정','소통','근성','실천'], #두산
            13 : ['패기','투지','도전','노력','협력','양보'], #롯데
            14 : ['고객','전문','지혜','정직','신뢰','용기','실천'], #미래에셋
            15 : ['정직','신뢰','용기','동료애','배려','존중','책임감','열정','창의','상상력','겸손'], #삼성전자
            16 : ['창의','책임','도전','용기','열정'], #셀트리온
            17 : ['고객','헌신','창의','도전','열정'], #신세계
            18 : ['고객','공감','몰입','전문성','창의'], #아모레퍼시픽
            19 : ['도전','혁신','감사','소통','신뢰','정도'], #애경
            20 : ['전문','열정','도전','자기주도','신뢰','헌신'], #카카오
            21 : ['신뢰','존중','지성','열정','도전','창조'], #태영건설
            22 : ['실천','겸손','존중','배려','창의'], #포스코
            23 : ['열정','혁신','협동','도전','리더'], #한국타이어 앤 테크놀로지
            24 : ['창의','신념','성의','실천','책임','봉사'], #한진
            25 : ['도전','창의','자신감','헌신','정도'], #한화
            26 : ['전문','창의','도전','도덕','책임','실행'], #현대백화점
            27 : ['창의','혁신','정직','원칙','실행','열정','소통','협력'], #현대산업개발
            28 : ['도전','창의','열정','책임감','협력','소통','존중'], #현대자동차
            29 : ['최고','전문','혁신','긍정','책임','열정','신뢰'] #효성
            }[x]

def Keyword_Similarity(corporate_number):
    Path = '../../Final/07_Saramin_dataset/dataset'
    #Repeat = 6592
    print(f"{corporate_number}에 해당하는 기업에 대한 키워드와 비교합니다.")
    corporate_keyword_list = keyword_load(corporate_number)
    corporate_keyword_str = ' '.join(corporate_keyword_list)

    f = open(f'{Path}/0.txt', 'r', encoding='utf-8')
    intro_data_list = f.readlines()
    intro_data_str = intro_data_list[2:]  # 기업명과 부서제외
    intro_data_str = '\n'.join(intro_data_str)

    textrank = TextRank(intro_data_str)
    nouns_list = textrank.nouns
    keyword_str = ' '.join(nouns_list)
    keyword_list = []

    in_keyword_temp = []
    in_keyword = []
    not_in_keyword = []

    count_vec = CountVectorizer()

    # 명사 리스트로 추출
    for noun in nouns_list:
        keyword_list.extend(noun.split())

    # 일치 키워드 추출
    for key in corporate_keyword_list:
        for k in keyword_list:
            distance = nltk.edit_distance(k, key)
            if distance == 0:
                in_keyword_temp.append(key)

    # 중복 키워드 제거
    for v in in_keyword_temp:
        if v not in in_keyword:
            in_keyword.append(v)

    # 검출되지 않은 키워드
    for key in corporate_keyword_list:
        if key not in in_keyword:
            not_in_keyword.append(key)

    check_keyword = ' '.join(in_keyword_temp)
    doc_term_matrix = count_vec.fit_transform([corporate_keyword_str, check_keyword]).toarray()
    percent = cosine_similarity(doc_term_matrix[0], doc_term_matrix[1])

    return in_keyword, not_in_keyword, percent

corporate_number = input("기업을 입력해주세요 ex) 0은 CJ : ")
in_keyword , not_in_keyword, percent = Keyword_Similarity(int(corporate_number))
print(f'검출된 키워드 :{in_keyword}')
print(f'나타나지 않은 키워드 : {not_in_keyword}')
print(f'키워드 일치율: {percent * 100}%')