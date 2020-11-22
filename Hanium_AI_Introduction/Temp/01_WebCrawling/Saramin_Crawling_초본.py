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
        question = box.find_next('h3').text                             # 자소서 질문
        erase1 = box.find_next('div', class_='txt_byte').text           # 글자수 | bytes
        erase2 = box.find_next('button', class_='btn_tsp_hide').text    # 접기

        answer = box.text.replace(question, '')                         # 자소서 질문 삭제
        answer = answer.replace(erase1, '')                             # 글자수 | bytes 삭제
        answer = answer.replace(erase2, '')                             # 접기 삭제

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
    # 데이터 경로 생성
    createFolder(DATA_PATH)

    # 크롤링 결과로그 존재시 삭제
    if os.path.exists(f'{BASE_PATH}/Crawling_Succeed_log.txt'):
        os.remove(f'{BASE_PATH}/Crawling_Succeed_log.txt')
    if os.path.exists(f'{BASE_PATH}/Crawling_Failed_log.txt'):
        os.remove(f'{BASE_PATH}/Crawling_Failed_log.txt')

    total_cnt = 0
    succeed_cnt = 0
    failed_cnt = 0
    for page_num in tqdm(range(0, 35126)):
        log_text = f'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq={page_num}\n'
        try:
            # 자소서 텍스트 생성
            introduction = crawling(page_num)
            fp1 = open(f'{DATA_PATH}/{succeed_cnt}.txt', 'w', encoding='UTF-8')
            fp1.write(introduction)
            fp1.close()

            # 크롤링 성공 로그 수정
            succeed_cnt += 1
            fp2 = open(f'{BASE_PATH}/Crawling_Succeed_log.txt', 'a', encoding='UTF-8')
            fp2.write(log_text)
            fp2.close()

        except Exception as e:
            # 크롤링 실패 로그 수정
            failed_cnt += 1
            fp3 = open(f'{BASE_PATH}/Crawling_Failed_log.txt', 'a', encoding='UTF-8')
            fp3.write(log_text)
            fp3.write(str(e) + '\n')
            fp3.close()

        finally:
            total_cnt += 1

        print('===================================================================================================')
        print('Total Try: ', total_cnt)
        print('Succeed: ', succeed_cnt)
        print('Failed: ', failed_cnt)

    # 크롤링 최종 결과 로그 생성
    result_log = f'Total Try: {total_cnt}\n' \
                 f'Succeed: {succeed_cnt}\n' \
                 f'Failed: {failed_cnt}\n'
    fp4 = open(f'{BASE_PATH}/Crawling_Result_log.txt', 'w', encoding='UTF-8')
    fp4.write(result_log + '\n')
    fp4.close()