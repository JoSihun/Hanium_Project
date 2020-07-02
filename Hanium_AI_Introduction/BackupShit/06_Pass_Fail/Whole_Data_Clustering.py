import os, shutil

def createFolder(directory):
    print(f'==========================================================================================================')
    print(f'Creating New Folder... {directory}')

    directory = directory.split('/')
    mkdir_path = ''
    for direct in directory:
        mkdir_path += direct
        if not os.path.exists(mkdir_path):
            print(f'Not Exist! Making Directory Path {mkdir_path}')
            os.mkdir(mkdir_path)
        else:
            print(f'Already Exist! {mkdir_path}')
        mkdir_path += '/'
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
from konlpy.tag import Okt
okt = Okt()

# 문장의 토큰화
def tokenizer(text):
    print(f'==========================================================================================================')
    print(f'Tokenizing Text...')
    print(f'Text: \n{text}\n')
    text = regular_expression(text)                         # 정규 표현식, 특수문자 제거
    tokens = okt.pos(text, norm=True, stem=True, join=True) # norm=정규화, stem=어간추출, join=형태소/품사형태
    print(f'Tokens: \n{tokens}\n')
    print(f'Tokenizing Complete!')

    return tokens
########################################################################################################################
import numpy as np

# 문장의 Word2Vec 벡터화
def sentence_vectorizer(sentence, model, size):  # sentence: 문장, model: 단어사전, size: 벡터의 차원
    print(f'Vectorizing One Sentence...')
    print(f'Sentence: {sentence}')
    sentence_vector = np.zeros((size), dtype=np.float32)  # 출력 벡터 초기화
    index2word_set = set(model.wv.index2word)  # 어휘 사전

    num_words = 0
    for word in sentence:  # 문장의 각 단어에 대해
        if word in index2word_set:  # 단어가 사전에 있으면
            sentence_vector = np.add(sentence_vector, model[word])  # 사전에 있는 단어의 벡터값을 더함
            num_words += 1  # 단어 개수 증가

    # 문장의 단어 수만큼 나누어 단어 벡터의 평균값을 문장 벡터로
    sentence_vector = np.divide(sentence_vector, num_words)
    return sentence_vector
########################################################################################################################
# 여러 문장의 Word2Vec 벡터화
def embedding_dataset(sentences, model, size):  # sentences: 문장 모음, model: 단어사전, size: 벡터의 차원
    print(f'Vectorizing Whole Sentences...')
    dataset = []
    for sentence in sentences:  # 문장모음 중 하나의 문장에 대하여
        dataset.append(sentence_vectorizer(sentence, model, size))  # 해당 문장의 벡터값을 더함

    result = np.stack(dataset)
    return result
########################################################################################################################
from gensim.models.word2vec import Word2Vec

# 폴더로 부터 모든 '.txt'읽어 임베딩하기
def embedding_folder(path):
    sentences = []
    for i, file in enumerate(os.listdir(path)):
        print(f'======================================================================================================')
        print(f'Embedding Folder...')
        print(f'Path: {path}')
        print(f'Now: {i+1}/{len(os.listdir(path))}')
        text = open(f'{path}/{file}', 'r', encoding='UTF-8').read()
        tokens = tokenizer(text)
        sentences.append(tokens)

    words_vector = Word2Vec(sentences, size=100, window=3, sg=1)
    dataset = embedding_dataset(sentences, words_vector, 100)

    return dataset, words_vector
########################################################################################################################
# 라벨별로 질문 새로운 폴더에 분류하기
def Categorize_question(origin_path, copy_path, words_vector, kmeans):
    for i, file in enumerate(os.listdir(origin_path)):
        print(f'======================================================================================================')
        print(f'Clustering Questions...')
        print(f'Path: {origin_path}/{file}')
        print(f'Now: {i + 1}/{len(os.listdir(origin_path))}')

        # 텍스트 전처리(토큰화, 문장벡터화)
        classify_sentence = []
        text = open(f'{origin_path}/{file}', 'r', encoding='UTF-8').read()
        tokens = tokenizer(text)
        classify_sentence.append(tokens)
        classify_data = embedding_dataset(classify_sentence, words_vector, 100)

        # 해당문장의 라벨 확인 및 분류
        classify_label = kmeans.predict(classify_data)[0]
        classify_path = f'{copy_path}/Category[{classify_label}]'
        createFolder(classify_path)
        shutil.copy(f'{origin_path}/{file}', f'{classify_path}/{file}')

        print(f'Result: {origin_path}/{file}')
        print(f'    Is Clustered As Category[{kmeans.predict(classify_data)}]')
        print(f'    Is Copied To {classify_path}/{file}')

    print(f'Clustering Questions Done!')

