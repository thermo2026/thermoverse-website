# ThermoVerse 網站字體與排版規範 (Typography & Design System Guidelines)

> **⚠️ 核心原則（不可變更 / IMMUTABLE DESIGN RULE）**  
> 參考任何外部設計截圖時，**僅限參考其版面佈局（Layout / 結構 / 區塊排列）**。  
> **嚴禁隨意替換或引入截圖中的字體、字型、全大寫壓縮標題或自定義小按鈕樣式。**  
> 全站所有頁面與後續開發均必須嚴格遵守本文件所訂定的字型、字級、字重、行距與色彩層級規範。

---

## 1. 唯一指定字型 (Font Family)

- **全站唯一無襯線幾何字型**：`'Outfit', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;`
- **Google Fonts 載入設定**：
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  ```
- **字型禁止事項**：禁止載入任何襯線體（Serif）、手寫體或與 Outfit 衝突的第三方字型。

---

## 2. 標準色彩體系 (Typographic Color System)

| 變數 / 色碼 | 名稱 | 使用情境 |
| :--- | :--- | :--- |
| `var(--ink)` (`#26343e` / `#0f172a`) | Primary Ink | 頁面大標題 (H1/H2)、卡片標題 (H3)、主要強調整文字 |
| `var(--muted)` (`#647078` / `#64748b`) | Slate Body | 區塊導言 (`.section-intro`)、內文段落、卡片說明文字 |
| `var(--coral)` (`#df4862` / `#f05a48`) | Thermo Coral | 眉標 (`.eyebrow`)、時間軸年份/節點、關鍵強調標籤、Hover 箭頭 |
| `#ffffff` | Pure White | 區塊背景、主要白色卡片、純白丸形按鈕文字或背景 |
| `rgba(15, 23, 42, 0.08)` | Border Line | 輕量分割線、卡片淺灰色邊框 |

---

## 3. 字體階層與大小大小規矩 (Hierarchy & Scale Rules)

### 3.1 頁面主標題 (Page Hero / H1)
- **HTML 標籤**：`<h1>`、`.hero h1`、`.page-hero h1`
- **字級 (Font Size)**：`clamp(2.5rem, 4.2vw, 4.5rem)`（手機版：`clamp(2.0rem, 8vw, 2.75rem)`）
- **字重 (Font Weight)**：`350`（極簡輕量幾何質感）
- **行高 (Line Height)**：`1.04`
- **字距 (Letter Spacing)**：`-0.025em`
- **外距 (Margin)**：`20px 0 28px`
- **顏色**：`var(--ink)`

### 3.2 區塊主標題 (Section Heading / H2)
- **HTML 標籤**：`<h2>`、`.section h2`、`.band h2`、`.timeline-header h2`
- **字級 (Font Size)**：`clamp(2.25rem, 2.8vw, 3rem)`（手機版：`clamp(1.75rem, 6.5vw, 2.25rem)`）
- **字重 (Font Weight)**：`350`（優雅大標，非粗黑全大寫）
- **行高 (Line Height)**：`1.15`
- **字距 (Letter Spacing)**：`-0.02em`
- **外距 (Margin)**：`0 0 16px`
- **文字大小寫**：標準英文大小寫（Sentence case / Title case），**禁止強制全大寫（UPPERCASE）與不自然換行（`<br>`）**。

### 3.3 中心展示主標題 (Centerpiece Display Title / H2)
- **HTML 標籤**：`.center-goals-title`（用於 Section 01 願景中心標題、Section 03 FAITHE 中心標題）
- **字級 (Font Size)**：`clamp(28px, 3.2vw, 38px)`
- **字重 (Font Weight)**：`800`（粗體大展視覺中心）
- **行高 (Line Height)**：`1.15`
- **字距 (Letter Spacing)**：`-0.02em`
- **顏色**：`#1e252b`

### 3.4 區塊眉標 (Eyebrow)
- **HTML 標籤**：`<div class="eyebrow">`
- **字級 (Font Size)**：`0.85rem`（約 13.6px）
- **字重 (Font Weight)**：`600` ~ `700`
- **字距 (Letter Spacing)**：`0.09em` ~ `0.12em`
- **文字大小寫**：`text-transform: uppercase;`
- **顏色**：`var(--coral)`（品牌珊瑚紅）
- **外距 (Margin)**：靠左標題一般為 `margin-bottom: 14px` ~ `16px`；三柱置中佈局為 `margin-bottom: 48px; text-align: center;`

