# 참고 : https://excelsior-cjh.tistory.com/93
# 참고 : https://korbillgates.tistory.com/171
# 참고 : https://m.blog.naver.com/myincizor/221643594756 //코사인 유사도
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk
import math
from deepsquareapp.models import Corporate_Keyword

from konlpy.tag import Mecab
import konlpy
mecab = Mecab()

STOPWORDS_PATH = '../../07_Saramin_dataset/testset/stop_words.txt'
def eliminate_stopwords(orig_text, stop_text):
    word_tokens = mecab.morphs(orig_text)  # 형태소 추출
    stop_words = stop_text.split()

    result = []
    for w in word_tokens:
        if w not in stop_words:
            if len(w) > 1:  # 1개 이하의 단어도 추가로 제거
                result.append(w)

    return result


class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.okt = Okt()
        self.stopwords = '하'
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
                                if noun not in self.stopwords and len(noun) > 1]))      # 키워드로 추출할 글자개수 정해줄수있음(현재 2개이상)
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

"""
def keyword_load(x):
    return {'CJ' : ['정직','도전','근성','열정','창의'],
            'DB' : ['창의','도전','전문','신뢰','화합','글로벌 역량'],
            'KCC' : ['지식','도전','의지','창의','용기','정직','사명감','책임감','성실','협동',],
            'KT' : ['도전','존중','소통','기본','원칙'],
            'LG' : ['열정','도전','창의','혁신','고객','경쟁'],
            'LS' : ['긍정','기본','윤리','창의','변화','혁신','전문','열정','노력'],
            'SK' : ['패기','자발','의욕','실행','역량','팀워크'],
            '넥슨' : ['열정','패기','도전','유연','창의','용기','경험'],
            '넷마블' : ['열정','책임','일류','도전','자신감','혁신','변화'],
            '농협' : ['협력','행복','전문','정직','신뢰','도전','창의','열정'],
            '대우건설' : ['도전','열정','자율','책임','신념'],
            '동원' : ['책임감','노력','리드','소통','몰입','협력','공감'],
            '두산' : ['존중','배려','팀워크','열정','소통','근성','실천'],
            '롯데' : ['패기','투지','도전','노력','협력','양보'],
            '미래에셋' : ['고객','전문','지혜','정직','신뢰','용기','실천'],
            '삼성전자' : ['정직','신뢰','용기','동료애','배려','존중','책임감','열정','창의','상상력','겸손'],
            '셀트리온' : ['창의','책임','도전','용기','열정'],
            '신세계' : ['고객','헌신','창의','도전','열정'],
            '아모레퍼시픽' : ['고객','공감','몰입','전문성','창의'],
            '애경' : ['도전','혁신','감사','소통','신뢰','정도'],
            '카카오' : ['전문','열정','도전','자기주도','신뢰','헌신'],
            '태영건설' : ['신뢰','존중','지성','열정','도전','창조'],
            '포스코' : ['실천','겸손','존중','배려','창의'],
            '한국타이어' : ['열정','혁신','협동','도전','리더'],
            '한진' : ['창의','신념','성의','실천','책임','봉사'],
            '한화' : ['도전','창의','자신감','헌신','정도'],
            '현대백화점' : ['전문','창의','도전','도덕','책임','실행'],
            '현대산업개발' : ['창의','혁신','정직','원칙','실행','열정','소통','협력'],
            '현대자동차' : ['도전','창의','열정','책임감','협력','소통','존중'],
            '효성' : ['최고','전문','혁신','긍정','책임','열정','신뢰']
            }[x]
"""

# 공통
def keyword_load_etc():
    return ['자신감','열정','리더쉽','창의']


def Keyword_Similarity(corporate_name, str):
    stopwords_text = konlpy.utils.read_txt(STOPWORDS_PATH, encoding='UTF-8')

    check_value = False
    corporate_list = ['CJ','DB','KCC','KT','LG','LS','SK','넥슨','넷마블','농협','대우건설','동원','두산','롯데','미래에셋','삼성전자','셀트리온',
                      '신세계','아모레퍼시픽','애경','카카오','태영건설','포스코','한국타이어','한진','한화','현대백화점','현대산업개발','현대자동차','효성']

    print(f"{corporate_name}에 해당하는 기업에 대한 키워드와 비교합니다.")

    for c in corporate_list:
        if c == corporate_name:
            check_value = True

    if check_value:
        #corporate_keyword_list = keyword_load(corporate_name)
        # 데이터베이스에 존재하는 해당기업의 키워드를 가져와서 리스트로 구성
        corporate_keyword_list = []
        corporate_keyword_db = Corporate_Keyword.objects.all()
        for keyword_db in corporate_keyword_db:
            # 선택한 기업과 기업키워드 테이블의 기업명과 일치하면
            if keyword_db.corporate_name.corporate_name == corporate_name:
                # 해당 기업에 등록된 모든 키워드 리스트로 저장
                corporate_keyword_list.append(keyword_db.corporate_keyword)
        #print(f'{corporate_name} 키워드 : {corporate_keyword_list}')

    else:
        corporate_keyword_list = keyword_load_etc()

    corporate_keyword_str = ' '.join(corporate_keyword_list)

    #textrank = TextRank(str)
    #nouns_list = textrank.nouns

    # Mecab으로 전처리
    nouns_list = eliminate_stopwords(str, stopwords_text)
    keyword_list = []
    print("전처리 완료")
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


    if math.isnan(percent):
        percent = 0


    return in_keyword, not_in_keyword, percent * 100


