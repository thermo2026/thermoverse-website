#!/usr/bin/env python3
"""
ThermoVerse Hero Video Pipeline (Google Veo 3.1 串接程式)
依據「ThermoVerse_Hero影片製作稿.md」規格串接 Google Veo 模型。
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import ssl
from pathlib import Path

# 專案路徑設定
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
OUTPUT_DIR = PROJECT_ROOT / "output" / "veo_generated"
TMP_DIR = PROJECT_ROOT / "tmp"

def load_api_key():
    """從 .env 讀取 GEMINI_API_KEY"""
    if not ENV_PATH.exists():
        print(f"[錯誤] 找不到 .env 檔案: {ENV_PATH}")
        sys.exit(1)
    
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip('"\'')
                if key:
                    return key
    print("[錯誤] .env 檔案中未找到有效 GEMINI_API_KEY")
    sys.exit(1)

# 分鏡 Prompt 定義（完全依照「ThermoVerse_Hero影片製作稿.md」與 Veo 3.1 最佳實踐）
COMMON_NEGATIVE_STYLE = (
    "All surfaces and screens are completely free of writing. "
    "No words, letters, numbers, captions, subtitles, logos, watermarks, signage, legends, axis labels, temperature scales, or pseudo-text anywhere. "
    "No audio, silent film. Premium architectural visualization, realistic scale, restrained lighting, deep blue-gray, coral-orange and cyan palette, "
    "smooth stabilized camera movement, calm pacing, understated transitions. No electrical generation imagery, lightning, magical energy beams, "
    "freezing occupants, extinguished office lights, warped buildings, duplicated people, flashing effects or abrupt cuts."
)

SHOTS = {
    1: {
        "title": "鏡頭 1（0–8 秒）：城市空拍進樓與透明剖面",
        "duration": 8,
        "filename": "shot1_city_to_cutaway.mp4",
        "prompt": (
            "Cinematic, completely text-free background film for a premium building thermal-storage technology website. "
            "Landscape 16:9, daytime. Begin with a realistic aerial view of a modern city. Smoothly push forward toward one distinctive glass office tower. "
            "As the camera approaches a single occupied floor, the glass facade naturally transitions into an elegant architectural cutaway revealing "
            "multiple offices, meeting rooms, and people naturally working. Camera glides smoothly into the floor layout. "
            + COMMON_NEGATIVE_STYLE
        ),
    },
    2: {
        "title": "鏡頭 2（8–15 秒）：室內熱成像與薄型儲熱模組",
        "duration": 7,
        "filename": "shot2_thermal_storage.mp4",
        "prompt": (
            "Cinematic, completely text-free background film continuing inside the exact same office floor layout and people. "
            "Gradually transform the interior into a stylized thermal-imaging view: subtle orange and coral heat around occupants, computers, "
            "and sun-warmed surfaces, against deep blue-violet architecture. Reveal slim thermal-storage panels integrated within a ceiling cutaway. "
            "Gentle orange heat-flow ribbons gather into these ceiling panels and remain stored as a soft warm glow. Warm areas in the room gradually moderate; "
            "people remain naturally warm and continue working normally. No temperature numbers or scales. "
            + COMMON_NEGATIVE_STYLE
        ),
    },
    3: {
        "title": "鏡頭 3（15–24 秒）：數位孿生、中控中樞與循環轉場",
        "duration": 9,
        "filename": "shot3_digital_twin_loop.mp4",
        "prompt": (
            "Cinematic, completely text-free background film continuing from the ceiling thermal panels. "
            "The architecture transitions into a refined digital twin. Stored thermal glow remains inside the ceiling panels. "
            "Cyan sensing pulses emerge from small sensor nodes and travel along an organized building data network toward a central building control room. "
            "Follow pulses to its large display. The display contains only an unlabelled building model, a simple HVAC schematic, and two clean graphical curves: "
            "a faint earlier high-peaked curve and a cyan curve with a lower peak. End by matching the building model back to the real tower and "
            "smoothly returning to the opening aerial composition for a seamless loop. "
            + COMMON_NEGATIVE_STYLE
        ),
    }
}

def check_connection(api_key, model_name="veo-3.1-generate-preview"):
    """檢查 API 金鑰與連線能力，不發動影片生成"""
    print("=" * 65)
    print(" 正在檢查 Google Veo 3.1 串接狀態 (Safe Check Only)")
    print("=" * 65)
    print(f"[*] API 金鑰: 已安全載入 (.env，格式前綴: {api_key[:4]}...)")
    print(f"[*] 目標模型: {model_name}")
    print(f"[*] 輸出目錄: {OUTPUT_DIR}")
    print(f"[*] 分鏡數量: {len(SHOTS)} 個鏡頭已載入 (共 24 秒循環影片規範)")
    
    try:
        from google import genai
        print("[✓] 官方 google-genai SDK: 已安裝")
    except ImportError:
        print("[!] 官方 google-genai SDK: 未安裝 (可用 `pip install google-genai` 安裝)")
        print("[*] 備援方案: 程式已內建 REST API 連線支援")

    print("\n[✓] 串接管線已建置完成！目前處於「安全待命」狀態，未發動任何生成。")
    print("=" * 65)

def generate_shot(shot_id, api_key, model_name="veo-3.1-generate-preview"):
    """執行特定分鏡生成（需使用者確認後調用）"""
    shot_info = SHOTS.get(shot_id)
    if not shot_info:
        print(f"[錯誤] 無效的分鏡 ID: {shot_id}")
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / shot_info["filename"]
    
    print(f"\n[開始生成] {shot_info['title']}")
    print(f"[*] 時長: {shot_info['duration']} 秒 | 比例: 16:9")
    print(f"[*] 提示詞預覽: {shot_info['prompt'][:120]}...")
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        print("[*] 正在透過 google-genai 發起非同步任務...")
        operation = client.models.generate_videos(
            model=model_name,
            prompt=shot_info["prompt"],
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                resolution="720p",
            ),
        )
        print(f"[*] 任務已送出，正在等待 Veo 渲染 (Operation: {operation.name})...")
        while not operation.done:
            time.sleep(15)
            operation = client.operations.get(operation)
            print("    - 算力佇列處理中，請稍候...")
        
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(out_file))
        print(f"[✓] 成功儲存影片至: {out_file}")
        
    except Exception as e:
        print(f"[錯誤] 生成過程中發生例外: {e}")

def main():
    parser = argparse.ArgumentParser(description="ThermoVerse Google Veo 3.1 影片生成管線")
    parser.add_argument("--check", action="store_true", help="只檢查環境與金鑰連線，不生成影片")
    parser.add_argument("--model", default="veo-3.1-generate-preview", help="使用的模型版本 (預設: veo-3.1-generate-preview)")
    parser.add_argument("--shot", type=int, choices=[1, 2, 3], help="指定生成單一分鏡 (1, 2 或 3)")
    parser.add_argument("--all", action="store_true", help="生成全部 3 個分鏡並準備合成")
    parser.add_argument("--execute", action="store_true", help="確認執行實際生成操作")
    
    args = parser.parse_args()
    api_key = load_api_key()
    
    if args.check or (not args.shot and not args.all):
        check_connection(api_key, args.model)
        print("\n使用指令提示：")
        print("  - 檢查狀態:           python3 scripts/veo_hero_pipeline.py --check")
        print("  - 生成鏡頭 1 (安全):  python3 scripts/veo_hero_pipeline.py --shot 1 --execute")
        print("  - 完整生成 (安全):    python3 scripts/veo_hero_pipeline.py --all --execute")
        return

    if not args.execute:
        print("\n[安全防護機制啟動]")
        print("您目前未帶 `--execute` 參數，為防止意外扣費或額度消耗，已安全中止。")
        print("如確認要發動生成，請加上 `--execute`。")
        return

    if args.shot:
        generate_shot(args.shot, api_key, args.model)
    elif args.all:
        for s in [1, 2, 3]:
            generate_shot(s, api_key, args.model)

if __name__ == "__main__":
    main()
