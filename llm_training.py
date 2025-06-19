import json
from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from peft import get_peft_model, LoraConfig, TaskType
import torch
import os

# Load data
data_path = "Partial_pdf_extraction/llm_dataset.jsonl"
raw_data = [
    json.loads(line)
    for line in open(data_path, "r", encoding="utf-8")
    if line.strip() and "text" in json.loads(line).get("type", "").lower()
]

# Format into prompt-completion pairs
examples = [{
    "prompt": f"What does the company report on page {d['page']}?",
    "completion": d["content"]
} for d in raw_data]

dataset = Dataset.from_list(examples)

# Load tokenizer and model (LLaMA 3 8B)
model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="auto", load_in_8bit=True
)

# Apply LoRA (QLoRA) config
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.05
)
model = get_peft_model(model, peft_config)

# Tokenization function
def tokenize_function(example):
    prompt = f"<s>{example['prompt']}\n\n"
    completion = f"{example['completion']}</s>"
    full_input = prompt + completion
    return tokenizer(full_input, truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=False)

# Training arguments
training_args = TrainingArguments(
    output_dir="./llama3-finetuned",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_dir="./logs",
    evaluation_strategy="no",
    save_strategy="epoch",
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()
