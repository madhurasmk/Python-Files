# from flask import Flask, render_template_string
# import markdown
#
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     with open("README.md", "r") as md_file:
#         md_content = md_file.read()
#         html_content = markdown.markdown(md_content)  # Convert Markdown to HTML
#     return render_template_string("<html><body>{{ content|safe }}</body></html>", content=html_content)
#
# if __name__ == "__main__":
#     app.run(debug=True)
# from collections import Counter, defaultdict
#
# so = defaultdict(list)
# from pytube import YouTube
from pytube import YouTube, extract
extract.video_id.cache_clear()
yt_video = YouTube("https://www.youtube.com/watch?v=uME2usudN5g")

# Print available streams
for stream in yt_video.streams:
    print(stream)

# Try fetching 360p MP4 stream
v_file = yt_video.streams.filter(file_extension="mp4", res="360p", progressive=True).first()

if v_file:
    v_file.download("C:/0Madhura/InfoWebPages/PyWeb")
    print("Download successful!")
else:
    print("360p MP4 stream not found. Try a different resolution.")
