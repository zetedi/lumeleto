from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_dir = "/Volumes/lumeleto//gpt2-lumeleto/lumeleto-model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)

model.eval()

# Run on CPU
inputs = tokenizer("What is the Lifetree Network good for?", return_tensors="pt")
# outputs = model.generate(
#    **inputs,
#    max_new_tokens=50,
#    do_sample=True,
#    top_k=40,
#    top_p=0.95,
#    temperature=0.7,
#    pad_token_id=tokenizer.eos_token_id,
#)


outputs = model.generate(
    **inputs,
    max_new_tokens=80,
    pad_token_id=tokenizer.eos_token_id,
    do_sample=True,            # Enable sampling
    temperature=0.8,           # Add randomness
    top_p=0.9,                 # Nucleus sampling
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))