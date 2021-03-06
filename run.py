import torch
import pandas as pd
import numpy as np
from transformers import BertTokenizerFast as BertTokenizer
from utils.plot_results import plot_results
from resources.train_val_model import train_model
from resources.get_data import get_data
from resources.build_model import BertClassifier
from resources.test_model import test_model
from resources.build_dataloader import build_dataloader


##################################
#            get data
##################################

train_df, val_df, test_df = get_data()

# fixed parameters
label_columns = train_df.columns.tolist()[3:-1]
num_labels = len(label_columns)
max_token_len = 30
BERT_MODEL_NAME = "bert-base-uncased"

##################################
#        build data loaders
##################################
tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)

train_dataloader = build_dataloader(
    train_df, label_columns, tokenizer, max_token_len, trainset=True
)
val_dataloader = build_dataloader(val_df, label_columns, tokenizer, max_token_len)
test_dataloader = build_dataloader(test_df, label_columns, tokenizer, max_token_len)

##################################
#        build model
##################################

bert_classifier = BertClassifier(
    num_labels=num_labels, BERT_MODEL_NAME=BERT_MODEL_NAME, freeze_bert=False
)

##################################
#     train and validate model
##################################

trained_model, training_stats, train_loss_set = train_model(
    bert_classifier,
    train_dataloader,
    val_dataloader=val_dataloader,
    epochs=1,
    evaluation=True,
)

# plot_results(training_stats, train_loss_set)

##################################
#           test model
##################################

test_model(
    test_dataloader=test_dataloader,
    BERT_MODEL_NAME=BERT_MODEL_NAME,
    num_labels=num_labels,
    label_columns=label_columns,
)
