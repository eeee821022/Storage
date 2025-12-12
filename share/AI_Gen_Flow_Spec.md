# AI Gen Flow - 完整系統功能與操作手冊 (Full System Manual)

本文件詳細定義「AI Gen Flow」網頁應用程式中所有按鈕、區塊、互動邏輯與底層運作流程。本系統旨在透過視覺化節點編輯器，實現「結構化參數 -> AI 敘事轉譯 -> 影像生成」的自動化工作流。

---

## 1. 全域介面佈局 (Global Interface)

### 1.1 頂部工具列 (Top Toolbar)
*   **位置**：畫面頂部中央偏左。
*   **功能**：全域畫布操作。
*   **按鈕詳解**：
    *   **清空畫布 (Clear)**：
        *   **圖示**：垃圾桶圖示。
        *   **行為**：立即刪除畫布上所有節點與連線，重置 `nodes` 與 `connections` 陣列，將 `nextNodeId` 重置為 1。
    *   **匯入 (Import)**：
        *   **圖示**：上傳箭頭。
        *   **行為**：觸發檔案選擇視窗，僅接受 `.json` 格式。讀取 JSON 後，解析 `nodes` 與 `connections` 結構，並在畫布上重建完整的工作流佈局。
    *   **匯出 (Export)**：
        *   **圖示**：下載箭頭。
        *   **行為**：將當前畫布上的所有節點狀態 (位置、類型、內部參數值) 與連線關係打包為 JSON 檔案，並觸發瀏覽器下載，檔名格式為 `workflow_[timestamp].json`。

### 1.2 左側元件庫 (Sidebar)
*   **位置**：畫面左側，預設寬度 260px。
*   **功能**：容納所有可用的功能節點 (Nodes)。
*   **互動邏輯**：
    *   **拖曳生成 (Drag & Drop)**：使用者按住任一項目 (如 "生成核心") 拖曳至中央畫布，放開滑鼠後，系統會讀取該項目的 `data-type` 屬性，並在落點座標呼叫 `createNode()` 函式生成對應的 DOM 結構。
    *   **收折按鈕**：位於 Sidebar 右上角，點擊可收起/展開側邊欄，增加畫布可視空間。

### 1.3 中央無限畫布 (Infinite Canvas)
*   **位置**：畫面中央佔據主要區域 (`#board-container`)。
*   **功能**：節點編輯與連線操作的工作區。
*   **互動邏輯**：
    *   **平移 (Pan)**：按住 `空白鍵 (Space)` + `左鍵拖曳`，或直接使用 `滑鼠中鍵` 拖曳，可移動畫布視角。
    *   **縮放 (Zoom)**：使用 `滑鼠滾輪` 可放大/縮小畫布 (Scale 0.1x ~ 3.0x)。
    *   **連線 (Connection)**：
        1.  點擊任一節點右側的 **輸出點 (Output Socket)**。
        2.  拖曳虛線至另一節點左側的 **輸入點 (Input Socket)**。
        3.  放開滑鼠，若邏輯合法 (Output -> Input)，系統會繪製一條貝茲曲線 (Bezier Curve) 連接兩者，並在程式內部建立 `connections` 關聯。
    *   **刪除 (Delete)**：點擊選取節點或連線 (變為紅色/藍色高亮)，按下 `Delete` 或 `Backspace` 鍵移除。
    *   **複製貼上 (Copy/Paste)**：
        *   `Ctrl+C`：複製選取的節點 (僅複製類型與基本參數)。
        *   `Ctrl+V`：在滑鼠游標處貼上節點。亦支援直接 `Ctrl+V` 貼上剪貼簿中的圖片，系統會自動建立一個包含該圖片的 **Image Node**。

### 1.4 右側生成控制台 (Result Sidebar)
*   **位置**：畫面右側，預設隱藏，生成時自動滑出。
*   **功能**：顯示 API 執行狀態、進度條與最終生成的圖片結果。
*   **區塊結構**：
    *   **Header**：顯示 "生成控制台" 標題與關閉按鈕。
    *   **Drafts Grid**：圖片生成的容器 (`#drafts-grid`)，API 回傳的圖片會動態插入此處。
    *   **Debug Info**：摺疊選單，顯示當前傳送給 API 的 System Prompt 長度與內容。

