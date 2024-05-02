# Javascript examples (NodeJS, server-side)

These examples are for using Javascript using NodeJS. This could for example be
an Express API or NextJS page you expose to your application, or a script you
write using Javascript.


## Requirements

You can use any HTTP client, but we'll use
[the fetch API](https://nodejs.org/dist/latest-v21.x/docs/api/globals.html#fetch)
available in NodeJS v21 in these examples.


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

We will run the code in [match_name.js](match_name.js), also shown below:

```javascript
const headers = {
  // Prepare authentication using the Authorization header
  "Authorization": OS_API_KEY,
  
  // We're going to encode the request body as JSON.
  'Content-Type': 'application/json',
};
// Prepare a query to match on schema and the name property
const requestBody = {
  "queries": {
    "q1": { 
      "schema": "Person",
      "properties": { "name": ["Barack Obama"] }
    }
  }
}

// Make the request
const response = await fetch(
'https://api.opensanctions.org/match/default',
{
  'method': 'POST',
  'headers': headers,
  'body': JSON.stringify(requestBody),
});

// Check for errors
if (!response.ok) {
  console.error(await response.text());
  throw new Error('HTTP error\n' + response.status + ' ' + response.statusText);
}

// Get the results for our query
const responseBody = await response.json();
// We're just JSON encoding the response data here for pretty printing
console.log(JSON.stringify(responseBody.responses.q1.results, null, 2));
```

Run the code:

```bash
node match_name.js
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

We will run the code in [match_name_birth_date.js](match_name_birth_date.js), also shown below:

```javascript
// Prepare a query to match on schema and the name and birthDate properties
const requestBody = {
  "queries": {
    "q1": {
      "schema": "Person",
      "properties": {
        "name": ["Barack Obama"],
        "birthDate": ["1961-08-04"]
      }
    }
  }
}

// Make the request
const response = await fetch(
  'https://api.opensanctions.org/match/default',
  {
    'method': 'POST',
    'headers': headers,
    'body': JSON.stringify(requestBody),
  });

    // Get the results for our query
  const responseBody = await response.json();

  // Get the ID, name, match status, score, and features for each result
  const results = responseBody.responses.q1.results.map((result) => {
    return {
      "id": result.id,
      "name": result.properties.name,
      "match": result.match,
      "score": result.score,
      "features": result.features
    }
  });
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

We will run the code in [match_name_address.js](match_name_address.js), also shown below:

```javascript
// Prepare a query to match on schema and the name, address, and country properties
const requestBody = {
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

// Construct the request URL
const url = new URL('https://api.opensanctions.org/match/default');
url.searchParams.set('algorithm', 'regression-v1');

// Make the request
const response = await fetch(
  url,
  {
    'method': 'POST',
    'headers': headers,
    'body': JSON.stringify(requestBody),
  });
```

Run the code:

```bash
node match_name_address.js
```


### Performing multiple queries in one request

You can batch up multiple queries into the same HTTP request to reduce overhead.
We recommend 20-50 queries per request, rather than hundreds or thousands.

Each query is identified by a unique key you can make up, and the results relevant
to that key will be listed under that key in the response. In this case, you'll
find results for `Arkady` under `query-A` and `Stroygazmontazh` under `query-B`.

We will run the code in [multiple_queries.js](multiple_queries.js), also shown below:

```javascript
// Prepare two queries for one request
const requestBody = {
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
      "properties": { "name": ["Stroygazmontazh"], "jurisdiction": ["Russia"] },
    },
  }
}

// Construct the request URL
const url = new URL('https://api.opensanctions.org/match/default');
url.searchParams.set('algorithm', 'regression-v1');

// Make the request
const response = await fetch(
  url,
  {
    'method': 'POST',
    'headers': headers,
    'body': JSON.stringify(requestBody),
  });
```

Run the code:

```bash
node multiple_queries.js
```
