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
import requests

cloud_cred = {
    "COUCH_URL": "https://05c35462-27e4-4eb3-bafa-2d78d4ee463d-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "rmaabsX7VQZyv9zf2hhxCICk6bnPeiFpAJ-O8kQEu_HO",
    "COUCH_USERNAME": "05c35462-27e4-4eb3-bafa-2d78d4ee463d-bluemix"
}


def main(dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}


main(cloud_cred)
