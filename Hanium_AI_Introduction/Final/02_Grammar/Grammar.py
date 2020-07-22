# 최종본, cmd 콘솔에서 출력가능
from hanspell import spell_checker
import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x00
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_INTENSITY = 0x08  # text color is intensified.
BACKGROUND_BLUE = 0x10  # background color contains blue.
BACKGROUND_GREEN = 0x20  # background color contains green.
BACKGROUND_RED = 0x40  # background color contains red.
BACKGROUND_INTENSITY = 0x80  # background color is intensified.

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
TEST_PATH = '../07_Saramin_dataset/testset'

def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

def grammar_check(text):
    origin_list = []
    result_list = []

    lines = text.split('\n')                            # 텍스트를 라인별로 분리, 전체텍스트에서 \n은 모두 삭제됨
    for line in lines:
        grammar_result = spell_checker.check(line)
        grammar_result = grammar_result.as_dict()
        original = grammar_result['original']
        checked = grammar_result['checked']
        origin_list.append(original)
        result_list.append(checked)

    return origin_list, result_list

# 원본출력, 틀린 것은 빨간색으로 출력
def print_wrong_text(origin_list, result_list):
    for origin_line, result_line in zip(origin_list, result_list):
        if origin_line != result_line:                              # 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')                   # 해당라인 단어단위로 분할
            for word in origin_words:                               # 각 단어별로 맞춤법 검사
                grammar_result = spell_checker.check(word)
                grammar_result = grammar_result.as_dict()
                original = grammar_result['original']               # 원본 단어
                checked = grammar_result['checked']                 # 첨삭된 단어
                if original != checked:                                         # 틀린 원본 단어를
                    # print('\033[31m' + f'{original} ' + '\033[0m', end='')      # 빨간색으로 출력 / 파이참 콘솔에서
                    sys.stdout.flush()                                          # cmd 콘솔에서
                    set_color(FOREGROUND_RED)
                    print(f'{original} ', end='')
                    sys.stdout.flush()
                    set_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
                else:                                                           # 맞은 원본 단어는
                    print(f'{original} ', end='')                               # 검은색으로 출력
        else:                                                       # 첨삭된 내용이 없으면
            print(f'{origin_line}', end='')                         # 그냥 출력
        print()                                                     # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 출력

# 첨삭출력, 고친 것은 파란색으로 출력
def print_correct_text(origin_list, result_list):
    for origin_line, result_line in zip(origin_list, result_list):
        if origin_line != result_line:                              # 첨삭된 내용이 있으면
            origin_words = origin_line.split(' ')                   # 해당라인 단어단위로 분할
            for word in origin_words:                               # 각 단어별로 맞춤법 검사
                grammar_result = spell_checker.check(word)
                grammar_result = grammar_result.as_dict()
                original = grammar_result['original']               # 원본 단어
                checked = grammar_result['checked']                 # 첨삭된 단어
                if original != checked:                                         # 고친 첨삭 단어를
                    # print('\033[34m' + f'{checked} ' + '\033[0m', end='')       # 파란색으로 출력 / 파이참 콘솔에서
                    sys.stdout.flush()                                          # cmd 콘솔에서
                    set_color(FOREGROUND_BLUE)
                    print(f'{checked} ', end='')
                    sys.stdout.flush()
                    set_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
                else:                                                           # 맞은 첨삭 단어는
                    print(f'{checked} ', end='')                                # 검은색으로 출력
        else:                                                       # 첨삭된 내용이 없으면
            print(f'{result_line}', end='')                         # 그냥 출력
        print()                                                     # \n이 모두 삭제되었기 때문에 별도로 라인마다 줄바꿈 출력

if __name__ == '__main__':
    text_file_name = f'{TEST_PATH}/test.txt'

    origin_text = open(text_file_name, 'r', encoding='UTF-8').read()
    origin_list, result_list = grammar_
    check(origin_text)
    print(f'------------------------------------------------- 원본 텍스트 -------------------------------------------------')
    print_wrong_text(origin_list, result_list)
    print(f'------------------------------------------------- 첨삭된 텍스트 -------------------------------------------------')
    print_correct_text(origin_list, result_list)