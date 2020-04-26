# https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582

from gtts import gTTS
from fastai.text import *
import streamlit as st
import pandas as pd
import os

abs_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.dirname(abs_path)

"""
# Lyricist Companion Bot
Enter any text and let me compose something for you!
"""
data_path = os.path.join(os.path.dirname(abs_path), "data/")

data_lm = load_data(data_path, 'lm_databunch', bs=192)

learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.5)

model_path = os.path.join(parent_path, "model/",
                          "ft_enc_base")

learn.load_encoder(model_path)


N_WORDS = st.text_input('Number of words:', (100))
temperature = st.text_input('Creativity level (between 0 - 2):', (0.8))
text_input = st.text_input('Enter text...', ('a new song I sing'))

poem = learn.predict(text_input, int(N_WORDS), temperature=float(temperature))

"""
# Here's your poem!
"""
poem
