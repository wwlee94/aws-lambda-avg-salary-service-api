# AWS Lambda API를 이용한 회사별 평균 연봉 조회 

## 공공데이터(data.go.kr) 사이트 "사업장 정보 조회 서비스" 를 사용
### 1. 사업장 정보 조회 서비스
* 회사이름 , 사업자등록번호로 전체 목록 조회 후 가장 최근 데이터의 식별번호를 추출
### 2. 상세 정보 조회
* 추출한 식별번호로 상세 정보를 조회해 직원 수, 국민연금 지출 내역을 추출

## 회사별 평균 연봉 구하기
* 1인 국민연금 지출 금액 = 회사 국민연금 지출 내역 / 직원 수 / 2 -> 2로 나누는 이유는 회사 반, 직원 반 부담하기 때문
* https://job.cosmosfarm.com/ko/calculator/salary 에서 국민연금과 연봉을 대략적으로 매칭

## AWS Lambda 와 AWS API Gateway를 사용하여 lambda api 서버 구축
### 요청 URL
- https://sh49eptmi2.execute-api.ap-northeast-2.amazonaws.com/v2/programmers/api/avgSalaryService
### 요청 POST body
- name -> 회사의 이름(한글)
- bsNo -> 사업자등록번호
- ex) {"name":"당근","bsNo":"375870"}
