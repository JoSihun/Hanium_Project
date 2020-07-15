# 참고 : https://excelsior-cjh.tistory.com/93
# 참고 : https://korbillgates.tistory.com/171
from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.twitter = Twitter()
        self.stopwords = ['이기','대해','때문','여러','위해','대한','통해','로서','전반','한번','관련','또한','통한','우선','이후',
                          '그것','동안']   # 나오면 안되는 단어들 적어줘야함
    def url2sentences(self, url):
        article = Article(url, language='ko')
        article.download()
        article.parse()
        sentences = self.kkma.sentences(article.text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
            return sentences

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
                nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence))
                                if noun not in self.stopwords and len(noun) > 1])) # 키워드로 추출할 글자개수 정해줄수있음(현재 2개이상)
        return nouns


class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []

    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return self.graph_sentence

    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # diagonal 부분을 0으로
            link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}

class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()
        if text[:5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    def summarize(self, sent_num=3):
        summary = []
        index=[]
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        index.sort()
        for idx in index:
            summary.append(self.sentences[idx])
        return summary

    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        keywords = []
        index=[]
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
        #index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        return keywords

####################################################################################################################################
corpor_field_dict = {}
corporate_dict = {}
field_dict = {}

Path = '../../Final/07_Saramin_dataset/dataset'
for i in range(6586):   # 총 자소서 6586개
    f = open(f'{Path}/{i}.txt', 'r', encoding='utf-8')
    intro_data_list = f.readlines()
    intro_data_str = intro_data_list[2:]    # 기업명과 부서제외
    intro_data_str = '\n'.join(intro_data_str)

    corporate_name = intro_data_list[0].replace('㈜','').replace('(주)','')   # 특정문자 제거
    corporate_name = corporate_name[:len(corporate_name)-1]                  # \n제거
    field_name = intro_data_list[1][:len(intro_data_list[1])-1]              # \n제거

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

    print(f"{i}.txt파일 탐색중")
    textrank = TextRank(intro_data_str)     # 매개변수로 url주소와 텍스트를 넣을수가 있음
    #for row in textrank.summarize(6):   # 몇줄로 요약 할것인지 지정할수 있음(현재 6줄)
    #    print(row)
    #    print()
    #print('keywords :',textrank.keywords(10))   # 키워드 개수를 지정할수 있음(현재 10개)
    #print('=======================================================================================================================================')
"""
print(f"기업 : {corporate_dict}")
print(f"총 기업개수 : {len(corporate_dict)}")
print(f"분야 : {field_dict}")
print(f"총 분야개수 : {len(field_dict)}")
print(f"기업별 분야 : {corpor_field_dict}")
"""
