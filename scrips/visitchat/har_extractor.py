import json
import sys

def extract_restaurants(har_file):
    with open(har_file, 'r') as f:
        data = json.load(f)
    
    # Find entries with restaurant data
    restaurant_entries = []
    for entry in data['log']['entries']:
        try:
            response_text = entry['response']['content'].get('text', '')
            if '"docs":' in response_text and '"title":' in response_text:
                response_content = json.loads(response_text)
                if 'docs' in response_content and isinstance(response_content['docs'], list):
                    for doc in response_content['docs']:
                        if isinstance(doc, dict) and 'title' in doc:
                            restaurant_entries.append(doc)
        except Exception as e:
            continue
    
    # Sort restaurants by quality score
    restaurant_entries.sort(key=lambda x: float(x.get('qualityScore', 0)), reverse=True)
    
    # Print all restaurant names for debugging
    print("\nAll restaurant names:")
    for r in restaurant_entries:
        print(f"- {r.get('title', '')}")
    
    # Format restaurant data
    formatted_restaurants = []
    for r in restaurant_entries:
        formatted = {
            'name': r.get('title', ''),
            'url': f"https://www.visitchattanooga.com{r.get('url', '')}",
            'quality_score': r.get('qualityScore'),
            'website': r.get('weburl'),
            'address': r.get('address1'),
            'latitude': r.get('latitude'),
            'longitude': r.get('longitude'),
            'category': r.get('primary_category', {}).get('subcatname'),
            'yelp_rating': r.get('yelp', {}).get('rating') if 'yelp' in r else None,
            'yelp_reviews': r.get('yelp', {}).get('review_count') if 'yelp' in r else None,
            'yelp_price': r.get('yelp', {}).get('price') if 'yelp' in r else None
        }
        formatted_restaurants.append(formatted)
    
    # Save to file
    output_file = '/opt/noogabites/Results/visitchat/all_restaurants.json'
    with open(output_file, 'w') as f:
        json.dump(formatted_restaurants, f, indent=2)
    
    print(f"\nFound {len(formatted_restaurants)} restaurants:")
    for r in formatted_restaurants:
        print(f"- {r['name']} (Quality Score: {r['quality_score']})")
    print(f"\nSaved to {output_file}")

if __name__ == '__main__':
    har_file = '/opt/noogabites/www.visitchattanooga.com.har'
    
    extract_restaurants(har_file)
