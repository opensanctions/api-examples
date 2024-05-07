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
      "q1": {
        "schema": "Person",
        "properties": {
          "name": ["Barack Obama"]
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

  // Check for errors
  if (!response.ok) {
    console.error(await response.text());
    throw new Error('HTTP error\n' + response.status + ' ' + response.statusText);
  }

  // Get the results for our query
  const responseBody = await response.json();
  // We're just JSON encoding the response data here for pretty printing
  console.log(JSON.stringify(responseBody.responses.q1.results, null, 2));
}

match()
  .then()
  .catch((error) => console.log("Error:" + error.message));
