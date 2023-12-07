import csv
import openai  # Import OpenAI Python client
from mock_openai import mock_openai_completion_create
from evaluation import evaluate_personality_prompt
import matplotlib.pyplot as plt
import pandas as pd
import difflib

# Function to compare responses using difflib
def compare_responses(reference_prompt, examinee_prompt):
    # Calculate the similarity ratio between the two prompts
    similarity_ratio = difflib.SequenceMatcher(None, reference_prompt, examinee_prompt).ratio()

    return similarity_ratio


def generate_scores_csv():
    # Initialize/Open the CSV file for writing scores
    with open('scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Personality Type', 'Evaluation Score'])

        scores = []  # Store scores for later plotting

        # Loop through different personality types
        for personality_type in ['Openness', 'Meticulousness', 'Extroversion', 'Agreeableness', 'Sensitivity']:
            # Example reference prompt (replace with your actual reference prompts)
            reference_prompt = f"Reference prompt for {personality_type}"

            try:
                # Attempt to make an actual API call (replace with your OpenAI API key)
                openai.api_key = 'sk-1O8EUfLLhtsk-1O8EUfLLht20MkNtgPlET3BlbkFJxlJIwDF7PELidWIZhSnn20MkNtgPlET3BlbkFJxlJIwDF7PELidWIZhSnn'
                completion_text, examinee_prompt = openai.Completion.create(
                    engine="text-davinci-002",  # Replace with your engine choice
                    prompt=reference_prompt,
                    max_tokens=100
                )

                # Extract relevant information from the API response
                examinee_prompt = f'Mock examinee prompt for prompt: "{examinee_prompt}"'
                
            except Exception as e:
                print(f"No API call/connection. Using mock data. Error: {e}")

                # Use mock data in case of no API call or connection
                completion_text, examinee_prompt = mock_openai_completion_create(reference_prompt, max_tokens=100)

            # Evaluate examinee's response and compare it with the reference
            similarity_score = compare_responses(reference_prompt, examinee_prompt)

            # Example: Write the scores to the CSV file
            writer.writerow([personality_type, similarity_score])

            # Save scores for later plotting
            scores.append({'Personality': personality_type, 'Score': similarity_score})

        # Generate a bar graph based on the scores
        df = pd.DataFrame(scores)
        plt.figure(figsize=(8, 6))
        plt.bar(df["Personality"], df["Score"], color='skyblue')
        plt.title("Personality Scores")
        plt.xlabel("Personality Traits")
        plt.ylabel("Scores")
        plt.savefig("scores_plot.png")  # Save the plot as an image file
        plt.show()



# Main function
def main():
    generate_scores_csv()

if __name__ == "__main__":
    main()
