# 對話紀錄：Python 排序演算法工具規格書討論與制定

---

## 訊息 1 (User)

請撰寫一個 Python 程式，將以下 3 種排序法包含其中：
Bubble Sort
Selection Sort  
Insertion Sort
使用者可以：
自由選擇任何一種排序方法，直到不再測試為止。
可選擇從小排到大，或從大排到小。
可以自行輸入任意一組數值，數值的個數可以彈性調整。
可以上傳一個 .csv 檔案，檔案內存有一組數值，程式讀取檔案時，會計算數值的個數。

請幫我以claude cowork可以理解的方式表示這個題目

---

## 訊息 2 (Assistant)

這是一份結構化、格式嚴謹的規格需求說明書（Specification Prompt），已針對 Claude Cowork / 程式協作模型進行最佳化，包含清晰的角色設定、輸入輸出介面規格、演算法要求與防呆機制，可直接複製貼給模型執行：

### **Task Specification: Interactive Sorting Algorithm Tool (Python)**

#### **1. Objective**
Develop an interactive command-line Python application that implements three classic sorting algorithms (**Bubble Sort**, **Selection Sort**, and **Insertion Sort**). The program must support flexible data input (manual console entry or CSV file upload/reading), flexible sorting directions (ascending/descending), and continuous execution via an interactive loop until explicitly terminated by the user.

#### **2. Core Requirements & Architecture**

##### **A. Sorting Algorithms Implementation**
Implement the following algorithms as standalone functions. Each function must accept a list of numbers (`List[float]` or `List[int]`) and a boolean flag `reverse: bool = False` (or equivalent) to control order:
1. `bubble_sort(arr: list, reverse: bool) -> list`
2. `selection_sort(arr: list, reverse: bool) -> list`
3. `insertion_sort(arr: list, reverse: bool) -> list`
*Note: Sort in-place on a copied list to prevent unintended side effects on the original input dataset.*

##### **B. Input Methods**
The user must be able to choose between two input modes:
1. **Manual Entry:**
   - Allow the user to input numbers separated by spaces, commas, or enters.
   - Dynamic length (no fixed limit on the number of elements).
   - Display the total count of numbers entered.
2. **CSV File Import:**
   - Prompt the user to provide a path to a `.csv` file.
   - Automatically parse numeric values (handling single-row, single-column, or grid format).
   - Count and print the total number of numeric elements extracted from the file before sorting.

##### **C. Sorting Configuration**
- **Direction:** Ascending (從小到大, `reverse=False`) or Descending (從大到小, `reverse=True`).
- **Algorithm Selection:** Bubble Sort, Selection Sort, or Insertion Sort.

##### **D. Control Flow (Main Loop)**
- Wrap the entire workflow in an interactive menu loop (`while True`).
- After each sort operation, display the **original data**, **element count**, **chosen configuration**, and **sorted result**.
- Provide an option to continue testing with new/existing data or exit cleanly.

##### **E. Validation & Edge Cases**
- Gracefully handle `FileNotFoundError` or unreadable CSV files.
- Reject or skip non-numeric strings with a clear warning prompt.
- Handle empty lists gracefully without crashing.

#### **3. Expected CLI Flow Example**
```text
==================================================
           SORTING ALGORITHM SUITE
==================================================
Select Input Method:
  1. Manual console input (space/comma-separated)
  2. Load from .csv file
  3. Exit program
> 2

Enter CSV file path: data.csv
[Success] Loaded 15 numbers from data.csv: [12, 45, 2, 88, 19, ...]

Select Sorting Algorithm:
  1. Bubble Sort
  2. Selection Sort
  3. Insertion Sort
> 1

Select Order:
  1. Ascending (Small to Large)
  2. Descending (Large to Small)
> 1

--------------------------------------------------
Original Count: 15
Algorithm: Bubble Sort
Direction: Ascending
Result: [2, 12, 19, 45, 88, ...]
--------------------------------------------------

Test another dataset or algorithm? (y/n): y
```

#### **4. Deliverables Expected from Claude**
1. Clean, PEP 8-compliant Python script.
2. Modular design with clear function separation (`csv_reader`, sorting algorithms, CLI handler).
3. Built-in standard library usage (`csv`, `os`, `sys`) without requiring external dependencies like `pandas` or `numpy` unless explicitly requested.

---

## 訊息 3 (User)

可以先給我中文版，我確認一下有甚麼問題

---

## 訊息 4 (Assistant)

這是一份繁體中文版的規格需求說明書（Specification Prompt），你可以直接拿去貼給 Claude 或其他 AI 協作，也可以先檢視是否有符合你的作業或專題要求：

### **任務需求說明書：互動式排序演算法工具（Python）**

#### **1. 專案目標**
使用 Python 開發一個互動式終端機（CLI）排序工具，包含 **氣泡排序（Bubble Sort）**、**選擇排序（Selection Sort）** 與 **插入排序（Insertion Sort）** 三種經典演算法。支援手動動態輸入與讀取 `.csv` 檔案兩種資料來源、正反向排序，並提供可反覆測試的互動式選單，直到使用者主動退出。

