#!/usr/bin/env python3
"""
ThermoVerse Full Hero Video Generator v2 (修正版)
1. 嚴格鎖定 Z 軸垂直壓縮合體，嚴禁切開、十字分割、長出多餘金屬件，終點完全比照 LATCHES Image 1.png。
2. 辦公室熱成像轉化：嚴禁火焰 (No fire/flames/smoke)，以真實 FLIR 溫場散熱冷卻取代桌上起火。
3. 自動拼接為單一 MP4。
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types
import imageio_ffmpeg

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
OUTPUT_DIR = PROJECT_ROOT / "output" / "veo_generated"
TMP_DIR = PROJECT_ROOT / "tmp"

def load_api_key():
    if not ENV_PATH.exists():
        print(f"[錯誤] 找不到 .env: {ENV_PATH}")
        sys.exit(1)
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip('"\'')
                if key:
                    return key
    print("[錯誤] 未找到 GEMINI_API_KEY")
    sys.exit(1)

def prepare_frames():
    """準備 16:9 白底居中的起始幀與結束幀"""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    f_start = TMP_DIR / "frame_start_mvp.png"
    f_end = TMP_DIR / "frame_end_assembled.png"
    
    mvp_path = PROJECT_ROOT / "LATCHES MVP.png"
    img1_path = PROJECT_ROOT / "LATCHES Image 1.png"
    
    mvp = Image.open(mvp_path).convert("RGBA")
    img1 = Image.open(img1_path).convert("RGBA")
    
    # MVP 居中
    canvas1 = Image.new("RGB", (1920, 1080), (255, 255, 255))
    ratio1 = 850 / mvp.height
    new_w1, new_h1 = int(mvp.width * ratio1), 850
    res1 = mvp.resize((new_w1, new_h1), Image.Resampling.LANCZOS)
    canvas1.paste(res1, ((1920 - new_w1) // 2, (1080 - new_h1) // 2), res1)
    canvas1.save(f_start, "PNG")
    
    # Image 1 居中
    canvas2 = Image.new("RGB", (1920, 1080), (255, 255, 255))
    ratio2 = 800 / img1.height
    new_w2, new_h2 = int(img1.width * ratio2), 800
    res2 = img1.resize((new_w2, new_h2), Image.Resampling.LANCZOS)
    canvas2.paste(res2, ((1920 - new_w2) // 2, (1080 - new_h2) // 2), res2)
    canvas2.save(f_end, "PNG")
        
    return f_start, f_end

def generate_part(client, model_name, prompt, negative_prompt, first_frame_path, last_frame_path=None, out_path=None):
    """呼叫 Veo 3.1 生成影片"""
    print(f"\n{'='*65}")
    print(f"[*] 正在生成: {out_path.name}")
    print(f"[*] 首幀: {first_frame_path.name}")
    if last_frame_path:
        print(f"[*] 尾幀 (嚴格鎖定): {last_frame_path.name}")
    
    first_img = types.Image.from_file(location=str(first_frame_path), mime_type="image/png")
    
    config_args = {
        "aspect_ratio": "16:9",
        "resolution": "720p",
        "negative_prompt": negative_prompt,
    }
    if last_frame_path:
        config_args["last_frame"] = types.Image.from_file(location=str(last_frame_path), mime_type="image/png")
        
    config = types.GenerateVideosConfig(**config_args)
    
    operation = client.models.generate_videos(
        model=model_name,
        prompt=prompt,
        image=first_img,
        config=config,
    )
    
    print(f"[*] 任務已提交: {operation.name}，算力佇列運算中...")
    start_time = time.time()
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"    - 算力運算中...（已耗時 {elapsed} 秒）")
        time.sleep(15)
        operation = client.operations.get(operation)
        
    print(f"[✓] 算力渲染完成！耗時: {int(time.time() - start_time)} 秒")
    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(str(out_path))
    print(f"[✓] 已儲存至: {out_path}")
    return out_path

def concat_videos(video_list, final_output):
    """透過內建 FFmpeg 無縫拼接影片"""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    concat_txt = TMP_DIR / "concat_list_v2.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for v in video_list:
            f.write(f"file '{v.resolve()}'\n")
            
    print(f"\n[*] 正在將分段拼接為單一完整版...")
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(final_output)
    ]
    subprocess.run(cmd, check=True)
    print(f"[✓] 完整版拼接成功！位置: {final_output}")

def main():
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    model_name = "veo-3.1-generate-preview"
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    f_start, f_end = prepare_frames()
    
    # -------------------------------------------------------------
    # 鏡頭 1：垂直壓縮組裝（嚴禁切開、十字割裂、長出多餘物件）
    # -------------------------------------------------------------
    part1_out = OUTPUT_DIR / "part1_exact_assembly_v2.mp4"
    prompt_part1 = (
        "Clean minimal industrial design animation. "
        "The floating horizontal layers from the initial exploded diagram simply move along the vertical Z-axis straight down, compressing and stacking cleanly together. "
        "All layers flatly sandwich into the single, solid, seamless pure-white rectangular ceiling tile shown in the last frame. "
        "Simple straight downward vertical movement only. Completely solid closed form at the end. "
        "Bright pristine white studio background, smooth slow motion, realistic soft contact shadows, silent."
    )
    negative_part1 = (
        "cutaway, sliced, cross section, vertical partitions, vertical dividers, cross walls, splitting in four, "
        "folding, expanding outwards, extra brackets, extra parts, legs, pins, interior walls, hollow, explosion, "
        "fire, smoke, text, numbers, letters, logos, watermarks, abrupt cut."
    )
    generate_part(client, model_name, prompt_part1, negative_part1, f_start, f_end, part1_out)
    
    # -------------------------------------------------------------
    # 鏡頭 2：天花板陣列 -> 辦公室成形 -> FLIR熱成像散熱平衡（嚴禁火焰）
    # -------------------------------------------------------------
    part2_out = OUTPUT_DIR / "part2_office_and_thermal_v2.mp4"
    prompt_part2 = (
        "High-end architectural commercial video for thermal storage technology. "
        "Starts from the white modular ceiling tile. The camera tilts up as the single tile duplicates into a neat, seamless grid across a modern office ceiling. "
        "The camera smoothly tilts down into a bright, spacious, sunlit corporate office. Professionals sit at desks working quietly on computers. "
        "The scene smoothly transitions into a genuine FLIR thermal imaging view: human occupants and running laptops naturally show subtle warm coral-orange thermal body heat, while desks, chairs, and walls remain cool dark blue. "
        "The ceiling tiles calmly absorb ambient room heat, gently glowing with a soft stored thermal warmth, while the surrounding air temperature gently cools and equilibrates into a comfortable, balanced deep-blue tone. "
        "Scientific thermal visualization, serene and elegant, no destruction. Completely text-free, no UI, no letters, no numbers, silent."
    )
    negative_part2 = (
        "fire, flames, blaze, campfire, fire pillars, fire on table, fire rising, smoke, burning, ash, sparks, explosion, "
        "glowing fireballs, laser beams, glowing torches, text, numbers, letters, subtitles, logos, watermarks."
    )
    generate_part(client, model_name, prompt_part2, negative_part2, f_end, None, part2_out)
    
    # -------------------------------------------------------------
    # 拼接完整版 v2
    # -------------------------------------------------------------
    final_hero = OUTPUT_DIR / "thermoverse_hero_full_v2.mp4"
    concat_videos([part1_out, part2_out], final_hero)
    
    print("\n" + "=" * 65)
    print(" 修正版全流程完成！")
    print(f" 完整影片: {final_hero}")
    print("=" * 65)

if __name__ == "__main__":
    main()
