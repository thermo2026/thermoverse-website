#!/usr/bin/env python3
"""Generate a two-shot, product-faithful LATCHES website hero with Veo 3.1."""

import os
import subprocess
import time
from pathlib import Path

import imageio_ffmpeg
from PIL import Image
from google import genai
from google.genai import types


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "latches-ceiling-hero"
TMP = ROOT / "tmp" / "latches-ceiling-hero"
SOURCE = ROOT / "LATCHES Image 1.png"


def api_key():
    for raw in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if raw.strip().startswith("GEMINI_API_KEY="):
            return raw.split("=", 1)[1].strip().strip("\"'")
    raise RuntimeError("GEMINI_API_KEY not found")


def prepare_reference():
    TMP.mkdir(parents=True, exist_ok=True)
    target = TMP / "latches-single-panel-16x9.png"
    panel = Image.open(SOURCE).convert("RGBA")
    canvas = Image.new("RGB", (1920, 1080), (238, 241, 242))
    scale = min(1320 / panel.width, 790 / panel.height)
    panel = panel.resize(
        (round(panel.width * scale), round(panel.height * scale)),
        Image.Resampling.LANCZOS,
    )
    canvas.paste(panel, ((1920 - panel.width) // 2, (1080 - panel.height) // 2), panel)
    canvas.save(target)
    return target


def generate(client, prompt, negative, reference, destination):
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        image=types.Image.from_file(location=str(reference), mime_type="image/png"),
        config=types.GenerateVideosConfig(
            aspect_ratio="16:9",
            resolution="720p",
            negative_prompt=negative,
        ),
    )
    print(f"submitted {destination.name}: {operation.name}", flush=True)
    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        print(f"rendering {destination.name}", flush=True)
    generated = operation.response.generated_videos[0]
    client.files.download(file=generated.video)
    generated.video.save(str(destination))


def run_ffmpeg(*args):
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", *map(str, args)], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reference = prepare_reference()
    client = genai.Client(api_key=api_key())

    shot1 = OUT / "01-panel-to-room.mp4"
    generate(
        client,
        """Premium architectural product film, one continuous slow camera move. Begin with the exact single white square LATCHES thermal battery panel from the reference image, preserving its thin profile, rounded metal edge and plain unmarked white face. The camera gently pulls backward and tilts below the panel. Identical panels extend outward one by one in straight rows, becoming a precise standard suspended drop-ceiling grid. Do not transform or redesign the panel. As the grid expands, a realistic modern office room is digitally constructed beneath it in an elegant architectural visualization: floor, glass walls, desks and chairs resolve cleanly from subtle geometric lines into photoreal materials. Several realistically proportioned office workers appear already seated and calmly working at desktop computers. Finish on a wide, symmetrical, photoreal office interior with the LATCHES panels clearly visible across the ceiling. Smooth restrained motion, realistic daylight, premium commercial cinematography, no cuts, silent, completely text-free.""",
        """words, letters, numbers, logos, watermarks, captions, interface text, floating UI, fake screens, fire, flames, smoke, sparks, magical beams, electrical lightning, panel changing shape, panel opening, panel splitting, extra components, exposed internals, warped ceiling, broken grid, duplicated people, distorted hands, camera shake, abrupt cut""",
        reference,
        shot1,
    )

    bridge = TMP / "room-bridge.png"
    run_ffmpeg("-sseof", "-0.12", "-i", shot1, "-frames:v", "1", bridge)

    shot2 = OUT / "02-thermal-absorption.mp4"
    generate(
        client,
        """Continue the exact same office, camera position, people, computers and ceiling from the reference frame in one uninterrupted slow shot. People keep working naturally at their computers. The photoreal scene gradually and smoothly becomes a scientifically credible FLIR thermal-imaging visualization. People and operating computers show contained coral-orange heat signatures; walls, desks and surrounding air become deep blue and violet. The white square LATCHES panels remain fixed in the ceiling grid and keep their exact geometry. Soft diffuse thermal energy moves upward from people, computers and warm room surfaces toward the ceiling, then is visibly absorbed into the LATCHES panels as a restrained warm coral glow held inside each panel. As the panels store the heat, the occupied room below gradually shifts toward an even, comfortable cool blue while people continue working. Show heat transfer, not electricity. Calm scientific visualization, elegant premium architecture film, smooth camera, silent, completely text-free.""",
        """words, letters, numbers, logos, watermarks, captions, interface text, graphs, fake screens, fire, flames, smoke, sparks, combustion, glowing fireballs, laser beams, electrical current, lightning, heat traveling through data cables, freezing people, disappearing people, empty office, lights turning off, panel deformation, panel opening, extra devices, distorted faces, abrupt cut""",
        bridge,
        shot2,
    )

    final = OUT / "LATCHES-ceiling-hero.mp4"
    concat = TMP / "concat.txt"
    concat.write_text(
        f"file '{shot1.resolve()}'\nfile '{shot2.resolve()}'\n",
        encoding="utf-8",
    )
    run_ffmpeg(
        "-f", "concat", "-safe", "0", "-i", concat,
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", final,
    )
    print(final, flush=True)


if __name__ == "__main__":
    main()
