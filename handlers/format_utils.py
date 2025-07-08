def format_restaurants(restaurants):
    formatted_restaurants = []
    for r in restaurants:
        if isinstance(r, dict):
            s = f'<span class="restaurant-name">{r.get("name", "Unknown")}</span> ({r.get("type", "Unknown")})'
            if r.get("outdoor"):
                s += ' <span class="outdoor-badge">Outdoor</span>'
        else:
            s = str(r)
        formatted_restaurants.append(s)
    return formatted_restaurants 