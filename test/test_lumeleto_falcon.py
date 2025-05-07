import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_dir = "/Volumes/lumeleto/tiiuae/falcon-rw-1b-m1"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)

# Move model to CPU
device = torch.device("cpu")
model = model.to(device)

# Tokenize and move input to device
inputs = tokenizer("What does initiation mean in Lifetree Network?", return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}

# Generate output
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=False,
    pad_token_id=tokenizer.eos_token_id
)

# Decode and print response
print(tokenizer.decode(outputs[0], skip_special_tokens=True))