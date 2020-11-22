# 최종본
# from hanspell import spell_checker
from .hanspell import spell_checker

# 맞춤법 검사
def grammar_line_check(text):
    origin_list = []
    result_list = []

    lines = text.split('\n')                            # 텍스트를 라인별로 분리, 전체텍스트에서 \n은 모두 삭제됨
    for line in lines:                                  # 각 라인별로
        grammar_result = spell_checker.check(line)      # 맞춤법 검사
        grammar_result = grammar_result.as_dict()       # 맞춤법 검사결과 dict형으로 저장
        original = grammar_result['original']           # 원본 라인단위
        checked = grammar_result['checked']             # 첨삭 라인단위
        origin_list.append(original)                    # 원본 라인별로 리스트 저장
        result_list.append(checked)                     # 첨삭 라인별로 리스트 저장

    return origin_list, result_list

def grammar_word_check(origin_list, result_list):
    wrong_list = []
    correct_list = []
    for origin_line, result_line in zip(origin_list, result_list):  # 원본, 첨삭본 리스트 라인별로 매칭
        if origin_line != result_line:                              # 두 내용이 다르면 = 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')                   # 해당라인 단어단위로 분할
            for word in origin_words:                               # 각 단어별로
                grammar_result = spell_checker.check(word)          # 맞춤법 검사
                grammar_result = grammar_result.as_dict()           # 맞춤법 검사결과 dict형으로 저장
                original = grammar_result['original']               # 원본 단어
                checked = grammar_result['checked']                 # 첨삭 단어
                wrong_list.append(original)                         # 원본 단어 원본 리턴리스트에 추가
                correct_list.append(checked)                        # 첨삭 단어 첨삭 리턴리스트에 추가
        else:                                                       # 두 내용이 같으면 = 첨삭된 내용이 없으면
            wrong_list.append(result_line)                          # 원본 문장 원본 리턴리스트에 추가
            correct_list.append(result_line)                        # 원본 문장 첨삭 리턴리스트에 추가
        wrong_list.append('\n')                             # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 리턴리스트에 추가
        correct_list.append('\n')                           # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 리턴리스트에 추가

    return wrong_list, correct_list

class Grammar_Result:
    def __init__(self):
        self.origin_str = ''
        self.checked_str = ''
        self.origin_list = []
        self.checked_list = []
        self.result_list = []

    def save_result_list(self):
        for origin, checked in zip(self.origin_list, self.checked_list):    # 원본과 첨삭본을 매칭
            if checked.endswith('\n'):
                self.origin_str += origin
                self.checked_str += checked
            else:
                self.origin_str += origin + ' '                                 # 원본 string 형태
                self.checked_str += checked + ' '                               # 첨삭본 string 형태
            self.result_list.append([origin, checked])                      # 어간단위로 매칭하여 저장

        # self.result_list = [[origin, checked] for origin, checked in zip(self.origin_list, self.checked_list)]

def grammar_run(text):
    print(f'맞춤법 검사 시작')
    origin_text = text.replace('\r', '')                                        # Linux 개행문자 \r 인식오류 처리
    origin_list, result_list = grammar_line_check(origin_text)                  # 라인별로 맞춤법 검사
    origin_list, result_list = grammar_word_check(origin_list, result_list)     # 어간별로 맞춤법 검사

    grammar_result = Grammar_Result()               # HTML로 넘기기 위한 결과 객체 생성
    grammar_result.origin_list = origin_list        # 결과 객체에 원본 어간 리스트 저장
    grammar_result.checked_list = result_list       # 결과 객체에 첨삭 어간 리스트 저장
    grammar_result.save_result_list()               # 원본과 첨삭본을 어간단위로 매칭하여 저장
    print(f'맞춤법 검사 종료')
    
    return grammar_result