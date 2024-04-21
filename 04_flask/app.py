# simple flask app
import yaml
from flask import Flask
from flask import request, jsonify
from openai import OpenAI
from recommender import Recommender
from functools import wraps

# load the configs
with open("../config_private.yaml", "r") as f:
    config_private = yaml.safe_load(f)
with open("../config_public.yaml", "r") as f:
    config_public = yaml.safe_load(f)
config = {**config_private, **config_public}

# create the OpenAI client
client = OpenAI(api_key=config["OPENAI"]["API_KEY"])

# create the app
app = Flask(__name__)


# add a decorator that checks the Bearer token
def check_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        # get the token from the request
        token = request.headers.get("Authorization")

        # check if the token is correct
        if token and token == f"Bearer {config['FLASK']['SECRET']}":
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper


# add endpoint to run the recommender with manuscript input
@app.route("/recommend_streamlit", methods=["POST"])
@check_token
def recommend_streamlit():
    """Recommend a journal in a streamlit format based on the user manuscript"""

    # get the manuscript from the request
    manuscript = request.json

    # create the recommender
    recommender = Recommender(config)

    # return the recommendations
    return jsonify(
        recommender.generate_recommendations(client, manuscript, format="streamlit")
    )


# add endpoint to run the recommender with manuscript input
@app.route("/recommend_api", methods=["POST"])
@check_token
def recommend_api():
    """Recommend a journal in API format based on the user manuscript"""

    # get the manuscript from the request
    manuscript = request.json

    # create the recommender
    recommender = Recommender(config)

    # return the recommendations
    return jsonify(
        recommender.generate_recommendations(client, manuscript, format="API")
    )


if __name__ == "__main__":
    app.run(port=5000)
