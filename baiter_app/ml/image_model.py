from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


MODEL_ID = "Salesforce/blip-image-captioning-base"

print("Loading image model...")

processor = BlipProcessor.from_pretrained(MODEL_ID)

model = BlipForConditionalGeneration.from_pretrained(MODEL_ID)
model.eval()

print("Image model loaded!")


def generate_image_description(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    )

    output = model.generate(**inputs)

    description = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return description