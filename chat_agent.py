from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import openai
import pandas as pd
import re
import json

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

app.secret_key = "some_very_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Path to CSV
CSV_FILE_PATH = r"C:\Users\shiva\Downloads\Crew Agent (Responses) - Form Responses 1 (1).csv"

def load_crew_schedules(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    column_map = {
        "preferred wakeup time": "wakeup",
        "preferred breakfast time": "breakfast",
        "preferred lunch time": "lunch",
        "preferred dinner time": "dinner",
        "preferred exercise time": "exercise",
        "use of lunar rock kit": "lunar_rock",
        "use of navigation system": "navigation",
        "use mobility gear": "mobility"
    }

    schedules = {}
    for _, row in df.iterrows():
        crew_name = str(row["crew name"]).strip()
        if crew_name not in schedules:
            schedules[crew_name] = {}
        for csv_col, short_key in column_map.items():
            if csv_col in row and pd.notnull(row[csv_col]):
                schedules[crew_name][short_key] = str(row[csv_col]).strip()

    return schedules

CREW_SCHEDULES = load_crew_schedules(CSV_FILE_PATH)
SCHEDULE_JSON = json.dumps(CREW_SCHEDULES, indent=2)

INITIAL_SYSTEM_PROMPT = f"""\
You are an advanced scheduling assistant for astronauts. 
You have access to the entire crew schedule data in JSON format.

When a user asks about scheduling or conflicts, you must:
1. Identify the user's crew name, the activity, and the requested time.
2. Analyze the JSON data to see if that activity/time conflicts with any other crew member's schedule.
3. If there is a conflict, propose at least two alternative time slots.
4. Respond in a friendly, concise tone, without revealing your internal reasoning or the raw JSON.

Crew schedule data (for reference):
{SCHEDULE_JSON}
"""


MAX_TOKENS = 7500

def trim_conversation(conversation):
    """
    Keeps conversation length below MAX_TOKENS by removing older messages.
    """
    while len(json.dumps(conversation)) > MAX_TOKENS:
        conversation.pop(1)
    return conversation
def parse_user_intent(user_message):
    """
    Extract crew name, activity, and time from the user message.
    E.g.: "Hi, I'm Crew William. I'd like to schedule exercise at 4:00 PM."
    """
    crew_name_match = re.search(r"(?:I am|I'm) crew\s+(\w+)", user_message, re.IGNORECASE)
    crew_name = crew_name_match.group(1).strip() if crew_name_match else None

    possible_activities = [
        "exercise", "lunch", "dinner", "breakfast",
        "wakeup", "lunar_rock", "navigation", "mobility"
    ]
    found_activity = None
    for act in possible_activities:
        if act in user_message.lower():
            found_activity = act
            break

    time_match = re.search(r"(\d{1,2}:\d{2}\s?(?:am|pm))", user_message, re.IGNORECASE)
    requested_time = time_match.group(1).upper() if time_match else None

    return crew_name, found_activity, requested_time

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")


    if "conversation" not in session:
        session["conversation"] = []

    conversation = session["conversation"]

    conversation = trim_conversation(conversation)


    if not conversation:
        conversation.append({"role": "system", "content": INITIAL_SYSTEM_PROMPT})


    crew_name, found_activity, requested_time = parse_user_intent(user_message)


    if crew_name:
        session["crew_name"] = crew_name.lower()


    dynamic_system_prompt = f"""
    Analyze the schedule JSON below, then handle the user's query.
    JSON Data:
    {SCHEDULE_JSON}

    The user might be crew: {crew_name or 'Unknown'}.
    The user might want to do activity: {found_activity or 'Unknown'}.
    The user might want the time: {requested_time or 'Unknown'}.

    Remember to:
    1) Check if any other crew member has the same activity at that time.
    2) If conflict, propose alternative slots.
    3) Reply in a friendly tone, not revealing JSON or chain-of-thought.
    """


    conversation.append({"role": "system", "content": dynamic_system_prompt})
    conversation.append({"role": "user", "content": user_message})


    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation
        )
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

    assistant_reply = response.choices[0].message.content.strip()


    conversation.append({"role": "assistant", "content": assistant_reply})
    session["conversation"] = conversation


    return jsonify({"reply": assistant_reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
