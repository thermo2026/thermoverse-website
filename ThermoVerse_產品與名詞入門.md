# ThermoVerse 產品與名詞入門

給 Rome 的專案入門說明｜2026-09-10｜約 15–20 分鐘

這份文件幫你理解產品、看懂網站內容，以及與公司討論時知道該問什麼。依據資料夾內的網站規劃、SOW 原始文件，以及文末列出的技術機構資料整理。**公司文件中的產品描述，不等於已取得測試證明或正式發布核准。**

## 1. 先記住這三件事

1. **ThermoVerse 是公司，LATCHES 是它開發的技術／產品。**
2. **公司有兩個主要方向：Energy Services（能源服務）與 LATCHES（熱能儲存）。** 網站要同時讓訪客看懂服務與產品。
3. **LATCHES 的重點是管理建築的熱與空調負載。** 不能直接把它當成停電時供應插座電力的行動電源。

你可以先這樣介紹：

> ThermoVerse 提供建築能源評估與改善服務，也開發名為 LATCHES 的熱能儲存技術。它希望透過材料、感測與控制，配合建築空調調整熱能儲存和釋放的時機，協助管理尖峰負載與室內舒適度。目前網站也要招募適合進行概念驗證的場域合作夥伴。

英文工作草稿：

> ThermoVerse provides building energy services and is developing LATCHES, a thermal energy storage technology. LATCHES combines thermal storage, sensing and control to help manage building HVAC loads and indoor comfort. The company is also seeking site partners to evaluate the technology through proof-of-concept projects.

這段適合先幫你掌握方向；正式對外版本仍依公司核准文字。

## 2. 公司到底提供什麼？

| 方向 | 白話理解 | 對方會找它做什麼？ |
|---|---|---|
| Energy Services | 幫建築做能源健檢，找出改善方式 | 評估能源使用、空調與機電問題，規劃改善工程 |
| LATCHES | 開發可以控制熱能儲存與釋放時機的建築技術 | 討論技術整合、場域條件與 POC 驗證 |
| FACES Workforce Program | 能源相關的人才培育計畫 | 登記參與意願或洽談培訓合作 |

網站 Guidelines 把 Energy Services 描述為目前的服務營收方向，把 LATCHES 描述為技術創新方向。這是文件中的商業定位；本次沒有查核實際營收、客戶數或出貨數。

能源服務可以先讓公司了解一棟建築的現況，再判斷哪些改善適合它，以及是否適合驗證 LATCHES。但**不是每次能源評估都必須導入 LATCHES**。

## 3. LATCHES 要解決什麼問題？

想像一棟辦公大樓：下午天氣熱、人多、設備也都在運轉，空調需求集中在同一段時間。管理者需要兼顧室內舒適度、設備運轉與能源費用。

這裡有三個不同目標：

| 目標 | 代表什麼 | 常見誤解 |
|---|---|---|
| 降低總用電量 | 一段時間累計消耗較少電能，常用 kWh 表示 | 降低尖峰不一定代表整天都用更少電 |
| 降低尖峰負載 | 讓最吃電的時段不那麼集中，功率常用 kW 表示 | 不能把尖峰下降比例直接當成整張電費下降比例 |
| 維持舒適度 | 管理室內溫度等條件，讓人可以正常使用空間 | 不是只要關掉空調就算改善成功 |

**純教學例子，並非 LATCHES 測試結果：** 某建築把下午尖峰從 100 kW 降到 80 kW，代表該比較條件下尖峰功率減少 20%；不能據此說每天省電 20%，也不能保證電費省 20%。仍要看累計用電、運轉時間及適用電價。

## 4. 它怎麼運作？先用三個部分理解

```text
感測建築／空調與儲熱狀態
              ↓
控制器判斷何時儲存或釋放熱能
              ↓
熱能儲存材料與建築環境交換熱能
              ↓
配合 HVAC／建築控制，管理負載與舒適度
```

這是依文件整理的概念流程，**不是設備接線圖，也沒有證實每個控制細節已完成**。

### A. 儲存：PCM 是承接熱能的材料

PCM 是 Phase Change Material（相變材料）。它利用材料改變相態時吸收或釋放熱能的特性來儲熱。

