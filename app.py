"""
博客來 LLM 書籍管理系統

此檔案為程式的進入點，提供一個簡單的命令列選單。
"""

from database import BookDatabase
from scraper import scrape_books
import sys
from typing import List, Dict


class BookStoreApp:
    """博客來書籍管理系統"""

    def __init__(self) -> None:
        """初始化應用程式"""
        try:
            self.db = BookDatabase()
        except Exception as e:
            print(f"初始化資料庫失敗: {e}")
            sys.exit(1)

    def print_menu(self) -> None:
        """印出主選單"""
        print("\n" + "=" * 50)
        print("博客來 LLM 書籍管理系統")
        print("=" * 50)
        print("1. 更新書籍資料庫")
        print("2. 查詢書籍")
        print("3. 離開系統")
        print("=" * 50)

    def update_database(self) -> None:
        """
        更新書籍資料庫
        """
        print("\n正在更新書籍資料庫...")
        print("這可能需要幾分鐘時間,請稍候...\n")

        try:
            # 爬取書籍資料
            books = scrape_books()

            if not books:
                print("未能取得任何書籍資料。")
                return

            # 將資料存入資料庫
            inserted_count = self.db.insert_books(books)

            print(f"\n資料庫更新完成!")
            print(f"總共爬取: {len(books)} 筆書籍資料")
            print(f"成功新增: {inserted_count} 筆新書資料")
            print(f"重複略過: {len(books) - inserted_count} 筆")

        except Exception as e:
            print(f"更新資料庫時發生錯誤: {e}")

    def search_menu(self) -> None:
        """
        查詢子選單
        """
        while True:
            print("\n" + "-" * 50)
            print("查詢書籍")
            print("-" * 50)
            print("1. 依書名查詢")
            print("2. 依作者查詢")
            print("3. 返回主選單")
            print("-" * 50)

            choice = input("請選擇功能 (1-3): ").strip()

            if choice == '1':
                self.search_by_title()
            elif choice == '2':
                self.search_by_author()
            elif choice == '3':
                break
            else:
                print("無效的選項,請重新選擇。")

    def search_by_title(self) -> None:
        """
        依書名查詢
        """
        keyword = input("\n請輸入書名關鍵字: ").strip()

        if not keyword:
            print("關鍵字不可為空。")
            return

        try:
            results = self.db.search_by_title(keyword)
            self.display_results(results)
        except Exception as e:
            print(f"查詢時發生錯誤: {e}")

    def search_by_author(self) -> None:
        """
        依作者查詢
        """
        keyword = input("\n請輸入作者關鍵字: ").strip()

        if not keyword:
            print("關鍵字不可為空。")
            return

        try:
            results = self.db.search_by_author(keyword)
            self.display_results(results)
        except Exception as e:
            print(f"查詢時發生錯誤: {e}")

    def display_results(self, results: List[Dict[str, any]]) -> None:
        """
        顯示查詢結果
        """
        if not results:
            print("\n查無資料。")
            return

        print(f"\n找到 {len(results)} 筆資料:\n")
        print("=" * 100)

        for i, book in enumerate(results, 1):
            print(f"[{i}] 書名: {book['title']}")
            print(f"    作者: {book['author']}")
            print(f"    價格: NT$ {book['price']}")
            print(f"    連結: {book['link']}")
            print("-" * 100)

    def run(self) -> None:
        """
        執行主程式
        """
        print("\n歡迎使用博客來 LLM 書籍管理系統!")

        while True:
            self.print_menu()
            choice = input("請選擇功能 (1-3): ").strip()

            if choice == '1':
                self.update_database()
            elif choice == '2':
                self.search_menu()
            elif choice == '3':
                print("\n感謝使用,再見!")
                sys.exit(0)
            else:
                print("無效的選項,請重新選擇。")


def main() -> None:
    """
    主函式
    """
    app = BookStoreApp()

    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n程式已中斷。")
        sys.exit(0)
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()