def parse_query(query):
    query = query.lower()
    if "budget" in query:
        # Extract budget and items
        budget = int(query.split("budget")[1].split()[0])
        items = query.split("items")[1].strip().split(",")
        return {'type': 'budget', 'budget': budget, 'items': [x.strip() for x in items]}
    else:
        # Default availability check
        items = query.replace("check", "").replace("available", "").split(",")
        return {'type': 'availability', 'items': [x.strip() for x in items]}
