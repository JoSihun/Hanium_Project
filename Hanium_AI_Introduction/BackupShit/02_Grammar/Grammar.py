from hanspell import spell_checker

def grammar_check(user_answer_path):
    origin_text = open(user_answer_path, 'r', encoding='UTF-8').read()
    lines = open(user_answer_path, 'r', encoding='UTF-8').readlines()

    # read '.txt' file, makes it in one line
    checked_text = ''
    for line in lines:
        grammar_result = spell_checker.check(line)
        grammar_result = grammar_result.as_dict()
        original = grammar_result['original']
        checked = grammar_result['checked']
        checked_text += checked + '\n'

    checked_text = checked_text.strip()
    print('===========================================================================================================')
    print(f'Original_Text:\n{origin_text}')
    print('===========================================================================================================')
    print(f'Result_Text:\n{checked_text}')

    find_wrong_spelling(origin_text, checked_text)
########################################################################################################################
def find_wrong_spelling(origin_text, checked_text):
    origin_lines = origin_text.replace(']', '].').split('.')
    origin_lines.remove('')
    wrong_result = []
    total_wrong_cnt = 0

    for line in origin_lines:
        line = line.strip()
        if not line[-1] == ']':
            line += '.'

        grammar_result = spell_checker.check(line)
        grammar_result = grammar_result.as_dict()
        original = grammar_result['original']
        checked = grammar_result['checked']
        wrong_cnt = grammar_result['errors']

        if wrong_cnt != 0:
            total_wrong_cnt += wrong_cnt
            wrong_result.append([original, checked, wrong_cnt])

    print('===========================================================================================================')
    print('===========================================================================================================')
    if not wrong_result:
        print(f'대단합니다! 틀린 곳이 없습니다!')
    else:
        print(f'맞춤법 검사결과 틀린 부분입니다.')
        print(f'틀린 부분은 총 {total_wrong_cnt}군데 입니다.\n')
        for origin_text, checked_text, error_cnt in wrong_result:
            print(f'[다음 문장에서 틀린 부분은 {error_cnt}군데 입니다.]')
            print(f'사용자가 작성한 문장:\n{origin_text}')
            print(f'DeepFlow가 첨삭한 문장:\n{checked_text}\n')
########################################################################################################################
def run():
    # 백엔드 연결후 user_path 사용자 자소서 경로로 변경할 것
    user_path = f'../07_Saramin_dataset/user/answer/test.txt'
    grammar_check(user_path)
run()