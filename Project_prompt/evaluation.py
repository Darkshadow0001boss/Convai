# evaluation.py

from mock_openai import mock_openai_completion_create

def evaluate_personality_prompt(examinee_code):
    try:
        # Example prompt for testing
        user_query = "What would you do if you find a lost item in a public place?"

        # Call the mock OpenAI API for testing (replace with actual OpenAI API integration)
        print("Before API call")
        completion_text, examinee_prompt = mock_openai_completion_create(user_query, max_tokens=100)
        print("After API call")

        # Rest of your evaluation logic
        # You can analyze the examinee's response and compare it with the reference

        return completion_text, examinee_prompt

    except Exception as e:
        print(f"Error: {e}")

# Example usage for testing
if __name__ == "__main__":
    evaluate_personality_prompt(None)  # Pass examinee_code as needed
