"""전주대학교 대동제 및 해커톤 로그 데이터 정보 추출 프로그램입니다."""
from functools import reduce
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(
    BASE_DIR,
    "07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt",
)


def read_log_file(file_path):
    if not os.path.exists(file_path):
        return ""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_valid_emails(text):
    pattern = re.compile(
        r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"
    )
    return pattern.findall(text)


def extract_phone_numbers(text):
    pattern = re.compile(r"\b010[-.\s]\d{4}[-.\s]\d{4}\b")
    return pattern.findall(text)


def extract_students(text):
    pattern = re.compile(r"\[(202\d{6})\s*/\s*([^\]]+)\]")
    return pattern.findall(text)


def extract_github_and_coupons(text):
    github_pattern = re.compile(r"https?://github\.com/[^\s]+")
    coupon_pattern = re.compile(r"\bFEST-2026-[A-Z0-9]{4}\b")
    return github_pattern.findall(text), coupon_pattern.findall(text)


def extract_booth_sales(text):
    pattern = re.compile(r"매출:\s*(\d{1,3}(?:,\d{3})*원)")
    sales_list = pattern.findall(text)

    sales_ints = list(
        map(lambda s: int(s.replace(",", "").replace("원", "")), sales_list)
    )
    total_revenue = reduce(lambda x, y: x + y, sales_ints, 0)

    return sales_list, total_revenue


def main():
    log_text = read_log_file(LOG_FILE)

    if not log_text:
        print("로그 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
        return

    emails = extract_valid_emails(log_text)
    phones = extract_phone_numbers(log_text)
    students = extract_students(log_text)
    github_urls, coupons = extract_github_and_coupons(log_text)
    sales_list, total_revenue = extract_booth_sales(log_text)

    print("==========================================================")
    print("     대동제 및 해커톤 통합 로그 정규표현식 추출 결과")
    print("==========================================================")

    print(f"\n1. 유효한 이메일 추출 (총 {len(emails)}건)")
    for idx, email in enumerate(emails, 1):
        print(f"  {idx}. {email}")

    print(f"\n2. 휴대폰 번호 추출 (총 {len(phones)}건)")
    for idx, phone in enumerate(phones, 1):
        print(f"  {idx}. {phone}")

    print(f"\n3. 본교 재학생 학번 및 학과 튜플 추출 (총 {len(students)}건)")
    for idx, student_tuple in enumerate(students, 1):
        print(f"  {idx}. {student_tuple}")

    print("\n4. GitHub 저장소 및 유효 쿠폰 추출")
    print(f"  [GitHub 저장소 URL] (총 {len(github_urls)}건)")
    for idx, url in enumerate(github_urls, 1):
        print(f"    {idx}. {url}")

    print(f"  [2026년 유효 쿠폰 코드] (총 {len(coupons)}건)")
    for idx, coupon in enumerate(coupons, 1):
        print(f"    {idx}. {coupon}")

    print("\n5. 부스별 총 매출액 추출 및 합산")
    print(f"  - 추출된 부스별 매출액: {', '.join(sales_list)}")
    print(f"  - 전체 부스 매출 총합계: {total_revenue:,}원")
    print("==========================================================")


if __name__ == "__main__":
    main()
