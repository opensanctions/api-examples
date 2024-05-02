const OS_API_KEY = process.env.OS_API_KEY;
if (!OS_API_KEY) {
  console.log('Please set the OS_API_KEY environment variable');
  process.exit(1);
}

async function match() {
  const headers = {
    // Prepare authentication using the Authorization header
    "Authorization": OS_API_KEY,

    // We're going to encode the request body as JSON.
    'Content-Type': 'application/json',
  };

  // Prepare a query to match on schema and the name property
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

  // Check for errors
  if (!response.ok) {
    console.error(await response.text());
    throw new Error('HTTP error\n' + response.status + ' ' + response.statusText);
  }

  const responseBody = await response.json();

  // Get the results for each query
  for (const [queryId, query] of Object.entries(requestBody.queries)) {
    console.log(`\nResults for query ${queryId}:`)

    // We look up the query results by ID in the responses object
    const results = responseBody.responses[queryId].results.map((result) => {
      return {
        "id": result.id,
        "name": result.properties.name,
        "match": result.match,
      }
    });

    // We're just JSON encoding the response data here for pretty printing
    console.log(JSON.stringify(results, null, 2));
  };
}

match()
  .then()
  .catch((error) => console.log("Error:" + error.message));
