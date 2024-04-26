import yaml
import requests
import logging
import pandas as pd
import streamlit as st
from openai import OpenAI

# load the configs
with open("config_private.yaml", "r") as f:
    config_private = yaml.safe_load(f)
with open("config_public.yaml", "r") as f:
    config_public = yaml.safe_load(f)
config = {**config_private, **config_public}

######
# UI #
######

# set title
st.title("Match your manuscript to an MDPI journal")

# add a form with an input for the manuscript title and a text area for abstract
with st.form(key="my_form"):
    title = st.text_input(label="Manuscript title")
    abstract = st.text_area(label="Abstract")
    submit_button = st.form_submit_button(label="Submit")

# if the form is submitted
if submit_button:

    # call the recommender
    manuscript = {
        "title": title,
        "abstract": abstract,
    }
    url = config["STREAMLIT"]["BACKEND_URL"]
    headers = {"Authorization": f'Bearer {config["FLASK"]["SECRET"]}'}
    recommendation = requests.post(url, headers=headers, json=manuscript).json()

    # markdown for the response
    st.markdown(recommendation)
