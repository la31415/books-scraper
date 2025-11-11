"""
資料庫管理模組

此模組負責所有與 SQLite 資料庫相關的操作,
包括建立資料表、新增書籍資料、查詢書籍等功能。
"""
import sqlite3
from typing import List, Dict
from contextlib import closing


class BookDatabase:
    """處理書籍資料庫的所有操作"""

    def __init__(self, db_name: str = "books.db") -> None:
        """
        初始化資料庫連線

        Args:
            db_name: 資料庫檔案名稱,預設為 'books.db'
        """
        self.db_name = db_name
        self.create_table()

    def get_connection(self) -> sqlite3.Connection:
        """
        取得資料庫連線並設定 Row factory

        Returns:
            資料庫連線物件
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self) -> None:
        """建立書籍資料表(若不存在)"""
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS llm_books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL UNIQUE,
                            author TEXT,
                            price INTEGER,
                            link TEXT
                        )
                    ''')
                    conn.commit()
        except sqlite3.Error as e:
            print(f"建立資料表時發生錯誤: {e}")
            raise

    def insert_books(self, books: List[Dict[str, any]]) -> int:
        """
        批次插入書籍資料(使用 INSERT OR IGNORE 避免重複)

        Args:
            books: 書籍資料列表,每個元素為包含 title, author,
                   price, link 的字典

        Returns:
            成功插入的書籍數量

        Raises:
            sqlite3.Error: 資料庫操作失敗時拋出
        """
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    # 記錄插入前的總數
                    cursor.execute('SELECT COUNT(*) as count FROM llm_books')
                    count_before = cursor.fetchone()['count']

                    # 批次插入書籍資料
                    for book in books:
                        cursor.execute('''
                            INSERT OR IGNORE INTO llm_books
                            (title, author, price, link)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            book['title'],
                            book['author'],
                            book['price'],
                            book['link']
                        ))

                    conn.commit()

                    # 記錄插入後的總數
                    cursor.execute('SELECT COUNT(*) as count FROM llm_books')
                    count_after = cursor.fetchone()['count']

                    # 返回實際新增的筆數
                    inserted_count = count_after - count_before
                    return inserted_count

        except sqlite3.Error as e:
            print(f"插入資料時發生錯誤: {e}")
            raise

    def search_by_title(self, keyword: str) -> List[Dict[str, any]]:
        """
        依書名模糊搜尋

        Args:
            keyword: 搜尋關鍵字

        Returns:
            符合條件的書籍列表,每個元素為包含書籍資訊的字典

        Raises:
            sqlite3.Error: 資料庫查詢失敗時拋出
        """
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute('''
                        SELECT id, title, author, price, link
                        FROM llm_books
                        WHERE title LIKE ?
                    ''', (f'%{keyword}%',))

                    results = cursor.fetchall()

                    # 使用 Row factory 可以直接以欄位名稱存取
                    books = []
                    for row in results:
                        books.append({
                            'id': row['id'],
                            'title': row['title'],
                            'author': row['author'],
                            'price': row['price'],
                            'link': row['link']
                        })

                    return books

        except sqlite3.Error as e:
            print(f"查詢資料時發生錯誤: {e}")
            raise

    def search_by_author(self, keyword: str) -> List[Dict[str, any]]:
        """
        依作者模糊搜尋

        Args:
            keyword: 搜尋關鍵字

        Returns:
            符合條件的書籍列表,每個元素為包含書籍資訊的字典

        Raises:
            sqlite3.Error: 資料庫查詢失敗時拋出
        """
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute('''
                        SELECT id, title, author, price, link
                        FROM llm_books
                        WHERE author LIKE ?
                    ''', (f'%{keyword}%',))

                    results = cursor.fetchall()

                    # 使用 Row factory 可以直接以欄位名稱存取
                    books = []
                    for row in results:
                        books.append({
                            'id': row['id'],
                            'title': row['title'],
                            'author': row['author'],
                            'price': row['price'],
                            'link': row['link']
                        })

                    return books

        except sqlite3.Error as e:
            print(f"查詢資料時發生錯誤: {e}")
            raise

    def get_all_books(self) -> List[Dict[str, any]]:
        """
        取得所有書籍資料

        Returns:
            所有書籍的列表,每個元素為包含書籍資訊的字典

        Raises:
            sqlite3.Error: 資料庫查詢失敗時拋出
        """
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute('''
                        SELECT id, title, author, price, link
                        FROM llm_books
                    ''')
                    results = cursor.fetchall()

                    books = []
                    for row in results:
                        books.append({
                            'id': row['id'],
                            'title': row['title'],
                            'author': row['author'],
                            'price': row['price'],
                            'link': row['link']
                        })

                    return books

        except sqlite3.Error as e:
            print(f"取得資料時發生錯誤: {e}")
            raise

    def get_book_count(self) -> int:
        """
        取得書籍總數

        Returns:
            資料庫中的書籍總數

        Raises:
            sqlite3.Error: 資料庫查詢失敗時拋出
        """
        try:
            with closing(self.get_connection()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(
                        'SELECT COUNT(*) as count FROM llm_books'
                    )
                    count = cursor.fetchone()['count']
                    return count

        except sqlite3.Error as e:
            print(f"取得書籍數量時發生錯誤: {e}")
            raise