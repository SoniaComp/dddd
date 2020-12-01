import api.berts.BERT
import torch

import pandas as pd

from transformers import BertTokenizer
from transformers import BertForSequenceClassification

def load_model():
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)
    device = torch.device("cuda")
    model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)
    model.load_state_dict(torch.load('api/berts/20201113-0056_10_(accu _ 0.82)(epoch _ 14).pt'))
    model.cuda()
    model.eval()

    return device, model, tokenizer