import os

def rename(path):
    file_name = os.listdir(path)
    for i, name in enumerate(file_name):
        print(f'======================================================================================================')
        print(f'Rename Proceeding ... {path}/{name}')
        original = f'{path}/{name}'
        changed = f'{path}/A{i+1}.txt'
        if os.path.isfile(changed):
            print(f'A{i+1}.txt is already exist')
            continue
        os.rename(original, changed)
        print(f'Original: {name} ---------------> Changed: A{i+1}.txt')

    file_name = os.listdir(path)
    for i, name in enumerate(file_name):
        print(f'======================================================================================================')
        print(f'Rename Proceeding ... {path}/{name}')
        original = f'{path}/{name}'
        changed = f'{path}/{i+1}.txt'
        if os.path.isfile(changed):
            print(f'{i+1}.txt is already exist')
            continue
        os.rename(original, changed)
        print(f'Original: {name} ---------------> Changed: {i+1}.txt')

def run():
    question_path = '../07_Saramin_dataset/whole/question'
    answer_path = '../07_Saramin_dataset/whole/answer'

    rename(question_path)
    rename(answer_path)