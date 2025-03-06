# 通訊錄管理系統

這是一個現代化的通訊錄管理系統，使用 Python 開發，具有圖形使用者介面（GUI）和完整的資料管理功能。

## 功能特點

- 新增聯絡人資料（姓名、電話、電子郵件、地址）
- 瀏覽所有聯絡人資料
- 更新現有聯絡人資料
- 刪除聯絡人資料
- 多功能搜尋系統
  - 支援按姓名搜尋
  - 支援按電話搜尋
  - 支援按電子郵件搜尋
  - 支援按地址搜尋
  - 支援全欄位搜尋
- 靈活的排序功能
  - 支援按任意欄位排序
  - 支援升序/降序切換
  - 可重置為預設排序順序

## 資料欄位限制

- 姓名：最多10個字元
- 電話：最多15個字元（僅允許數字）
- 電子郵件：最多20個字元
- 地址：最多50個字元

## 使用者介面特色

- 現代化深色主題設計
- 圓角按鈕和輸入框
- 清晰的視覺層次
- 直觀的操作方式
- 即時搜尋功能
- 排序狀態即時顯示

## 系統需求

- Python 3.6 或更高版本
- 必要的 Python 套件：
  - tkinter (通常包含在 Python 標準庫中)
  - typing (用於類型提示，通常包含在 Python 標準庫中)
  - json (用於資料儲存，通常包含在 Python 標準庫中)
  - os (用於檔案操作，通常包含在 Python 標準庫中)

## 安裝步驟

1. 確保已安裝 Python 3.6 或更高版本

2. 根據作業系統執行相應的安裝步驟：

   ### Windows

   - Python 安裝時通常已包含 tkinter
   - 直接執行程式即可

   ### macOS

   - 使用 Homebrew 安裝 Python（如果尚未安裝）：

     ```bash
     # 安裝 Homebrew（如果尚未安裝）
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

     # 安裝 Python
     brew install python
     ```

   - 安裝 tkinter（如果需要）：

     ```bash
     brew install python-tk@3.9  # 根據您的 Python 版本選擇
     ```

   ### Linux

   - Ubuntu/Debian：

     ```bash
     sudo apt-get install python3-tk
     ```

   - Fedora：

     ```bash
     sudo dnf install python3-tkinter
     ```

   - CentOS：

     ```bash
     sudo yum install python3-tkinter
     ```

3. 下載專案檔案並確保所有檔案在同一目錄下

4. 執行程式：

   ```bash
   # Windows
   python address_book_main.py

   # macOS/Linux
   python3 address_book_main.py
   ```

## 字體相容性說明

- Windows 預設使用 Microsoft JhengHei UI 字體
- macOS 和 Linux 系統會自動使用系統預設中文字體
  - macOS 可能使用 PingFang TC 或 Heiti TC
  - Linux 可能使用 Noto Sans CJK TC 或其他中文字體

如果遇到字體顯示問題，程式會自動使用系統可用的替代字體。

## 常見問題解決

1. macOS 執行時遇到權限問題：

   ```bash
   chmod +x address_book_main.py
   ```

2. 找不到 tkinter 模組：
   - 確認 Python 版本：

     ```bash
     python3 --version
     ```

   - 重新安裝 tkinter：

     ```bash
     brew reinstall python-tk@3.9  # 使用對應的 Python 版本
     ```

3. 字體顯示異常：
   - 檢查系統是否安裝了中文字體
   - 程式會自動使用系統可用的替代字體

## 使用方式

1. 確保所有檔案都在同一個目錄下
2. 執行主程式：

  ```bash
  python address_book_main.py
  ```

2. 基本操作：

   - 點擊「新增聯絡人」按鈕來新增資料
   - 在搜尋框輸入關鍵字進行搜尋
   - 使用下拉選單選擇搜尋類型
   - 點擊表格標題進行排序
   - 右鍵點擊聯絡人可進行編輯或刪除
   - 點擊「重置排序」回到預設排序順序

## 資料儲存

- 所有聯絡人資料會自動儲存在 `contacts.json` 檔案中
- 程式啟動時會自動載入既有的聯絡人資料
- 所有操作（新增、更新、刪除）都會即時儲存

## 檔案結構

專案包含以下關鍵檔案：

- `address_book_main.py`: 主程式入口點
- `models.py`: 資料模型（Contact 和 AddressBook 類別）
- `gui.py`: 圖形介面實現
- `widgets.py`: 自定義控件（按鈕和輸入框）
- `constants.py`: 常數設定（顏色主題等）
- `contacts.json`: 資料儲存檔案（自動生成）

## 注意事項

- 電話號碼僅允許輸入數字
- 所有欄位都是必填的
- 不允許重複的聯絡人姓名
