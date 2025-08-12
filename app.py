import streamlit as st
from datetime import datetime
import re
import base64
import pandas as pd

# Custom CSS for enhanced styling and mobile responsiveness
st.markdown("""
<style>
    :root {
        --primary: #26A69A;
        --accent: #FF6F61;
        --light: #e6f3f5;
        --dark: #2c3e50;
        --deep-blue: #1E3A8A;
    }
    .stApp {
        background-color: var(--light);
        background-image: url('https://www.transparenttextures.com/patterns/subtle-white-feathers.png');
        font-family: 'Inter', sans-serif;
        color: var(--dark);
        min-height: 100vh;
        width: 100%;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif;
        color: var(--deep-blue) !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    h1 { font-size: 2.2rem; }
    h2 { font-size: 1.8rem; }
    h3 { font-size: 1.4rem; }
    h4 { font-size: 1.2rem; }
    .service-card, .testimonial-card, .event-card, .partnership-card, .blog-card, .tracker-card, .volunteer-card, .founder-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .primary-btn {
        background: linear-gradient(135deg, var(--primary), #4DB6AC);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        font-size: 0.9rem;
    }
    .primary-btn:hover {
        background: linear-gradient(135deg, var(--accent), #FF8A80);
        transform: translateY(-2px);
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #4DB6AC);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent), #FF8A80);
    }
    .st-expander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background: #f9f9f9;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        background: #e8f4f8;
        border-top: 1px solid #ddd;
        margin-top: 1rem;
    }
    .cta-banner {
        background: linear-gradient(135deg, var(--primary), #4DB6AC);
        color: white;
        text-align: center;
        padding: 0.8rem;
    }
    .chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 300px;
        max-height: 400px;
        overflow-y: auto;
        z-index: 1000;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        display: none;
    }
    .chatbot-container.active {
        display: block;
    }
    .chatbot-message.user {
        background: #e8f4f8;
        text-align: right;
        color: var(--dark);
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    .chatbot-message.bot {
        background: white;
        text-align: left;
        color: var(--primary);
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid var(--primary);
        font-size: 0.9rem;
    }
    .chatbot-input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    .chatbot-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1001;
        background: linear-gradient(135deg, var(--primary), #4DB6AC);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .chatbot-toggle:hover {
        background: linear-gradient(135deg, var(--accent), #FF8A80);
    }
    html {
        scroll-behavior: smooth;
    }
    @media (max-width: 768px) {
        .stColumn {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .service-card, .testimonial-card, .event-card, .partnership-card, .blog-card, .tracker-card, .volunteer-card, .founder-card {
            margin: 0.3rem 0;
            width: 100% !important;
            padding: 0.5rem;
        }
        h1 { font-size: 1.6rem; }
        h2 { font-size: 1.4rem; }
        h3 { font-size: 1.2rem; }
        h4 { font-size: 1.0rem; }
        .chatbot-container {
            width: 90%;
            right: 5%;
            bottom: 70px;
            max-height: 300px;
        }
        .chatbot-toggle {
            bottom: 20px;
            right: 5%;
            width: 40px;
            height: 40px;
            font-size: 1rem;
        }
        img {
            max-width: 100% !important;
            height: auto !important;
        }
        .cta-banner {
            padding: 0.5rem;
        }
        .st-expander {
            margin: 0.3rem 0;
        }
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="SafeSpace Organisation",
    page_icon="🧠",
    layout="wide",
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "outreach_form_data" not in st.session_state:
    st.session_state.outreach_form_data = {"name": "", "email": "", "phone": "", "experience": "", "skills": [], "role": "Any"}
if "event_form_data" not in st.session_state:
    st.session_state.event_form_data = {"name": "", "email": "", "phone": "", "experience": "", "skills": []}
if "partnership_form_data" not in st.session_state:
    st.session_state.partnership_form_data = {"name": "", "organization": "", "email": "", "phone": "", "type": "Partner"}
if "counseling_form_data" not in st.session_state:
    st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}

# Function to create download link
def get_download_link(file_content, file_name):
    b64 = base64.b64encode(file_content.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="primary-btn" style="display: block; text-align: center; margin-top: 0.5rem;">Download</a>'
    return href

# Function to export mood history
def export_mood_history():
    df = pd.DataFrame(st.session_state.mood_history, columns=["Date", "Mood", "Note"])
    df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x)
    csv = df.to_csv(index=False)
    return csv

# Chatbot knowledge base
knowledge_base = [
    {"question": r"what is safespace organisation\??", "answer": "SafeSpace Organisation, founded in 2023 by Jerim Owino and Hamdi Roble, is a non-profit providing accessible, culturally-appropriate mental health care, addressing trauma, depression, and more with counseling and outreach."},
    {"question": r"what services do you offer\??", "answer": "We offer Individual Counseling, Group Therapy, Family Counseling, Trauma Recovery Therapy, and Online Counseling, using methods like CBT, EMDR, and mindfulness, tailored to diverse mental health needs. Register at the Services section."},
    {"question": r"how can i contact you\??", "answer": "Contact us at +254 781 095 919 (8 AM-7 PM EAT) or info@safespaceorganisation.org (24-hour response). Visit Greenhouse Plaza, Ngong Road, Nairobi."},
    {"question": r"what are your hours\??", "answer": "Office hours are Mon-Fri 9 AM-5 PM, Sat 10 AM-2 PM, closed Sundays and holidays. Crisis line is 8 AM-7 PM EAT."},
    {"question": r"how much does it cost\??", "answer": "Fees range from KSh 500-2,000 per session on a sliding scale, with subsidies and free workshops for low-income clients."},
    {"question": r"who are the founders\??", "answer": "Our founders are Jerim Owino, a certified psychologist from Maasai Mara University, and Hamdi Roble, a cultural therapy expert with a Master’s in Public Health."},
    {"question": r"what events are coming up\??", "answer": "Upcoming events include a Stress Management Workshop on July 30, 2025, in Nairobi, and a Youth Mental Health Forum on August 15, 2025, in Kisumu. Register at events@safespaceorganisation.org."},
    {"question": r"how can i volunteer\??", "answer": "Volunteer roles include Outreach Support, Event Volunteer, and Crisis Line Assistant. Register via the Volunteer form with your details and preferred role."},
    {"question": r"what is the crisis line\??", "answer": "Our Crisis Line is +254 781 095 919 (8 AM-7 PM EAT), with Befrienders Kenya at 1199 available 24/7 for emergencies."},
    {"question": r"how can i partner with you\??", "answer": "You can partner with us by registering through the Partnership form on our Partnerships page, or donate via the Donor form."},
    {"default": "I’m sorry, I didn’t understand. Ask about services, contact, hours, costs, founders, events, volunteering, crisis support, or partnerships, or visit Contact. Time: 12:50 AM EAT, July 25, 2025."}
]

# Function to get chatbot response
def get_chatbot_response(query):
    query = query.lower()
    for entry in knowledge_base:
        if "question" in entry and re.search(entry["question"], query):
            return entry["answer"]
    return knowledge_base[-1]["default"]

# HEADER
st.markdown("""
<div style='text-align: center; padding: 0.8rem; background: var(--primary); color: white;'>
    <h1>SafeSpace Organisation</h1>
    <p>Empowering Minds, Nurturing Hope Since 2023</p>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("<div id='hero'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 0.8rem; background: linear-gradient(rgba(38,166,154,0.9), rgba(77,182,172,0.9)); border-radius: 8px; color: white;'>
    <h1>Healing Minds, Restoring Lives</h1>
    <p style='font-size: 1rem; max-width: 100%; margin: 0.5rem auto;'>SafeSpace Organisation offers professional, confidential counseling in a culturally-sensitive environment for all communities.</p>
    <img src='https://images.unsplash.com/photo-1588195539435-d6b5f19e1c24?auto=format&fit=crop&w=600&q=80' style='width: 100%; max-width: 600px; border-radius: 8px; margin: 0.5rem auto; box-shadow: 0 2px 4px rgba(0,0,0,0.2);' alt='Counseling outreach session'/>
    <div style='display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;'>
        <a href='#about' class='primary-btn'>About Us</a>
        <a href='#services' class='primary-btn'>Our Services</a>
        <a href='#events' class='primary-btn'>Upcoming Events</a>
    </div>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our Mission", expanded=False):
    st.markdown("""
    - **Mission**: Break mental health stigma and provide affordable care.
    - **Vision**: A thriving world with emotional support for all.
    - **Contact**: info@safespaceorganisation.org or +254 781 095 919.
    - **Impact**: 600+ clients in 2025, 90% satisfaction.
    """)

# ABOUT SECTION
st.markdown("<div id='about'></div>", unsafe_allow_html=True)
st.markdown("## About SafeSpace Organisation")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p><strong>SafeSpace Organisation</strong>, founded in 2023 by Jerim Owino and Hamdi Roble, provides accessible mental health care. With 15 professionals, we serve Nairobi, Kisumu, Eldoret, and more, addressing trauma, depression, and family issues via multiple channels.</p>
    <p>We blend traditions with modern therapies, partnering with NGOs and the Ministry of Health to reach 20+ districts, focusing on inclusivity.</p>
    <a href='#services' class='primary-btn'>Explore Our Services</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our History", expanded=False):
    st.markdown("""
    - **Founding**: 2022 Nakuru pilot aided 50, leading to 2023 launch.
    - **Growth**: 2 to 15 staff, aiming for 20 by 2025 end.
    - **Awards**: 2024 Health Federation Award, 2025 Global Grant.
    - **Team**: Specialists in child, trauma, and cultural therapy.
    """)

# FOUNDERS SECTION
st.markdown("<div id='founders'></div>", unsafe_allow_html=True)
st.markdown("## Our Founders")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <div class='founder-card'>
        <h4>Jerim Owino</h4>
        <p>Jerim is a certified psychologist from Maasai Mara University with over 12 years of experience in mental health. Raised in Narok among the Maasai community, he developed a deep understanding of cultural influences on trauma, particularly from his work with pastoralist communities affected by displacement and cattle raids. His expertise lies in trauma counseling and community-based interventions, shaping SafeSpace’s rural outreach programs.</p>
    </div>
    <div class='founder-card'>
        <h4>Hamdi Roble</h4>
        <p>Hamdi holds a Master’s in Public Health from the University of Nairobi and brings 8 years of experience as a community health advocate. Born in Kisumu, she grew up immersed in Luo cultural practices, which inspired her to integrate storytelling and traditional healing into modern therapy. She has worked with women’s groups in rural Kenya, addressing gender-based violence, and leads SafeSpace’s efforts to expand services to underserved regions.</p>
    </div>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our Founders", expanded=False):
    st.markdown("""
    - **Jerim**: Trained 50+ community health workers, co-authored a guide on trauma in pastoral communities.
    - **Hamdi**: Led 15 workshops on gender-based violence, secured funding from local NGOs for rural projects.
    - **Collaboration**: Developed SafeSpace’s culturally-sensitive therapy model after a 2022 pilot.
    - **Community Work**: Both volunteer monthly in low-income areas, offering free sessions.
    """)

# SERVICES SECTION
st.markdown("<div id='services'></div>", unsafe_allow_html=True)
st.markdown("## Our Therapeutic Services")
st.markdown("A comprehensive suite of evidence-based therapies by 15 certified professionals with over 75 years of combined experience, tailored to diverse mental health needs.")
services = [
    {
        "icon": "👤",
        "title": "Individual Counseling",
        "desc": "This service provides personalized, one-on-one therapy sessions targeting conditions such as chronic depression (persistent sadness, loss of interest, fatigue), generalized anxiety disorder (excessive worry, restlessness, sleep disturbances), post-traumatic stress disorder (PTSD) from events like violence or accidents (flashbacks, nightmares, hypervigilance), and low self-esteem (self-doubt, negative self-image). Conducted by therapists with 5+ years of experience, sessions use Cognitive Behavioral Therapy (CBT) to reframe negative thoughts, Dialectical Behavior Therapy (DBT) for emotional regulation, Acceptance and Commitment Therapy (ACT) for value-based living, and mindfulness-based stress reduction (MBSR) for relaxation. Each 50-minute session is available in-person at our Nairobi office, via secure video conferencing, or through mobile outreach units in rural areas. We offer flexible scheduling (evenings, weekends) and a free 15-minute initial consultation to assess needs, match you with a therapist, and provide a personalized treatment plan, including progress reports every 5 sessions."
    },
    {
        "icon": "👥",
        "title": "Group Therapy",
        "desc": "Designed for individuals dealing with grief (prolonged sorrow after loss, guilt, isolation), addiction recovery (alcohol dependency with withdrawal symptoms, substance abuse with cravings), post-traumatic stress disorder (PTSD) from war or natural disasters (avoidance, emotional numbness), and social anxiety (fear of judgment, avoidance of social settings). Facilitated by two counselors with 10+ years of group experience, these 90-minute weekly sessions accommodate up to 10 participants, ensuring personalized support. The program includes role-playing to practice social skills, peer support circles for shared experiences, guided meditations for stress relief, and monthly theme-based discussions (e.g., resilience, coping with loss), adjusted based on participant feedback. Offered in-person and online, with a waiting list and a 3-month commitment encouraged for optimal results."
    },
    {
        "icon": "🏠",
        "title": "Family Counseling",
        "desc": "Aims to improve family dynamics and resolve conflicts for conditions like parenting challenges (discipline issues, communication gaps), marital disputes (infidelity, financial stress, emotional disconnection), intergenerational trauma (inherited stress from historical events), and cultural clashes (differing values, traditions). Led by family therapists trained in systemic therapy (addressing family patterns) and narrative therapy (reframing family stories), these 60-minute sessions incorporate culturally-sensitive practices such as proverbs for wisdom, community elder mediation for resolution, and storytelling to heal relationships. Available in-person at our center, via video calls, or through home visits in select regions, with a focus on long-term family wellness plans, including monthly check-ins and a 6-session initial program."
    },
    {
        "icon": "🧠",
        "title": "Trauma Recovery Therapy",
        "desc": "Targets individuals and families affected by severe trauma, including survivors of physical violence (beatings, assaults causing physical and emotional scars), sexual abuse (long-term shame, trust issues), accidents (car crashes, injuries leading to fear), and natural disasters (floods, earthquakes causing displacement). Using Eye Movement Desensitization and Reprocessing (EMDR) to process traumatic memories, trauma-focused Cognitive Behavioral Therapy (CBT) to manage triggers, and somatic experiencing to release bodily tension, our specialists provide 75-minute sessions in a safe, controlled environment at our Nairobi center or via telehealth. The program includes a 6-session initial phase followed by ongoing support groups, with priority given to refugees, victims of gender-based violence, and those with acute symptoms like panic attacks or dissociation."
    },
    {
        "icon": "💻",
        "title": "Online Counseling",
        "desc": "Offers virtual therapy sessions for individuals facing barriers to in-person care, addressing conditions such as anxiety, depression, and stress (panic attacks, sleep issues, overwhelm). Delivered by licensed therapists via secure video platforms, each 50-minute session utilizes CBT, mindfulness, and teletherapy techniques tailored to remote settings. Available 24/7 with flexible scheduling, this service ensures privacy with end-to-end encryption and includes a free 15-minute consultation to assess needs and assign a therapist. Register below to start your journey."
    }
]
for service in services:
    st.markdown(f"""
    <div class='service-card'>
        <h3>{service['title']}</h3>
        <p>{service['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<div id='counseling-form'></div>", unsafe_allow_html=True)
with st.form("counseling_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email", placeholder="your.email@example.com")
    phone = st.text_input("Phone", placeholder="+254 XXX XXX XXX")
    counseling_type = st.selectbox("Counseling Type", ["Online", "In-Person"])
    submit = st.form_submit_button("Register")
    if submit:
        if not all([name, email, re.match(r"[^@]+@[^@]+\.[^@]+", email), phone]):
            st.error("Fill all required fields.")
        else:
            st.session_state.counseling_form_data = {"name": name, "email": email, "phone": phone, "type": counseling_type}
            st.success(f"Thank you, {name}! Your {counseling_type} counseling registration at 12:50 AM EAT, July 25, 2025, is received. Contact at {email} within 48 hours.")
            st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}
st.markdown("""
<div style='text-align: center; margin-top: 0.5rem;'>
    <a href='#blog' class='primary-btn'>Explore Our Blog</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our Services", expanded=False):
    st.markdown("""
    - **Credentials**: All therapists hold Master’s degrees or higher, certified in multiple modalities (e.g., EMDR, ACT).
    - **Accessibility**: Sliding scale fees (KSh 500-2,000/session), subsidies for low-income clients, and free community workshops monthly.
    - **Feedback**: 95% of clients report improved wellbeing after 6 sessions, with 85% continuing therapy based on 2024 surveys.
    - **Innovation**: Piloting AI-assisted therapy tools for rural access, launching in Q4 2025 with a focus on real-time support.
    """)

# TESTIMONIALS SECTION
st.markdown("<div id='testimonials'></div>", unsafe_allow_html=True)
st.markdown("## What Our Clients Say")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <div class='testimonial-card'><p><em>'Counseling helped me recover from anxiety after my accident!'</em> - Jane K., Nairobi, 2025</p></div>
    <div class='testimonial-card'><p><em>'Group therapy gave me a community during my grief!'</em> - Peter O., Kisumu, 2025</p></div>
    <div class='testimonial-card'><p><em>'Family counseling resolved our conflicts with cultural wisdom!'</em> - Amina H., Eldoret, 2025</p></div>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Testimonials", expanded=False):
    st.markdown("""
    - **Verification**: Collected with consent from verified clients.
    - **Diversity**: Reflects urban, rural, and various age groups.
    - **Impact**: Over 200 testimonials received in 2025, with a yearly report planned.
    """)

# COUNSELING SESSIONS SECTION
st.markdown("<div id='counseling-sessions'></div>", unsafe_allow_html=True)
st.markdown("## Our Counseling Sessions in Action")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
    <div style='margin-bottom: 0.5rem;'>
        <img src='https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=400&q=80' style='width: 100%; max-width: 400px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);' alt='Counselor leading a supportive group therapy session'/>
        <p>A counselor leading a supportive group therapy session in Nairobi.</p>
    </div>
    <div>
        <img src='https://images.unsplash.com/photo-1573496359142-b8d87734a5a4?auto=format&fit=crop&w=400&q=80' style='width: 100%; max-width: 400px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);' alt='One-on-one counseling session in a rural outreach program'/>
        <p>A one-on-one counseling session during a rural outreach program in Kisumu.</p>
    </div>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our Sessions", expanded=False):
    st.markdown("""
    - **Settings**: Conducted in urban centers, rural areas, and via telehealth.
    - **Diversity**: Includes youth, adults, and families from various backgrounds.
    - **Safety**: All sessions adhere to strict confidentiality and cultural sensitivity protocols.
    - **Impact**: Photos reflect our reach to over 600 clients in 2025.
    """)

# MENTAL HEALTH BLOG SECTION
st.markdown("<div id='blog'></div>", unsafe_allow_html=True)
st.markdown("## Mental Health Blog")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p>Articles by experts for wellbeing:</p>
""", unsafe_allow_html=True)
blogs = [
    {"title": "Coping with Economic Stress", "date": "July 20, 2025", "desc": "Strategies including budgeting and relaxation by Dr. Amina Hassan."},
    {"title": "Cultural Therapy in Organisation", "date": "July 15, 2025", "desc": "Integrating storytelling by Hamdi Roble."},
    {"title": "PTSD Survivor Guide", "date": "July 10, 2025", "desc": "Symptoms and recovery by Dr. James Otieno."}
]
for blog in blogs:
    st.markdown(f"""
    <div class='blog-card'>
        <h4>{blog['title']}</h4>
        <p><strong>Date:</strong> {blog['date']}</p>
        <p>{blog['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-top: 0.5rem;'>
    <a href='#crisis' class='primary-btn'>Crisis Support</a>
    <a href='#tracker' class='primary-btn'>Tracker</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Our Blog", expanded=False):
    st.markdown("""
    - **Updates**: Bi-weekly posts, youth series in August 2025.
    - **Panel**: Psychologists, cultural advisors, and a psychiatrist.
    - **Engagement**: Submit questions to blog@safespaceorganisation.org.
    - **Downloads**: Free PDFs under Resources.
    """)

# CRISIS RESOURCES SECTION
st.markdown("<div id='crisis'></div>", unsafe_allow_html=True)
st.markdown("## Crisis Resources")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p>Immediate support:</p>
    <ul>
        <li><strong>Befrienders Kenya:</strong> 1199, 24/7.</li>
        <li><strong>SafeSpace Crisis:</strong> +254 781 095 919, 8 AM-7 PM EAT.</li>
    </ul>
    <p>Emergency: Call 999 or visit a hospital.</p>
    <a href='#contact' class='primary-btn'>Get Help Now</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Crisis Support", expanded=False):
    st.markdown("""
    - **Training**: 40 hours annually for volunteers.
    - **Partnerships**: With Kenyatta Hospital for referrals.
    - **Confidentiality**: Encrypted calls, strict privacy.
    - **Resources**: Free crisis pamphlets at locations.
    """)

# PROGRESS TRACKER SECTION
st.markdown("<div id='tracker'></div>", unsafe_allow_html=True)
st.markdown("## Progress Tracker")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p>Track your mental health:</p>
    <div class='tracker-card'>
        <h4>Mood Tracker</h4>
        <p>Rate mood (1-5) and add notes.</p>
    </div>
""", unsafe_allow_html=True)
mood = st.slider("How do you feel? (1 = Low, 5 = High)", 1, 5, 3, key="mood_input")
note = st.text_input("Add a note", placeholder="e.g., Stressful day", key="mood_note")
if st.button("Log Mood"):
    st.session_state.mood_history.append({"date": datetime.now(), "mood": mood, "note": note})
    st.success(f"Logged at 12:50 AM EAT, July 25, 2025!")
for entry in st.session_state.mood_history[-5:]:
    st.markdown(f"- {entry['date'].strftime('%Y-%m-%d %H:%M')}: Mood {entry['mood']}/5 {'(' + entry['note'] + ')' if entry['note'] else ''}")
if st.button("Export Mood History"):
    csv = export_mood_history()
    st.markdown(get_download_link(csv, "mood_history.csv"), unsafe_allow_html=True)
st.markdown("""
    <a href='#volunteer' class='primary-btn'>Next: Volunteer</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Tracking", expanded=False):
    st.markdown("""
    - **Features**: Export as CSV.
    - **Usage**: Log daily for 30 days.
    - **Support**: support@safespaceorganisation.org.
    - **Privacy**: Secure access.
    """)

# VOLUNTEER OPPORTUNITIES SECTION
st.markdown("<div id='volunteer'></div>", unsafe_allow_html=True)
st.markdown("## Volunteer Opportunities")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p>Join our mission with training:</p>
""", unsafe_allow_html=True)
volunteer_roles = [
    {"title": "Outreach Support", "desc": "2-4 hr campaigns in Nakuru/Mombasa, 10-hr training."},
    {"title": "Event Volunteer", "desc": "4-6 hr support for July 30/August 15 events."},
    {"title": "Crisis Line Assistant", "desc": "8 AM-7 PM shifts, 20-hr training."}
]
for role in volunteer_roles:
    st.markdown(f"""
    <div class='volunteer-card'>
        <h4>{role['title']}</h4>
        <p>{role['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-top: 0.5rem;'>
    <a href='#volunteer-form' class='primary-btn'>Register to Volunteer</a>
</div>
""", unsafe_allow_html=True)
st.markdown("<div id='volunteer-form'></div>", unsafe_allow_html=True)
with st.form("volunteer_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email", placeholder="your.email@example.com")
    phone = st.text_input("Phone", placeholder="+254 XXX XXX XXX")
    experience = st.text_area("Experience", placeholder="e.g., counseling")
    role_preference = st.selectbox("Role", ["Outreach Support", "Event Volunteer", "Crisis Line Assistant", "Any"])
    submit = st.form_submit_button("Register")
    if submit:
        if not all([name, email, re.match(r"[^@]+@[^@]+\.[^@]+", email), phone, experience]):
            st.error("Fill all fields.")
        else:
            st.session_state.outreach_form_data = {"name": name, "email": email, "phone": phone, "experience": experience, "role": role_preference}
            st.success(f"Thank you, {name}! Registered at 12:50 AM EAT, July 25, 2025. Contact at {email} within 48 hours.")
            st.session_state.outreach_form_data = {"name": "", "email": "", "phone": "", "experience": "", "role": "Any"}
st.markdown("""
<div style='text-align: center; margin-top: 0.5rem;'>
    <a href='#contact' class='primary-btn'>Contact Us</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Volunteering", expanded=False):
    st.markdown("""
    - **Impact**: 1,200 in 2024, 2,000 target 2025.
    - **Training**: 10-hr online, 5-hr in-person.
    - **Recognition**: Certificates, Volunteer Day Dec 15, 2025.
    - **Support**: Monthly check-ins.
    """)

# EVENTS SECTION
st.markdown("<div id='events'></div>", unsafe_allow_html=True)
st.markdown("## Upcoming Events")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <div class='event-card'>
        <h4>Stress Management Workshop</h4>
        <p>July 30, 2025, 9 AM-1 PM, Nairobi Hall. Free, register at events@safespaceorganisation.org.</p>
    </div>
    <div class='event-card'>
        <h4>Youth Mental Health Forum</h4>
        <p>August 15, 2025, 10 AM-2 PM, Kisumu Center. Ages 13-25.</p>
    </div>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Events", expanded=False):
    st.markdown("""
    - **Registration**: 50 per event, email required.
    - **Workshops**: Handouts, online Q&A.
    - **Past**: June 2025 Trauma Day, 80 attendees.
    - **Accessibility**: Sign language, wheelchair access.
    """)

# PARTNERSHIPS SECTION
st.markdown("<div id='partnerships'></div>", unsafe_allow_html=True)
st.markdown("## Our Partnerships")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <div class='partnership-card'>
        <h4>Kenyatta National Hospital</h4>
        <p>Referrals and trauma programs since 2024.</p>
    </div>
    <div class='partnership-card'>
        <h4>Kenya Red Cross</h4>
        <p>Disaster response training since 2023.</p>
    </div>
    <div class='partnership-card'>
        <h4>Ministry of Health</h4>
        <p>Policy support and rural funding.</p>
    </div>
    <div style='text-align: center; margin-top: 0.5rem;'>
        <a href='#partnership-form' class='primary-btn'>Register as Partner or Donor</a>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div id='partnership-form'></div>", unsafe_allow_html=True)
with st.form("partnership_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    organization = st.text_input("Organization Name (if applicable)")
    email = st.text_input("Email", placeholder="your.email@example.com")
    phone = st.text_input("Phone", placeholder="+254 XXX XXX XXX")
    partnership_type = st.selectbox("Register As", ["Partner", "Donor"])
    submit = st.form_submit_button("Submit")
    if submit:
        if not all([name, email, re.match(r"[^@]+@[^@]+\.[^@]+", email), phone]):
            st.error("Fill all required fields.")
        else:
            st.session_state.partnership_form_data = {"name": name, "organization": organization, "email": email, "phone": phone, "type": partnership_type}
            st.success(f"Thank you, {name}! Your {partnership_type} registration at 12:50 AM EAT, July 25, 2025, is received. Contact at {email} within 48 hours.")
            st.session_state.partnership_form_data = {"name": "", "organization": "", "email": "", "phone": "", "type": "Partner"}

# PARTNER WITH US SECTION
st.markdown("<div id='partner-with-us'></div>", unsafe_allow_html=True)
st.markdown("## Partner With Us")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
    <p>We invite schools, businesses, NGOs, and community organizations to join us in expanding mental health care. Your partnership can support training for local health workers, funding mobile clinics, or sponsoring outreach programs in underserved areas.</p>
    <p><strong>Benefits:</strong> Enhance your CSR profile, gain access to mental health resources, and collaborate on community impact projects.</p>
    <p>Register as a partner or donor using the form above or contact us at <a href='mailto:partnership@safespaceorganisation.org'>partnership@safespaceorganisation.org</a> for more details.</p>
    <a href='#partnership-form' class='primary-btn'>Get Started</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Partnerships", expanded=False):
    st.markdown("""
    - **Opportunities**: Joint workshops, co-funded initiatives, or shared research.
    - **Impact**: Reach 2,000+ additional clients with new partners by 2026.
    - **Process**: Initial consultation within 72 hours of contact.
    - **Examples**: Past partners include health NGOs and educational institutions.
    """)

# FAQ SECTION
st.markdown("<div id='faq'></div>", unsafe_allow_html=True)
st.markdown("## Frequently Asked Questions")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p><strong>Q: Ages?</strong> A: All ages, specialized programs.</p>
    <p><strong>Q: Confidentiality?</strong> A: Yes, encrypted, compliant.</p>
    <p><strong>Q: Payment?</strong> A: Cash, M-Pesa, subsidies.</p>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About FAQs", expanded=False):
    st.markdown("""
    - **Support**: faq@safespaceorganisation.org.
    - **Updates**: Quarterly, last July 2025.
    - **Resources**: Download FAQ PDF.
    """)

# CONTACT SECTION
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.markdown("## Contact Us")
st.markdown("""
<div style='background: white; padding: 0.8rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p><strong>📍</strong> Greenhouse Plaza, Ngong Road, Nairobi.</p>
    <p><strong>📞</strong> +254 781 095 919, 8 AM-7 PM EAT.</p>
    <p><strong>✉️</strong> <a href='mailto:info@safespaceorganisation.org'>info@safespaceorganisation.org</a>, 24-hr response.</p>
    <p><strong>Hours:</strong> Mon-Fri 9 AM-5 PM, Sat 10 AM-2 PM.</p>
    <a href='#' class='primary-btn'>Book Consultation</a>
</div>
""", unsafe_allow_html=True)
with st.expander("Learn More About Contacting Us", expanded=False):
    st.markdown("""
    - **Appointments**: Online or call, same-day slots.
    - **Accessibility**: Wheelchair, sign language.
    - **Follow-Up**: Within one week.
    - **Map**: On our website.
    """)

# CHATBOT
st.markdown("""
<button class='chatbot-toggle' id='chatbot-toggle'>💬</button>
<div class='chatbot-container' id='chatbot'>
    <h4>Ask SafeSpace Bot</h4>
    <div id='chat-messages' style='max-height: 300px; overflow-y: auto; margin-bottom: 0.5rem;'>
""", unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    st.markdown(f"<div class='chatbot-message {sender}'><p>{message}</p></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Ask me anything...", key="chat_input")
    submit = st.form_submit_button("Send")
    if submit and user_input:
        response = get_chatbot_response(user_input)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", response))
st.markdown("</div>", unsafe_allow_html=True)

# JavaScript to toggle chatbot
st.markdown("""
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const toggleButton = document.getElementById('chatbot-toggle');
        const chatbot = document.getElementById('chatbot');
        if (toggleButton && chatbot) {
            toggleButton.addEventListener('click', function() {
                chatbot.classList.toggle('active');
            });
        }
    });
</script>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p style='font-size: 0.9rem;'>© 2023-2025 SafeSpace Organisation | Designed with ❤️</p>
    <div style='display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;'>
        <a href='https://facebook.com/safespaceorganisation' target='_blank' class='primary-btn'>Facebook</a>
        <a href='https://instagram.com/safespaceorganisation' target='_blank' class='primary-btn'>Instagram</a>
        <a href='https://twitter.com/safespaceorganisation' target='_blank' class='primary-btn'>Twitter</a>
        <a href='https://linkedin.com/company/safespaceorganisation' target='_blank' class='primary-btn'>LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("newsletter_form", clear_on_submit=True):
    st.markdown("<div style='max-width: 300px; margin: 0.5rem auto; display: flex; gap: 0.3rem;'>", unsafe_allow_html=True)
    newsletter_email = st.text_input("", placeholder="Subscribe for tips...", key="newsletter_email")
    submit_newsletter = st.form_submit_button("Subscribe")
    st.markdown("</div>", unsafe_allow_html=True)
    if submit_newsletter:
        if not newsletter_email or not re.match(r"[^@]+@[^@]+\.[^@]+", newsletter_email):
            st.error("Valid email required.")
        else:
            st.success(f"Subscribed! Next newsletter: August 1, 2025, 9 AM EAT.")