### 3.5 區塊導言與內文 (Section Intro & Body)
- **HTML 標籤**：`<p class="section-intro">`、`.center-goals-subtitle`
- **字級 (Font Size)**：`1.02rem` ~ `1.08rem`（約 16px ~ 17.2px）
- **字重 (Font Weight)**：`400`（Regular），重要詞彙使用 `<strong>`（`font-weight: 600; color: var(--ink);`）
- **行高 (Line Height)**：`1.62` ~ `1.65`（保持呼吸感與絕佳易讀性）
- **顏色**：`#64748b`（Slate Gray）
- **最大寬度 (Max Width)**：一般限制在 `680px` ~ `740px`，防止行寬過長造成閱讀疲勞。

### 3.6 三柱展翼卡片標題與描述 (Triad Item Heading & Text)
- **標題標籤**：`<h3 class="goals-item-title">`
  - **字級**：`clamp(20px, 2.1vw, 25px)`
  - **字重**：`800`
  - **字距**：`-0.015em`
  - **顏色**：`#1e252b`（懸停時漸變為 `var(--coral)`）
- **指示箭頭**：`<span class="goals-item-arrow">`
  - **字級**：`18px`，`font-weight: 600`，懸停帶有 `transform: translateX(±6px)` 動態。
- **內文標籤**：`<p class="goals-item-desc">`
  - **字級**：`14.5px`
  - **行高**：`1.65`
  - **顏色**：`#556270`

### 3.6.1 軌道環繞卡片標題與徽章 (Orbit Card Title & Badge - Section 01)
- **卡片標題 (`.orbit-card-title`)**：
  - **字級**：`clamp(17px, 1.3vw, 20px)`（精緻和諧比例，嚴禁字體過大）
  - **字重**：`500`（Medium 典雅細緻，嚴禁粗黑失衡）
  - **字距**：`-0.01em`
  - **行高**：`1.3`
  - **色彩**：`var(--ink)`（**禁止懸停變紅，維持沉穩深色**）
- **右上角編號徽章 (`.orbit-card-badge`)**：
  - **字級**：`0.78rem`，`font-weight: 600`
  - **色彩**：中性淺灰 `#f8fafc` 底、灰邊框 `#e2e8f0`、灰文字 `#64748b`、小灰圓點 `#cbd5e1`（**禁止變紅**）
- **卡片內文 (`.orbit-card-desc`)**：
  - **字級**：`14px` ~ `14.5px`，`line-height: 1.6`，`color: #64748b`

### 3.6.2 FAITHE 展台字母與指針卡片 (FAITHE Stage Character & Pointer Cards - Section 03)
- **背部巨大描邊字母 (`.faithe-char`)**：
  - **字級**：`clamp(5.2rem, 7.6vw, 8.8rem)`，`font-weight: 800`，字體 `Outfit`。
  - **預設樣式**：透明文字 `color: transparent;`，帶有 `1.8px` 淺色描邊（`-webkit-text-stroke: 1.8px rgba(15, 23, 42, 0.22);`）。
  - **懸停／選中（點到變實心）**：`color: var(--ink); -webkit-text-stroke: 1.8px var(--ink); transform: translateY(-4px) scale(1.04);`，嚴禁變紅，轉為沉穩實心深色。
- **指示線與節點箭頭 (`.faithe-pointer`)**：
  - 高度 `44px`，包含圓點 (`.faithe-pointer-node`)、引導垂直實線 (`.faithe-pointer-stem`) 與向下箭頭 (`.faithe-pointer-arrow`)。
  - 懸停／選中時激活為珊瑚紅 `var(--coral)`。
- **原則卡片標題 (`.faithe-card-title`)**：
  - **字級**：`clamp(16px, 1.25vw, 19px)`，`font-weight: 500`（Medium），`color: var(--ink)`。
- **原則卡片內文 (`.faithe-card-desc`)**：
  - **字級**：`0.85rem`（約 13.6px），`line-height: 1.58`，`color: #64748b`。

