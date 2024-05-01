# Curl (Linux and OS X command line) examples


## Requirements

- [curl](https://curl.se/)
- [jq] (optional) for formatting the JSON responses
  - Leave out the `| jq .` part in the examples if you don't want to use this.


## Configuration

Set your secret API key as an environment variable. That way you can use it in
the code examples without having to paste it in all the time or sharing it accidentally.

```bash
export OS_API_KEY=...your key here without dots...
```


## Simple name matching

In this example we query for entities of the Person schema matching a single full
name, Barack Obama.

In the response, we look for results under the `responses.q1.results`. Each result
is a FollowTheMoney entity with additional keys like `score`, `match`, and
`features` indicating how strongly this entity matched the query.

```bash
curl \
  --silent \
  -H"Content-Type: application/json"  \
  -H"Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "q1": {
            "properties": {
                "name": "Barack Obama"
            },
            "schema": "Person"
        }
    }
}' \
 'https://api.opensanctions.org/match/default' | jq .
```


## Name and date of birth matching

In this example we query for Persons matching by name and date of birth.

In the results, note which [features](https://www.opensanctions.org/matcher/)
were good matches contributing to the score, and which features weren't, reducing
the score.

```bash
curl \
  --silent \
  -H"Content-Type: application/json"  \
  -H"Authorization: ${OS_API_KEY}" \
  --data '
{
    "queries": {
        "q1": {
            "properties": {
                "name": "Barack Obama",
                "birthDate": "1961-08-04"
            },
            "schema": "Person"
        }
    }
}' \
 'https://api.opensanctions.org/match/default' | jq .
