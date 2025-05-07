import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_dir = "/Volumes/lumeleto/tiiuae/falcon-rw-1b-m1"


from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-rw-1b")

inputs = tokenizer("Hello, who are you?", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
