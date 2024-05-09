# Description: 生徒の希望に基づいた会社の割り当て
# Author: Enomoto Yuki
# Last Update: 2024/05/10
# Comment: 可読性が終わってる

import random

STUDENTS_NUMBER = 10
COMPANIES_NUMBER = 10

# For debugging purposes only
#random.seed(0)

# 生徒の希望をランダム割り当て
def randomPreferenceSurvey(students_number, companies_number):
    preference_survey = []
    for i in range(students_number):
        preference = random.sample(range(companies_number), companies_number)
        print(f"Student {i:2d}: {preference}")
        preference_survey.append(preference)
    return preference_survey

# 生徒の希望に基づいた会社の割り当て
def studentAllocation(preference_survey, companies_number):
    allocated_student_flag = [True] * len(preference_survey)
    allocated_company_flag = [True] * companies_number

    if len(preference_survey[0]) == 0:
        print("No preference survey")
        return

    for i in range(companies_number):
        same_preference_order = [x[i] for x in preference_survey]
        lottery_reservation = []
        for index, value in enumerate(same_preference_order):
            # もし同一順位で希望している生徒が一人で、
            # かつその生徒が割り当てられていないかつその会社が割り当てられていない場合
            if (
                same_preference_order.count(value) == 1
                and allocated_student_flag[index]
                and allocated_company_flag[value]
            ):
                print(f"Student {index} is allocated to Company {value}")
                allocated_student_flag[index] = False
                allocated_company_flag[value] = False
            # もし同一順位で希望している生徒が複数いる場合
            # かつその生徒が割り当てられていないかつその会社が割り当てられていない場合
            # かつ抽選予約がされていない場合
            elif (
                same_preference_order.count(value) > 1
                and allocated_company_flag[value]
                and allocated_student_flag[index]
                and value not in lottery_reservation
            ):
                lottery_reservation.append(value)
        
        # 抽選予約がある場合
        if len(lottery_reservation) > 0:
            for target_value in lottery_reservation:
                # 同一順位で希望している生徒を取得
                indices = [i for i, value in enumerate(same_preference_order) if value == target_value and allocated_student_flag[i]]
                lottery_winner = random.choice(indices)
                print(
                    f"Student {lottery_winner} is allocated to Company {target_value}"
                )
                allocated_student_flag[lottery_winner] = False
                allocated_company_flag[target_value] = False

if __name__ == "__main__":
    preference_survey = randomPreferenceSurvey(STUDENTS_NUMBER, COMPANIES_NUMBER)
    studentAllocation(preference_survey, COMPANIES_NUMBER)
