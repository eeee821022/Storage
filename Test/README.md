# UX 設計工具箱 (UX Design Toolbox)

一套實用的設計思考工具，協助您進行用戶研究、發想與資訊架構。所有工具均支援 JSON 匯入/匯出與截圖功能。

## 📦 包含的工具

### 1. 顧客旅程地圖 (Customer Journey Map)
視覺化顧客與產品互動的完整歷程，從接觸點到情感變化，幫助團隊發現痛點與機會點。

**核心功能：**
- 泳道設計
- 階段劃分
- 情感曲線追蹤

### 2. 曼陀羅思考法 (Mandala Chart)
從核心主題向八個方向發散思考的結構化發想工具，像蓮花般層層展開。

**核心功能：**
- 九宮格思考框架
- 多層次發想
- 顏色標記功能

### 3. 親和圖法 (Affinity Diagram)
透過分組與歸類，將大量零散的想法或資料組織成有意義的群組。

**核心功能：**
- 虛擬便利貼
- 拖曳分組
- 群組管理

## 🚀 快速開始

### 本地使用

1. 下載或 Clone 此專案：
```bash
git clone https://github.com/你的用戶名/ux-design-toolbox.git
cd ux-design-toolbox
```

2. 直接在瀏覽器中打開 `index.html` 即可使用

### GitHub Pages 部署

1. 在 GitHub 上創建新的 Repository

2. 上傳所有文件到 Repository

3. 在 Repository 設定中啟用 GitHub Pages：
   - 前往 `Settings` → `Pages`
   - Source 選擇 `main` branch
   - 保存後即可透過 `https://你的用戶名.github.io/repository名稱/` 訪問

## 📁 專案結構

建議的檔案結構如下：

```
ux-design-toolbox/
├── index.html                           # 主控制頁面
├── 1763304193199_網頁-使用者地圖.html     # 顧客旅程地圖工具
├── 1763304193199_網頁-曼陀羅思考法.html   # 曼陀羅思考法工具
├── 1763304193199_網頁-親和圖法.html       # 親和圖法工具
├── README.md                            # 專案說明文件
└── docs/                                # (選填) 文檔資料夾
    ├── 規格書-按鍵樣式_功能.txt
    └── 規格書-網頁樣式_功能.txt
```

**建議重新命名檔案**（以便於管理）：

```
ux-design-toolbox/
├── index.html
├── customer-journey-map.html     # 重新命名
├── mandala-chart.html            # 重新命名
├── affinity-diagram.html         # 重新命名
├── README.md
└── docs/
    ├── button-spec.txt
    └── design-spec.txt
```

如果您重新命名檔案，請記得同時修改 `index.html` 中的連結：
- `1763304193199_網頁-使用者地圖.html` → `customer-journey-map.html`
- `1763304193199_網頁-曼陀羅思考法.html` → `mandala-chart.html`
- `1763304193199_網頁-親和圖法.html` → `affinity-diagram.html`

## 🎨 設計系統

本專案採用統一的設計規範：

- **字型**：Inter、Noto Sans TC
- **色系**：Gray 中性色系 + Blue 主題色
- **框架**：Tailwind CSS
- **組件**：統一的按鈕樣式、彈窗、右鍵選單等

詳細設計規範請參考 `docs/` 資料夾中的規格書文件。

## 💾 資料匯入/匯出

所有工具都支援 JSON 格式的資料匯入與匯出：

1. **匯出**：點擊工具列的「匯出 JSON」按鈕，將當前工作內容儲存為 JSON 檔案
2. **匯入**：點擊「匯入 JSON」按鈕，選擇先前匯出的 JSON 檔案即可恢復工作

## 📸 截圖功能

每個工具都內建截圖功能，點擊「截圖」按鈕即可將當前畫面儲存為 PNG 圖片，方便分享與存檔。

## 🌐 瀏覽器支援

建議使用以下瀏覽器以獲得最佳體驗：
- Chrome / Edge (最新版)
- Firefox (最新版)
- Safari (最新版)

## 📝 授權

本專案採用 [MIT License](LICENSE)（您可以根據需要調整授權條款）

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request 來改善這個工具箱！

---

**開發者備註：** 本工具箱使用純前端技術開發（HTML + CSS + JavaScript），無需後端伺服器，所有資料都儲存在本地瀏覽器中。
