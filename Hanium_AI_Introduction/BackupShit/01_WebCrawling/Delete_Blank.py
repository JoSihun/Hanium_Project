import os

def delete_blank(path):
    for file in os.listdir(path):
        # Read '.txt' file
        lines = open(f'{path}/{file}', 'r', encoding='UTF-8').readlines()
        text = open(f'{path}/{file}', 'r', encoding='UTF-8').read()

        # Delete Useless Blank
        result_text = ''
        for line in lines:
            if line == '\n':
                continue
            line = line.replace('  ', '')
            result_text += line

        print(f'======================================================================================================')
        print(f'Delete Uselss Blank Proceeding... {path}/{file}')
        print(f'Original_Text:\n{text}')
        print(f'Result_Text:\n{result_text}')

        # Rewrite '.txt' file
        f = open(f'{path}/{file}', 'w', encoding='UTF-8')
        f.write(result_text)
        f.close()

def run():
    question_path = '../07_Saramin_dataset/whole/question'
    answer_path = '../07_Saramin_dataset/whole/answer'
    
    delete_blank(question_path)
    delete_blank(answer_path)