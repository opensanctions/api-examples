from pprint import pprint
import requests
import os

OS_API_KEY = os.getenv("OS_API_KEY")
if not OS_API_KEY:
    raise ValueError("The OS_API_KEY environment variable is not set")


def main():
    # Prepare a query to match on schema and the name property
    query = {
        "queries": {
            "q1": {"schema": "Person", "properties": {"name": ["Barack Obama"]}}
        }
    }
    # Authenticate using the API key in the Authorization header
    headers = {
        "Authorization": OS_API_KEY,
    }
    response = requests.post(
        "https://api.opensanctions.org/match/default", headers=headers, json=query
    )
    # Check for HTTP errors
    response.raise_for_status()

    # Get the results for our query
    q1_results = response.json()["responses"]["q1"]["results"]

    # print it out with nice formatting
    pprint(q1_results, sort_dicts=False)


if __name__ == "__main__":
    main()
