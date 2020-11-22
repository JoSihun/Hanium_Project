import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests

BASE_PATH = '../07_Saramin_dataset'
DATA_PATH = '../07_Saramin_dataset/dataset'

# 지정된 경로에 폴더가 없으면 폴더 생성
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

# 해당 페이지 크롤링
def crawling(page_num):
    html = requests.get(f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}')
    source = html.text
    soup = BeautifulSoup(source, "html.parser")

    # 기업명
    company_name = soup.find('title').text
    company_name = company_name.split()[0]

    # 직종
    occupation = soup.find('span', class_='tag_apply').text
    occupation = occupation.split()[2]

    # 자소서내용
    contents = ''
    boxes = soup.find_all("div", class_="box_ty3")

    for box in boxes:
        #print(f'\n\n{box}')
        question = box.find_next('h3').text                             # 자소서 질문
        erase_list = box.find_all('div')
        erase_list.append(box.find_next('button'))

        answer = box.text.replace(question, '')                         # 자소서 질문 삭제
        for erase in erase_list:
            answer = answer.replace(erase.text, '')
        #print(f'\n\n{answer}')


        if box.find_next('h4', class_='tsp_ty2'):                       # 첨삭 존재시
            erase3 = box.find_next('h4', class_='tsp_ty2').text         # 첨삭결과
            erase4 = box.find_next('p').text                            # 첨삭내용
            answer = answer.replace(erase3, '')                         # 첨삭결과 삭제
            answer = answer.replace(erase4, '')                         # 첨삭내용 삭제

        contents += answer                                              # 자소서내용

    text = f'{company_name}\n{occupation}\n{contents}'                  # 기업명, 직종, 자소서내용
    result = text_normalization(text)                                   # 추출 자소서 텍스트 정규화

    return result

# 자소서 텍스트 정규화
def text_normalization(text):
    result = ''
    lines = text.split('\n')                    # 라인단위로 분할
    for line in lines:                          # 각 라인별로
        if line.strip() != '':                  # 해당 라인이 공백이 아니면(내용이 존재하면)
            result += line.strip() + '\n'       # 해당 라인 + '\n'

    return result.strip()                       # 최종 텍스트 양 끝 공백제거


if __name__ == '__main__':
    total_cnt = 0
    succeed_cnt = 0
    failed_cnt = 0
    for page_num in tqdm(range(35125, 35126)):
        log_text = f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}\n'
        try:
            # 자소서 텍스트 생성
            introduction = crawling(page_num)
            print(introduction)

        except Exception as e:
            # 크롤링 실패 로그 수정
            failed_cnt += 1



