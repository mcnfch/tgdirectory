import json
from collections import defaultdict

def load_json_file(filepath):
    """Load JSON file and return its contents"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_categories_from_live(data):
    """Extract categories from live data file"""
    categories = defaultdict(int)
    
    for restaurant in data['restaurants'].values():
        if 'basic_info' in restaurant and 'types' in restaurant['basic_info']:
            for category in restaurant['basic_info']['types']:
                # Convert to human readable format
                human_readable = category.replace('_', ' ').title()
                categories[human_readable] += 1
    
    return categories

def extract_categories_from_extended(data):
    """Extract categories from extended data file"""
    categories = defaultdict(int)
    
    for restaurant in data['restaurants'].values():
        if 'types' in restaurant:
            for category in restaurant['types']:
                # Convert to human readable format
                human_readable = category.replace('_', ' ').title()
                categories[human_readable] += 1
    
    return categories

def merge_categories(live_cats, extended_cats):
    """Merge categories from both sources and sum their counts"""
    merged = defaultdict(int)
    
    # Add counts from both sources
    for cat, count in live_cats.items():
        merged[cat] += count
    
    for cat, count in extended_cats.items():
        merged[cat] += count
    
    # Convert to sorted list of dicts
    categories_list = [
        {"name": cat, "count": count}
        for cat, count in merged.items()
    ]
    
    # Sort by count (descending) and then name
    categories_list.sort(key=lambda x: (-x["count"], x["name"]))
    
    return categories_list

def main():
    # Load both data files
    live_data = load_json_file('src/data/static/live_data.json')
    extended_data = load_json_file('src/data/static/extended_live.json')
    
    # Extract categories from both sources
    live_categories = extract_categories_from_live(live_data)
    extended_categories = extract_categories_from_extended(extended_data)
    
    # Merge and sort categories
    merged_categories = merge_categories(live_categories, extended_categories)
    
    # Create output structure
    output = {
        "metadata": {
            "total_categories": len(merged_categories),
            "source_files": [
                "live_data.json",
                "extended_live.json"
            ]
        },
        "categories": merged_categories
    }
    
    # Save to file
    with open('src/data/static/categories.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Found {len(merged_categories)} unique categories")
    print("Top 10 categories:")
    for cat in merged_categories[:10]:
        print(f"- {cat['name']}: {cat['count']} restaurants")

if __name__ == "__main__":
    main()
