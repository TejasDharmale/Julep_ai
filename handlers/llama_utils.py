from transformers import pipeline

# Use a small language model that can run on CPU
llama_pipeline = pipeline(
    task="text-generation",
    model="google/flan-t5-small"  # Very lightweight and accurate
)

def get_llama_city_dishes(city):
    prompt = f"List 3 iconic dishes and the country of {city}. Respond as: Country: <name>, Dishes: <comma-separated>"
    try:
        result = llama_pipeline(prompt, max_new_tokens=50)[0]["generated_text"]
        # Basic parse (you can improve this)
        lines = result.split(', Dishes:')
        country = lines[0].replace('Country:', '').strip()
        dishes = [dish.strip() for dish in lines[1].split(',')]
        return country, dishes
    except Exception as e:
        print("❌ LLaMA model error:", e)
        return None, ["Dish 1", "Dish 2", "Dish 3"]
