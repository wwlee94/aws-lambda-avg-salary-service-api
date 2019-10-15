import csv
def get_salary_pension_csv(price):
    with open('./resources/pension_per_employee.csv', 'r', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        pre = 0
        result = 0
        for row in reader:
            pension = int(row['국민연금'])
            if pre == 0 and price <= pension:
                result = row['연봉']
                break
            elif pre <= price and price <= pension:
                # 더 가까운 곳의 연봉을 넣어줌
                if (price - pre) < (pension - price):
                    result = pre_salary
                else :
                    result = row['연봉']
                break
            elif price >= pension:
                pre = pension
                pre_salary = row['연봉']
    return result

price = 35000
result = get_salary_pension_csv(price)
print(result)
