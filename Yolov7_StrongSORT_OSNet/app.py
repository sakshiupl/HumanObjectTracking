import streamlit as st
import subprocess
import os
import tempfile
from moviepy.editor import VideoFileClip


# Define the header content
header_text = """
    <div style="background-color:cadetblue; width:100%;  padding:10px;border-radius:10px">
        <h1 style="color:#333333;text-align:center;">Human/Object Tracking - Team 13</h1>
    </div>
"""

# Display the header using st.markdown
st.markdown(header_text, unsafe_allow_html=True)


def video_upload_and_tracking():
    st.subheader('Upload a Video for Tracking')
    uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            # Write the uploaded video to a temporary file
            tmpfile.write(uploaded_file.read())
            input_video_path = tmpfile.name

        # Command to run the tracking script
        command = [
            'python', 'track.py',
            '--yolo-weights', 'yolov7.pt',
            '--strong-sort-weights', 'osnet_x0_25_msmt17.pt',
            '--source', input_video_path,
            '--save-vid',
            '--conf-thres', '0.15'
        ]
        st.write("Running command:", ' '.join(command))
        subprocess.run(command, check=True)

        # Locate the newest output directory
        base_path = 'runs/track/'
        list_of_dirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        latest_dir = max(list_of_dirs, key=os.path.getmtime)

        # Find the first .mp4 file in the latest directory
        video_files = [f for f in os.listdir(latest_dir) if f.endswith('.mp4')]
        if video_files:
            output_video_path = os.path.join(latest_dir, video_files[0])
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
            # Cleanup
            os.remove(input_video_path)
            os.remove(transcoded_video_path)
        else:
            st.error('Processed video file not found. Please check the output directory.')

def real_time_tracking():
    st.subheader('Real-time Video Tracking')
    if st.button('Start Tracking'):
        if 'proc' not in st.session_state or st.session_state.proc.poll() is not None:
            command = [
                'python', 'track.py',
                '--yolo-weights', 'yolov7.pt',
                '--strong-sort-weights', 'osnet_x0_25_msmt17.pt',
                '--source', '0',
                '--conf-thres', '0.15'
            ]
            st.session_state.proc = subprocess.Popen(command)
            st.write("Tracking started...")
    if st.button('Stop Tracking'):
        if 'proc' in st.session_state and st.session_state.proc.poll() is None:
            st.session_state.proc.terminate()
            st.write("Tracking stopped.")

def view_sample_video():
    st.subheader('Sample Training Video')
    output_video_path = 'output.mp4'
    transcoded_video_path = output_video_path.replace('.mp4', '_transcoded.mp4')

    # Load the original video file
    clip = VideoFileClip(output_video_path)

    # Write the video file with the desired codec, resolution, etc.
    clip.write_videofile(transcoded_video_path, codec='libx264', preset='fast', ffmpeg_params=['-crf', '23'])

    # Display the video in the Streamlit app
    st.video(transcoded_video_path)


#st.title('Video Tracking Application')

option = st.selectbox(
    'Choose your tracking option:',
    ('Upload a Video', 'Real-time Tracking', 'View Sample Video')
)

if option == 'Upload a Video':
    video_upload_and_tracking()
elif option == 'Real-time Tracking':
    real_time_tracking()
elif option == 'View Sample Video':
    view_sample_video()