---

## 2. 節點功能詳解 (Node Details)

### 2.1 核心邏輯節點 (Core Logic Nodes)

#### **A. 生成核心 (Generator Node)**
*   **定義**：整個工作流的「大腦」，負責彙整所有上游參數。
*   **輸入端 (Inputs)**：
    *   `Model`, `Prompt`, `Negative`, `Image`, `Style`, `Layout`, `Camera`。
*   **內部參數**：
    *   **Refresh 按鈕**：點擊後，系統會執行 `collectNodeData()`，將所有連接到此節點的參數組裝成 JSON，並顯示在下方的預覽框中 (僅供除錯確認)。此預覽框內的文字 (`generated_prompt`) 若被修改，將作為轉譯的主要依據。
*   **數據彙整與 Prompt 組合邏輯 (Data Aggregation & Logic)**：
    當點擊 Refresh 或被下游節點讀取時，系統會執行以下彙整：
    1.  **文字參數 (Text Parameters)**：
        *   **Main Prompt**: 來自 `Prompt Node` 的主要描述。
        *   **Negative**: 來自 `Negative Node`，前綴加上 "Negative: "。
        *   **Style**: 來自 `Style Node` 的風格描述，前綴加上 "Style: "。
        *   **Camera**: 來自 `Camera Node` 的鏡頭參數，前綴加上 "Camera: "。
        *   **Layout**: 來自 `Layout Node` 的構圖參數，前綴加上 "Layout: "。
    2.  **視覺參數 (Visual Parameters)**：
        *   **Reference Images**: 若 Style/Layout/Camera 節點有連接 `Reference Node`，系統會讀取圖片的 Base64 編碼、權重 (Weight) 與類型 (Type)，並打包進對應的 JSON 物件中 (例如 `style.reference`)。
        *   **Input Images**: 若 Generator 直接連接 `Image Node` 或 `3D Node`，圖片 Base64 數據會被收集至 `images` 陣列，用於圖生圖 (Image-to-Image) 或 ControlNet 應用。
    *   **最終文字預覽範例** (僅顯示文字部分)：
        ```text
        A futuristic city with flying cars
        Negative: blur, low quality
        Style: Cyberpunk, neon lights
        Camera: Wide angle lens, 24mm
        Layout: 16:9 aspect ratio
        [Visual Data Attached: 2 Reference Images, 1 Input Image]
        ```
*   **運作原理**：此節點本身不呼叫 API，它的作用是作為「數據聚合點」，供下游的 Instruction Node 讀取。

#### **B. AI 指令建構 (Instruction Node) - [轉譯階段]**
*   **定義**：第一階段 AI 處理，負責將「結構化參數」轉譯為「敘事性 Prompt」。
*   **輸入端**：必須連接至 `Generator Node`。
*   **關鍵按鈕**：**「生成轉譯指令 (Build)」**
    *   **觸發行為**：
        1.  **追蹤數據**：沿著連線回溯找到 `Generator Node`，並遞迴收集所有參數 (Style, Camera, Ref Images...)。
        2.  **鎖定 UI**：按鈕變為 Loading 轉圈動畫，防止重複點擊。
        3.  **API 呼叫**：將收集到的 JSON 數據 + 內建的 System Prompt (Nano Banana Guide) 發送至 **Gemini 2.0 Flash Exp** 模型。
        4.  **回填結果**：API 回傳的「敘事性 Prompt」會自動填入節點下方的 `<textarea>`。
*   **手動介入**：使用者可以在 `<textarea>` 中直接修改 AI 轉譯出來的文字，下游節點會讀取修改後的版本。

#### **C. 啟動按鈕 (Trigger Node) - [生成階段]**
*   **定義**：第二階段 AI 處理，負責執行最終生圖。
*   **輸入端**：必須連接至 `Instruction Node`。
*   **參數控制**：
    *   **Chaos (滑桿)**：0-100，控制生成的變異程度 (Chaos/Creativity)。
    *   **Count (輸入框)**：1-8，控制一次生成的圖片數量 (預設 4)。
