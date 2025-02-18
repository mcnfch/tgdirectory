# Directory Listing Components

## URL Structure
Each restaurant listing should link to its detail page following this format:
```
https://noogabites.com/listing/{restaurant-name-hyphenated}-{last-6-chars-of-google-places-id}
```

Example:
```
https://noogabites.com/listing/frothy-monkey-fLBMFE
```

## Implementation Requirements

### DirectoryList Component
- The entire listing card should be clickable, not just the restaurant name
- URL generation:
  1. Convert restaurant name to lowercase and replace spaces/special chars with hyphens
  2. Take the last 6 characters of the Google Places ID
  3. Combine them with a hyphen: `{name}-{id}`
  4. Prepend with base URL: `https://noogabites.com/listing/{name}-{id}`

### Example Code
```typescript
const generateListingUrl = (name: string, placeId: string) => {
  const slug = name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
  const idSuffix = placeId.slice(-6);
  return `https://noogabites.com/listing/${slug}-${idSuffix}`;
};
```
