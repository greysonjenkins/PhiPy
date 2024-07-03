import pandas as pd
import json

# Load the JSON data
with open('../data/philpapers-survey.json', 'r') as file:
    data = json.load(file)

# Create a list to store the cleaned data
cleaned_data = []

# Iterate through each question and its answers
for question, answers in data.items():
    # Check if the answers are nested (like in 'other_minds' and 'philosophical_methods')
    if isinstance(answers, dict) and any(isinstance(v, dict) for v in answers.values()):
        for sub_question, sub_answers in answers.items():
            if isinstance(sub_answers, dict):
                cleaned_data.append({
                    'Question': f"{question} - {sub_question}",
                    'Answers': sub_answers
                })
    else:
        cleaned_data.append({
            'Question': question,
            'Answers': answers
        })

# Create a DataFrame from the cleaned data
df = pd.DataFrame(cleaned_data)

# Function to convert the 'Answers' column to a more readable format
def format_answers(answers):
    return ', '.join([f"{k}: {v}%" for k, v in answers.items()])

# Apply the formatting function to the 'Answers' column
df['Formatted Answers'] = df['Answers'].apply(format_answers)

# Display the result
print(df[['Question', 'Formatted Answers']])
