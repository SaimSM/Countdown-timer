import streamlit as st
from datetime import timedelta
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Interactive Countdown Timer", page_icon="⏱️", layout="centered")
st.markdown(
    """
    <style>
    .big-title {
        font-size: 3em;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .timer-display {
        font-size: 2.5em;
        text-align: center;
        color: #FF5722;
        margin-top: 20px;
    }
    body {
        background: linear-gradient(to right, #ece9e6, #ffffff);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds = 0
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'paused' not in st.session_state:
    st.session_state.paused = False

st.markdown("<div class='big-title'>Interactive Countdown Timer</div>", unsafe_allow_html=True)
st.write("Start the timer and watch it auto-refresh every second.")

with st.sidebar:
    st.header("Timer Settings")
    hours = st.number_input("Hours", min_value=0, max_value=23, value=0, step=1)
    minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, step=1)
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=10, step=1)
    new_total = hours * 3600 + minutes * 60 + seconds

if not st.session_state.timer_running:
    st.session_state.total_seconds = new_total
    st.session_state.remaining_seconds = new_total

timer_placeholder = st.empty()
progress_bar = st.progress(100 if st.session_state.total_seconds else 0)

def update_display():
    time_str = str(timedelta(seconds=st.session_state.remaining_seconds))
    timer_placeholder.markdown(f"<div class='timer-display'>{time_str}</div>", unsafe_allow_html=True)

update_display()

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Start"):
        if st.session_state.total_seconds <= 0:
            st.error("Set a time greater than 0 seconds!")
        else:
            st.session_state.timer_running = True
            st.session_state.paused = False
with col2:
    if st.button("Pause"):
        st.session_state.paused = True
with col3:
    if st.button("Resume"):
        st.session_state.paused = False
with col4:
    if st.button("Reset"):
        st.session_state.timer_running = False
        st.session_state.paused = False
        st.session_state.remaining_seconds = st.session_state.total_seconds
        update_display()
        progress_bar.progress(100)

if st.session_state.timer_running and not st.session_state.paused:
    if st.session_state.remaining_seconds > 0:
        st_autorefresh(interval=1000, key="countdown_refresh")
        st.session_state.remaining_seconds -= 1
        progress = int((st.session_state.remaining_seconds / st.session_state.total_seconds) * 100)
        progress_bar.progress(progress)
        update_display()
    else:
        timer_placeholder.markdown("<div class='timer-display'>Time's Up!</div>", unsafe_allow_html=True)
        progress_bar.progress(0)
        st.balloons()
        st.success("Countdown Completed!")
        st.session_state.timer_running = False
