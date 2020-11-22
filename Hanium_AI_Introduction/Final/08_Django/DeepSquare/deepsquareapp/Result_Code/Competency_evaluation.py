from deepsquareapp.models import Competency
from konlpy.tag import Mecab
import konlpy
mecab = Mecab()

STOPWORDS_PATH = '../../07_Saramin_dataset/testset/stop_words.txt'
COMPETENCY_NUMBER = 147


def eliminate_stopwords(orig_text, stop_text):
    word_tokens = mecab.morphs(orig_text)  # 형태소 추출
    stop_words = stop_text.split()

    result = []
    for w in word_tokens:
        if w not in stop_words:
            if len(w) > 1:  # 1개 이하의 단어도 추가로 제거
                result.append(w)

    return result

"""
def text_nouns(text):
    nouns = [] # 명사 추출

    if text is not '':
        nouns.append(' '.join([noun for noun in mecab.nouns(str(text))
                              if len(noun) > 1]))
    result = ''.join(nouns).split()
    return result
"""

# 매개변수는 자기소개서
def evaluation_run(intro):

    # intro의 명사 추출
    stopwords_text = konlpy.utils.read_txt(STOPWORDS_PATH, encoding='UTF-8')
    inst_nouns = eliminate_stopwords(intro, stopwords_text)
    #inst_nouns = text_nouns(test_inst)


    competency_name_list = []
    competency_define_list = []
    competency_dict = {}

    # 역량 테이블 조회
    db_list = Competency.objects.all()
    for db in db_list:
        #competency_noun = text_nouns(db.competency_define)
        # 역량정의 명사 추출
        competency_noun = eliminate_stopwords(db.competency_define, stopwords_text)
        #print(competency_noun)

        # 역량이름 \n문자 제거
        competency_name = str(db.competency_name).replace("\n", "")

        # {역량 이름 : 명사로 추출된 역량정의} 딕셔너리
        competency_dict[competency_name] = competency_noun
        
        # 역량 이름 리스트
        competency_name_list.append(competency_name)
    for i in range(len(competency_name_list)):
        print(f"{competency_name_list[i]} : {competency_dict[competency_name_list[i]]}")
    print(competency_dict)
    #print(competency_dict[competency_name_list[0]])


    result_dict = {}
    # 147번 반복(역량개수 147개)
    for i in range(COMPETENCY_NUMBER):
        count = 0
        
        # 역량명사, 자소서명사 일치 비교
        for key in competency_dict[competency_name_list[i]]:
            for noun in inst_nouns:
                if key == noun:
                    count += 1
                    print(f"{competency_name_list[i]}의 '{key}'와 자소서의 '{noun}'가 일치함")
        print(f"{competency_name_list[i]}의 count : {count}")
        
        # {역량이름 : 일치수} 딕셔너리
        result_dict[competency_name_list[i]] = count

    # 딕셔너리 key기준 내림차순 정렬
    result = sorted(result_dict.items(), reverse=True, key=lambda item:item[1])
    print("=================================================================================================================")
    #print(result)
    for r in result:
        print(r)
    print("=================================================================================================================")
    print(f"사용자 자기소개서 역량Top10")  # TOP10 출력
    for i in range(10):
        print(f"{i+1}. {result[i][0]}")  # TOP10 출력

    return result


