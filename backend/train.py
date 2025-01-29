import torch
from transformers import BertForSequenceClassification, Trainer, TrainingArguments, DistilBertForSequenceClassification
from preprocessing import train_dataset, val_dataset
from metrics import compute_metrics

# Step 1 : Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Step 2: Load the pretrained BERT model
# Adding a classification head for binary classification (positive/negative sentiment)
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased",num_labels=2)
model.to(device)

# Step 3: Define training arguments/hyperparameters
training_args = TrainingArguments(
    output_dir="/Users/caldwellwachira/Downloads/Bulk-Files/models", # Where to save model checkpoints
    eval_strategy="epoch",                                           # Evaluate after epoch
    save_strategy="epoch",                                           # Save model after each epoch
    learning_rate=5e-5,                                              # Learning rate
    per_device_train_batch_size=8,                                  # Batch size for training
    per_device_eval_batch_size=8,                                   # Batch size for evaluation
    warmup_steps=100,                                                # Warmup steps for learning rate scheduler
    weight_decay=0.01,                                               # Weight decay for regularization
    logging_dir = "logs",                                            # Directory for logs
    logging_steps=10,                                                # Log every 10 steps
    save_total_limit =2,                                             # Keep only the latest 2 checkpoints
    load_best_model_at_end=True,                                     # Load the best model at the end of training
    metric_for_best_model="accuracy"                                 # Select the best model based on accuracy
)

trainer=Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

print("Starting training....")
trainer.train()