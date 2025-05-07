from datasets import load_dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    Trainer, 
    TrainingArguments,
    DataCollatorForLanguageModeling
)

# Load data
data = load_dataset("csv", data_files="Lumeleto_108_Prompt-Completion_Dataset.csv")

# Load tokenizer and model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Padding token
tokenizer.pad_token = tokenizer.eos_token
model.resize_token_embeddings(len(tokenizer))

# Preprocess
def preprocess_function(example):
    return tokenizer(example["prompt"] + " " + example["completion"], truncation=True, padding="max_length", max_length=128)

tokenized_data = data.map(preprocess_function)

# Collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training args
training_args = TrainingArguments(
    output_dir="/Volumes/lumeleto//gpt2-lumeleto",
    overwrite_output_dir=True,
    per_device_train_batch_size=1,
    num_train_epochs=5,
    logging_steps=5,
    save_strategy="epoch",
    save_total_limit=1,
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    data_collator=data_collator
)

trainer.train()
trainer.save_model("/Volumes/lumeleto//gpt2-lumeleto")