from konlpy.tag import Okt
import konlpy

okt = Okt()
TEST_PATH = 'C:/Hanium_Project/Hanium_AI_Introduction/Final/07_Saramin_dataset/testset'


def token_morphs(text):
    word_morphs = okt.morphs(text)  # 형태소 추출
    print(f'<형태소 추출>')
    print(word_morphs)
    return word_morphs


def token_pos(text):
    word_pos = okt.pos(text) # 품사 태깅
    print(f'<품사 태깅>')
    print(word_pos)
    return word_pos


def token_nouns(text):
    word_nouns = okt.nouns(text) # 명사 추출
    print(f'<명사 추출>')
    print(word_nouns)
    return word_nouns


if __name__ == '__main__':
    # 원본 텍스트 데이터
    origin_text = konlpy.utils.read_txt(f'{TEST_PATH}/test.txt', encoding='UTF-8')  # txt 파일 읽음
    print(f'<원본 텍스트>')
    print(origin_text, '\n')
    token_morphs(origin_text)
    token_pos(origin_text)
    token_nouns(origin_text)

