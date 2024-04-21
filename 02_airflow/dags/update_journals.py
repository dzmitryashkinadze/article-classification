from __future__ import annotations

# python packages
import time
import yaml
import requests
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from bs4 import BeautifulSoup

# airflow packages
from airflow.decorators import dag, task


@dag()
def UPDATEJOURNALS():
    @task()
    def run():

        # load the configs
        with open("/config_private.yaml", "r") as f:
            config_private = yaml.safe_load(f)
        with open("/config_public.yaml", "r") as f:
            config_public = yaml.safe_load(f)
        config = {**config_private, **config_public}

        # create the client
        client = OpenAI(api_key=config["OPENAI"]["API_KEY"])

        # load the soap from url
        url = config["DATA"]["JOURNALS_URL"]
        headers = config["DATA"]["HEADERS"]
        r = requests.get(url, headers=headers)
        soap = BeautifulSoup(r.content, "html5lib")

        # find all <td> with class 'journal-title'
        journals_html = soap.find_all("td", class_="journal-name-cell")
        print("Number of journals:", len(journals_html))
        journals = []

        # for each journal extract the title and the link
        for j in journals_html:

            # extract the title and remove the \n
            title = j.find("a").text
            title = title.replace("\n", "")

            # extract the link
            link = f"https://www.mdpi.com{j.find('a').get('href')}"
            journals.append((title, link))

        # convert journals to pandas
        journals = pd.DataFrame(journals, columns=["title", "link"])

        # for each journal navigate to the link and extract the description
        descriptions = []
        for link in tqdm(journals["link"]):
            r = requests.get(link, headers=headers)
            soap = BeautifulSoup(r.content, "html5lib")
            description = soap.find("div", class_="journal__description__content").text
            descriptions.append(description)

            # sleep for 1 second
            time.sleep(1)

        # add the descriptions to the journals
        journals["description"] = descriptions

        # clean the descriptions
        def extract_open_access(description):
            end = description.find("Open Access")
            return description[:end].strip().replace("\n", " ")

        journals["description"] = journals["description"].apply(extract_open_access)
        journals.to_csv("/data/journals.csv", index=False)

        return True

    # set variables
    run()


UPDATEJOURNALS()
