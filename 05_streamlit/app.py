import yaml
import pandas as pd
import streamlit as st
from openai import OpenAI

# load the config
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

# create the client
client = OpenAI(api_key=config["OPENAI"]["API_KEY"])

# load the cleaned journals
journals = pd.read_csv('../data/journals_with_description_cleaned.csv')

# load the cleaned journals into the context
CONTEXT = 'MDPI journals:\n'
for i, row in journals.iterrows():
    CONTEXT += f"""Journal {i+1}. {row['title']}\nLink: {row['link']}\nDescription: {row['description']}\n\n"""

######
# UI #
######

# set title
st.title('Match your manuscript to an MDPI journal')

# add a form with an input for the manuscript title and a text area for abstract
with st.form(key='my_form'):
    title = st.text_input(label='Manuscript title')
    abstract = st.text_area(label='Abstract')
    submit_button = st.form_submit_button(label='Submit')

# if the form is submitted
if submit_button:

    # user prompt
    USER_PROMPT = config['GENAI']['USER_PROMPT'].format(title=title, abstract=abstract)

    # create completion
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": config['GENAI']['SYSTEM_PROMPT']},
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": CONTEXT},
        ]
    )

    # markdown for the response
    st.markdown(completion.choices[0].message.content)

