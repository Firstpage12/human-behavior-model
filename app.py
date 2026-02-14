import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np
# --------- SECRET PAGE STATE ----------
if "valentine" not in st.session_state:
    st.session_state.valentine = False

st.set_page_config(page_title="Chinu's State Inference", page_icon="🧠", layout="centered")

# ---------------- Load Data ----------------
df = pd.read_csv("data.csv")

# Encode categorical column
music_encoder = LabelEncoder()
df["music_listened"] = music_encoder.fit_transform(df["music_listened"])

label_encoder = LabelEncoder()
df["current_state"] = label_encoder.fit_transform(df["current_state"])

# Features & labels
X = df.drop("current_state", axis=1)
y = df["current_state"]

# Train model
model = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42)
model.fit(X, y)

# ---------------- UI ----------------
st.title("Chinu's Mood")

st.markdown("---")

st.subheader(" Input Observations")

sleep = st.slider("😴 Sleep hours last night", 3, 8, 6)
meal = st.slider("🍽 Hours since last meal", 0, 10, 3)
water = st.slider("💧 Water intake (glasses)", 3, 12, 6)
steps = st.slider("👟 Steps walked today", 3000, 15000, 6000)

col1, col2 = st.columns(2)

with col1:
    shower = st.selectbox("🚿 Shower taken today?", [0,1])
    outside = st.selectbox("🌤 Went outside today?", [0,1])

with col2:
    memes = st.slider("😂 Memes sent today", 0, 8, 2)
    music = st.selectbox("🎧 Music listened", ["none","calm","loud"])

boredom = st.slider("🧍 Boredom level", 1, 5, 3)

# Encode music
music_encoded = music_encoder.transform([music])[0]

# ---------------- Prediction ----------------
if st.button("Run Behavioral Inference 🔍"):

    input_data = pd.DataFrame({
        "sleep_hours_last_night":[sleep],
        "hours_since_last_meal":[meal],
        "water_intake_glasses":[water],
        "steps_walked":[steps],
        "shower_today":[shower],
        "went_outside_today":[outside],
        "sent_memes_today":[memes],
        "music_listened":[music_encoded],
        "boredom_level":[boredom]
    })

    # Predict
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    state = label_encoder.inverse_transform([prediction])[0]
    confidence = np.max(probabilities) * 100

    st.markdown("---")
    st.subheader("🧾 Model Output")

    # ---------- INTERPRETATIONS ----------
    messages = {
        "sleepy": "sojaaaaa.",
        "hungry": "Khale yrrr.Nhi hoga mota",
        "lazy_mode": "Code karoo.",
        "productive": "sahi h sahi h.",
        "social_mood": ".",
        "outside_chilling": "Mere bina.",
        "overthinking": "Jyada mat soch , vo me kar lungi ",
        "missing_you": "Awwwww. I miss you too ."
    }

    emojis = {
        "sleepy":"😴",
        "hungry":"🍕",
        "lazy_mode":"🛌",
        "productive":"💻",
        "social_mood":"😄",
        "outside_chilling":"🌤",
        "overthinking":"🧠",
        "missing_you":"❤️"
    }

    st.success(f"{emojis[state]} **Predicted State: {state}**")
    st.info(messages[state])
    st.write(f"**Model confidence:** {confidence:.2f}%")

    # Easter egg
    if state == "missing_you":

    

        st.balloons()
        st.markdown("## Rare Emotional Event Detected ❤️")
        st.session_state.valentine = True
        st.rerun()

    st.markdown("---")
    st.caption("Model trained on observational lifestyle data. Accuracy improves with snacks.")

# ================= VALENTINE PAGE =================
# ================= SECRET VALENTINE WORLD =================
# ================= VALENTINE WEEK QUEST =================
if st.session_state.valentine:

    st.markdown("""
    <style>
    .bigmsg {
        text-align:center;
        font-size:55px;
        font-weight:800;
        color:#ff2e63;
        padding-top:20px;
    }
    .submsg {
        text-align:center;
        font-size:22px;
        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bigmsg">I miss you too ❤️</div>', unsafe_allow_html=True)
    st.markdown('<div class="submsg">You unlocked the hidden world</div>', unsafe_allow_html=True)

    st.write("---")
    st.title("🔐 Valentine Week Quest")

    st.caption("Complete each day to reach the final message")

    if "day" not in st.session_state:
        st.session_state.day = 1

    st.write(f"### Current Day: {st.session_state.day}/7")
    st.write("---")

    # ---------- DAY 1 : ROSE DAY ----------
    if st.session_state.day == 1:
        st.header("🌹 Rose Day — Cipher")

        st.write("Decode this (Caesar shift -1):")
        st.code("ZPV")

        ans = st.text_input("Your answer")

        if ans.lower().strip() == "you":
            st.success("Rose accepted 🌹")
            st.session_state.day = 2
            st.rerun()


    # ---------- DAY 2 : TEDDY DAY ----------
    elif st.session_state.day == 2:
        st.header("🧸 Teddy Day — Memory")

        st.info("Memorize: 🐻 🌙 🍕 🎧 ⭐")

        seq = st.text_input("Enter emojis without spaces")

        if seq == "🐻🌙🍕🎧⭐":
            st.success("Teddy unlocked 🧸")
            st.session_state.day = 3
            st.rerun()

    # ---------- DAY 3 : CHOCOLATE DAY ----------
    elif st.session_state.day == 3:
        st.header("🍫 Chocolate Day — ASCII Puzzle")

        st.code("73 32 108 105 107 101 32 121 111 117")

        ans = st.text_input("Decode the message")

        if ans.lower().strip() == "i like you":
            st.success("Chocolate unlocked 🍫")
            st.session_state.day = 4
            st.rerun()


    # ---------- DAY 4 : PROPOSE DAY ----------
    elif st.session_state.day == 4:
        st.header("💍 Propose Day — Logic")

        st.write(
        """
        If I say:
        1 + 1 = 1  
        2 + 2 = 1  
        What does this represent?
        """
        )

        ans = st.text_input("Your guess")

        if "love" in ans.lower() or "together" in ans.lower():
            st.success("Proposal accepted 💍")
            st.session_state.day = 5
            st.rerun()


    # ---------- DAY 5 : HUG DAY ----------
    elif st.session_state.day == 5:
        st.header("🤗 Hug Day — Riddle")

        st.write(
        """
        I am not a person  
        but I make people feel safe.  
        I need no words  
        but I say everything.
        What am I?
        """
        )

        ans = st.text_input("Answer")

        if ans.lower().strip() in ["hug","a hug"]:
            st.success("Hug received 🤗")
            st.session_state.day = 6
            st.rerun()


    # ---------- DAY 6 : KISS DAY ----------
    elif st.session_state.day == 6:
        st.header("😘 Kiss Day — Pattern")

        st.write("Fill the blank:")

        st.code("🙂 🙂 🙂 ❤️ 🙂 🙂 ?")

        ans = st.text_input("What comes next?")

        if ans in ["❤️","❤","heart"]:
            st.success("Kiss unlocked 😘")
            st.session_state.day = 7
            st.rerun()


    # ---------- DAY 7 : VALENTINE DAY ----------
    elif st.session_state.day == 7:
        st.header("❤️ Final Day — Valentine")

        st.balloons()

        st.markdown(
        """
        ## Happy Valentine's Day ❤️

        """
        )

        if st.button("Return to model"):
            st.session_state.day = 1
            st.session_state.valentine = False
            st.rerun()

    st.stop()
