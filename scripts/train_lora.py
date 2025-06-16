#!/usr/bin/env python3
import os, argparse
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

parser = argparse.ArgumentParser()
parser.add_argument("--base-model", required=True)
parser.add_argument("--data", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--output", required=True)

args = parser.parse_args()
MODEL      = args.base_model
DATA  = args.data
OUT    = args.output

tokenizer = AutoTokenizer.from_pretrained(MODEL, use_fast=False)
model     = AutoModelForCausalLM.from_pretrained(MODEL)

dataset = load_dataset("json", data_files=DATA)["train"]
def tokenize(ex): return tokenizer(ex["text"], truncation=True, max_length=512)
ds = dataset.map(tokenize, batched=True, remove_columns=["text"])

lora_cfg = LoraConfig(
    r=8, lora_alpha=16, target_modules=["q_proj","v_proj"], 
    inference_mode=False, bias="none"
)
model = get_peft_model(model, lora_cfg)

training_args = TrainingArguments(
    output_dir=OUT, 
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    logging_steps=50,
    fp16=True,
    save_total_limit=1,
    save_strategy="epoch",
)
trainer = Trainer(model=model, args=training_args, train_dataset=ds)
trainer.train()
model.save_pretrained(OUT)