*   **關鍵按鈕**：**「START」**
    *   **觸發行為**：
        1.  **獲取 Prompt**：讀取上游 `Instruction Node` 文字框內的最終內容。
        2.  **開啟控制台**：自動展開右側 Result Sidebar。
        3.  **顯示狀態**：在控制台中顯示 "AI 正在繪製中..." 動畫。
        4.  **API 呼叫**：將 Prompt 發送至 **Gemini 2.5 Flash Image Preview** (或 Imagen) 模型。
        5.  **渲染結果**：接收 API 回傳的 Base64 影像數據，建立 `<img>` 標籤並插入控制台。

### 2.2 參數與資源節點 (Parameter & Resource Nodes)

#### **D. 模型選擇 (Model Node)**
*   **功能**：指定生成使用的底層模型。
*   **選項**：
    *   `Imagen 4 (Text to Image)`: 高品質寫實生成。
    *   `gemini-2.5-flash-image-preview`: 快速預覽與圖生圖功能。
*   **輸出**：`Model ID` 字串，供 Generator 收集。

#### **E. AI Prompt / 負面提示 (Prompt / Negative Nodes)**
*   **AI Prompt**：
    *   **元件**：大型文字框 (`<textarea>`)。
    *   **功能**：輸入主要的畫面描述 (主體、動作、場景)。
*   **負面提示 (Negative)**：
    *   **元件**：文字框。
    *   **功能**：輸入不希望出現的元素 (如 "blur, distortion, low quality")。
    *   **備註**：系統會將此內容標記為 `negative_prompts` 欄位傳送給轉譯 AI。

#### **F. 風格設定 (Style Node)**
*   **功能**：快速套用預設藝術風格。
*   **動態載入**：選項內容由外部 `styles.json` 定義，可透過 GitHub 遠端更新。
*   **互動元件**：
    *   **下拉選單 (Dropdown)**：包含多個分類 (動畫風格, 藝術流派, 插畫設計, 攝影寫實)。
        *   *例*：Cyberpunk, Studio Ghibli, Impressionism, Photorealistic (8k, bokeh)。
    *   **文字框 (Textarea)**：選擇下拉選單後，對應的 Prompt 會自動填入此處。使用者可在此基礎上進行修改或追加關鍵字。

#### **G. 鏡頭與光影 (Camera Node)**
*   **功能**：設定攝影機參數與光照氛圍。
*   **動態載入**：選項內容由外部 `cameras.json` 定義。
*   **互動元件**：
    *   **視角 (View)**：Eye Level, Low Angle, High Angle, Bird's Eye, Worm's Eye。
    *   **光影 (Lighting)**：Golden Hour, Studio, Cinematic, Neon, Natural。
    *   **鏡頭 (Lens)**：Wide Angle (24mm), Portrait (85mm), Macro, Fisheye。
    *   **連動**：所有選擇會組合成一段描述字串 (如 "Low angle shot, Cinematic lighting, Wide angle lens") 顯示於下方文字框。

#### **H. 構圖與版面 (Layout Node)**
*   **功能**：設定圖片比例與構圖方式。
*   **動態載入**：選項內容由外部 `layouts.json` 定義。
*   **互動元件**：
    *   **比例 (Aspect Ratio)**：1:1 (Square), 16:9 (Landscape), 9:16 (Portrait), 21:9 (Cinematic)。
    *   **構圖 (Composition)**：Minimalist (極簡), Knolling (平鋪), Isometric (等角), Comic Panel (漫畫分鏡), Symmetrical (對稱)。
    *   **連動**：選擇後自動組合成描述字串。

#### **I. 參考素材 (Reference Node)**
*   **功能**：提供圖片給 AI 參考 (Style/Character/Composition)。
*   **互動**：
    *   **上傳區**：點擊 "+" 號或拖曳圖片至此，支援多張圖片。
    *   **類型選擇**：下拉選單選擇參考類型 (Style, Character, Composition, Content)。
    *   **權重滑桿**：設定參考強度 (0.0 - 1.0)。
*   **數據流**：被 Generator 收集時，會將 Base64 數據與類型標籤一同打包。

