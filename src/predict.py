import joblib
import config
import torch

from dataset import EntityDataset
from model import EntityModel

meta_data = joblib.load("meta.bin")
enc_pos = meta_data["enc_pos"]
enc_tag = meta_data["enc_tag"]

num_pos = len(list(enc_pos.classes_))
num_tag = len(list(enc_tag.classes_))

sentence = """
daijianghai was born in jiangsu and his school is harvard
"""
tokenized_sentence = config.TOKENIZER.encode(sentence)

sentence = sentence.split()
print(sentence)
print(tokenized_sentence)

test_dataset = EntityDataset(
    texts=[sentence],
    pos=[[0] * len(sentence)],
    tags=[[0] * len(sentence)]
)

device = torch.device("cuda")
model = EntityModel(num_tag=num_tag, num_pos=num_pos)
model.load_state_dict(torch.load(config.MODEL_PATH))
model.to(device)

with torch.no_grad():
    data = test_dataset[0]
    for k, v in data.items():
        data[k] = v.to(device).unsqueeze(0)
    tag, pos, _ = model(**data)

    print(
        enc_tag.inverse_transform(
            tag.argmax(2).cpu().numpy().reshape(-1)
        )[1:len(tokenized_sentence)-1]
    )
    print(
        enc_pos.inverse_transform(
            pos.argmax(2).cpu().numpy().reshape(-1)
        )[1:len(tokenized_sentence)-1]
    )