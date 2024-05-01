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

    # Prepare two queries for one request
    query = {
        "queries": {
            "query-A": {
                "schema": "Person",
                "properties": {
                    "name": ["Arkadiii Romanovich Rotenberg", "Ротенберг Аркадий"],
                    "birthDate": ["1951"],
                },
            },
            "query-B": {
                "schema": "Company",
                "properties": {"name": ["Stroygazmontazh"], "jurisdiction": ["Russia"]},
            },
        }
    }

    # Make the request
    response = requests.post(
        "https://api.opensanctions.org/match/default", headers=headers, json=query
    )

    # Check for HTTP errors
    response.raise_for_status()

    for query_id in query["queries"].keys():
        print(f"\nResults for query {query_id}:")
        # Get the ID, name, match, score, and features for each result
        results = []
        for match in response.json()["responses"][query_id]["results"]:
            results.append(
                {
                    "id": match["id"],
                    "name": match["properties"]["name"],
                    "match": match["match"],
                }
            )

        # print it out with nice formatting
        pprint(results, sort_dicts=False)


if __name__ == "__main__":
    main()
