from konlpy.tag import Okt
import konlpy

okt = Okt()
TEST_PATH = 'C:/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset'


def eliminate_stopwords(orig_text, stop_text):
    word_tokens = okt.morphs(orig_text)  # 형태소 추출
    print(f'<텍스트 토큰화>')
    print(word_tokens)

    stop_words = []
    stop_words = stop_text

    result = []
    for w in word_tokens:
        if w not in stop_words:
            result.append(w)
    print(f'<불용어 제거>')
    print(result)

    return result


if __name__ == '__main__':
    # 원본 텍스트 데이터
    origin_text = konlpy.utils.read_txt(f'{TEST_PATH}/test.txt', encoding='UTF-8')  # txt 파일 읽음
    stopwords_text = konlpy.utils.read_txt(f'{TEST_PATH}/stop_words.txt', encoding='UTF-8')  # 불용어 파일

    print(f'<원본 텍스트>')
    print(origin_text, '\n')

    # 불용어 제거
    eliminate_stopwords(origin_text, stopwords_text)