#### **J. 圖片輸入 (Image Node)**
*   **功能**：作為圖生圖 (Image-to-Image) 的底圖來源。
*   **架構設計**：採用「Prompt 綁定素材」架構。
*   **互動**：
    *   **上傳區**：點擊上傳或直接貼上 (`Ctrl+V`) 圖片。
    *   **專屬描述框 (Bound Prompt)**：節點內建文字框，用於輸入「針對這張特定圖片」的描述。此設計解決了多圖輸入時，API 無法判斷 Prompt 對應關係的問題。

#### **K. 3D 預覽 (3D Node)**
*   **功能**：載入 GLB 模型輔助構圖。
*   **架構設計**：採用「Prompt 綁定素材」架構。
*   **互動**：
    *   **上傳按鈕**：選擇本機 `.glb` / `.gltf` 檔案 (Max 100MB)。
    *   **3D 檢視器**：使用 Three.js (動態載入) 渲染模型，支援旋轉/縮放視角。
    *   **截圖 (Snapshot)**：點擊後，當前畫面會被轉存為 2D 圖片。
    *   **連線指引**：截圖後，必須將節點右側的 `Snapshot` 輸出點連接至 `Generator Node` 的 `Image` 插槽，或 `Paint Node` 的 `Input`。
    *   **專屬描述框 (Bound Prompt)**：輸入針對此 3D 場景的描述，與截圖一同打包傳送。

#### L. 智能繪圖 (Smart Paint Node)
*   **功能**：提供可繪圖的畫布，支援塗改 (Inpainting) 或手繪草圖。
*   **互動元件**：
    *   **畫布 (Canvas)**：可直接繪圖。若 `img_in` 有連接圖片 (如 3D Snapshot)，該圖會顯示為半透明背景供描繪。
    *   **筆刷控制**：可調整顏色與粗細。
    *   **塗改用意 (Intent)**：輸入框。使用者輸入該顏色的代表意義 (例如 "mask area", "remove object")。
*   **Prompt 自動生成**：系統會自動將「筆刷色碼」與「用意」組合成一段 Prompt (例如 `[Annotation]: Color #ff00ff represents "mask area"`)，讓 AI 理解繪圖內容。
*   **數據流**：輸出合併後的圖片 (背景+筆跡) 與生成的 Prompt。

#### M. 骨架姿勢 (Pose Node)
*   **功能**：提供 2D 骨架編輯與匯出功能，用於精確控制角色動作 (ControlNet)。
*   **模組化設計**：
    *   **預覽窗**：節點本身僅顯示縮小的預覽 Canvas。
    *   **模態編輯器 (Modal Editor)**：點擊預覽圖會開啟全螢幕的「骨架編輯器」。
*   **編輯器功能**：
    *   **2D CAD 操作**：支援新增/刪除骨架線段與節點。
    *   **底圖參照**：可上傳底圖並調整透明度/位置，方便描繪動作。
    *   **AI 姿勢捕捉 (AI Capture)**：點擊「AI 捕捉姿勢」按鈕，系統將上傳底圖至 Gemini Vision API，自動分析人體結構並產生對應的骨架數據。
    *   **自動吸附**：拖曳節點時會自動吸附鄰近端點。
*   **數據流**：
    *   **Canvas 輸出**：將編輯好的骨架 Canvas 轉為 Base64 圖片 (`inputs.images`).
    *   **JSON 儲存**：原始骨架數據儲存於 `dataset.skeleton` 供再次編輯。
    *   **自動提示**：匯出時自動附加 "Reference Pose: Use this skeleton..." 描述。

---

## 3. 完整操作流程 (Step-by-Step Workflow)

### 步驟 1: 搭建工作流 (Setup)
1.  從左側拖曳 **Generator Node** 到畫布中央。
2.  拖曳 **Instruction Node**，將其 Input 連接至 Generator 的 Output。
3.  拖曳 **Trigger Node**，將其 Input 連接至 Instruction 的 Output。
4.  (選用) 拖曳 **Style Node**、**Prompt Node** 等，連接至 Generator 的對應 Input。

