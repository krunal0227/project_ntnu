from transformers import pipeline
from datasets import load_dataset
import evaluate
import json

# Load test examples
with open("Partial_pdf_extraction/llm_dataset.jsonl", "r", encoding="utf-8") as f:
    samples = [json.loads(line) for line in f if line.strip() and "text" in line]

# Select 5 examples for evaluation
eval_data = samples[:5]

# Load model
pipe = pipeline("text-generation", model="./llama3-finetuned", device=0)

# Metrics
rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")
from nltk.translate.bleu_score import sentence_bleu

refs, preds = [], []

for ex in eval_data:
    prompt = f"What does the company report on page {ex['page']}?"
    generated = pipe(prompt, max_new_tokens=100)[0]["generated_text"]
    answer = ex["content"]

    refs.append(answer)
    preds.append(generated)

# Compute
print("ROUGE:", rouge.compute(predictions=preds, references=refs))
print("BLEU:", bleu.compute(predictions=preds, references=refs))
