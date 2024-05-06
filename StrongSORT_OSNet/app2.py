import streamlit as st
import subprocess
import os

st.title('Real-time Video Tracking')

if 'proc' not in st.session_state or st.session_state.proc.poll() is not None:
    # Process not started or previous process finished
    if st.button('Start Tracking'):
        command = [
            'python', 'track.py',
            '--yolo-weights', 'yolov7.pt',
            '--strong-sort-weights', 'osnet_x0_25_msmt17.pt',
            '--source', '0',
            '--conf-thres', '0.15'
        ]
        st.session_state.proc = subprocess.Popen(command)  # This will start the process
else:
    if st.button('Stop Tracking'):
        st.session_state.proc.terminate()  # This will terminate the process

# Optional: Display whether tracking is running or not
if 'proc' in st.session_state:
    st.write(f"Tracking is {'running' if st.session_state.proc.poll() is None else 'not running'}")
