import os
import subprocess
import tempfile

import torch
from PIL import Image
from transformers import (
    AutoProcessor,
    LlavaOnevisionForConditionalGeneration,
)


MODEL_ID = "llava-hf/llava-onevision-qwen2-0.5b-ov-hf"
print("Loading video model...")
device = "cuda" if torch.cuda.is_available() else "cpu"

model = LlavaOnevisionForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    low_cpu_mem_usage=True,
)

model = model.to(device)
model.eval()

processor = AutoProcessor.from_pretrained(MODEL_ID)
print("Video model loaded!")


def generate_video_description(video_path):
    frames_dir = tempfile.mkdtemp()

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                "-vf",
                "fps=1",
                "-frames:v",
                "6",
                os.path.join(frames_dir, "frame_%02d.jpg"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        frame_files = sorted(
            os.path.join(frames_dir, f)
            for f in os.listdir(frames_dir)
            if f.endswith(".jpg")
        )

        images = [
            Image.open(path).convert("RGB")
            for path in frame_files
        ]

        content = [
            {
                "type": "text",
                "text": (
                    "Look at these frames from a video and describe "
                    "what is happening in the video in one short sentence."
                ),
            }
        ]

        for _ in images:
            content.append({"type": "image"})

        conversation = [
            {
                "role": "user",
                "content": content,
            }
        ]

        prompt = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
        )

        inputs = processor(
            text=prompt,
            images=images,
            return_tensors="pt",
        )

        inputs = {
            key: value.to(device)
            if hasattr(value, "to")
            else value
            for key, value in inputs.items()
        }

        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=False,
            )

        result = processor.decode(
            output[0],
            skip_special_tokens=True,
        )

        if "assistant" in result:
            result = result.split("assistant", 1)[1].strip()

        return result

    finally:
        for filename in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, filename))

        os.rmdir(frames_dir)