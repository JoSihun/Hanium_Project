# 원본출력시 맨 앞에 공백이 생기거나, 마침표가 2개찍히는 문제발생함
from hanspell import spell_checker

TEST_PATH = '../07_Saramin_dataset/testset'

def grammar_check(text):
    origin_list = []
    result_list = []

    lines = text.split('\n')
    for line in lines:
        line = line.replace('  ', ' ')
        sentences = line.split('. ')
        for sentence in sentences:
            if len(sentences) > 1:
                sentence = sentence + '.'
            grammar_result = spell_checker.check(sentence)
            grammar_result = grammar_result.as_dict()
            original = grammar_result['original']
            checked = grammar_result['checked']
            origin_list.append(original.strip() + '\n')
            result_list.append(checked.strip() + '\n')


    return origin_list, result_list



# 출력을 깔끔하게 하는 방법 필요
# grammar_check 단계에서 리스트 형태로 단어들을 잘라 넣는 방법 재고할 것
def print_wrong_text(origin_list, result_list):
    for origin_sentence, result_sentence in zip(origin_list, result_list):
        if origin_sentence != result_sentence:

            origin_words = origin_sentence.split(' ')
            for word in origin_words:
                grammar_result = spell_checker.check(word)
                grammar_result = grammar_result.as_dict()
                original = grammar_result['original']
                checked = grammar_result['checked']
                if original != checked:
                    print('\033[31m' + f'{original} ' + '\033[0m', end='')
                else:
                    print(f'{original} ', end='')
        else:
            print(f'{origin_sentence}', end='')


# 출력을 깔끔하게 하는 방법 필요
def print_correct_text(origin_list, result_list):
    for origin_sentence, result_sentence in zip(origin_list, result_list):
        if origin_sentence != result_sentence:
            origin_words = origin_sentence.split(' ')
            for word in origin_words:
                grammar_result = spell_checker.check(word)
                grammar_result = grammar_result.as_dict()
                original = grammar_result['original']
                checked = grammar_result['checked']
                if original != checked:
                    print('\033[34m' + f'{checked} ' + '\033[0m', end='')
                else:
                    print(f'{checked} ', end='')
        else:
            print(f'{result_sentence}', end='')


if __name__ == '__main__':
    text_file_name = f'{TEST_PATH}/test.txt'

    origin_text = open(text_file_name, 'r', encoding='UTF-8').read()
    origin_list, result_list = grammar_check(origin_text)
    print_wrong_text(origin_list, result_list)
    print(f'==================================================================================')
    print_correct_text(origin_list, result_list)



########################################################################################################################
#print('\033[31m' + '1.안녕' + '\033[0m')
#print('\033[34m' + '1.안녕' + '\033[0m')
