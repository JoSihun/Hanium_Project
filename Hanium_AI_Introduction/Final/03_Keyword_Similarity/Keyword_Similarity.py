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
        #self.stopwords = ['이기','대해','때문','여러','위해','대한','통해','로서','전반','한번','관련','또한','통한','우선','이후',
        #                  '그것','동안','시오','다른','거기']   # 불용어
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

def classification(Path, repeat=6586):
    corpor_field_dict = {}
    corporate_dict = {}
    field_dict = {}

    for i in range(repeat):
        f = open(f'{Path}/{i}.txt', 'r', encoding='utf-8')
        intro_data_list = f.readlines()

        corporate_name = intro_data_list[0].replace('㈜', '').replace('(주)', '')  # 특정문자 제거
        corporate_name = corporate_name[:len(corporate_name) - 1]  # \n제거
        field_name = intro_data_list[1][:len(intro_data_list[1]) - 1]  # \n제거

        # 기업 분류 and 기업&분야 분류
        if corporate_name in corporate_dict:
            corporate_dict[corporate_name] += 1
            if field_name not in corpor_field_dict[corporate_name]:
                corpor_field_dict[corporate_name].append(field_name)
        else:
            corporate_dict[corporate_name] = 1
            corpor_field_dict[corporate_name] = [field_name]

        # 분야 분류
        if field_name in field_dict:
            field_dict[field_name] += 1
        else:
            field_dict[field_name] = 1
    return corpor_field_dict, corporate_dict, field_dict

def cosine_similarity(v1, v2):
    prod = np.dot(v1, v2)
    len1 = np.sqrt(np.dot(v1, v1))
    len2 = np.sqrt(np.dot(v2, v2))
    return prod / (len1 * len2)

####################################################################################################################################
Path = '../../Final/07_Saramin_dataset/dataset'
Repeat = 6592
#corpor_field_dict, corporate_dict, field_dict = classification(Path, Repeat)
corporate_keyword_list = ['정직','신뢰','용기','동료애','배려','존중','책임감','열정','창의','상상력','겸손']
corporate_keyword_str = ' '.join(corporate_keyword_list)
Step = 0
for i in range(Repeat):   # 총 자소서 6592개
    f = open(f'{Path}/{i}.txt', 'r', encoding='utf-8')
    intro_data_list = f.readlines()
    intro_data_str = intro_data_list[2:]    # 기업명과 부서제외
    intro_data_str = '\n'.join(intro_data_str)

    print(f"{i}.txt파일 탐색중...")

    textrank = TextRank(intro_data_str)
    nouns_list = textrank.nouns
    keyword_str = ' '.join(nouns_list)
    keyword_list = []
    same_keyword_temp = []
    same_keyword = []
    not_keyword = []

    count_vec = CountVectorizer()
    #print(doc_term_matrix)

    # 명사 리스트로 추출
    for noun in nouns_list:
        keyword_list.extend(noun.split())
    #print(keyword_list)

    # 일치 키워드 추출
    for key in corporate_keyword_list:
        for k in keyword_list:
            distance = nltk.edit_distance(k, key)
            if len(key) == 2:
                if distance == 0:
                    same_keyword_temp.append(key)
            else:
                if distance == 0:
                    same_keyword_temp.append(key)

    # 중복 키워드 제거
    for v in same_keyword_temp:
        if v not in same_keyword:
            same_keyword.append(v)

    # 검출되지 않은 키워드
    for key in corporate_keyword_list:
        if key not in same_keyword:
            not_keyword.append(key)

    check_keyword = ' '.join(same_keyword_temp)
    doc_term_matrix_temp = count_vec.fit_transform([corporate_keyword_str, check_keyword]).toarray()
    persent_temp = cosine_similarity(doc_term_matrix_temp[0], doc_term_matrix_temp[1])
    doc_term_matrix = count_vec.fit_transform([keyword_str, corporate_keyword_str]).toarray()  # 희소행렬을 넘파이 배열로 변경
    persent = cosine_similarity(doc_term_matrix[0], doc_term_matrix[1])  # 코사인 유사도 측정(퍼센트)

    print(f'{i}.txt 검출된 키워드 :{same_keyword}')
    print(f'{i}.txt 나타나지 않은 키워드 : {not_keyword}')
    #print(f'{i}.txt 전체문장 키워드 일치율 : {persent * 100}%')
    print(f'{i}.txt 키워드 일치율: {persent_temp * 100}%')
    print("==========================================================================================================================")

