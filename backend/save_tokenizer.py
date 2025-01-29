from transformers import AutoTokenizer

# Replace with the base model of your trained checkpoint
model_name = "distilbert-base-uncased"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save tokenizer to your checkpoint directory
tokenizer.save_pretrained("/Users/caldwellwachira/Downloads/Bulk-Files/models/checkpoint-5000")

print("Tokenizer files saved successfully!")