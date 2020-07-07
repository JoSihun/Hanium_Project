# 깔끔하게 출력되나 틀린부분이 단어단위가 아니라 문장단위로 출력됨
from hanspell import spell_checker

TEST_PATH = '../07_Saramin_dataset/testset'

def grammar_check(text):
    result_text = ''
    lines = text.split('\n')
    for line in lines:
        grammar_result = spell_checker.check(line)
        grammar_result = grammar_result.as_dict()
        original = grammar_result['original']
        checked = grammar_result['checked'] + '\n'
        result_text += checked
    return result_text

# 출력을 깔끔하게 하는 방법 필요
# grammar_check 단계에서 리스트 형태로 단어들을 잘라 넣는 방법 재고할 것
def print_wrong_text(origin_text, result_text):
    origin_lines = origin_text.split('\n')
    result_lines = result_text.split('\n')
    for origin_line, result_line in zip(origin_lines, result_lines):        # 라인별로 추출
        origin_words = origin_line.split()
        result_words = result_line.split()
        for origin_word, result_word in zip(origin_words, result_words):    # 단어별로 추출
            if origin_word != result_word:
                print('\033[31m' + f'{origin_word} ' + '\033[0m', end='')
            else:
                print(f'{origin_word} ', end='')
        print()

# 출력을 깔끔하게 하는 방법 필요
def print_correct_text(origin_text, result_text):
    origin_lines = origin_text.split('\n')
    result_lines = result_text.split('\n')
    for origin_line, result_line in zip(origin_lines, result_lines):
        origin_words = origin_line.split()
        result_words = result_line.split()
        for origin_word, result_word in zip(origin_words, result_words):
            if origin_word != result_word:
                print('\033[34m' + f'{result_word} ' + '\033[0m', end='')
            else:
                print(f'{result_word} ', end='')
        print()


if __name__ == '__main__':
    text_file_name = f'{TEST_PATH}/test.txt'

    origin_text = open(text_file_name, 'r', encoding='UTF-8').read()
    result_text = grammar_check(origin_text)

    print_wrong_text(origin_text, result_text)
    print_correct_text(origin_text, result_text)


########################################################################################################################
#print('\033[31m' + '1.안녕' + '\033[0m')
#print('\033[34m' + '1.안녕' + '\033[0m')
