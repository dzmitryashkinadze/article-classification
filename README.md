# Article Classification Tool
I will use this repo to demonstrate the end-to-end development process for the tool able to recommend MDPI journals for the user-written manuscript.

Development Steps:
1. Solution Design
2. Backend Development
3. Application Development
4. Packaging and Deployment

## Solution Design
In here is my prep, or a "research phase" before jumping into the code.

### Main requirement
The tool should be able to process user manuscript (title and abstract), recommend top 3 of the available MDPI journals to publish it in and give detailed explanation.

### Data source
For access to the articles I will use the MDPI journals list website (https://www.mdpi.com/about/journals) 

### Tech stack
1. The whole solution will be written in Python 3.12
2. I will use OpenAI SDK for access to the LLM model
3. Flask to build a REST API for article recommendation
4. Streamlit to build a minimalistic UI

### How this is going to work?
Prototyping (Step 1). First I will prototype a script to extract the list of MDPI journals and treir descriptions from the web, pass journal descriptions to the LLM together with user-written manuscript and get the matching (prototype.ipynb).

Data Pypeline (Step 2). Than I will package the journal data extraction step in an Airflow DAG (this will later be deployed and scheduled for a regular automated update).

Backend Development (Step 3). Than I will package the GenAI code in a pip-installable Python package.

Flask Development (Step 4). Than I will develop a simlple REST-API for article recommendation that can be used on its-own but will also drive our Streamlit font-end.

Streamlit Development (Step 5). Than I will develop a simple Streamlit UI for the article recommendation.

## Prototyping (Step 1)
Have a look in 01_prototyping

## Data Pypeline (Step 2)
Here I will package the code responsible for the generation of the journal list in an Airflow DAG

## Backend Development (Step 3)
Here I will package the GenAI code (query generation and submission on OpenAI) in a Python package

## Flask Development (Step 4)
Here I will develop the Flask REST API

## Streamlit Development (Step 5)
Here I will develop the Streamlit interface


