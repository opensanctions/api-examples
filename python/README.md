#

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

We will run the code in [match_name.py]("match_name.py"), also shown below:

```python
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
q1 = response.json()["responses"]["q1"]["results"]

# print it out with nice formatting
pprint(q1, sort_dicts=False)
```

Run the code:

```bash
python match_name.py
```


### Matching on name and date of birth

In the response, we look for results under the `responses.q1.results` keys. Each
result is a FollowTheMoney entity with additional keys like `score`, `match`, and
`features` indicating how strongly this entity matched the query.
