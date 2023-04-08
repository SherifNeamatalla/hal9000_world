import stripJsonTrailingCommas from 'strip-json-trailing-commas';

export function parseJSONWithTrailingCommas(jsonString) {
  // Remove trailing commas from objects and arrays using a regular expression
  const cleanedJSONString = stripJsonTrailingCommas(jsonString);

  // Parse the cleaned JSON string using the standard JSON.parse() method
  return JSON.parse(cleanedJSONString);
}

const jsonWithTrailingCommas = `
{
  "name": "John Doe",
  "age": 30,
  "hobbies": [
    "reading",
    "travelling",
  ],
}
`;

try {
  const parsedObject = parseJSONWithTrailingCommas(jsonWithTrailingCommas);
  console.log(parsedObject);
} catch (error) {
  console.error('Invalid JSON:', error);
}
