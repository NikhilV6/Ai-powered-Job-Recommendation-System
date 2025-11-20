from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import os

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LORA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "models", "tinyllama-career-assistant"
)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_4bit=True,
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, LORA_PATH)
model.eval()

def generate_answer(instruction: str, inp: str | None = None, max_new_tokens: int = 256) -> str:
    if inp:
        prompt = f"Instruction: {instruction}\nInput: {inp}\nAnswer:"
    else:
        prompt = f"Instruction: {instruction}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.3,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Optionally strip the prompt from beginning:
    return text.replace(prompt, "").strip()
