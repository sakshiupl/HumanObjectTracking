import streamlit as st
import subprocess

st.write('Here are some of the samples from the original #track.py that were generated while training.')

output_video_path = 'output.mp4'
transcoded_video_path = output_video_path.replace('.mp4', '_transcoded.mp4')
subprocess.run([
'ffmpeg', '-i', output_video_path,
'-vcodec', 'libx264',
'-crf', '23',
'-preset', 'fast',
'-pix_fmt', 'yuv420p',
transcoded_video_path
], check=True)

st.video(transcoded_video_path)