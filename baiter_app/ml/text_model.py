import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


MODEL_ID = "EnglishVoice/t5-base-keywords-to-headline"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading text model...")

tokenizer = T5Tokenizer.from_pretrained(MODEL_ID)

model = T5ForConditionalGeneration.from_pretrained(MODEL_ID)
model = model.to(device)
model.eval()

print("Text model loaded!")


def generate_headlines(keywords):
    text = "headline: " + keywords

    encoding = tokenizer(
        text,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        do_sample=True,
        num_return_sequences=5,
        temperature=0.95,
        top_k=50,
        top_p=0.95,
        max_new_tokens=30,
    )

    headlines = []

    for output in outputs:
        result = tokenizer.decode(
            output,
            skip_special_tokens=True
        )
        headlines.append(result)

    return headlines