生活類比：冰塊融化時會吸收熱，冰還沒完全融完前，可以持續提供冷卻效果。這只是說明相變概念，**不表示 LATCHES 使用冰，也不表示已知道它的材料配方**。

### B. 感測：知道現在的狀態

控制系統需要掌握建築與設備條件，也需要估計熱能儲存的狀態。文件使用 State-of-Charge Monitor & Controller 這個名稱。

可以先把它理解成「狀態表＋控制中樞」。實際量測哪些訊號、準確度如何，以及怎麼換算剩餘可用熱能，仍須工程團隊說明。

### C. 控制：決定什麼時候使用

一般儲熱材料會隨環境條件交換熱能；LATCHES 文件強調感測與可控制的時間安排，希望配合建築需求使用儲存的熱能。

文件也提到 predictive edge controller（預測式邊緣控制器）。這表示它的設計方向包含靠近設備端的判斷與控制；**不能僅憑這個名稱就說它使用特定 AI 模型、完全不需網路，或能自動適用所有建築**。

## 5. 熱電池與一般電池差在哪？

| 比較 | 建築熱能儲存 | 一般電化學電池儲能 |
|---|---|---|
| 主要儲存形式 | 熱能／可供冷暖需求使用的熱狀態 | 電化學能 |
| 使用方式 | 透過熱交換支援冷暖需求 | 放電後供應電力 |
| 本案溝通重點 | 空調負載、熱流與室內環境 | 若比較，需要明確限定用途與條件 |
| 不能直接推論 | 能供應插座電力或取代所有備援電池 | 所有產品都受相同限制或有相同風險 |

