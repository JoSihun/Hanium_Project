import os

def delete(path):
    for file in os.listdir(path):
        print(f'======================================================================================================')
        print(f'Delete 0Byte File Proceeding... {path}/{file}')
        file_size = os.path.getsize(f'{path}/{file}')
        if  file_size == 0:
            os.remove(f'{path}/{file}')
            print(f'{path}/{file} is 0 Byte!')
            print(f'{path}/{file} is Terminated!')
        else:
            print(f'{path}/{file} is {file_size} Byte!')
            print(f'{path}/{file} is NOT Terminated!')

def run():
    question_path = '../07_Saramin_dataset/whole/question'
    answer_path = '../07_Saramin_dataset/whole/answer'

    delete(question_path)
    delete(answer_path)

    file_num1 = len(os.listdir(question_path))
    file_num2 = len(os.listdir(answer_path))

    print(f'Whole Question Drectory Len: {file_num1}')
    print(f'Whole Answer Drectory Len: {file_num2}')