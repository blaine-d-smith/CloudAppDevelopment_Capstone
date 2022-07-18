#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
import requests
import json


with open('../cloud-creds.json', 'r') as f:
    cloud_creds = json.load(f)


def main():
    try:
        client = Cloudant.iam(
            account_name=cloud_creds["COUCH_USERNAME"],
            api_key=cloud_creds["IAM_API_KEY"],
            connect=True,
        )
        # print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}


def get_dealerships():
    try:
        client = Cloudant.iam(
            account_name=cloud_creds["COUCH_USERNAME"],
            api_key=cloud_creds["IAM_API_KEY"],
            connect=True,
        )
        # print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    dealerships = client["dealerships"]

    # for dealership in dealerships:
    #     print(dealership)

    end_point = '{0}/{1}'.format(client.server_url, 'dealerships/_all_docs')
    params = {'include_docs': 'true'}
    response = client.r_session.get(end_point, params=params)
    return response.json()

# def get_dealership_reviews(params):
#     try:
#         CLOUDANT_URL = cloud_creds["COUCH_URL"]
#         CLOUDANT_APIKEY = cloud_creds["IAM_API_KEY"]
#         CLOUDANT_USERNAME = cloud_creds["COUCH_USERNAME"]
#
#         authenticator = IAMAuthenticator(CLOUDANT_APIKEY)
#         client = CloudantV1(authenticator=authenticator)
#         client.set_service_url(CLOUDANT_URL)
#
#     except CloudantException as ce:
#         print("unable to connect")
#         return {"error": ce}
#     except (requests.exceptions.RequestException, ConnectionResetError) as err:
#         print("connection error")
#         return {"error": err}
#
#     results = []
#     db_name = "reviews"
#     dealerId = params["dealer_id"]
#
#     json_result = client.post_find(
#         db=db_name,
#         selector={'dealership': {'$eq': dealerId}},
#         bookmark=None
#     ).get_result()
#
#     if json_result:
#         # Get the row list in JSON as reviews
#         reviews = json_result["docs"]
#         # For each review object
#         for review in reviews:
#             review_obj = DealerReview(dealership=review["dealership"], name=review["name"], review=review["review"],
#                                       purchase=review["purchase"], purchase_date=review["purchase_date"],
#                                       car_make=review["car_make"], car_model=review["car_model"],
#                                       car_year=review["car_year"], sentiment=review["sentiment"], id=review["id"])
#             # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             results.append(review_obj)
#
#     return results


def get_dealership_by_state(st):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=cloud_creds["COUCH_USERNAME"],
            api_key=cloud_creds["IAM_API_KEY"],
            connect=True,
        )
        # print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    dealerships = client[databaseName]

    for dealership in dealerships:
        pass


# print(get_dealership_reviews({'dealer_id': 23}))
# get_dealerships()

