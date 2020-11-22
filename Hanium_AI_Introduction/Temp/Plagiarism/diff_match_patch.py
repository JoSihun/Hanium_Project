import os
from diff_match_patch import diff_match_patch

def compute_similarity_and_diff(text1, text2):
    dmp = diff_match_patch()
    dmp.Diff_Timeout = 0.0
    diff = dmp.diff_main(text1, text2, False)

    # similarity
    common_text = sum([len(txt) for op, txt in diff if op == 0])
    text_length = max(len(text1), len(text2))
    sim = common_text / text_length

    return sim

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
        similarity =compute_similarity_and_diff(user, compare)
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