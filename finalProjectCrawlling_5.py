import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# WebDriver 설정
driver = webdriver.Chrome()
URL = "https://www.inflearn.com/courses/data-science?isDiscounted=false&types=ONLINE&sort="
driver.get(URL)

# 페이지 로드 대기
time.sleep(5)

course_data = []

while True:
    # 페이지 끝까지 스크롤
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 강의 데이터 수집
    course_list_selector = '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > main > div.css-1etb3gv.mantine-1pure0w > section:nth-child(2) > ul.css-sdr7qd.mantine-1avyp1d > li'
    courses = driver.find_elements(By.CSS_SELECTOR, course_list_selector)

    if not courses:
        print("강의 정보를 찾을 수 없습니다.")
        break

    for course in courses:
        try:
            # 강의명
            try:
                title = course.find_element(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-17cnqmk.mantine-5n4x4z > p').text.strip()
            except:
                title = "제목 없음"

            # 가격
            try:
                price = course.find_element(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-4542l5.mantine-1avyp1d > div:nth-child(1) > div > div:nth-child(1) > p > p').text.strip()
            except:
                price = "가격 정보 없음"

            # 할인율
            try:
                discount = course.find_element(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-4542l5.mantine-1avyp1d > div:nth-child(1) > div > div:nth-child(1) > p.mantine-Text-root.css-uzjboo.mantine-gntgg5').text.strip()
            except:
                discount = "할인 없음"

            # 링크
            try:
                course_url = course.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:
                course_url = "링크 없음"

            # 강의 상세 페이지에서 추가 데이터 수집
            driver.execute_script("window.open(arguments[0], '_blank');", course_url)
            driver.switch_to.window(driver.window_handles[-1])

            # 좋아요 수
            try:
                likes = driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > aside > div > div.mantine-Stack-root.css-y48vtv.mantine-14kdbyl > div.mantine-SimpleGrid-root.mantine-1dfaauk > button:nth-child(2) > div > span.mantine-1bvbs5e.mantine-Button-label').text.strip()
            except:
                likes = "좋아요 수 없음"

            # 추가 정보 2
            try:
                extra_info_2 = driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > aside > div > div.css-1ncs04q.mantine-4zwhfa > div > div:nth-child(2) > div > div > p:nth-child(2)').text.strip()
            except:
                extra_info_2 = "추가 정보 없음"

            # 추가 정보 3 (굵은 글씨 탐색)
            try:
                bold_elements = [
                    driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > aside > div > div.css-1ncs04q.mantine-4zwhfa > div > div:nth-child(5) > div > div > div:nth-child(1) > div > p'),
                    driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > aside > div > div.css-1ncs04q.mantine-4zwhfa > div > div:nth-child(5) > div > div > div:nth-child(2) > div > p'),
                    driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > aside > div > div.css-1ncs04q.mantine-4zwhfa > div > div:nth-child(5) > div > div > div:nth-child(3) > div > p')
                ]
                for element in bold_elements:
                    if "mantine-ovwq0i" in element.get_attribute("class"):
                        extra_info_3 = element.text.strip()
                        break
                else:
                    extra_info_3 = "추가 정보 없음"
            except:
                extra_info_3 = "추가 정보 없음"

            # 세부 주제
            try:
                course_subject = driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > div > section.css-1h0915r.mantine-1avyp1d > div > div > section > div > div:nth-child(1) > h2 > span > strong:nth-child(4)').text.strip()
                course_subject = course_subject.replace("[", "").replace("]", "")
            except:
                course_subject = "세부 주제 없음"

            # 데이터 저장
            course_data.append({
                "title": title,
                "price": price,
                "discount": discount,
                "link": course_url,
                "extra_info_2": extra_info_2,
                "extra_info_3": extra_info_3,
                "course_subject": course_subject,
                "likes": likes
            })

            # 새 탭 닫기
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Error with a course: {e}")

    # 다음 페이지로 이동
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > main > div.mantine-1tut1p5 > div > button:nth-child(9)')
        if "mantine-Button-disabled" in next_button.get_attribute("class"):
            print("마지막 페이지입니다.")
            break
        next_button.click()
        time.sleep(3)  # 페이지 로드 대기
    except:
        print("더 이상 다음 페이지로 이동할 수 없습니다.")
        break

# 데이터 확인 및 저장
print(f"Total courses collected: {len(course_data)}")
df = pd.DataFrame(course_data)
file_name = "inflearn_courses_datascience_with_links.csv"

try:
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    file_path = os.path.abspath(file_name)
    print(f"Data saved to {file_path}")
except Exception as e:
    print(f"Error saving the file: {e}")

# 브라우저 종료
driver.quit()
