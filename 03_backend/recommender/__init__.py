import pandas as pd


class Recommender:
    """
    Recommender base class
    """

    def __init__(self, config):

        # copy over the config
        self.config = config

        # load the cleaned journals
        journals = pd.read_csv(config["DATA"]["JOURNALS_PATH"])

        # load the cleaned journals into the context
        self.context = ""
        for i, row in journals.iterrows():
            self.context += f"""Journal {i+1}. {row['title']}\nLink: {row['link']}\nDescription: {row['description']}\n\n"""

    def generate_recommendations(self, client, manuscript, format):
        """Recommend a journal based on the user manuscript"""

        # get system prompt from config
        SYSTEM_PROMPT = self.config["GENAI"]["SYSTEM_PROMPT"]

        # construct user prompt`
        match format:
            case "streamlit":
                USER_PROMPT = self.config["GENAI"]["USER_PROMPT"].format(
                    title=manuscript["title"], abstract=manuscript["abstract"]
                )
            case "API":
                USER_PROMPT = self.config["GENAI"]["USER_PROMPT_API"].format(
                    title=manuscript["title"], abstract=manuscript["abstract"]
                )
            case _:
                raise ValueError(f"Invalid format: {format}")

        # construct the context prompt
        self.CONTEXT_PROMPT = self.config["GENAI"]["CONTEXT_PROMPT"].format(
            context=self.context
        )

        # create completion
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
                {"role": "assistant", "content": self.CONTEXT_PROMPT},
            ],
        )

        # return the response
        return completion.choices[0].message.content
