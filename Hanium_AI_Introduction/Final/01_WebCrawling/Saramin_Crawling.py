import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests

BASE_PATH = '../07_Saramin_dataset'
DATA_PATH = '../07_Saramin_dataset/dataset'


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


def crawling(page_num):
    html = requests.get(f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}')
    source = html.text
    soup = BeautifulSoup(source, "html.parser")

    # 기업명
    company_name = soup.find('title').text
    company_name = company_name.split()[0]
    # print(company_name, type(company_name))

    # 직종
    occupation = soup.find('span', class_='tag_apply').text
    occupation = occupation.split()[2]
    # print(occupation, type(occupation))

    # 자소서내용
    contents = ''
    boxes = soup.find_all("div", class_="box_ty3")
    for box in boxes:
        question = box.find_next('h3').text
        index = box.text.find('글자수')
        answer = box.text[:index].replace(question, '')
        contents += answer
    # print(contents)

    text = f'{company_name}\n{occupation}\n{contents}'
    result = text_normalization(text)

    return result


def text_normalization(text):
    result = ''
    lines = text.split('\n')
    for line in lines:
        if line.strip() != '':
            result += line.strip() + '\n'

    return result.strip()


if __name__ == '__main__':
    createFolder(DATA_PATH)

    succeed_log = ['Succeed Log:\n']
    failed_log = ['Failed Log:\n']
    total_cnt = 0
    succeed_cnt = 0
    failed_cnt = 0
    for page_num in tqdm(range(35001, 35126)):
        log_text = f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}\n'
        try:
            introduction = crawling(page_num)
            fp = open(f'{DATA_PATH}/{succeed_cnt}.txt', 'w', encoding='UTF-8')
            fp.write(introduction)
            fp.close()

            succeed_cnt += 1
            succeed_log.append(log_text)

        except:
            failed_cnt += 1
            failed_log.append(log_text)

        finally:
            total_cnt += 1

        #print('===================================================================================================')
        #print('Total Try: ', total_cnt)
        #print('Succeed: ', succeed_cnt)
        #print('Failed: ', failed_cnt)

    result_log = f'Total Try: {total_cnt}\n' \
                 f'Succeed: {succeed_cnt}\n' \
                 f'Failed: {failed_cnt}\n'
    print(result_log)
    fp = open(f'{BASE_PATH}/Crawling_log.txt', 'w', encoding='UTF-8')
    fp.write(result_log + '\n')
    fp.write(''.join(succeed_log) + '\n')
    fp.write(''.join(failed_log))
    fp.close()