import transformers


MAX_LEN = 128
TRAIN_BATCH_SIZE = 12
VALID_BATCH_SIZE = 4
EPOCHS = 3
BASE_MODEL_PATH = r"E:\Huggingface_Model\BERT\bert-base-uncased"
MODEL_PATH = "model.bin"
TRAINING_FILE = "../input/ner_dataset.csv"
TOKENIZER = transformers.BertTokenizer.from_pretrained(
    BASE_MODEL_PATH,
    do_lower_case=True
)