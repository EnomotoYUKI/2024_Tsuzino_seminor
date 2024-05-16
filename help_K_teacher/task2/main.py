"""
Auther: Enomoto YUKI
Date: 2024-05-16
Note: Gale-Shapleyアルゴリズムを参考に実装してみる
"""

import pandas as pd
import time

FILE_NUMBER = 2

# CSVファイルからデータを読み込み
company_preferences = pd.read_csv(
    "input_p1c_c{}.csv".format(FILE_NUMBER)
).values.tolist()
student_preferences = pd.read_csv(
    "input_p1s_c{}.csv".format(FILE_NUMBER)
).values.tolist()

# 企業の受け入れ枠数 (今回は全企業1名と仮定)
company_quota = [1] * len(company_preferences)


def gale_shapley(students, companies, quotas):
    n_students = len(students)
    n_companies = len(companies)

    # 各学生と企業のマッチングを初期化
    matches = [None] * n_students
    free_students = list(range(n_students))

    # 学生がまだ拒否されていない企業のインデックス
    next_proposal_index = [0] * n_students

    # 各企業の選好リストで-1のインデックスを特定
    company_rejections = [
        prefs.index(-1) if -1 in prefs else len(prefs) for prefs in companies
    ]
    student_rejections = [
        prefs.index(-1) if -1 in prefs else len(prefs) for prefs in students
    ]

    while free_students:
        student = free_students.pop(0)

        # 学生が次にプロポーズする企業を取得
        while next_proposal_index[student] < student_rejections[student]:
            company = students[student][next_proposal_index[student]]
            next_proposal_index[student] += 1

            # 有効な企業インデックスかチェック
            if company == -1 or company >= n_companies:
                continue

            # 企業の受け入れ枠に余裕がある場合
            if quotas[company] > 0:
                if companies[company].index(student) < company_rejections[company]:
                    matches[student] = company
                    quotas[company] -= 1
                    break
            else:
                # 企業の現在の受け入れ学生の中で最も選好順位が低い学生を探す
                worst_student, worst_rank = get_worst_student(
                    company, matches, companies
                )

                if is_preferred(company, student, worst_student, companies):
                    matches[worst_student] = None
                    free_students.append(worst_student)
                    matches[student] = company
                    break
        else:
            matches[student] = -1

    return matches


def get_worst_student(company, matches, companies):
    worst_student = None
    worst_rank = -1
    for student, matched_company in enumerate(matches):
        if matched_company == company:
            rank = companies[company].index(student)
            if rank > worst_rank:
                worst_student = student
                worst_rank = rank
    return worst_student, worst_rank


def is_preferred(company, student, other_student, companies):
    preferences = companies[company]
    return preferences.index(student) < preferences.index(other_student)


# 実行開始時刻を記録
start_time = time.time()

# マッチングアルゴリズムの実行
matches = gale_shapley(student_preferences, company_preferences, company_quota)

# 実行終了時刻を記録
end_time = time.time()

# 実行時間を計算
execution_time = end_time - start_time

# 結果表示
for student, company in enumerate(matches):
    if company != -1:
        print(f"Student {student} is matched with Company {company}")
    else:
        print(f"Student {student} is not matched with any company")

# 実行時間を表示
print(f"Execution time: {execution_time:.4f} seconds")

# 結果をCSVファイルに出力
results_df = pd.DataFrame({"Student": list(range(len(matches))), "Company": matches})

results_df.to_csv("matching_results_no{}.csv".format(FILE_NUMBER), index=False)