#### **2. 功能與架構規格**

##### **A. 排序演算法實作**
請將三種排序法分別寫成獨立函式。每個函式需接收一個數值列表（`List[float]` 或 `List[int]`）以及一個控制順序的布林參數 `reverse: bool = False`：
1. `bubble_sort(arr: list, reverse: bool) -> list`
2. `selection_sort(arr: list, reverse: bool) -> list`
3. `insertion_sort(arr: list, reverse: bool) -> list`
*注意：排序時需操作原陣列的複本（copy），避免改動到原始輸入資料。*

##### **B. 資料輸入方式**
提供兩種彈性輸入模式：
1. **自行輸入數值（手動輸入）：**
   - 支援以空格、逗號或換行分隔的一串數字。
   - 不限制元素數量，可彈性調整長度。
   - 輸入完成後，自動統計並印出目前輸入的數值個數。
2. **讀取 `.csv` 檔案：**
   - 提示使用者輸入 `.csv` 檔案的路徑。
   - 程式自動解析檔案內的數值（相容單欄、單列或多欄資料）。
   - 成功讀取後，自動計算並顯示該檔案內含有的數值總個數。

##### **C. 排序設定**
- **排序方向：** 由小排到大（遞增，`reverse=False`）或 由大排到小（遞減，`reverse=True`）。
- **演算法選擇：** 使用者可從三種排序法中自由挑選。

##### **D. 程式流程與持續測試（Main Loop）**
- 主程式需以迴圈架構（如 `while True`）包裝。
- 每次完成排序後，清楚列印出：**原始資料個數**、**所選演算法**、**排序方向** 與 **排序後的結果**。
- 提供提示詢問使用者是否要繼續（例如：「更換演算法」、「輸入新資料」或「退出程式」），直到使用者明確選擇結束為止。

##### **E. 防呆與異常處理**
- 當找不到指定的 `.csv` 檔案或檔案格式錯誤時，顯示友善提示而非直接報錯崩潰。
- 輸入資料若包含非數字字元，需有錯誤攔截機制。
- 處理空輸入或空列表的邊界狀況。

#### **3. 預期終端機互動範例（CLI Flow）**
```text
==================================================
              排序演算法測試工具
==================================================
請選擇資料輸入方式：
  1. 手動輸入一組數值（以空格或逗號分隔）
  2. 讀取 .csv 檔案
  3. 離開程式
> 2

請輸入 CSV 檔案路徑：test_data.csv
[讀取成功] 已從 test_data.csv 載入 15 個數值：[12, 45, 2, 88, 19, ...]

請選擇排序演算法：
  1. 氣泡排序 (Bubble Sort)
  2. 選擇排序 (Selection Sort)
  3. 插入排序 (Insertion Sort)
> 1

請選擇排序方向：
  1. 由小排到大 (遞增)
  2. 由大排到小 (遞減)
> 1

--------------------------------------------------
原始資料個數：15
使用演算法：Bubble Sort
排序方向：由小排到大
排序結果：[2, 12, 19, 45, 88, ...]
--------------------------------------------------

是否繼續測試其他資料或排序法？(y/n)：y
```

#### **4. 交付成果要求**
1. 程式碼需遵循 PEP 8 規範，並附上清晰註解。
2. 模組化設計（拆分檔案讀取、排序演算法、CLI 互動邏輯）。
3. 優先使用 Python 標準函式庫（如 `csv`、`sys`、`os`），不強求安裝第三方套件（如 pandas）。

---

## 訊息 5 (User)

預期終端機互動範例
這是甚麼

---

## 訊息 6 (Assistant)

簡單來說，**「預期終端機互動範例」就是模擬「這個程式在命令提示字元（黑底白字畫面 / Terminal）跑起來時，螢幕上會長什麼樣子」。**

它就像是**介面草圖（Mockup）**，把程式執行時：
* **電腦會印出什麼提示**（例如：`請選擇資料輸入方式：`、`請選擇排序演算法：`）
* **使用者會輸入什麼指令**（例如按 `1`、輸入檔名 `test_data.csv`、按 `y`）
* **最後算完會怎麼把結果秀出來**

一步一步預先演練給 AI 看。

### 為什麼要在需求裡放這個範例？
1. **避免 AI 做成你不想要的樣子：**
   如果只跟 AI 說「寫一個可以選擇排序法與檔案的程式」，AI 可能會寫成視窗軟體（GUI）或一次性執行腳本。
2. **精準控制操作體驗：**
   給出這個範例，AI 就會明確知道這是一個在終端機運作的互動式選單，且流程不會中途直接退出。

---

## 訊息 7 (User)

匯出成.md

---

## 訊息 8 (Assistant)

（已將中文規格需求說明書獨立輸出為 `sorting_tool_specification.md` 文件）