### 3.6.3 人才培訓雙欄展台 (Workforce Showcase - Section 04)
- **區塊頂部大標 (`.workforce-header-title h2`)**：
  - **字級**：`clamp(2.25rem, 3.2vw, 3.25rem)`，`font-weight: 350`。
  - **副標斜體標註 (`.workforce-title-accent`)**：`font-style: italic; font-weight: 300; color: var(--ink);`。
- **數據指標卡片 (`.workforce-stat-num`)**：
  - **字級**：`clamp(3.5rem, 5.2vw, 5rem)`，`font-weight: 750`，`color: var(--ink)`。
  - **數據描述 (`.workforce-stat-caption`)**：`0.95rem`，`line-height: 1.58`，`color: #64748b`。
- **培訓學員頭像疊加 (`.workforce-avatar-stack`)**：
  - 圓形頭像 `48px x 48px`，白邊框 `border: 3px solid #ffffff`，負間距 `-12px` 重疊。
  - `+120` 更多標籤以珊瑚紅強調數字。
- **右側影音卡片 (`.workforce-media-card`)**：
  - 圓角 `24px`，右上方配置半透明毛玻璃播放圓形標章（`.workforce-play-badge`），左下角配置半透明深色膠囊標籤。

### 3.7 時間軸里程碑節點 (Milestones / Timeline)
- **節點編號 (`.timeline-step-num`)**：`1.45rem`，`font-weight: 500`，`color: var(--coral)`
- **年份日期 (`.timeline-step-date`)**：`0.72rem`，`font-weight: 750`，`letter-spacing: 0.1em; text-transform: uppercase; color: var(--coral);`
- **階段標題 (`.timeline-step-title`)**：`0.98rem`，`font-weight: 650`，`letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink); line-height: 1.35;`
- **精簡內文 (`.timeline-step-desc`)**：`0.88rem`（約 14px），`font-weight: 400`，`line-height: 1.55; color: #64748b;`（控制在 1～2 句核心事實，避免擁擠）。

### 3.8 導覽列與連結 (Navigation Links)
- **HTML 標籤**：`.nav-links a`
- **字級 (Font Size)**：`0.92rem`
- **字重 (Font Weight)**：`400` ~ `500`
- **顏色**：`rgba(255, 255, 255, 0.88)`（Dark Header）/ 懸停與當前頁面為 `var(--coral)`

### 3.9 丸形按鈕 (Pill Action Buttons)
- **HTML 標籤**：`.btn-pill`、`.button`、`.btn-pill.btn-outline`
- **字級 (Font Size)**：`0.92rem` ~ `0.95rem`
- **字重 (Font Weight)**：`600`
- **字距 (Letter Spacing)**：`0.02em`
- **外觀特徵**：高度至少 `48px`、內距 `12px 24px`、圓角 `border-radius: 999px`。
- **嚴禁事項**：**禁止隨意出現如「Go ↗」這類未經全站規範審查的非標準迷你圓形／膠囊按鈕**。

### 3.10 標籤膠囊 (Pill Tags)
- **HTML 標籤**：`.faithe-tag`、`.goals-pane-tag`
- **字級 (Font Size)**：`0.84rem`（約 13.5px）
- **字重 (Font Weight)**：`500`
- **內距與外觀**：`padding: 6px 14px; border-radius: 999px; background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155;`

---

## 4. 驗收核對清單 (Design Verification Checklist)

在任何程式碼提交前，必須嚴格檢查：
- [ ] 是否全站所有標題與內文均使用 `Outfit` 字型？
- [ ] 區塊主標題 `h2` 是否保持優雅的 `font-weight: 350`，而非粗黑全大寫或帶有不必要的大寫斷行？
- [ ] 區塊眉標是否為 `0.85rem`、珊瑚紅 `var(--coral)`、全大寫且帶有適當字距？
- [ ] 內文段落是否維持 `1.02rem` ~ `1.08rem`、行高 `1.62` ~ `1.65`、色彩為 `#64748b`？
- [ ] 是否已徹底排除非標準的 `Go ↗` 雜質按鈕？
- [ ] 在參考外部截圖時，是否僅借鑑其佈局結構，而完全保留本規範所規定的字型與大小？
