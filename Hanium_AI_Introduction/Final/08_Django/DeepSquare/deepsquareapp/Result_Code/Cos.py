import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def cos_similarity(v1, v2):                                                    #코사인 유사도 함수
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm
    return similarity


def plagiarism_check(user_intro, db_intro_list):
    highest_similarity = 0
    highest_file_path = ''
    highest_introduction = ''
    for intro in db_intro_list:
        compare = intro
        doc_list = [user_intro, compare]

        tfidf_vect_simple = TfidfVectorizer()                               # 코사인 유사도 사용을 위한 문서 TF-IDF 백터화
        feature_vect_simple = tfidf_vect_simple.fit_transform(doc_list)     # 중복 단어 제거
        feature_vect_dense = feature_vect_simple.todense()                  # 희소 행렬을 코사인 함수 인자로 사용하기 위한 밀집행렬화

        user_vect1 = np.array(feature_vect_dense[0]).reshape(-1, )          # feature vector 추출
        compare_vect2 = np.array(feature_vect_dense[1]).reshape(-1, )

        similarity = cos_similarity(user_vect1, compare_vect2)              # 합격자소서와 사용자의 자소서를
        if highest_similarity < similarity:                                 # 순차적으로 비교
            highest_similarity = similarity
            #highest_file_path = f'{compare_path}/{file}'
            highest_introduction = compare


    return highest_similarity * 100                                         # 표절율 출력
