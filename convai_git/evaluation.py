import csv
import re
import dataset
import openai

PROMPT_TEMPLATE = """The following is a backstory of {character_name}, which may be in first, second or third person :
*Start Backstory*
{backstory}
*end backstory

You, {character_name}, can also perform certain actions like {action_list}

You have certain objects in your surrounding. Take note of the objects known to you, {character_name}, with their description: {object_list}

You, {character_name}, are speaking directly to User. Always use first person, do not refer to yourself in third person nor as an AI, and avoid suggesting you have capabilities, origins, or characteristics outside of those belonging to {character_name}. You are {character_name}, and not an AI nor a text-based AI.

"""

OPENAI_API_KEY = "Your_api_key"

# .........................OLD SCORING_PROPMPT................................
# SCORING_PROMPT = """You will rate the personality traits of a character given the character interaction with the user. The personality traits are openness, meticulousness, extroversion, agreeableness and sensitivity. You will judge the character response and give a rating ranging from 0 to 4. Below is the detailed semantics of the ratings

# The range is as follows
# for Openness, [0 means, Dislikes changes, 4 means, Likes Exploring]
# for Meticulousness, [0 means , Let things happen, 4 means, More attention to details]
# for Extroversion, [0 means, Introvert, 4 means, Extrovert]
# for Agreeableness, [0 means, not agreeable, 4 means, Agreeable]

# You will return a JSON of the the ratings with the traits as keys and ratings as values. The ratings will range from 0 to 4. Sample json output is {{"openness":0, "meticulousness":2, "extroversion": 3, "agreeableness": 4, "sensitivity": 4}}

# The character has backstory: 
# *Start backstory*
# {backstory}
# *End backstory*

# The character, {character_name}, can also perform following actions: {action_list}.

# The character have certain objects in your surrounding: {object_list}

# User query: {user_query}

# Judge the character response, and give 0 to 4 rating to the five personality traits, openness, meticulousness, extroversion, agreeableness and sensitivity. Output should be in a JSON format.
# E.g. output 
# {{"openness":0, "meticulousness":2, "extroversion": 3, "agreeableness": 4, "sensitivity": 4}}

# Only return the JSON with no explanation.
# """

# ......................NEW SCORING PROMPT.................................................................................
SCORING_PROMPT = """
You will rate the personality traits of a character given the character interaction with the user. The personality traits are openness, meticulousness, extroversion, agreeableness, and sensitivity. You will judge the character's response and give a rating ranging from 0 to 4. Below is the detailed semantics of the ratings:

The range is as follows:
- Openness: [0 means, Dislikes changes, 4 means, Likes Exploring]
- Meticulousness: [0 means, Let things happen, 4 means, More attention to details]
- Extroversion: [0 means, Introvert, 4 means, Extrovert]
- Agreeableness: [0 means, not agreeable, 4 means, Agreeable]
- Sensitivity: [0 means, Rarely Emotional, 4 means, Highly Emotional]

You will return a JSON of the ratings with the traits as keys and ratings as values. The ratings will range from 0 to 4. Sample JSON output is {{"openness": 0, "meticulousness": 2, "extroversion": 3, "agreeableness": 4, "sensitivity": 4}}

The character has a backstory:
*Start backstory*
{backstory}
*End backstory*

The character, {character_name}, can also perform the following actions: {action_list}.

The character has certain objects in their surroundings: {object_list}

User query: {user_query}

Now, when evaluating the character's response, consider their personality traits, backstory, and the specific user query. Provide ratings that accurately reflect how well the character embodies each trait based on their actions and responses.

Judge the character response, and give a rating of 0 to 4 to the five personality traits: openness, meticulousness, extroversion, agreeableness, and sensitivity. Output should be in a JSON format.
E.g., output: {{"openness": 0, "meticulousness": 2, "extroversion": 3, "agreeableness": 4, "sensitivity": 4}}

Only return the JSON with no explanation.
"""



# ................................... AFTER TASK 1....................................................................
# def get_big5_personality_prompt(personality: dict):
#     """
#     Implement this method.

#     Args:
#         - Dictionary containing the level for each of the Big5 personality.
#         Example:
#         {
#             "openness": 2,
#             "meticulousness": 4,
#             "extroversion": 2,
#             "agreeableness": 0,
#             "sensitivity": 2
#         }
#     Output:
#         - string: Prompt for Big5 personality.
#     """

#     # Map personality traits to corresponding descriptions
#     openness_desc = ["Dislikes changes", "", "", "", "Likes Exploring"]
#     meticulousness_desc = ["Let things happen", "", "", "", "More attention to details"]
#     extroversion_desc = ["Introvert", "", "", "", "Extrovert"]
#     agreeableness_desc = ["Competitive", "", "", "", "Agreeable"]
#     sensitivity_desc = ["Rarely Emotional", "", "", "", "Highly Emotional"]

#     # Construct the prompt for each personality trait
#     prompt = f"Openness: [{personality['openness']} => {openness_desc[personality['openness']]}]\n"
#     prompt += f"Meticulousness: [{personality['meticulousness']} => {meticulousness_desc[personality['meticulousness']]}]\n"
#     prompt += f"Extroversion: [{personality['extroversion']} => {extroversion_desc[personality['extroversion']]}]\n"
#     prompt += f"Agreeableness: [{personality['agreeableness']} => {agreeableness_desc[personality['agreeableness']]}]\n"
#     prompt += f"Sensitivity: [{personality['sensitivity']} => {sensitivity_desc[personality['sensitivity']]}]\n"

