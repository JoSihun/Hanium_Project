import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer


# pip install scikit
# 모르는코드 싫어해서 최대한 기존에 했던 자이로디스턴스 비슷하게 했음

def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm
    return similarity


def run():
    user_path = f'..Final\\07_Saramin_dataset\\testset\\test.txt'
    compare_path = f'..Final\\07_Saramin_dataset\\dataset'
    plagiarism_check(user_path, compare_path)


def print_plagiarism_result(highest_file_path, highest_similarity, highest_introduction, user):
    # Result
    print('===========================================================================================================')
    print(f'Most Similar Self-Introduction')
    print(f'Highest File Path: {highest_file_path}')
    print(f'Highest Similarity: {highest_similarity}')
    print(f'User Self-Introduction: \n{user}')
    print(f'Highest Self-Introduction: \n{highest_introduction}')


def plagiarism_check(user_path, compare_path):
    user = open(user_path, 'r', encoding='UTF-8').read()
    highest_similarity = 0
    highest_file_path = ''
    highest_introduction = ''
    for i, file in enumerate(os.listdir(compare_path)):
        compare = open(f'{compare_path}/{file}', 'r', encoding='UTF-8').read()
        doc_list = [user, compare]
        # 코사인 유사도 구하려면 문서(str)을 TF-IDF 백터화된 행렬로 변경해야함
        tfidf_vect_simple = TfidfVectorizer()
        feature_vect_simple = tfidf_vect_simple.fit_transform(doc_list)

        # print(feature_vect_simple.shape) 문서의 갯수(doc_list)와 중복제거된 단어의 갯수 확인가능
        # print(type(feature_vect_simple))  타입 확인가능

        # 희소 행렬을 위에 코사인 유사도 함수의 인자인 arrary로 바꾸기위해 다시 밀집 행렬로 변환하기 위한 과정
        feature_vect_dense = feature_vect_simple.todense()
        # feature vector 추출
        user_vect1 = np.array(feature_vect_dense[0]).reshape(-1, )
        compare_vect2 = np.array(feature_vect_dense[1]).reshape(-1, )

        similarity = cos_similarity(user_vect1, compare_vect2)
        if highest_similarity < similarity:
            highest_similarity = similarity
            highest_file_path = f'{compare_path}/{file}'
            highest_introduction = compare

        print(f'======================================================================================================')
        print(f'Plagiarism Introduction Searching ... ({i + 1}/{len(os.listdir(compare_path))})')
        print(f'Now Checking: {compare_path}/{file}')
        print(f'Now Similarity: {similarity}')
        print(f'Highest File Path: {highest_file_path}')
        print(f'Highest Similarity: {highest_similarity}')
    print_plagiarism_result(highest_file_path, highest_similarity, highest_introduction, user)


run()