# GitHub Pages 部署指南

本指南將幫助您將 UX 設計工具箱部署到 GitHub Pages，讓您可以透過網址分享給團隊使用。

## 📋 前置準備

1. **GitHub 帳號**：如果還沒有，請先到 [github.com](https://github.com) 註冊
2. **專案檔案**：確保您已經準備好所有工具檔案

## 🚀 部署步驟

### 步驟 1️⃣：創建 GitHub Repository

1. 登入 GitHub
2. 點擊右上角的 `+` 號 → 選擇 `New repository`
3. 填寫 Repository 資訊：
   - **Repository name**：例如 `ux-design-toolbox`（這將成為您的網址一部分）
   - **Description**：例如「UX 設計思考工具箱」
   - **Public/Private**：選擇 `Public`（GitHub Pages 免費版需要 Public）
   - 勾選 `Add a README file`（或稍後手動加入）
4. 點擊 `Create repository`

### 步驟 2️⃣：上傳檔案到 Repository

#### 方法 A：透過網頁介面上傳（簡單）

1. 在 Repository 頁面，點擊 `Add file` → `Upload files`
2. 將以下檔案拖曳到上傳區：
   - `index.html`
   - `1763304193199_網頁-使用者地圖.html`（或重新命名後的檔案）
   - `1763304193199_網頁-曼陀羅思考法.html`
   - `1763304193199_網頁-親和圖法.html`
   - `README.md`
   - （選填）其他文檔檔案
3. 在頁面下方填寫 Commit message，例如：「Initial commit: 上傳 UX 工具箱」
4. 點擊 `Commit changes`

#### 方法 B：使用 Git 指令（進階）

```bash
# 1. Clone 你的 repository
git clone https://github.com/你的用戶名/ux-design-toolbox.git
cd ux-design-toolbox

# 2. 將所有檔案複製到這個資料夾

# 3. 加入檔案到 Git
git add .

# 4. 提交變更
git commit -m "Initial commit: 上傳 UX 工具箱"

# 5. 推送到 GitHub
git push origin main
```

### 步驟 3️⃣：啟用 GitHub Pages

1. 在 Repository 頁面，點擊 `Settings`（齒輪圖示）
2. 在左側選單找到 `Pages`
3. 在 **Source** 區域：
   - Branch: 選擇 `main`
   - Folder: 選擇 `/ (root)`
4. 點擊 `Save`
5. 等待約 1-2 分鐘，頁面會顯示部署成功的訊息

### 步驟 4️⃣：訪問您的工具箱

部署完成後，您的工具箱將可以透過以下網址訪問：

```
https://你的用戶名.github.io/ux-design-toolbox/
```

例如，如果您的 GitHub 用戶名是 `johndoe`，Repository 名稱是 `ux-design-toolbox`，則網址為：
```
https://johndoe.github.io/ux-design-toolbox/
```

## 🔄 更新部署內容

當您修改了工具檔案並想要更新線上版本時：

### 方法 A：透過網頁介面

1. 在 Repository 中找到要修改的檔案
2. 點擊檔案，然後點擊鉛筆圖示 ✏️ 進行編輯
3. 或點擊 `Add file` → `Upload files` 上傳新版本（會覆蓋舊檔案）
4. 提交變更後，GitHub Pages 會自動重新部署（約 1-2 分鐘）

### 方法 B：使用 Git 指令

```bash
# 1. 進入專案資料夾
cd ux-design-toolbox

# 2. 修改檔案後，加入變更
git add .

# 3. 提交變更
git commit -m "描述您的變更內容"

# 4. 推送到 GitHub
git push origin main
```

## ⚙️ 進階設定（選填）

### 自訂網域名稱

如果您有自己的網域名稱（例如 `tools.yourcompany.com`），可以設定：

1. 在 GitHub Pages 設定頁面，找到 **Custom domain** 區域
2. 輸入您的網域名稱
3. 在您的網域 DNS 設定中新增 CNAME 記錄指向 `你的用戶名.github.io`
4. 等待 DNS 生效（可能需要數小時）

詳細步驟請參考：[GitHub 官方文檔](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

### 使用 HTTPS

GitHub Pages 預設已啟用 HTTPS，無需額外設定。

## 🐛 常見問題

### Q1: 為什麼我的頁面顯示 404？

**可能原因：**
- GitHub Pages 尚未完成部署（請等待 1-2 分鐘）
- Branch 或 Folder 設定錯誤（請檢查 Settings → Pages）
- Repository 設為 Private（免費版 GitHub Pages 需要 Public）

### Q2: 我修改了檔案，但線上版本沒有更新？

**解決方法：**
- 清除瀏覽器快取後重新整理（Ctrl + Shift + R 或 Cmd + Shift + R）
- 等待幾分鐘讓 GitHub Pages 重新部署
- 確認您的變更已成功推送到 GitHub

### Q3: 工具的連結點擊後出現 404？

**可能原因：**
- 檔案名稱與 `index.html` 中的連結不一致
- 檔案未成功上傳到 GitHub

**解決方法：**
- 檢查 Repository 中是否有所有工具檔案
- 確認 `index.html` 中的 `href` 與實際檔案名稱完全一致

### Q4: 可以設為私密但仍然分享給團隊嗎？

**方法一（推薦）：**
將 Repository 設為 Public，但不公開分享網址

**方法二（需付費）：**
升級到 GitHub Pro，可以在 Private Repository 使用 GitHub Pages

**方法三（替代方案）：**
使用其他託管服務，如 Netlify、Vercel，它們提供免費的私密部署

## 📞 需要協助？

- GitHub Pages 官方文檔：https://docs.github.com/pages
- GitHub 社群論壇：https://github.community/
- Git 基礎教學：https://git-scm.com/book/zh-tw/v2

---

🎉 **恭喜！** 您的 UX 設計工具箱現在已經成功部署到 GitHub Pages，可以隨時隨地透過網址存取了！
