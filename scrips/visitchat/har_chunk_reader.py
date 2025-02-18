import json

def read_file_in_chunks(file_path, chunk_size=1024*1024):  # 1MB chunks
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def extract_json_objects(text):
    objects = []
    start = 0
    while True:
        try:
            # Find start of a potential restaurant object
            start = text.find('"title":', start)
            if start == -1:
                break
                
            # Find the next comma or closing brace
            end = text.find(',', start)
            if end == -1:
                end = text.find('}', start)
            if end == -1:
                break
                
            # Extract the title
            title_text = text[start:end]
            if '"title":' in title_text and title_text.count('"') >= 4:
                # Extract the actual title value
                title = title_text.split(':', 1)[1].strip().strip('"')
                objects.append(title)
                
            start = end + 1
            
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return objects

har_file = '/opt/noogabites/www.visitchattanooga.com.har'

# Read the HAR file
with open(har_file, 'r') as f:
    content = f.read()

# Extract all restaurant titles
restaurants = extract_json_objects(content)

print(f"\nFound {len(restaurants)} restaurant titles:")
for restaurant in sorted(set(restaurants)):  # Using set to remove duplicates
    print(f"- {restaurant}")
