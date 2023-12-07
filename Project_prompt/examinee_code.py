# examinee_code.py

import openai

def get_big5_personality_prompt(personality_traits, character_name, fictional_city, chat_history, user_query):
    # Define the scale ranges for each personality trait
    openness_scale = ["Dislikes changes", "Likes Exploring"]
    meticulousness_scale = ["Let things happen", "More attention to details"]
    extroversion_scale = ["Introvert", "Extrovert"]
    agreeableness_scale = ["Competitive", "Agreeable"]
    sensitivity_scale = ["Rarely Emotional", "Highly Emotional"]

    # Helper function to get a scaled description based on user rating
    def get_scaled_description(rating, scale):
        index = min(rating, len(scale) - 1)  # Ensure the index is within the scale range
        return scale[index]

    # Generate prompts for each personality trait based on user ratings
    openness_prompt = f"Openness: [{personality_traits['openness']}] - {get_scaled_description(personality_traits['openness'], openness_scale)}"
    meticulousness_prompt = f"Meticulousness: [{personality_traits['meticulousness']}] - {get_scaled_description(personality_traits['meticulousness'], meticulousness_scale)}"
    extroversion_prompt = f"Extroversion: [{personality_traits['extraversion']}] - {get_scaled_description(personality_traits['extraversion'], extroversion_scale)}"
    agreeableness_prompt = f"Agreeableness: [{personality_traits['agreeableness']}] - {get_scaled_description(personality_traits['agreeableness'], agreeableness_scale)}"
    sensitivity_prompt = f"Sensitivity: [{personality_traits['sensitivity']}] - {get_scaled_description(personality_traits['sensitivity'], sensitivity_scale)}"

    # Combine all prompts into a single string
    big5_personality_prompt = f"{openness_prompt}\n{meticulousness_prompt}\n{extroversion_prompt}\n{agreeableness_prompt}\n{sensitivity_prompt}"

    return big5_personality_prompt

# Example usage:
personality_traits = {
    "openness": 0,
    "meticulousness": 2,
    "extraversion": 4,
    "agreeableness": 4,
    "sensitivity": 2
}

# Uncomment the following line to test the function
prompt = get_big5_personality_prompt(personality_traits, "Aria", "Celestial City", "Character: Hello! I am Aria. User: Hi there! Celestial City seems fascinating.", "What is your favorite place in the city?")
print(prompt)
