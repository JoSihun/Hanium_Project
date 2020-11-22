from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
def cosine_similarity(v1, v2):
    prod = np.dot(v1, v2)
    len1 = np.sqrt(np.dot(v1, v1))
    len2 = np.sqrt(np.dot(v2, v2))
    print(prod)
    print(len1)
    print(len2)
    return prod / (len1 * len2)

doc1 = '사랑 사과 바나나 친구'
doc2 = '사랑 사과'

count_vec = CountVectorizer()
doc_term_matrix = count_vec.fit_transform([doc1, doc2]).toarray()


print(doc_term_matrix)
#print(count_vec.vocabulary_)
print(cosine_similarity(doc_term_matrix[1], doc_term_matrix[0]))


test = ['CJ','DB','KCC','KT','LG','LS','SK','넷마블','넥슨','농협','동원','대우건설','두산','롯데','미래에셋','삼성전자','셀트리온','신세계','아모레퍼시픽',
'애경','카카오','포스코','한국타이어앤 테크놀로지','태영건설', '한진','한화','현대백화점','현대산업개발','현대자동차','효성']

test.sort()
print(test)
print(len(test))