#     return prompt

# ................................................AFTER TASK 2...................................................................................
current_entry_index = 0

def get_big5_personality_prompt(personality: dict):
    """
    Implement this method.

    Args:
        - Dictionary containing the level for each of the Big5 personality.
          Example:
          {
              "openness": 2,
              "meticulousness": 4,
              "extroversion": 2,
              "agreeableness": 0,
              "sensitivity": 2
          }
    Output:
        - string: Prompt for Big5 personality.
    """
    global current_entry_index  # Access the global variable

    current_entry = dataset.test_data_set[current_entry_index]
    current_entry_index += 1  # Increment the index for the next iteration

    # Map personality traits to corresponding descriptions
    openness_desc = ["Dislikes changes", "", "", "", "Likes Exploring"]
    meticulousness_desc = ["Let things happen", "", "", "", "More attention to details"]
    extroversion_desc = ["Introvert", "", "", "", "Extrovert"]
    agreeableness_desc = ["Competitive", "", "", "", "Agreeable"]
    sensitivity_desc = ["Rarely Emotional", "", "", "", "Highly Emotional"]

    # Construct an improved and context-rich prompt for each personality trait
    prompt = f"{current_entry['character_name']} is known for their personality traits. Let's explore them:\n\n"
    prompt += f"1. **Openness**: {openness_desc[personality['openness']]}\n"
    prompt += f"2. **Meticulousness**: {meticulousness_desc[personality['meticulousness']]}\n"
    prompt += f"3. **Extroversion**: {extroversion_desc[personality['extroversion']]}\n"
    prompt += f"4. **Agreeableness**: {agreeableness_desc[personality['agreeableness']]}\n"
    prompt += f"5. **Sensitivity**: {sensitivity_desc[personality['sensitivity']]}\n\n"

    prompt += f"Now, imagine {current_entry['character_name']} finds themselves in a situation where they can {', '.join(current_entry['action_list'])}. "
    prompt += f"Surrounded by objects like {', '.join(current_entry['object_list'])}, {current_entry['character_name']} is ready to engage with the user. "
    prompt += "You can ask anything, and {current_entry['character_name']} will respond based on their unique personality. "
    prompt += "How do you think {current_entry['character_name']} would react in different scenarios?"

    return prompt


# .............................................AFTER TASK 3..............................................................................





def get_gpt35_response(messages: list):
    openai.api_key = OPENAI_API_KEY 
    responses = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["User:"],
        stream=True
    )

    resp_text = ""
    for response in responses:
        choice_content = response.choices[0].delta.get('content') if response.choices else None
        if not choice_content:
                continue
        resp_text += choice_content

    return resp_text


def get_test_prompt(data: dict, user_query: str, chat_history: list = []):
    messages = []
    system_prompt = PROMPT_TEMPLATE.format(
        character_name=data['character_name'], backstory=data['backstory'],
        action_list=data['action_list'], object_list=data['object_list'])
    messages.append({"role": "system", "content": system_prompt})

    big5_personality_prompt = get_big5_personality_prompt(data['personality_traits'])
    messages.append({"role": "system", "content": big5_personality_prompt})

    for chat in chat_history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["assistant"]})

    messages.append({"role": "user", "content": user_query})
    return messages 


def score_prompt(data: dict, user_query: str, gpt_response: str):
    system_prompt = SCORING_PROMPT.format(
        character_name=data['character_name'], backstory=data['backstory'],
        action_list=data['action_list'], object_list=data['object_list'],
        user_query=user_query)
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": gpt_response})

    openai.api_key = OPENAI_API_KEY 
    responses = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["User:"],
        stream=True
    )

    resp_text = ""
    for response in responses:
        choice_content = response.choices[0].delta.get('content') if response.choices else None
        if not choice_content:
                continue
        resp_text += choice_content

    # Parse json
    pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
    
    # Find the first match
    match = re.search(pattern, resp_text, re.DOTALL)

    # Load the JSON object and extract the ratings for each criterion
    json_str = match.group()
    return json_str.replace("'", '"')


def run_evaluation():
    score_filename = "scores.csv"

    # Writing to the csv file
    with open(score_filename, 'w', newline='') as score_file:
        fwriter = csv.writer(score_file)

        for entry in dataset.test_data_set:
            chat_history = []
            total_score = {
                 "openness": 0,
                 "meticulousness": 0,
                 "extroversion": 0,
                 "agreeableness": 0,
                 "sensitivity": 0
            }
            num_chats = 0
            for uquery in entry["user_query"]:
                prompt_to_evaluate = get_test_prompt(entry, uquery, chat_history)
                gpt_response = get_gpt35_response(prompt_to_evaluate)
                chat_history.append({"user": uquery, "assistant": gpt_response})

                new_score = eval(score_prompt(entry, uquery, gpt_response))
                for k,v in new_score.items():
                     total_score[k] += (abs(v - entry["personality_traits"][k]) / 4)
                num_chats += 1

            avg_score = {}
            for k,v in total_score.items():
                avg_score[k] = round(v / num_chats, 2)
            fwriter.writerow([entry["id"], avg_score["openness"],avg_score["meticulousness"],avg_score["extroversion"],avg_score["agreeableness"],avg_score["sensitivity"]])


if __name__ == "__main__":
    run_evaluation()




    
