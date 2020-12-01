from api.berts import BERT

from barlaw.settings import device, model, tokenizer

import torch


def recommend(title, content, *category):
    # model.load_state_dict(torch.load('api/berts/20201112-1650_0_(accu _ 0.81)(epoch _ 10).pt', map_location = device))
    # # model.cuda()
    # model.eval()
    # device, model, tokenizer = USE_BERT_dict.load_model()

    df_BERT = BERT.get_similar(device, model, tokenizer, title, content,  *category)
    dict_BERT = df_BERT.to_dict("records")
    return dict_BERT
