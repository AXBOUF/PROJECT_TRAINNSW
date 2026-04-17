import json 

# we will print the schema of a JSON file, which is a dictionary of key-value pairs
with open('sydneytrains.json') as f:
    data = json.load(f)

# we will print the keys of the dictionary, which are the names of the fields in the JSON file


print("TYPE:", type(data))

if isinstance(data, dict):
    print("\nTOP KEYS:", len(data))
    print(list(data.keys())[:20])

elif isinstance(data, list):
    print("\nLENGTH:", len(data))

    print("\nFIRST ITEM TYPE:", type(data[0]))

    if isinstance(data[0], dict):
        print("\nFIRST ITEM KEYS:")
        print(list(data[0].keys()))
    