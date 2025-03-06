Crew Agent: AI-Powered Astronaut Scheduling Assistant 🚀
Version: 1.0  
Author: Shivam Shukla  

Overview 
Crew Agent is an intelligent scheduling assistant designed to enhance astronaut autonomy in long-duration space missions. It assists astronauts in self-scheduling tasks, resolving conflicts, and optimizing daily routines based on crew preferences and mission constraints.

The agent processes crew schedule data from a CSV file, and helps users find the best time slots for their activities while minimizing conflicts.

---

Features
✅ Analyzes and processes astronaut scheduling preferences
✅ Detects conflicts in scheduling (e.g., overlapping exercise times, shared equipment usage)
✅ Suggests alternative time slots to avoid scheduling clashes 
✅ Maintains a friendly, natural, and conversational tone 
✅ Remembers user identity for multi-turn conversations  
✅ Handles real-time adjustments based on changing preferences


Required Python Packages: 
- `Flask` (for backend API)
- `Flask-Session` (for managing user sessions)
- `openai` (for AI-powered responses)
- `pandas` (for processing CSV data)
- `json` (for formatting structured crew schedules)
- `re` (for extracting scheduling details from messages)

The app will be available at: http://127.0.0.1:5000

---

How It Works
1️⃣ Data Processing: Loading the Crew Schedule 
Crew members fill out a **Google Form**, and their responses are saved as a CSV file. The agent reads this data, formats it into structured JSON, and uses it for conflict detection.

📁 Sample CSV File Format:  
| Crew Name | Preferred Wakeup Time | Preferred Exercise Time | Use of Lunar Rock Kit |  
|-----------|----------------------|----------------------|----------------------|  
| William   | 7:00 AM              | 4:00 PM              | 5:00 PM              |  
| Darian    | 6:30 AM              | 4:00 PM              | 6:00 PM              |  

2️⃣ AI-Powered Conflict Resolution & Suggestions  
The agent processes each query by:  
✔️ Identifying the Crew Member (e.g., “I am Crew William”)  
✔️ Extracting the Activity & Time (e.g., “I have exercise at 4:00 PM”)  
✔️ Checking for Scheduling Conflicts (e.g., "Darian also has exercise at 4:00 PM")  
✔️ Providing Conflict-Free Suggestions (e.g., “Would 5:30 PM work for you?”)  

3️⃣ Multi-turn Conversation Memory
The agent remembers the crew member's identity throughout the conversation so they don’t have to keep reintroducing themselves.


Troubleshooting & FAQs

🔴 Issue: Error: Maximum context length exceeded (8192 tokens). 
✅ Solution: The conversation length is too long. The app now trims old messages using MAX_TOKENS = 7500.

🔴 Issue: Agent doesn’t remember user identity between messages. 
✅ Solution:The Flask-Session module ensures continuity. Ensure `"SESSION_TYPE": "filesystem"` is correctly set.

🔴 Issue: Agent provides incorrect or incomplete responses.  
✅ Solution: Ensure the CSV data is correctly formatted and matches column mappings in `column_map`.

🔴 Issue: Flask server doesn’t start. 
✅ Solution: Run `python -m flask run` instead.

This project is created as a futurework of my Capstone Project sponsored by the NASA Ames Research center
Special thanks to NASA’s Human-Computer Interaction Group for inspiring this project. 🙌  
Special thanks to Chatgpt! For helping me out in fixing and writing code. 
For any questions, feature requests, or bug reports, please contact me at sshukla3@ucsc.edu.