### 步驟 2: 設定參數 (Configuration)
1.  在 **Prompt Node** 輸入主要描述 (例如 "A futuristic city")。
2.  在 **Style Node** 選擇風格 (例如 "Cyberpunk")。
3.  (選用) 在 **Reference Node** 上傳參考圖。

### 步驟 3: 執行轉譯 (Translation)
1.  點擊 **Instruction Node** 上的 **"生成轉譯指令 (Build)"** 按鈕。
2.  等待約 1-2 秒，按鈕轉圈結束。
3.  檢視下方文字框，確認 AI 是否已將 "A futuristic city, Cyberpunk" 擴寫為一段詳細的敘事性描述。
4.  (若需要) 手動微調文字框內的描述。

### 步驟 4: 執行生成 (Generation)
1.  點擊 **Trigger Node** 上的 **"START"** 按鈕。
2.  右側 **Result Sidebar** 自動滑出。
3.  等待約 3-5 秒，AI 生成的圖片將直接顯示在右側面板中。
4.  點擊圖片可放大檢視，或使用下方的「下載/複製」按鈕保存結果。

---

## 4. 技術實作細節 (Technical Implementation)

### 4.1 數據收集機制 (`collectNodeData`)
*   **核心邏輯**：系統採用 **逆向遞迴 (Reverse Recursion)** 方式收集數據。
*   **多圖對應架構 (Image-Prompt Binding)**：
    *   **Image/3D Node**：打包 `src` (Base64) 與 `prompt`。
    *   **Pose Node (New)**：
        *   偵測 `.pose-preview-canvas` 元素與 `dataset.skeleton` 數據。
        *   使用 `canvas.toDataURL()` 將當前骨架預覽轉為 PNG Base64。
        *   自動附加 Prompt: `"Reference Pose: Use this skeleton image..."`。
*   **流程**：`buildInstruction` 或 `refreshGenerator` 觸發時，遍歷連線收集所有參數至 JSON 物件。

### 4.2 API 呼叫規格
*   **環境適配 (Environment Logic)**：
    *   **API Key 處理**：系統會自動檢查 `apiKey` 變數。
        *   若 `apiKey` 有值 (本機開發)，URL 附加 `?key=...`。
        *   若 `apiKey` 為空 (Canvas 環境)，URL **不附加** `key` 參數，依賴環境 Proxy 自動驗證。
*   **轉譯 API**:
    *   **URL**: `.../models/gemini-2.5-flash-preview-09-2025:generateContent`
    *   **Payload**: 包含 System Prompt (來自 `prompts.json`) 與 User Config JSON。
*   **生圖 API**:
    *   **URL**: `.../models/[MODEL_ID]:generateContent` (或 `:predict` for Imagen)。
    *   **Payload**: Base64 圖片作為 Inline Data 傳送。
*   **AI 骨架捕捉 (Pose Estimation)**:
    *   **URL**: `.../models/gemini-2.5-flash-preview-09-2025:generateContent`
    *   **Payload**: 圖片 + System Prompt (要求回傳符合 `POSE_SCHEMA` 的 JSON)。

### 4.3 外部設定檔 (External Configuration)
*   **機制**：系統啟動時 (`loadAllConfigs`)，並行讀取 GitHub 上的 JSON 設定檔。
*   **來源 (Source)**：
    *   **Base URL**: `https://raw.githubusercontent.com/eeee821022/Storage/main/share/AI_Gen_Flow/`
    *   **Fallback**: 若 Fetch 失敗，自動切換使用程式碼內建的預設值 (Hardcoded Fallback Constants)，確保離線或 GitHub 連線異常時仍可運作。
*   **設定檔列表**：
    1.  `prompts.json`: 定義 System Prompts (Precise / Simple 模式)。
    2.  `models.json`: 定義可用模型列表 (Imagen 4, Gemini 2.5 Flash)。
    3.  `styles.json`: 定義風格選項。
    4.  `layouts.json`: 定義構圖選項。
    5.  `cameras.json`: 定義鏡頭選項。
    6.  `reference-types.json`: 定義參考圖類型 (Style, Character 等)。
    7.  `defaults.json`: 定義節點預設值 (尚未完全啟用)。


