import os
import jellyfish
# need to 'pip install jellyfish'

def plagiarism_check(user_path, compare_path):
    # Read User Self-Introduction txt
    user = open(user_path, 'r', encoding='UTF-8').read()

    # Plagiarism Check
    highest_similarity = 0
    highest_file_path = ''
    highest_introduction = ''

    for i, file in enumerate(os.listdir(compare_path)):
        compare = open(f'{compare_path}/{file}', 'r', encoding='UTF-8').read()
        similarity = jellyfish.jaro_distance(user, compare)
        if highest_similarity < similarity:
            highest_similarity = similarity
            highest_file_path = f'{compare_path}/{file}'
            highest_introduction = compare

        print(f'======================================================================================================')
        print(f'Plagiarism Introduction Searching ... ({i+1}/{len(os.listdir(compare_path))})')
        print(f'Now Checking: {compare_path}/{file}')
        print(f'Now Similarity: {similarity}')
        print(f'Highest File Path: {highest_file_path}')
        print(f'Highest Similarity: {highest_similarity}')

    # Result
    print_plagiarism_result(highest_file_path, highest_similarity, highest_introduction, user)
########################################################################################################################
def print_plagiarism_result(highest_file_path, highest_similarity, highest_introduction, user):
    # Result
    print('===========================================================================================================')
    print(f'Most Similar Self-Introduction')
    print(f'Highest File Path: {highest_file_path}')
    print(f'Highest Similarity: {highest_similarity}')
    print(f'User Self-Introduction: \n{user}')
    print(f'Highest Self-Introduction: \n{highest_introduction}')
########################################################################################################################
def run():
    # 백엔드 연결 후 user_path 부분만 수정
    user_path = f'../07_Saramin_dataset/user/answer/test.txt'
    compare_path = f'../07_Saramin_dataset/whole/answer'
    plagiarism_check(user_path, compare_path)
run()