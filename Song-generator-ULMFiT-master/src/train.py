import pandas as pd
from fastai.text import *
import torch

torch.cuda.set_device(0)

abs_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.dirname(abs_path)

# open file
data_path = os.path.join(parent_path, "data/songdata.csv")
df = pd.read_csv(data_path)

# clean dataset


def clean_dataset(df):
    df = df.dropna()
    df = df.drop(columns=["artist", "song", "link"])
    df = df[:2000]
    return df


df = clean_dataset(df)

# create databunch
nrows, ncols = df.shape
train_size = math.floor(nrows * 0.8)
data_lm = TextLMDataBunch.from_df(
    '.', df.iloc[:train_size], df.iloc[train_size:], text_cols=['text'])
data_lm.save('lm_databunch')

# create language model


def load_databunch(path):
    bs = 32  # lower the batch size if you face 'CUDA out of memory issue'
    path = Path('.')
    data_lm = load_data(path, '..data/lm_databunch', bs=bs)
    return data_lm


# create learner object
learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.5)

# find optimum learning rate


def find_optimum_lr(learner):
    learn.lr_find(start_lr=1e-3, end_lr=1e2)
    learn.recorder.plot()
    return None


# fir one cycle
# Clear unused cache https://pytorch.org/docs/stable/cuda.html#torch.cuda.empty_cache
torch.cuda.empty_cache()
learn.fit_one_cycle(cyc_len=1, max_lr=1e-1, moms=(0.8, 0.7))

# unfreeze model and fine-tune it
learn.unfreeze()
learn.lr_find()
learn.recorder.plot(skip_end=15)

# fit x epoch
learn.fit_one_cycle(cyc_len=5, max_lr=1e-2, moms=(0.8, 0.7))
model_path = os.path.join(parent_path, "models/ft_enc_base")
learn.save_encoder(model_path)

# predict words
TEXT = "You are the sapphire of my heart"
N_WORDS = 200


def compose(TEXT, N_WORDS):
    composed = learn.predict(TEXT, N_WORDS, temperature=0.05)
    print(composed)
    return composed
