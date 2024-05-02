from pprint import pprint
import requests
import os

OS_API_KEY = os.getenv("OS_API_KEY")
if not OS_API_KEY:
    raise ValueError("The OS_API_KEY environment variable is not set")


def main():
    # Prepare authentication using the Authorization header
    headers = {
        "Authorization": OS_API_KEY,
    }

    # Prepare a query to match on schema and the name and address properties
    query = {
        "queries": {
            "q1": {
                "schema": "Person",
                "properties": {
                    "name": ["Vladimir", "Wladimir"],
                    "address": ["Kremlin, Moscow"],
                    "country": ["ru"],
                },
            }
        }
    }

    # Select the regresion-v1 algorithm for address matching support
    params = {
        "algorithm": "regression-v1",
    }

    # Make the request
    response = requests.post(
        "https://api.opensanctions.org/match/default",
        params=params,
        headers=headers,
        json=query,
    )

    # Check for HTTP errors
    response.raise_for_status()

    # Get the ID, name, match, score, and features for each result
    results = []
    for result in response.json()["responses"]["q1"]["results"]:
        results.append(
            {
                "id": result["id"],
                "name": result["properties"]["name"],
                "match": result["match"],
                "score": result["score"],
                "features": result["features"],
            }
        )

    # print it out with nice formatting
    pprint(results, sort_dicts=False)


if __name__ == "__main__":
    main()
