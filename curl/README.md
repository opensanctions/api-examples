# Curl (Linux and OS X command line) examples


## Requirements

- [curl](https://curl.se/)
- [jq](https://jqlang.github.io/jq/) (optional) for formatting the JSON responses
  - Leave out `| jq .` onwards in the examples if you don't want to use this.


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

```bash
curl \
  --silent \
  --fail-with-body \
  --show-error \
  --header "Content-Type: application/json"  \
  --header "Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "q1": {
            "schema": "Person",
            "properties": {
                "name": ["Barack Obama"]
            }
        }
    }
}' \
 'https://api.opensanctions.org/match/default' | jq .
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

```bash
curl \
  --silent \
  --fail-with-body
  --show-error \
  --header "Content-Type: application/json"  \
  --header "Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "q1": {
            "schema": "Person",
            "properties": {
                "name": ["Barack Obama"],
                "birthDate": ["1961-08-04"]
            }
        }
    }
}' \
 'https://api.opensanctions.org/match/default' | jq .
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

```bash
curl \
  --silent \
  --fail-with-body
  --show-error \
  --header "Content-Type: application/json"  \
  --header "Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "q1": {
            "schema": "Person",
            "properties": {
                "name": ["Vladimir", "Wladimir"],
                "address": ["Kremlin, Moscow"],
                "country": ["ru"]
            }
        }
    }
}' \
 'https://api.opensanctions.org/match/default?algorithm=regression-v1' | jq .
```


### Performing multiple queries in one request

You can batch up multiple queries into the same HTTP request to reduce overhead.
We recommend 20-50 queries per request, rather than hundreds or thousands.

Each query is identified by a unique key you can make up, and the results relevant
to that key will be listed under that key in the response. In this case, you'll
find results for `Arkady` under `query-A` and `Stroygazmontazh` under `query-B`.

```bash
curl \
  --silent \
  --fail-with-body
  --show-error \
  --header "Content-Type: application/json"  \
  --header "Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "query-A": {
            "schema": "Person",
            "properties": {
                "name": ["Arkadiii Romanovich Rotenberg", "Ротенберг Аркадий"],
                "birthDate": ["1951"]
            }
        },
        "query-B": {
            "schema": "Company",
            "properties": {
                "name": ["Stroygazmontazh"],
                "jurisdiction": ["Russia"]
            }
        }
    }
}' \
 'https://api.opensanctions.org/match/default' | jq .
```
