import requests
import json
from .models import CarModel, CarDealer, CarMake, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, KeywordsOptions
from ibmcloudant.cloudant_v1 import CloudantV1
from cloudant.error import CloudantException
from .cloud_creds import cloud_creds

api_key = cloud_creds["IAM_API_KEY"]
couch_url = cloud_creds["COUCH_URL"]
iam_api_key = cloud_creds["IAM_API_KEY"]
couch_username = cloud_creds["COUCH_USERNAME"]
watson_api_key = cloud_creds["WATSON_API_KEY"]
watson_url = cloud_creds["WATSON_URL"]
dealerid_api_url = cloud_creds["DEALERID_API_URL"]
dealerst_api_url = cloud_creds["DEALERST_API_URL"]


def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response


def get_dealers_from_cf(url, **kwargs):
    """
    Retrieves all dealers.
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in doc object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in dealer_doc
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_from_cf(dealer_id):
    """
    Retrieves a dealer by dealer_id.
    """
    results = []
    dealer_id_dict = {"dealer_id": dealer_id}
    payload = json.dumps(dealer_id_dict)
    url = dealerid_api_url
    response = requests.request("GET", url, headers={'Content-Type': 'application/json'}, data=payload)
    json_result = json.loads(response.text)

    if json_result:
        dealers = json_result["result"]["docs"]

        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
            results.append(dealer_obj)
    # print(results)
    return results


def get_dealer_by_state_from_cf(dealer_st):
    """
    Retrieves a dealer by dealer_st (state abbreviation).
    """
    results = []
    dealer_st_dict = {"dealer_st": dealer_st}
    payload = json.dumps(dealer_st_dict)
    url = dealerst_api_url
    response = requests.request("GET", url, headers={'Content-Type': 'application/json'}, data=payload)
    json_result = json.loads(response.text)

    if json_result:
        dealers = json_result["result"]["docs"]

        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
            results.append(dealer_obj)
    # print(results)
    return results


def get_dealership_reviews_from_db(dealer_id):
    """
    Retrieves all reviews associated with a dealer.
    """
    try:
        authenticator = IAMAuthenticator(iam_api_key)
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(couch_url)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    results = []
    db_name = "reviews"
    dealerId = dealer_id

    # Get reviews (posts) by dealerId
    json_result = client.post_find(
        db=db_name,
        selector={'dealership': {'$eq': dealerId}},
        bookmark=None
    ).get_result()

    if json_result:
        # Get the docs list in JSON as reviews
        reviews = json_result["docs"]
        # For each review object
        for review in reviews:
            # Create a DealerReview object with values in review
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], review=review["review"],
                                      purchase=review["purchase"], purchase_date=review["purchase_date"],
                                      car_make=review["car_make"], car_model=review["car_model"],
                                      car_year=review["car_year"], sentiment="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    # print(results)
    return results


def post_dealership_review_to_db(json_payload):
    """
    Posts a new dealer review to database.
    """
    try:
        authenticator = IAMAuthenticator(iam_api_key)
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(couch_url)

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    db_name = "reviews"
    review_doc = json_payload["review"]

    # Post review (document) to database
    json_result = client.post_document(
        db=db_name,
        document=review_doc
    ).get_result()

    # print(json_result)
    return json_result


def analyze_review_sentiments(review_text):
    """
    Analyzes the text from review_obj.review and returns a sentiment label.
    """
    authenticator = IAMAuthenticator(watson_api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)
    natural_language_understanding.set_service_url(watson_url)

    response = natural_language_understanding.analyze(
        text=review_text,
        features=Features(
            keywords=KeywordsOptions(sentiment=True, limit=5),
            sentiment=SentimentOptions(document=True)),
        return_analyzed_text=True).get_result()

    json_dump = json.dumps(response)
    json_result = json.loads(json_dump)
    sentiment_label = json_result['sentiment']['document']['label']

    # print("Sentiment Result: " + sentiment_label)
    return sentiment_label
