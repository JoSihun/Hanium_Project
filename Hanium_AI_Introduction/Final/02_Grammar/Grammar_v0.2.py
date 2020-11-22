# 최종본, CMD/파이참 콘솔에서 출력가능
#from hanspell import spell_checker
from .hanspell import spell_checker
#import ctypes
import os, sys
# CMD 콘솔 컬러 코드
FOREGROUND_BLACK = 0x00         # text color contains black.
FOREGROUND_BLUE = 0x01          # text color contains blue.
FOREGROUND_GREEN = 0x02         # text color contains green.
FOREGROUND_RED = 0x04           # text color contains red.
FOREGROUND_INTENSITY = 0x08     # text color is intensified.
BACKGROUND_BLUE = 0x10          # background color contains blue.
BACKGROUND_GREEN = 0x20         # background color contains green.
BACKGROUND_RED = 0x40           # background color contains red.
BACKGROUND_INTENSITY = 0x80     # background color is intensified.

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
#std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
TEST_PATH = '../../../../../Final/07_Saramin_dataset/testset'

# CMD 콘솔 컬러 설정
'''
def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
'''
# 맞춤법 검사
def grammar_check(text):
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

# 원본출력, 틀린 것은 빨간색으로 출력
def print_wrong_text(origin_list, result_list):
    for origin_line, result_line in zip(origin_list, result_list):  # 원본, 첨삭본 리스트 라인별로 매칭
        if origin_line != result_line:                              # 두 내용이 다르면 = 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')                   # 해당라인 단어단위로 분할
            for word in origin_words:                               # 각 단어별로
                grammar_result = spell_checker.check(word)          # 맞춤법 검사
                grammar_result = grammar_result.as_dict()           # 맞춤법 검사결과 dict형으로 저장
                original = grammar_result['original']               # 원본 단어
                checked = grammar_result['checked']                 # 첨삭 단어
                if original != checked:                                         # 원본, 첨삭 단어가 다르면 = 틀린 원본 단어를
                    # print('\033[31m' + f'{original} ' + '\033[0m', end='')    # 틀린 원본 단어를 파이참 콘솔에서 빨간색으로 출력
                    sys.stdout.flush()                                          # 틀린 원본 단어를 CMD 콘솔에서 빨간색으로 출력
                    #set_color(FOREGROUND_RED)
                    print(f'{original} ', end='')
                    sys.stdout.flush()
                    #set_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
                else:                                                           # 맞은 원본 단어는
                    print(f'{original} ', end='')                               # 검은색으로 출력
        else:                                                       # 두 내용이 같으면 = 첨삭된 내용이 없으면
            print(f'{origin_line}', end='')                         # 그냥 출력
        print()                                                     # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 출력

# 첨삭출력, 고친 것은 파란색으로 출력
def print_correct_text(origin_list, result_list):
    for origin_line, result_line in zip(origin_list, result_list):  # 원본, 첨삭본 리스트 라인별로 매칭
        if origin_line != result_line:                              # 두 내용이 다르면 = 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')                   # 해당라인 단어단위로 분할
            for word in origin_words:                               # 각 단어별로
                grammar_result = spell_checker.check(word)          # 맞춤법 검사
                grammar_result = grammar_result.as_dict()           # 맞춤법 검사결과 dict형으로 저장
                original = grammar_result['original']               # 원본 단어
                checked = grammar_result['checked']                 # 첨삭 단어
                if original != checked:                                         # 원본, 첨삭 단어가 다르면 = 고친 첨삭 단어를
                    # print('\033[34m' + f'{checked} ' + '\033[0m', end='')     # 고친 첨삭 단어를 파이참 콘솔에서 파란색으로 출력
                    sys.stdout.flush()                                          # 고친 첨삭 단어를 CMD 콘솔에서 파란색으로 출력
                    #set_color(FOREGROUND_BLUE)
                    print(f'{checked} ', end='')
                    sys.stdout.flush()
                    #set_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
                else:                                                           # 맞은 첨삭 단어는
                    print(f'{checked} ', end='')                                # 검은색으로 출력
        else:                                                       # 두 내용이 같으면 = 첨삭된 내용이 없으면
            print(f'{result_line}', end='')                         # 그냥 출력
        print()                                                     # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 출력

def test_grammar_check(origin_list, result_list):
    wrong_list = []
    correct_list = []
    for origin_line, result_line in zip(origin_list, result_list):  # 원본, 첨삭본 리스트 라인별로 매칭
        if origin_line != result_line:  # 두 내용이 다르면 = 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')  # 해당라인 단어단위로 분할
            for word in origin_words:  # 각 단어별로
                grammar_result = spell_checker.check(word)  # 맞춤법 검사
                grammar_result = grammar_result.as_dict()  # 맞춤법 검사결과 dict형으로 저장
                original = grammar_result['original']  # 원본 단어
                checked = grammar_result['checked']  # 첨삭 단어
                if original != checked:  # 원본, 첨삭 단어가 다르면 = 고친 첨삭 단어를 리턴리스트에 추가(첨삭된 단어)
                    wrong_list.append(original)
                    correct_list.append(checked)
                else:  # 맞은 첨삭 단어는
                    wrong_list.append(original)
                    correct_list.append(checked)  # 그냥 리턴리스트에 추가(옳은 단어)
        else:  # 두 내용이 같으면 = 첨삭된 내용이 없으면
            wrong_list.append(result_line)
            correct_list.append(result_line)  # 그냥 리턴리스트에 추가(옳은 문장)
        wrong_list.append('\n')
        correct_list.append('\n')  # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 리턴리스트에 추가

    return wrong_list, correct_list

class Grammar_Result:
    result_list = []
    origin_list = []
    checked_list = []

    def save_result_list(self):
        self.result_list = [[origin, checked] for origin, checked in zip(self.origin_list, self.checked_list)]

def grammar_run(text):
    #text_file_name = f'{TEST_PATH}/test.txt'
    #print(text_file_name)

    origin_text = text.replace('\r', '')                        # Linux 개행문자 \r 인식오류 처리
    origin_list, result_list = grammar_check(origin_text)
    #print(f'------------------------------------------------- 원본 텍스트 -------------------------------------------------')
    #print_wrong_text(origin_list, result_list)
    #print(f'------------------------------------------------- 첨삭된 텍스트 -------------------------------------------------')
    #print_correct_text(origin_list, result_list)

    grammar_result = Grammar_Result()
    grammar_result.origin_list, grammar_result.checked_list = test_grammar_check(origin_list, result_list)
    grammar_result.save_result_list()

    return grammar_result

    #checked_text = '\n'.join(result_list)
    #return checked_text

'''
if __name__ == '__main__':
    text_file_name = f'{TEST_PATH}/test.txt'
    print(text_file_name)

    origin_text = open(text_file_name, 'r', encoding='UTF-8').read()
    origin_list, result_list = grammar_check(origin_text)
    print(f'------------------------------------------------- 원본 텍스트 -------------------------------------------------')
    print_wrong_text(origin_list, result_list)
    print(f'------------------------------------------------- 첨삭된 텍스트 -------------------------------------------------')
    print_correct_text(origin_list, result_list)
'''
########################################################################################################################
#print('\033[31m' + '1.안녕' + '\033[0m')
#print('\033[34m' + '1.안녕' + '\033[0m')