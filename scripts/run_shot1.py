#!/usr/bin/env python3
"""
ThermoVerse Hero Video - Shot 1 Generator
以 LATCHES MVP.png 為起始圖，透過 Google Veo 3.1 生成零件合體組裝動畫。
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
MVP_IMG_PATH = PROJECT_ROOT / "LATCHES MVP.png"
TMP_DIR = PROJECT_ROOT / "tmp"
OUTPUT_DIR = PROJECT_ROOT / "output" / "veo_generated"

def load_api_key():
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
    print("[錯誤] 未能讀取 GEMINI_API_KEY")
    sys.exit(1)

def prepare_reference_image():
    """將 LATCHES MVP.png 轉為 16:9 比例 (1920x1080)，置中於乾淨純白背景"""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out_ref_path = TMP_DIR / "shot1_input_16x9.png"
    
    print(f"[*] 正在準備參考圖：{MVP_IMG_PATH}")
    src_img = Image.open(MVP_IMG_PATH).convert("RGBA")
    
    # 建立 1920x1080 純白底圖
    target_w, target_h = 1920, 1080
    canvas = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 255))
    
    # 縮放原圖至適合高度 (例如高度佔 90%)
    max_h = int(target_h * 0.9)
    ratio = max_h / src_img.height
    new_w = int(src_img.width * ratio)
    new_h = max_h
    resized_src = src_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 置中貼上
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas.paste(resized_src, (paste_x, paste_y), resized_src)
    
    # 轉為 RGB JPEG/PNG 儲存
    final_rgb = canvas.convert("RGB")
    final_rgb.save(out_ref_path, "PNG")
    print(f"[✓] 16:9 參考圖已儲存至: {out_ref_path} ({target_w}x{target_h})")
    return out_ref_path

def main():
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    
    # 1. 準備首幀參考圖
    ref_img_path = prepare_reference_image()
    ref_image = types.Image.from_file(location=str(ref_img_path), mime_type="image/png")
    
    # 2. 定義 Shot 1 提示詞
    prompt = (
        "An elegant, high-precision industrial design commercial animation. "
        "Starting from the exact exploded multi-layer components shown in the reference image (circuit control box, metallic casing, thermal storage core, insulation sheets, and mounting frame). "
        "The floating layers smoothly converge vertically and assemble seamlessly into a sleek, clean, pure-white flat square modular ceiling tile. "
        "Camera smoothly orbits and pushes slightly closer with cinematic slow-motion. "
        "Minimalist aesthetic, premium architectural lighting, studio white background, realistic shadows, flawless mechanical fit. "
        "Completely text-free, no logos, no numbers, no words, no watermarks, no glitch, silent."
    )
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_video_path = OUTPUT_DIR / "shot1_assembled.mp4"
    
    # 優先嘗試的模型清單
    models_to_try = [
        "veo-3.1-generate-preview",
        "veo-3.1",
        "veo-2.0-generate-001"
    ]
    
    operation = None
    selected_model = None
    
    for m in models_to_try:
        print(f"\n[*] 嘗試使用模型: {m} ...")
        try:
            operation = client.models.generate_videos(
                model=m,
                prompt=prompt,
                image=ref_image,
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    resolution="720p",
                ),
            )
            selected_model = m
            print(f"[✓] 成功提交生成請求！模型: {selected_model}")
            print(f"[*] 任務 Operation 名稱: {operation.name}")
            break
        except Exception as e:
            print(f"[!] 模型 {m} 呼叫未成功: {e}")
            
    if not operation:
        print("[錯誤] 所有候選 Veo 模型皆未能成功啟動任務，請檢查上述錯誤訊息。")
        sys.exit(1)
        
    # 輪詢任務狀態
    print("\n[*] 正在等待 Veo 生成影片（一般需時約 1~2 分鐘）...")
    start_time = time.time()
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"    - 渲染運算中...（已耗時 {elapsed} 秒）")
        time.sleep(15)
        operation = client.operations.get(operation)
        
    print(f"[✓] 算力渲染完成！總耗時: {int(time.time() - start_time)} 秒")
    
    # 下載儲存
    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(str(out_video_path))
    print(f"\n==================================================")
    print(f" 鏡頭 1 生成成功！")
    print(f" 影片位置: {out_video_path}")
    print(f"==================================================")

if __name__ == "__main__":
    main()
