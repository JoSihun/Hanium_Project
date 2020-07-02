import os

def createFolder(directory):
    print(f'======================================================================================================')
    print(f'Creating New Folder... {directory}')

    directory = directory.split('/')
    mkdir_path = ''
    for direct in directory:
        mkdir_path += direct
        if not os.path.exists(mkdir_path):
            print(f'Not Exist! Making Directory Path {mkdir_path}')
            os.mkdir(mkdir_path)
        else:
            print(f'Already Exist! {mkdir_path}')
        mkdir_path += '/'
########################################################################################################################
from bs4 import BeautifulSoup
import requests
import time

def data_Crawling(question_path, answer_path):
    createFolder(question_path)
    createFolder(answer_path)

    error_cnt = 0
    data_count = 0
    for page_num in range(0, 35126):
        try:
            print('===================================================================================================')
            print('Page_num: ', page_num)
            print('Data_Count: ', data_count)
            print('Error_Count: ', error_cnt)

            html = requests.get("http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq=" + str(page_num))
            time.sleep(0.1)
            source = html.text
            soup = BeautifulSoup(source, "html.parser")
            line = soup.find_all("div", class_="box_ty3")

            question = ''
            answer = ''
            for l in line:
                print('===================================================================================================')
                question_temp = l.find_next('h3')
                question = question_temp.text
                print(question)

                idx1 = l.text.find('글자수')
                #idx2 = l.text.find('Byte')
                #idx3 = l.text.find('접기')
                answer = l.text[:idx1]
                answer = answer.replace(question, '')
                print(answer)

            data_count += 1
            f1 = open(f'{question_path}/{data_count}.txt', 'w', encoding='UTF-8')
            f2 = open(f'{answer_path}/{data_count}.txt', 'w', encoding='UTF-8')
            f1.write(question)
            f2.write(answer)
            f1.close()
            f2.close()

            log_text = f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}\n'
            f3 = open('../07_Saramin_dataset/whole/Crawling_Complete_log.txt', 'a', encoding='UTF-8')

        except:
            log_text = f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}\n'
            f3 = open('../07_Saramin_dataset/whole/Crawling_Fail_log.txt', 'a', encoding='UTF-8')
            error_cnt += 1
            pass

        finally:
            f3.write(log_text)
            f3.close()

    log_text = f'Result:\n' \
               f'Total_Data: {data_count}\n' \
               f'Normal_Error: {error_cnt}\n'
    f3 = open('../07_Saramin_dataset/whole/Crawling_Result_log.txt', 'a', encoding='UTF-8')
    f3.write(log_text)
    f3.close()

def run():
    question_path = '../07_Saramin_dataset/whole/question'
    answer_path = '../07_Saramin_dataset/whole/answer'
    data_Crawling(question_path, answer_path)