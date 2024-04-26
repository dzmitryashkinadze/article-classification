# simple flask app
import yaml
import logging
from flask import Flask
from flask import request, jsonify
from openai import OpenAI
from recommender import Recommender
from functools import wraps

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# load the configs
with open("config_private.yaml", "r") as f:
    config_private = yaml.safe_load(f)
with open("config_public.yaml", "r") as f:
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

            # log
            logging.info("Recorded unauthorized access")
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper


# add endpoint to run the recommender with manuscript input
@app.route("/recommend_streamlit", methods=["POST"])
@check_token
def recommend_streamlit():
    """Recommend a journal in a streamlit format based on the user manuscript"""

    # get the manuscript from the request
    manuscript = request.json

    # log
    logging.info("Endpoint /recommend_streamlit")
    logging.info(f"Input manuscript: {manuscript}")

    # create the recommender
    recommender = Recommender(config)

    # create recommendations
    recommendations = recommender.generate_recommendations(
        client, manuscript, format="streamlit"
    )

    # return the recommendations
    return jsonify(recommendations)


# add endpoint to run the recommender with manuscript input
@app.route("/recommend_api", methods=["POST"])
@check_token
def recommend_api():
    """Recommend a journal in API format based on the user manuscript"""

    # get the manuscript from the request
    manuscript = request.json

    # log
    logging.info("Endpoint /recommend_api")
    logging.info(f"Input manuscript: {manuscript}")

    # create the recommender
    recommender = Recommender(config)

    # create recommendations
    recommendations = recommender.generate_recommendations(
        client, manuscript, format="API"
    )

    # return the recommendations
    return jsonify(recommendations)


# Endpoint 3: Health Check
@app.route("/health", methods=["GET"])
def health_check():
    # The endpoint simply returns a JSON response indicating the service is up
    return jsonify({"status": "up"}), 200
