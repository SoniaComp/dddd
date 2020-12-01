from api.berts import BERT
import torch

import pandas as pd

from transformers import BertTokenizer
from transformers import BertForSequenceClassification

def load_model():
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)
    #device = torch.device("cuda")
    device = torch.device("cpu")
    model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)
    #model.load_state_dict(torch.load('./20201112-1650_0_(accu _ 0.81)(epoch _ 10).pt'))

    return device, model, tokenizer