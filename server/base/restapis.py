import requests
import json
from .models import CarModel, CarDealer, CarMake, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, EntitiesOptions, KeywordsOptions
from ibmcloudant.cloudant_v1 import CloudantV1
from cloudant.error import CloudantException
from .cloud_creds import cloud_creds

api_key = cloud_creds["IAM_API_KEY"]
couch_url = cloud_creds["COUCH_URL"]
iam_api_key = cloud_creds["IAM_API_KEY"]
couch_username = cloud_creds["COUCH_USERNAME"]


def get_request(url, **kwargs):
    # print(kwargs)
    # print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            # results.append(dealer_doc)
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    # all_keys = set().union(*(d.keys() for d in results))
    # return all_keys
    return results


def get_dealer_from_cf(dealer_id):
    results = []
    dealer_id_dict = {"dealer_id": dealer_id}
    payload = json.dumps(dealer_id_dict)
    # print(payload)
    url = "https://8f6ed1e1.us-south.apigw.appdomain.cloud/api/dealerid"
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

    # json_result = get_request(url, dealer_id=params)
    # print(json_result["result"]["docs"])
    # if json_result:
    #     dealers = json_result["docs"]
    #     for dealer in dealers:
    #         dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
    #                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
    #                                short_name=dealer["short_name"],
    #                                st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
    #         results.append(dealer_obj)
    # # print(results)
    # return results


def get_dealership_reviews_from_db(dealer_id):
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

    json_result = client.post_find(
        db=db_name,
        selector={'dealership': {'$eq': dealerId}},
        bookmark=None
    ).get_result()

    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["docs"]
        # print(reviews)
        # For each review object
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], review=review["review"],
                                      purchase=review["purchase"], purchase_date=review["purchase_date"],
                                      car_make=review["car_make"], car_model=review["car_model"],
                                      car_year=review["car_year"], sentiment=review["sentiment"], id=review["id"])
            # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    # print(results)
    return results


# def get_dealer_by_state(url, **kwargs):
#     results = []
#     dealer_st = kwargs['dealer_st']
#     # Call get_request with a URL parameter
#     json_result = get_request(url, dealer_st=dealer_st)
#

# def get_dealer_reviews_from_cf(url, dealer_id):
#     results = []
#     # get_request with params
#     # dealer_id = kwargs['dealer_id']
#     dealer_dict = {'dealer_id': 23}
#     print(dealer_dict)
#     json_result = get_request(url, dealer_id=dealer_dict)
#     if json_result:
#         # Get the row list in JSON as reviews
#         reviews = json_result["docs"]
#         # For each review object
#         for review in reviews:
#             review_obj = DealerReview(dealership=review["dealership"], name=review["name"], review=review["review"],
#                                       purchase=review["purchase"], purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"],
#                                       car_year=review["car_year"], sentiment=review["sentiment"], id=review["id"])
#             # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             results.append(review_obj)
#
#     return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(url, **kwargs):
#     authenticator = IAMAuthenticator('pBcLu4v_1q7736kiwEKR7LchAqW6fjmUCarcQO5Z7oLf')
#     natural_language_understanding = NaturalLanguageUnderstandingV1(
#         version='2022-04-07',
#         authenticator=authenticator)
#
#     natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/350966bb-e779-4d6f-99fc-ba646e7a7f68')
#
#     params = dict()
#     params["text"] = kwargs["text"]
#     params["version"] = kwargs["version"]
#     params["features"] = kwargs["features"]
#     params["return_analyzed_text"] = kwargs["return_analyzed_text"]
#
#     response = natural_language_understanding.analyze(
#
#     print(json.dumps(response, indent=2))
