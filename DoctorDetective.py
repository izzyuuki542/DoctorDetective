import streamlit as st
import random

diseases = {
    "Pulmonary Embolism": ["shortness of breath", "chest pain", "recent flight", "tachycardia", "haemoptysis"],
    "Myocardial Infarction": ["chest pain", "sweating", "nausea", "shortness of breath"],
    "Pneumonia": ["cough", "fever", "chest pain", "shortness of breath"],
    "Asthma": ["shortness of breath", "cough", "history of atopy"],
    "Pneumothorax": ["chest pain", "shortness of breath", "cough", "tachycardia"],
    "Arrhythmia": ["palpitations", "syncope", "dizziness", "chest discomfort", "shortness of breath"]
}

teaching_points = {
    "Pulmonary Embolism": "A PE often presents with pleuritic chest pain, dyspnoea, tachycardia, and risk factors such "
                          "as recent long flights. Diagnosis may require CTPA (pulmonary angio). Management includes "
                          "anticoagulation.",
    "Myocardial Infarction": "MI typically presents with crushing chest pain radiating to the arm/jaw, nausea, "
                             "and diaphoresis. ECG may show ST elevation. Acute management includes primary "
                             "Percutaneous Coronary Intervention (pPCI). Medications includes morphine , oxygen, "
                             "aspirin and nitroglycerin.",
    "Pneumonia": "Classically presents with cough, fever, chest pain, and productive sputum. CXR shows consolidation. "
                 "Management includes antibiotics and supportive care.",
    "Asthma": "Patients may present with wheeze, cough, and SOB, often with history of atopy. Management is with "
              "bronchodilators (SABA) and steroids if severe.",
    "Pneumothorax": "Sudden chest pain and SOB, sometimes with tracheal deviation on CXR. Management depends on size "
                    "and symptoms — can range from observation to chest drain insertion.",
    "Arrhythmia": "Presents with palpitations, dizziness, or syncope. ECG shows the specific rhythm (e.g., "
                  "AF: irregularly irregular). Management depends on type (rate/rhythm control, anticoagulation)."
}

if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "highscore" not in st.session_state:
    st.session_state.highscore = 0
if "investigations" not in st.session_state:
    st.session_state.investigations = []

if "case" not in st.session_state:
    st.session_state.case = random.choice(list(diseases.keys()))
    st.session_state.symptoms = random.sample(diseases[st.session_state.case], 2)
    st.session_state.asked = []
    st.session_state.extra_questions = 0
    st.session_state.finished = False
    st.session_state.game_id = 0  # unique key for resetting inputs
    st.session_state.penalty = 0

st.title("🩺 Guess the Breathlessness!")
st.write(f"💯 Total Score: {st.session_state.total_score} | 🏆 Highscore: {st.session_state.highscore}")

st.subheader("Presenting Complaint:")
st.write(", ".join(st.session_state.symptoms))

all_questions = ["Any history of long flights?", "Fever?", "Wheeze?", "Pain radiating to arm/jaw?", "Cough with sputum?"
                 , "CXR findings?", "ECG findings?"]

if st.session_state.extra_questions < 2 and not st.session_state.finished:
    question = st.selectbox("What question would you like to ask? (-2 pts for each extra qn)",
                            ["Select a question!"] + all_questions,
                            key=f"q_{st.session_state.game_id}")
    if question != "Select a question!" and question not in st.session_state.asked:
        st.session_state.asked.append(question)
        st.session_state.extra_questions += 1
        st.session_state.penalty -= 2  # penalty

        answer = "No / Findings are normal"
        if st.session_state.case == "Pulmonary Embolism" and question == "Any history of long flights?":
            answer = "Yes – recent long flight ✈️"
        elif st.session_state.case == "Pneumonia" and question == "Fever?":
            answer = "Yes – high fever 🌡️"
        elif st.session_state.case == "Asthma" and question == "Wheeze?":
            answer = "Yes – expiratory wheeze 💨"
        elif st.session_state.case == "Myocardial Infarction" and question == "Pain radiating to arm/jaw?":
            answer = "Yes – radiates to left arm 💪"
        elif st.session_state.case == "Pneumonia" and question == "Cough with sputum?":
            answer = "Yes – productive cough 🤒"
        elif st.session_state.case == "Pulmonary Embolism" and question == "CXR findings?":
            answer = random.choice(["Findings are normal", "CXR shows fluid buildup 💧"])
        elif st.session_state.case == "Pneumonia" and question == "CXR findings?":
            answer = "CXR shows consolidation ☁️"
        elif st.session_state.case == "Pneumothorax" and question == "CXR findings?":
            answer = "CXR shows tracheal deviation 🫁"
        elif st.session_state.case == "Arrhythmia" and question == "ECG findings?":
            answer = "ECG shows irregularly irregular rhythm ❤️‍🔥"
        elif st.session_state.case == "Myocardial Infarction" and question == "ECG findings?":
            answer = "ECG shows ST elevation 📈"
        elif st.session_state.case == "Pulmonary Embolism" and question == "ECG findings?":
            answer = "ECG shows sinus tachycardia ⚡"

        st.info(answer)
        st.session_state.investigations.append(f"{question}: {answer}")
elif st.session_state.extra_questions >= 2:
    st.warning("⚠️ You can only ask 2 additional questions.")
if st.session_state.investigations:
    st.subheader("📝 Clerking Notes")
    for i, inv in enumerate(st.session_state.investigations, 1):
        st.write(f"{i}. {inv}")

st.subheader("Your Differential Diagnosis")

cols = st.columns(3)
for i, disease in enumerate(diseases.keys()):
    col = cols[i % 3]
    with col:
        if st.button(
                disease,
                key=f"disease_{st.session_state.game_id}_{i}"
        ):
            st.session_state.guess = disease
            st.session_state.result_msg = None

if "guess" in st.session_state and st.session_state.guess:
    st.markdown(f"**🩺 You selected:** {st.session_state.guess}")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Confirm Diagnosis",
                     key=f"confirm_{st.session_state.game_id}") and not st.session_state.finished:
            if st.session_state.guess == st.session_state.case:
                st.session_state.total_score += 10 + st.session_state.penalty
                st.session_state.result_msg = f"✅ Correct! It was {st.session_state.case}"
            else:
                if st.session_state.total_score > st.session_state.highscore:
                    st.session_state.highscore = st.session_state.total_score
                st.session_state.result_msg = f"❌ Wrong! It was actually {st.session_state.case}"
                st.session_state.total_score = 0
            st.session_state.finished = True

    with c2:
        if st.session_state.finished:
            if st.button("🔄 Next Patient"):
                old_id = st.session_state.game_id
                st.session_state.case = random.choice(list(diseases.keys()))
                st.session_state.symptoms = random.sample(diseases[st.session_state.case], 2)
                st.session_state.asked = []
                st.session_state.extra_questions = 0
                st.session_state.finished = False
                st.session_state.game_id = old_id + 1
                st.session_state.penalty = 0
                st.session_state.investigations = []
                st.session_state.guess = None
                st.session_state.result_msg = None
                st.rerun()

    if "result_msg" in st.session_state and st.session_state.result_msg:
        if "✅" in st.session_state.result_msg:
            st.success(st.session_state.result_msg)
        else:
            st.error(st.session_state.result_msg)

        diagnosis = st.session_state.case
        if diagnosis in teaching_points:
            with st.expander("📚 Learn more"):
                st.write(teaching_points[diagnosis])
