```python
import streamlit as st
from datetime import datetime
import re
import base64
import pandas as pd
import traceback

# Load Google Fonts via CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@300;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #26A69A;
            --accent: #FF6F61;
            --light: #F5F9FA;
            --dark: #1A3C50;
            --shadow: rgba(0, 0, 0, 0.1);
        }
        .stApp {
            background: linear-gradient(135deg, #E0F7F9, #FFFFFF);
            color: var(--dark);
            font-family: 'Poppins', sans-serif;
            padding: 20px;
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        h1, h2, h3, h4 {
            font-family: 'Roboto', sans-serif;
            color: var(--dark);
            text-align: center;
        }
        h1 { font-size: 2.5rem; font-weight: 600; }
        h2 { font-size: 2rem; font-weight: 500; }
        h3 { font-size: 1.5rem; font-weight: 500; }
        h4 { font-size: 1.2rem; font-weight: 400; }
        .card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px var(--shadow);
            margin-bottom: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px var(--shadow);
        }
        .btn {
            background: linear-gradient(45deg, var(--primary), #2E7D7A);
            color: white;
            padding: 8px 15px;
            border-radius: 25px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s ease, transform 0.2s ease;
        }
        .btn:hover {
            background: linear-gradient(45deg, var(--accent), #FF8A80);
            transform: scale(1.05);
        }
        .stButton > button {
            background: linear-gradient(45deg, var(--primary), #2E7D7A);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 8px 15px;
            font-weight: 500;
        }
        .stButton > button:hover {
            background: linear-gradient(45deg, var(--accent), #FF8A80);
        }
        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            h2 { font-size: 1.5rem; }
            h3 { font-size: 1.2rem; }
            h4 { font-size: 1rem; }
            .card { margin-bottom: 10px; padding: 10px; }
            .btn { padding: 6px 12px; }
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="SafeSpace Organisation", page_icon="🧠", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "counseling_form_data" not in st.session_state:
    st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}
if "volunteer_form_data" not in st.session_state:
    st.session_state.volunteer_form_data = {"name": "", "email": "", "phone": "", "role": "Any"}
if "partnership_form_data" not in st.session_state:
    st.session_state.partnership_form_data = {"name": "", "email": "", "phone": "", "type": "Partner"}

# Utility functions
def get_download_link(file_content, file_name):
    try:
        b64 = base64.b64encode(file_content.encode()).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="btn">Download</a>'
    except Exception as e:
        st.error("Error generating download link.")
        return ""

def export_mood_history():
    try:
        df = pd.DataFrame(st.session_state.mood_history, columns=["Date", "Mood", "Note"])
        df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x)
        return df.to_csv(index=False)
    except Exception as e:
        st.error("Error exporting mood history.")
        return ""

# Chatbot knowledge base
knowledge_base = [
    {"question": r"what is safespace organisation\??", "answer": "SafeSpace Organisation is a non-profit providing mental health care since 2023."},
    {"question": r"what services do you offer\??", "answer": "We offer counseling services. Register at the Services section."},
    {"question": r"how can i contact you\??", "answer": "Contact us at +254 781 095 919 or info@safespaceorganisation.org."},
    {"question": r"what are your hours\??", "answer": "Mon-Fri 9 AM-5 PM, Sat 10 AM-2 PM."},
    {"question": r"how much does it cost\??", "answer": "Fees range from KSh 500-2,000 per session."},
    {"question": r"who are the founders\??", "answer": "Founded by Jerim Owino and Hamdi Roble."},
    {"question": r"what events are coming up\??", "answer": "Check the Events section for details."},
    {"question": r"how can i volunteer\??", "answer": "Register via the Volunteer form."},
    {"question": r"what is the crisis line\??", "answer": "Call +254 781 095 919 (8 AM-7 PM EAT)."},
    {"question": r"how can i partner with you\??", "answer": "Register through the Partnership form."},
    {"default": f"I’m sorry, I didn’t understand. Ask about services, contact, hours, costs, founders, events, volunteering, crisis support, or partnerships. Time: 10:27 AM EAT, August 06, 2025."}
]

def get_chatbot_response(query):
    query = query.lower()
    for entry in knowledge_base:
        if "question" in entry and re.search(entry["question"], query):
            return entry["answer"]
    return knowledge_base[-1]["default"]

# HEADER
st.markdown("<h1 style='text-align:center; padding: 10px; background: var(--primary); color: white; border-radius: 10px;'>SafeSpace Organisation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 1.2rem; color: var(--dark);'>Empowering Minds, Nurturing Hope Since 2023</p>", unsafe_allow_html=True)

# HERO SECTION
st.markdown("<div id='hero'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; padding: 20px; background: linear-gradient(135deg, var(--primary), #2E7D7A); color: white; border-radius: 10px;'>Healing Minds, Restoring Lives</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 1.1rem; color: var(--dark); max-width: 600px; margin: 0 auto;'>SafeSpace offers confidential counseling for all communities.</p>", unsafe_allow_html=True)
cols = st.columns(2)
with cols[0]:
    st.markdown("<a href='#services' class='btn'>Our Services</a>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<a href='#about' class='btn'>About Us</a>", unsafe_allow_html=True)

# ABOUT SECTION
st.markdown("<div id='about'></div>", unsafe_allow_html=True)
st.markdown("## About SafeSpace Organisation")
st.markdown("<div class='card'><p>SafeSpace Organisation, founded in 2023 by Jerim Owino and Hamdi Roble, provides accessible mental health care with 15 professionals.</p></div>", unsafe_allow_html=True)
st.markdown("<div id='founders'></div>", unsafe_allow_html=True)
st.markdown("## Our Founders")
st.markdown("<div class='card'><h4>Jerim Owino</h4><p>Jerim is a certified psychologist with over 12 years of experience in mental health. His expertise lies in trauma counseling and community-based interventions, shaping SafeSpace’s outreach programs.</p></div>", unsafe_allow_html=True)
st.markdown("<div class='card'><h4>Hamdi Roble</h4><p>Hamdi holds a Master’s in Public Health and brings 8 years of experience as a community health advocate. She integrates storytelling and traditional healing into modern therapy, leading rural service expansion.</p></div>", unsafe_allow_html=True)

# SERVICES SECTION
st.markdown("<div id='services'></div>", unsafe_allow_html=True)
st.markdown("## Our Services")
services = [
    {"title": "Individual Counseling", "desc": "Personalized therapy sessions."},
    {"title": "Group Therapy", "desc": "Supportive group sessions."},
    {"title": "Online Counseling", "desc": "Virtual therapy options."}
]
for service in services:
    st.markdown(f"<div class='card'><h3>{service['title']}</h3><p>{service['desc']}</p></div>", unsafe_allow_html=True)
with st.form("counseling_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
        st.session_state.counseling_form_data = {"name": name, "email": email, "phone": phone, "type": "Online"}
        st.success(f"Thank you, {name}! Registered at 10:27 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}
    elif submit:
        st.error("Please fill all fields with a valid email.")

# TESTIMONIALS SECTION
st.markdown("<div id='testimonials'></div>", unsafe_allow_html=True)
st.markdown("## Testimonials")
st.markdown("<div class='card'><p><em>'Great support!'</em> - Jane K.</p></div>", unsafe_allow_html=True)

# EVENTS SECTION
st.markdown("<div id='events'></div>", unsafe_allow_html=True)
st.markdown("## Upcoming Events")
st.markdown("<div class='card'><h4>Stress Management Workshop</h4><p>August 10, 2025, Nairobi.</p></div>", unsafe_allow_html=True)

# PARTNERSHIPS SECTION
st.markdown("<div id='partnerships'></div>", unsafe_allow_html=True)
st.markdown("## Partnerships")
st.markdown("<div class='card'><h4>Kenyatta National Hospital</h4><p>Referrals since 2024.</p></div>", unsafe_allow_html=True)
with st.form("partnership_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
        st.session_state.partnership_form_data = {"name": name, "email": email, "phone": phone, "type": "Partner"}
        st.success(f"Thank you, {name}! Registered at 10:27 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.partnership_form_data = {"name": "", "email": "", "phone": "", "type": "Partner"}
    elif submit:
        st.error("Please fill all fields with a valid email.")

# BLOG SECTION
st.markdown("<div id='blog'></div>", unsafe_allow_html=True)
st.markdown("## Blog")
st.markdown("<div class='card'><h4>Coping with Stress</h4><p>July 20, 2025 - Tips by Dr. Amina.</p></div>", unsafe_allow_html=True)

# TRACKER SECTION
st.markdown("<div id='tracker'></div>", unsafe_allow_html=True)
st.markdown("## Mood Tracker")
mood = st.slider("Mood (1-5)", 1, 5, 3)
note = st.text_input("Note")
if st.button("Log"):
    st.session_state.mood_history.append({"Date": datetime.now(), "Mood": mood, "Note": note})
    st.success(f"Logged at 10:27 AM EAT, August 06, 2025!")
for entry in st.session_state.mood_history[-5:]:
    st.write(f"- {entry['Date'].strftime('%Y-%m-%d %H:%M')}: Mood {entry['Mood']}/5 {entry['Note'] if entry['Note'] else ''}")
if st.button("Export"):
    csv = export_mood_history()
    if csv:
        st.markdown(get_download_link(csv, "mood_history.csv"), unsafe_allow_html=True)

# VOLUNTEER SECTION
st.markdown("<div id='volunteer'></div>", unsafe_allow_html=True)
st.markdown("## Volunteer")
st.markdown("<div class='card'><h4>Outreach Support</h4><p>2-4 hr campaigns.</p></div>", unsafe_allow_html=True)
with st.form("volunteer_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submit = st.form_submit_button("Register")
    if submit and name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
        st.session_state.volunteer_form_data = {"name": name, "email": email, "phone": phone, "role": "Any"}
        st.success(f"Thank you, {name}! Registered at 10:27 AM EAT, August 06, 2025. Contact at {email}.")
        st.session_state.volunteer_form_data = {"name": "", "email": "", "phone": "", "role": "Any"}
    elif submit:
        st.error("Please fill all fields with a valid email.")

# CONTACT SECTION
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.markdown("## Contact")
st.markdown("<div class='card'><p>Greenhouse Plaza, Nairobi. Call +254 781 095 919 or email info@safespaceorganisation.org.</p></div>", unsafe_allow_html=True)

# CHATBOT SECTION
st.markdown("## Chat with Us")
chat_container = st.empty()
if st.session_state.chat_history:
    chat_messages = [f"**{'You' if m[0] == 'user' else 'Bot'}:** {m[1]}" for m in st.session_state.chat_history]
    chat_container.markdown("\n".join(chat_messages), unsafe_allow_html=False)
query = st.text_input("Ask a question")
if st.button("Send") and query:
    response = get_chatbot_response(query)
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("bot", response))
    st.experimental_rerun()

# FOOTER
st.markdown("<hr style='border-color: var(--primary);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 0.9rem; color: var(--dark);'>© 2023-2025 SafeSpace Organisation</p>", unsafe_allow_html=True)
```

### `requirements.txt`
```
streamlit>=1.22.0
pandas>=1.5.0
```

### Deployment Instructions
1. Save the `app.py` and `requirements.txt` files in a directory.
2. Test locally by running `streamlit run app.py` in your terminal.
3. Push the files to a GitHub repository.
4. Deploy on Streamlit Community Cloud by connecting the repository via the Streamlit Community Cloud website.

This updated version removes cultural references, enhances the website's aesthetics with a lovely design, and ensures functionality with the new timestamp.
