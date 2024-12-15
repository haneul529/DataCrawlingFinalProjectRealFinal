from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd

# WebDriver 설정
driver = webdriver.Chrome()
URL = "https://www.inflearn.com/courses/artificial-intelligence?isDiscounted=false&types=ONLINE&sort="
driver.get(URL)

# 페이지 로드 대기
time.sleep(5)

course_data = []

def scrape_courses():
    course_list_selector = '#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > main > div.css-1etb3gv.mantine-1pure0w > section:nth-child(2) > ul.css-sdr7qd.mantine-1avyp1d > li'
    courses = driver.find_elements(By.CSS_SELECTOR, course_list_selector)

    for course in courses:
        try:
            # 강의명
            title_elements = course.find_elements(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-17cnqmk.mantine-5n4x4z > p')
            title = title_elements[0].text.strip() if title_elements else "제목 없음"

            # 가격
            price_elements = course.find_elements(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-4542l5.mantine-1avyp1d > div:nth-child(1) > div > div:nth-child(1) > p > p')
            price = price_elements[0].text.strip() if price_elements else "가격 정보 없음"

            # 할인율
            discount_elements = course.find_elements(By.CSS_SELECTOR, 'a > article > div.css-13udsys.mantine-5t8g7z > div.css-4542l5.mantine-1avyp1d > div:nth-child(1) > div > div:nth-child(1) > p.mantine-Text-root.css-uzjboo.mantine-gntgg5')
            discount = discount_elements[0].text.strip() if discount_elements else "할인 없음"

            # 강의 링크
            link_elements = course.find_elements(By.CSS_SELECTOR, 'a')
            link = link_elements[0].get_attribute('href') if link_elements else "링크 없음"

            # 상세 페이지 데이터 수집
            driver.execute_script("window.open(arguments[0], '_blank');", link)
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
                "link": link,
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


for page in range(2, 7):  # 다섯 페이지 순회
    scrape_courses()
    try:
        next_button_selector = f"#__next > div.css-1afo5g2.mantine-1fr50if > div.css-c31z9o.mantine-1jggmkl > main > div.mantine-1tut1p5 > div > button:nth-child({page})"
        next_button = driver.find_element(By.CSS_SELECTOR, next_button_selector)
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)  # 버튼 스크롤 후 대기
        next_button.click()
        time.sleep(3)  # 페이지 로드 대기
    except Exception as e:
        print(f"Error navigating to page {page}: {e}")
        break

# 데이터 확인 및 저장
print(f"Total courses collected: {len(course_data)}")
df = pd.DataFrame(course_data)
file_name = "inflearn_courses_ai_with_links.csv"

# CSV 파일 저장
try:
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"Data saved to {file_name}")
    print(f"File saved at: {os.path.abspath(file_name)}")
except Exception as e:
    print(f"Error saving the file: {e}")

# 브라우저 종료
driver.quit()
