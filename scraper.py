"""
網頁爬蟲模組

此模組負責所有與網頁爬取相關的邏輯。
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from bs4 import BeautifulSoup
import re
import time
from typing import List, Dict, Optional


class BookScraper:
    """博客來書籍爬蟲"""

    def __init__(self, headless: bool = True) -> None:
        """
        初始化爬蟲
        """
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None

    def setup_driver(self) -> None:
        """
        設定 Selenium WebDriver
        """
        try:
            options = webdriver.ChromeOptions()

            if self.headless:
                options.add_argument('--headless')

            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option(
                'excludeSwitches',
                ['enable-logging']
            )

            self.driver = webdriver.Chrome(options=options)

        except WebDriverException as e:
            print(f"WebDriver 初始化失敗: {e}")
            raise

    def close_driver(self) -> None:
        """關閉 WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"關閉 WebDriver 時發生錯誤: {e}")

    def extract_price(self, price_text: str) -> int:
        """
        從價格文字中提取數字
        """
        # 使用正則表達式找出所有數字
        numbers = re.findall(r'\d+', price_text)

        if numbers:
            # 取最後一個數字(通常是實際價格)
            return int(numbers[-1])
        return 0

    def parse_page(self, html: str) -> List[Dict[str, any]]:
        """
        解析單頁書籍資料
        """
        soup = BeautifulSoup(html, 'html.parser')
        books = []

        # 找到所有書籍容器
        book_containers = soup.select('div.table-searchbox div.table-td')

        for container in book_containers:
            try:
                # 提取書名和連結
                title_tag = container.select_one('h4 a')
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.get('href', '')

                # 提取作者(可能有多位)
                author_tags = container.select('p.author a')
                authors = [
                    tag.get_text(strip=True)
                    for tag in author_tags
                ]
                author = ', '.join(authors) if authors else 'N/A'

                # 提取價格
                price_tag = container.select_one('span.price')
                if price_tag:
                    price_text = price_tag.get_text(strip=True)
                    price = self.extract_price(price_text)
                else:
                    price = 0

                books.append({
                    'title': title,
                    'author': author,
                    'price': price,
                    'link': link
                })

            except Exception as e:
                print(f"解析書籍時發生錯誤: {e}")
                continue

        return books

    def scrape_llm_books(self) -> List[Dict[str, any]]:
        """
        爬取博客來 LLM 關鍵字的所有書籍資料
        """
        print("正在啟動爬蟲...")
        self.setup_driver()

        all_books = []

        try:
            # 直接訪問已篩選的搜尋結果頁面
            url = "https://search.books.com.tw/search/query/key/LLM/cat/BKA"
            print(f"正在訪問: {url}")
            self.driver.get(url)

            # 等待頁面載入
            time.sleep(2)

            page_num = 1

            while True:
                print(f"正在爬取第 {page_num} 頁...")

                # 等待書籍列表載入
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.table-searchbox")
                        )
                    )
                except TimeoutException:
                    print("等待頁面載入逾時")
                    break

                # 解析當前頁面
                html = self.driver.page_source
                books = self.parse_page(html)
                all_books.extend(books)

                print(f"第 {page_num} 頁找到 {len(books)} 本書")

                # 尋找並點擊「下一頁」按鈕
                try:
                    # 等待下一頁按鈕可點擊
                    next_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "a.nxt")
                        )
                    )

                    # 滾動到按鈕位置
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();",
                        next_button
                    )
                    time.sleep(1)

                    # 點擊下一頁
                    next_button.click()
                    time.sleep(2)

                    page_num += 1

                except (TimeoutException, NoSuchElementException):
                    print("已到達最後一頁")
                    break
                except Exception as e:
                    print(f"點擊下一頁時發生錯誤: {e}")
                    break

            print(f"\n爬取完成!總共找到 {len(all_books)} 本書")

        except WebDriverException as e:
            print(f"爬取過程發生錯誤: {e}")
            raise

        finally:
            self.close_driver()

        return all_books


def scrape_books() -> List[Dict[str, any]]:
    """
    便利函式: 爬取書籍資料
    """
    scraper = BookScraper(headless=True)
    return scraper.scrape_llm_books()