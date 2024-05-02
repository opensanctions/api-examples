# Python examples

## Requirements

You can use any HTTP client, but we'll use
[requests](https://requests.readthedocs.io/en/latest/) in these examples.

You can install and use it inside a virtual environment as follows:

Change to the python directory in this repository in your command line shell.

The first time, create a virtual environment and install the dependencies:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Subsequent times you come back to this, just activate the virtual environment.

```bash
source env/bin/activate
```

## Configuration

Set your secret API key as an environment variable. That way you can use it in
the code examples without having to paste it in all the time or sharing it accidentally.

```bash
export OS_API_KEY=...your key here without dots...
```


## Examples


### Simple name matching

In this example we query for entities of the Person schema matching a single full
name, Barack Obama.

We will run the code in [match_name.py](match_name.py), also shown below:

```python
from pprint import pprint
import requests
import os

OS_API_KEY = os.getenv("OS_API_KEY")

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
```

Run the code:

```bash
python match_name.py
```


### Matching on name and date of birth

In this example we query for Persons matching by name and date of birth.

The values are in arrays because in person and company data, it's common to have
multiple forms or versions of a name for the same entity. See this used below.

In the response, we look for results under the `responses.q1.results` keys. Each result
is a FollowTheMoney entity with additional keys like `score`, `match`, and
`features` indicating how strongly this entity matched the query. Note which
[features](https://www.opensanctions.org/matcher/) were good matches contributing
to the score, and which features weren't, reducing the score.

We will run the code in [match_name_birth_date.py](match_name_birth_date.py), also shown below:

```python
# Prepare a query to match on schema and the name and birthDate properties
query = {
    "queries": {
        "q1": {
            "schema": "Person",
            "properties": {"name": ["Barack Obama"], "birthDate": ["1961-08-04"]},
        }
    }
}

# Make the request
response = requests.post(
    "https://api.opensanctions.org/match/default", headers=headers, json=query
)

# Check for HTTP errors
response.raise_for_status()

# Get the ID, name, match status, score, and features for each result
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
```

Run the code:

```bash
python match_name_birth_date.py
```


### Matching on name and address

In this example we're matching on name and address. This field is a full address
in a single string.

While the Person schema requires these entities to have the `name` property, the
`address` property is optional and data for this is unavailable for most entities.
Still, it can be used to improve the score when it matches, moving good matching
entities higher up in the result list.

Note the use of the `regression-v1` [algorithm](https://www.opensanctions.org/matcher/#regression-v1)
which supports the `address` feature. Note also that
[custom thresholds should be adapted to the algorithm used](https://www.opensanctions.org/docs/api/scoring/).

Check the `features` object in the results to see if the address matched, and how well.

We will run the code in [match_name_address.py](match_name_address.py), also shown below:

```python
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
```

Run the code:

```bash
python match_name_address.py
```


### Performing multiple queries in one request

You can batch up multiple queries into the same HTTP request to reduce overhead.
We recommend 20-50 queries per request, rather than hundreds or thousands.

Each query is identified by a unique key you can make up, and the results relevant
to that key will be listed under that key in the response. In this case, you'll
find results for `Arkady` under `query-A` and `Stroygazmontazh` under `query-B`.

We will run the code in [multiple_queries.py](multiple_queries.py), also shown below:

```python
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
```

Run the code:

```bash
python multiple_queries.py
```
