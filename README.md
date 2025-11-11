# 博客來 LLM 書籍管理系統
## 功能

-  **自動化爬蟲**: 自動爬取博客來 LLM 關鍵字的所有書籍資料
-  **分頁處理**: 智慧處理多頁搜尋結果
-  **資料儲存**: 將書籍資料儲存至 SQLite 資料庫
-  **彈性查詢**: 支援書名與作者的模糊搜尋
-  **去重機制**: 自動過濾重複的書籍資料
-  **友善介面**: 簡潔直觀的命令列操作介面

##  系統需求

- Python 3.8 或以上版本
- Google Chrome 瀏覽器
- ChromeDriver (與 Chrome 版本相容)
- 穩定的網路連線

##  安裝步驟

### 1. 複製專案

```bash
git clone https://github.com/your-username/books-scraper.git
cd books-scraper
```

### 2. 建立虛擬環境 

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 安裝 ChromeDriver

#### 方法一: 使用 webdriver-manager 

已包含在 requirements.txt 中,會自動下載對應版本的 ChromeDriver。

#### 方法二: 手動安裝

1. 檢查 Chrome 版本: 開啟 Chrome > 設定 > 關於 Chrome
2. 下載對應版本的 ChromeDriver: [ChromeDriver 下載頁面](https://chromedriver.chromium.org/downloads)
3. 將 ChromeDriver 放置於系統 PATH 中

##  使用方式

### 啟動程式

```bash
python app.py
```

### 主選單功能

程式啟動後會顯示主選單:

```
==================================================
博客來 LLM 書籍管理系統
==================================================
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
==================================================
```

### 1. 更新書籍資料庫

- 選擇選項 `1`
- 程式會自動爬取博客來所有 LLM 相關書籍
- 爬取完成後會顯示統計資訊

### 2. 查詢書籍

選擇選項 `2` 後,會進入查詢子選單:

#### 依書名查詢

```
請輸入書名關鍵字: OOO
```

#### 依作者查詢

```
請輸入作者關鍵字: OOO
```

### 3. 離開系統

選擇選項 `3` 結束程式。

## 專案結構

```
books-scraper/
│
├── app.py                 # 主程式 (命令列介面)
├── scraper.py             # 爬蟲模組
├── database.py            # 資料庫模組
│
├── requirements.txt       # 相依套件清單
├── README.md             # 專案說明文件
├── LICENSE               # 授權條款
├── .gitignore            # Git 忽略檔案清單
├── .gitattributes        # Git 屬性設定
│
└── books.db              # SQLite 資料庫 (執行後自動建立)
```