美國能源部把建築熱能儲存描述為可以儲存熱能，並在需要時直接用來調節建築溫度的方式。這支持的是一般技術原理，並非 LATCHES 的個別性能證明。[DOE：Thermal Energy Storage](https://www.energy.gov/cmei/buildings/thermal-energy-storage)

## 6. 網站必懂的名詞

| 名詞 | 中文／白話 | 在本案的意思或注意點 |
|---|---|---|
| LATCHES | Large-Area Transactive Cooling & Heat Energy Storage | 公司文件中的產品全名；網站統一使用大寫 LATCHES，不自行創造官方中文譯名 |
| Thermal Energy Storage／TES | 熱能儲存 | 將熱能儲存起來，之後再使用 |
| Thermal Battery | 熱電池 | 用電池的比喻說明儲熱；不等於直接輸出電力 |
| PCM／PCMs | 相變材料 | 利用相態變化吸收與釋放熱能；本案配方未確認 |
| HVAC | Heating, Ventilation & Air Conditioning／暖氣、通風與空調 | 建築內調節空氣與室內環境的設備系統 |
| BAS | Building Automation System／建築自動化系統 | 管理與控制建築設備的系統 |
| BMS | Building Management System／建築管理系統 | 本案建築情境的管理系統稱呼；在電池情境也可能另指電池管理系統，需看上下文 |
| BACnet | 建築自動化與控制的通訊協定 | 可以比喻成設備間溝通的共同語言；不代表任何兩套設備都能免設定即用 |
| BACnet-native | 原生支援 BACnet 的產品描述 | 公司文件有此主張；實際支援範圍、測試與相容設備待確認 |
| State-of-Charge／SoC | 儲能狀態 | 在此是熱能儲存狀態的概念，不要直接當成一般電池電量百分比 |
| State-of-Charge Monitor & Controller | 儲能狀態監測與控制器 | 文件中的控制裝置名稱；產品名稱與規格待公司確認 |
| Tunable Thermal Storage | 可調控熱能儲存 | 強調熱能使用可受控制；具體可調項目與範圍待確認 |
| Setpoint | 設定值 | 例如空調設定溫度；設定值不等於每個位置的實測溫度 |
| Peak Load／Peak Demand | 尖峰負載／尖峰需量 | 某個高需求時段的用電功率或指定計量期間的需量 |
| Load Shifting | 負載移轉 | 把部分能源需求移到別的時間；不自動等於總能耗下降 |
| Demand Response | 需量反應 | 配合電網訊號或方案調整用電；實際參與條件需另確認 |
| BESS | Battery Energy Storage Systems／電池儲能系統 | 文件中的比較對象，不代表 LATCHES 能取代所有用途 |
| EUI | Energy Use Intensity／能源使用強度 | 常以一年能源使用量除以建築面積；比較時需一致單位與條件 |
| POC | Proof-of-Concept／概念驗證 | 在約定條件下測試構想是否可行，不等於全面商轉 |
| POC Site Partner | POC 場域合作夥伴 | 提供合適建築與合作條件來驗證；不是免費安裝的承諾 |
| CRM | Customer Relationship Management／客戶關係管理 | 本案主要是網站名單、分類及後續聯絡追蹤；不是產品控制系統 |
| FACES Workforce Program | FACES 人才培育計畫 | 與能源實務及工程人才有關；現有資料未提供完整縮寫、招生日期或資格 |

BACnet 的一般定義已對照 ASHRAE 官方說明；這並不構成 ThermoVerse 產品的相容性認證。[ASHRAE：BACnet](https://www.ashrae.org/technical-resources/bookstore/bacnet)

## 7. Energy Services 裡的名詞

| 名詞 | 白話解釋 |
|---|---|
| Energy Assessment | 能源評估：先了解建築怎麼用能、有哪些改善機會 |
| Energy Audit | 能源稽核：透過資料與現場檢視分析能源表現；深度依服務範圍而異 |
| BPI | Building Performance Institute：建築性能相關的標準與專業認證機構；不是 LATCHES 的零件 |
| BPI Energy Assessment | 文件列出的服務方向；不能因此認定公司所有人員都持有特定 BPI 證照 |
| ASHRAE | 暖通空調與建築環境相關的專業組織，發布標準與指引 |
| ASHRAE Audit | 依相關架構進行的能源稽核；本案提供哪個層級、哪些成果仍需確認 |
| MEP | Mechanical, Electrical and Plumbing／機械、電氣及給排水 | 
| MEP Consulting | 建築機電相關顧問服務，實際範圍依約定 |
| Energy Retrofit | 對既有建築或設備做能源改善，例如設備、控制或建築外殼改善；本案項目需依評估 |

參考：[BPI：Energy Auditor Scheme Handbook](https://www.bpi.org/__cms/docs/Energy-Auditor-Scheme-Handbook_Updated-3326.pdf)、[ASHRAE：Building EQ](https://www.ashrae.com/technical-resources/building-eq)。這些資料用於理解服務用語，不是確認公司證照或服務資格。

## 8. 文件裡聽起來很厲害的說法，怎麼解讀？

| 原始說法 | 白話理解 | 還缺什麼才能放心對外說？ |
|---|---|---|
| Zero-footprint | 依網站 Guidelines，主張整合天花板／牆面，減少占用可出租地板面積 | 不能解讀成沒有體積、重量或施工需求；需安裝圖、荷重與維修條件 |
| Urban-safe | 公司希望強調適合都市建築的產品定位 | 需具體安全測試、適用條件與認證；避免自行保證絕對安全 |
| Bypass fire codes | 原稿中的強烈行銷說法 | 不宜照字面說成「不必遵守消防法規」；應由公司確認合法、精確的文字 |
| Solid-state thermal battery | 公司對產品形式的稱呼 | 不等於固態鋰電池；與 PCM 的材料相態、封裝形式如何對應需公司解釋 |
| 20–60% peak HVAC reduction | DOCX 概述中的尖峰空調改善主張 | 測試場域、基準線、計量方式與適用範圍；不能改寫為整棟總用電省 20–60% |
| 4 hours longer | 文件聲稱可較久維持設定條件 | 比較對象、氣候、面積、溫度容許範圍、初始儲熱狀態 |
| 102 BTU/SF | 每平方英尺的熱能容量說法 | 材料或系統層級、厚度、測試條件；不是電功率或發電量 |
| 8× faster installation | 安裝較快的主張 | 比較方案、工序、施工人數與相同工作範圍 |
| World's first／most compact | 全球首創／最緊湊的比較主張 | 比較範圍、時間點及可核對證據 |

**特別容易混淆：** Email 範本中的 **312 W/cm²** 是對外洽談的學者散熱研究數字，不能拿來當 LATCHES 的效能。

減碳資料、ESG 報告與碳權也要分開理解：網站可談能源管理目標；是否達成減碳、能否報告特定成果或申請碳權，需要另有方法、量測與適用條件。本文件未進行碳權資格判定。

## 9. 有人問你產品問題，可以怎麼回答？

**「它是新型冷氣嗎？」**

目前文件把它定位為配合建築空調的熱能儲存與控制技術；我們還需要依場域確認整合方式，不能直接說它可以取代冷氣。

**「裝了可以省多少？」**

要先看建築、設備與用電條件，也要先確認你問的是尖峰負載、總用電還是費用。具體效果需要透過評估與測試確認。

**「已經買得到嗎？」**

目前資料有研發與 POC 招募方向，但不足以確認所有版本的上市、報價和交期。可以先安排需求討論，由團隊確認可提供的方案。

**「POC 是免費試用嗎？」**

不一定。POC 的範圍、設備、費用、資料與雙方責任要另外談；填表只是提出合作意願。

**「我們沒有要裝 LATCHES，還可以找你們嗎？」**

可以先洽詢 Energy Services，討論能源評估與改善需求；具體服務地區與可提供的項目再由團隊確認。

## 10. 下一次跟公司討論，優先取得這六項資料

1. **一頁產品圖解**：材料、感測器、控制器各在哪裡？熱怎麼流動？
2. **產品成熟度**：哪些是現有設備、哪些還在開發？現在能提供展示、POC 還是正式採購？
3. **一份可公開的測試摘要**：測了什麼、跟誰比、在哪些條件下得到什麼結果？
4. **安裝與整合條件**：重量、厚度、電源、網路、維修、HVAC／BACnet 支援範圍。
5. **能源服務清單**：服務地區、人員資格、交付內容及詢價方式。
6. **POC 與 FACES 的參與辦法**：找什麼對象、需要什麼資料、由誰回覆。

這六項是 PM 的資料補齊清單，不必等全部拿到才做網站原型。原型先用已掌握內容；涉及具體承諾的文字待確認後再補。

## 11. 來源與版本說明

### 本次已讀的本機資料

- [ThermoVerse_網站內容規劃.md](/Users/romeye/Desktop/ThermoVerse/ThermoVerse_網站內容規劃.md)：全文 11 節，作為網站架構與統一名稱依據。
- [FUTEX SOW - FINAL DRAFT (9_8).docx](</Users/romeye/Desktop/ThermoVerse/FUTEX SOW - FINAL DRAFT (9_8).docx>)：已讀本文與表格文字，包含 Project Overview、網站範圍、Appendix A 與 Website Guidelines。
- [SOW for FUTEX 2026 (1).pdf](</Users/romeye/Desktop/ThermoVerse/SOW for FUTEX 2026 (1).pdf>)：已讀 9 頁可擷取文字。未以產品圖推斷未見的構造。

PDF 與 DOCX 的網站重點並不完全一致；PDF 偏重 LATCHES，DOCX 的 Website Guidelines 明確加入 Energy Services 雙主軸。本次網站與本說明遵循現有網站內容規劃，不因檔案修改時間較新就認定另一份已取代它，也不判定任何文件已簽署生效。

### 一般技術原理參考

- [DOE：Thermal Energy Storage](https://www.energy.gov/cmei/buildings/thermal-energy-storage)
- [DOE：Grid-Interactive Efficient Buildings](https://www.energy.gov/cmei/buildings/articles/how-advanced-building-technologies-grid-interactive-efficient-buildings-can)
- [ASHRAE：BACnet](https://www.ashrae.org/technical-resources/bookstore/bacnet)
- [ASHRAE：Building EQ](https://www.ashrae.com/technical-resources/building-eq)
- [BPI：Energy Auditor Scheme Handbook](https://www.bpi.org/__cms/docs/Energy-Auditor-Scheme-Handbook_Updated-3326.pdf)

外部資料用於解釋通用概念，不用來替 LATCHES 背書。這份說明是內部學習文件，不是產品規格書、法規意見或已核准行銷文案。
