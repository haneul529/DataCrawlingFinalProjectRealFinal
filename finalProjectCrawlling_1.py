import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# WebDriver 설정
driver = webdriver.Chrome()
URL = "https://fastcampus.co.kr/category_online_datasciencedl"
driver.get(URL)

# 페이지 로드 대기
time.sleep(5)

# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 스크롤 후 대기
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 강의 데이터 수집
courses = driver.find_elements(By.CSS_SELECTOR, 'body > div.category-app > div:nth-child(7) > div > div')
course_data = []

for course in courses:
    try:
        # 강의명
        title = course.find_element(By.CSS_SELECTOR, 'a.CourseCard_courseCardDetailContainer__PnVam > div > div.CourseCard_courseCardInfo__1_3Of > span').text.strip()

        # 할인율
        try:
            discount = course.find_element(By.CSS_SELECTOR, 'a.CourseCard_courseCardDetailContainer__PnVam > div > div.CourseCard_courseCardPriceContainer__6T7bF > span.CourseCard_courseCardDiscount__yKHtx').text.strip()
        except:
            discount = "할인 없음"

        # 가격
        try:
            price = course.find_element(By.CSS_SELECTOR, 'a.CourseCard_courseCardDetailContainer__PnVam > div > div.CourseCard_courseCardPriceContainer__6T7bF > span.CourseCard_courseCardPrice__dbuVW').text.strip()
        except:
            price = "가격 정보 없음"

        # 추가 정보 처리
        extra_info_1, extra_info_2, extra_info_3 = "", "", ""
        try:
            extra_info_elements = course.find_elements(By.CSS_SELECTOR, 'a.CourseCard_courseCardDetailContainer__PnVam > div > div.CourseCard_courseCardInfo__1_3Of > div > span')
            if len(extra_info_elements) > 0:
                extra_info_1 = extra_info_elements[0].text.strip() if "주 과정" in extra_info_elements[0].text.strip() else ""
            if len(extra_info_elements) > 1:
                extra_info_2 = extra_info_elements[1].text.strip() if "약" in extra_info_elements[1].text.strip() else ""
            if len(extra_info_elements) > 2:
                extra_info_3 = extra_info_elements[2].text.strip() if "누구나" in extra_info_elements[2].text.strip() or "필요" in extra_info_elements[2].text.strip() else ""
        except:
            pass

        # 세부 주제
        try:
            course_subject = course.find_element(By.CSS_SELECTOR, 'div.CourseCard_courseCardCategoryContainer__1iB46 > a.TextWithArrowLinkButton_linkButton__NBtyJ').text.strip()
        except:
            course_subject = "세부 주제 없음"

        # 좋아요 수
        try:
            likes = course.find_element(By.CSS_SELECTOR, 'div > a').text.strip()
        except:
            likes = "좋아요 수 없음"

        # 강의 링크
        try:
            link = course.find_element(By.CSS_SELECTOR, 'a.CourseCard_courseCardDetailContainer__PnVam').get_attribute('href').strip()
        except:
            link = "링크 정보 없음"

        # 데이터를 딕셔너리로 저장
        course_data.append({
            "title": title,
            "discount": discount,
            "price": price,
            "extra_info_1": extra_info_1,
            "extra_info_2": extra_info_2,
            "extra_info_3": extra_info_3,
            "course_subject": course_subject,
            "likes": likes,
            "link": link  # 강의 링크 추가
        })
    except Exception as e:
        print(f"Error with a course: {e}")

# 크롤링 데이터 확인
print(f"Total courses collected: {len(course_data)}")

# 데이터프레임으로 변환 및 정리
df = pd.DataFrame(course_data)

# 누락된 데이터 처리
df['discount'] = df['discount'].fillna('할인 없음')
df['price'] = df['price'].fillna('가격 정보 없음')
df['extra_info_1'] = df['extra_info_1'].fillna('')
df['extra_info_2'] = df['extra_info_2'].fillna('')
df['extra_info_3'] = df['extra_info_3'].fillna('')
df['course_subject'] = df['course_subject'].fillna('세부 주제 없음')
df['likes'] = df['likes'].fillna('좋아요 수 없음')
df['link'] = df['link'].fillna('링크 정보 없음')

# CSV 파일로 저장 (utf-8-sig 인코딩 사용)
file_name = "fastcampus_courses_ai_with_links.csv"
df.to_csv(file_name, index=False, encoding="utf-8-sig")

# 저장 경로 출력
file_path = os.path.abspath(file_name)
print(f"Cleaned data saved to {file_path}")

# 브라우저 종료
driver.quit()
