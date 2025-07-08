import ast

def get_julep_recommendations(city_display, normalized_city, client=None, agent=None):
    prompt = f"Suggest 3 iconic dishes and 3 popular restaurants (with type and outdoor/indoor info if possible) for {city_display or normalized_city}. Respond in JSON: {{'dishes': [...], 'restaurants': [{{'name': ..., 'type': ..., 'outdoor': true/false}}]}}."
    recommendations = {"dishes": [], "restaurants": []}
    try:
        if client is not None and agent is not None:
            session = client.sessions.create(agent=agent.id)
            response = client.sessions.chat(
                session_id=session.id,
                messages=[{"role": "user", "content": prompt}],
                agent=agent.id
            )
            # If response is a tuple, get the second element
            if isinstance(response, tuple) and len(response) == 2:
                response = response[1]
            # If response is a Stream, convert to list and use the first element
            if hasattr(response, '__iter__') and not hasattr(response, 'choices'):
                response = list(response)[0]
            content = None
            choices = getattr(response, 'choices', None)
            if isinstance(choices, list) and choices:
                choice = choices[0]
                delta = getattr(choice, 'delta', None)
                if delta is not None and hasattr(delta, 'content'):
                    content = delta.content
                message = getattr(choice, 'message', None)
                if message is not None and hasattr(message, 'content'):
                    content = message.content
                messages = getattr(choice, 'messages', None)
                if isinstance(messages, list):
                    contents = [m.content for m in messages if hasattr(m, 'content') and m.content]
                    content = ' '.join(str(x) for x in contents if x)
            if isinstance(content, list):
                content = ' '.join(str(x) for x in content if x)
            if isinstance(content, str):
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = content[start:end]
                    julep_data = ast.literal_eval(json_str)
                    if julep_data.get('dishes'):
                        recommendations['dishes'] = julep_data['dishes']
                    if julep_data.get('restaurants'):
                        recommendations['restaurants'] = julep_data['restaurants']
    except Exception as e:
        print("❌ Julep fallback failed:", e)
    return recommendations 