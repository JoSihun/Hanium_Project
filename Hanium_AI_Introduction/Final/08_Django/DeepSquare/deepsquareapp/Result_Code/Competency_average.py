# 합격자 직무평균 역량
from deepsquareapp.models import SelfIntroduction
from deepsquareapp.models import Duties
from .Competency_evaluation import evaluation_run


def average_run(input_duty):

    # 모든 직무추출(데이터 베이스 삽입용)
    data = SelfIntroduction.objects.all()
    duties_list = []
    for intro in data:
        if intro.pass_fail_result == 'PASS':
            duty = intro.department_name.replace("\n","")
            if duty not in duties_list:
                duties_list.append(duty)

    duties_list.sort()

    MAIN_DUTY = duties_list[321] # 차후 수정해야함
    #print(input_duty)
    #print("시발",MAIN_DUTY)
    selected_intro = []
    data = SelfIntroduction.objects.all()
    for intro in data:
        if intro.pass_fail_result == 'PASS':
            if intro.department_name.replace("\n","") == MAIN_DUTY: # MAIN_DUTY은 차후에 사용자가 입력한 직무로 수정
                selected_intro.append(intro.contents)


    # 입력한 직무에 해당된 자소서 역량평가
    average = []
    for text in selected_intro:
        result = evaluation_run(text)
        average.append(result)


    # 입력한 직무의 평균역량 추출
    same_duty_average = {}
    for i in range(len(average[0])):
        duty_name = ""
        sum = 0
        for list in average:
            list.sort()
            #print(list[i])
            sum += list[i][1]
            duty_name = list[i][0]
            #print("==============================================================================")
        same_duty_average[duty_name] = sum/ len(average)

    # 결과
    result = sorted(same_duty_average.items(), reverse=True, key=lambda item:item[1])
    #print(f"{MAIN_DUTY} 직무의 평균 역량 :\n{result}")

    return result