# 라벨별로 답변 새로운 폴더에 분류하기
def Categorize_answer(origin_path, question_path, answer_path):
    for folder in os.listdir(question_path):
        for i, file in enumerate(os.listdir(f'{question_path}/{folder}')):
            file_cnt = len(os.listdir(f'{question_path}/{folder}'))
            print(f'==================================================================================================')
            print(f'Clustering Answers...')
            print(f'Compare Path: {question_path}/{folder}/{file}')
            print(f'Now: {i + 1}/{file_cnt}')

            createFolder(f'{answer_path}/{folder}')
            shutil.copy(f'{origin_path}/{file}', f'{answer_path}/{folder}/{file}')

            print(f'Result: {origin_path}/{file}')
            print(f'    Is Clustered As {folder}')
            print(f'    Is Copied To {answer_path}/{folder}/{file}')

    print(f'Clustering Answers Done!')
########################################################################################################################
import pickle

# 데이터 쓰기
def save_data(data, file_name):
    file = open(f'{file_name}', 'wb')
    pickle.dump(data, file)

# 데이터 읽기
def read_data(file_name):
    file = open(f'{file_name}', 'rb')
    data = pickle.load(file)
    return data
########################################################################################################################
from sklearn.cluster import KMeans

def Clustering():
    origin_path1 = f'../07_Saramin_dataset/whole/question'
    origin_path2 = f'../07_Saramin_dataset/whole/answer'

    copy_path1 = f'../07_Saramin_dataset/Clustered/question'
    copy_path2 = f'../07_Saramin_dataset/Clustered/answer'

    x, words_vector = embedding_folder(origin_path1)
    kmeans = KMeans(n_clusters=24)
    kmeans.fit(x)

    Categorize_question(origin_path1, copy_path1, words_vector, kmeans)
    Categorize_answer(origin_path2, copy_path1, copy_path2)

    save_data(words_vector, 'words_vector.pickle')
    save_data(kmeans, 'kmeans.pickle')
########################################################################################################################
def user_Clustering():
    # 백엔드 연결후 usesr_question_path 수정할 것
    user_question_path = f'../07_Saramin_dataset/user/question/test_question.txt'
    user_answer_path = f'../07_Saramin_dataset/user/answer/test_answer.txt'
    user_question = open(user_question_path, 'r', encoding='UTF-8').read()
    user_answer = open(user_answer_path, 'r', encoding='UTF-8').read()

    words_vector = read_data('words_vector.pickle')
    kmeans = read_data('kmeans.pickle')

    # 텍스트 전처리(토큰화, 문장벡터화)
    classify_sentence = []
    tokens = tokenizer(user_question)
    classify_sentence.append(tokens)
    classify_data = embedding_dataset(classify_sentence, words_vector, 100)

    # 해당문장의 라벨 확인 및 분류
    classified_label = kmeans.predict(classify_data)[0]
    classified_label = f'Category[{classified_label}]'

    print(f'==========================================================================================================')
    print(f'User Data:')
    print(f'{user_question}')
    print(f'\n{user_answer}')
    print(f'==========================================================================================================')
    print(f'해당 문항은 {classified_label}로 분류되었습니다.')
########################################################################################################################
import warnings
warnings.filterwarnings(action='ignore')
# 향후 버전 상향으로 인한 경고 무시

def run():
    # 백엔드 연결후 함수 user_Clustering 내부 변수 usesr_question_path 수정할 것
    Clustering()
    user_Clustering()

user_Clustering()