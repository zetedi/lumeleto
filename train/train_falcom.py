from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)

# Load your CSV dataset
data = load_dataset("csv", data_files="data.csv")

# Model name (using Mistral 7B Instruct)
model_name = "tiiuae/falcon-rw-1b"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Add pad_token if missing (required for dynamic padding)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.resize_token_embeddings(len(tokenizer))

# Preprocessing
def preprocess_function(examples):
    inputs = tokenizer(
        examples["prompt"],
        padding="max_length",
        truncation=True,
        max_length=512,
    )
    targets = tokenizer(
        examples["completion"],
        padding="max_length",
        truncation=True,
        max_length=512,
    )
    inputs["labels"] = targets["input_ids"]
    return inputs

tokenized_data = data.map(preprocess_function, batched=True)

# Data collator
data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    padding="longest",
    return_tensors="pt"
)

# Training arguments (no fp16 or eval strategy, optimized for M1 chip)
training_args = TrainingArguments(
    output_dir="/Volumes/lumeleto/tiiuae/falcon-rw-1b-m1",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    save_strategy="epoch",
    learning_rate=3e-5,
    weight_decay=0.01,
    save_total_limit=1,
    report_to="none",
    logging_steps=10,
    dataloader_pin_memory=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    data_collator=data_collator,
    tokenizer=tokenizer
)

# Train and save
trainer.train()
trainer.save_model("/Volumes/lumeleto/tiiuae/falcon-rw-1b-m1")