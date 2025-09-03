# from pathlib import Path
# dirName = input("Enter the directory name: ")
# # directory = Path(dirName)  # Change this to your target directory "C:/Books/TechBooks"
# #
# # files = [file.name for file in directory.iterdir() if file.is_file()]
# #
# # print("Files in directory:", files)
# # i = 1
# # for f in files:
# #     print(f"{i}. {f}")
# #     i +=1
# #
import os
from collections import defaultdict
#
#
def list_files_by_type(directory):
    file_types = defaultdict(list)

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            ext = os.path.splitext(file)[1] or "No Extension"
            file_types[ext].append(file)

    return file_types


# Example usage
directory = "C:/0Madhura/InfoWebPages/PyWeb/"  # Change to the desired directory
files_by_type = list_files_by_type(directory)

for ext, files in files_by_type.items():
    print(f"{ext}:")
    for file in files:
        print(f"  - {file}")
#
# import pandas as pd
# data  = pd.read_parquet('gold_vs_bitcoin.parquet')
# print(data)

# import speech_recognition as sr
# import pyttsx3
# import webbrowser
# import datetime
# import wikipedia
#
#
# # Initialize speech engine
# engine = pyttsx3.init()
#
#
# # Function to speak text
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()
#
#
# #Function to listen for commands
# def take_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
# #
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User said: {query}\n")
#     except Exception as e:
#         print("Say that again please...")
#         return "None"
#     return query
#
#
# # Main program loop
# if __name__ == "__main__":
#     # site = input("Enter the site name:")
#     # if site == "Donegal":
#     #     webbrowser.open(f"https://demo-dev.policypulse.io/")
#     query_list = ["wikipedia", "open youtube", "demo_donegal"]
#     query_list = [q.replace("wikipedia", "") for q in query_list]
#     print(query_list)
#     while True:
#
#
#         if 'wikipedia' in query_list:
#             speak('Searching Wikipedia...')
#             query =  [q.replace("wikipedia", "") for q in query_list]
#             webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
#
#         elif 'open youtube' in query_list:
#             speak("Opening YouTube...")
#             webbrowser.open("https://www.youtube.com")
#
#         elif 'demo_donegal' in query_list:
#             speak("Opening Donegal dashboard")
#             webbrowser.open("https://demo-dev.policypulse.io/")
#
#         elif 'time' in query_list:
#             str_time = datetime.datetime.now().strftime("%H:%M:%S")
#             speak(f"The time is {str_time}")
#
#         elif 'exit' in query_list:
#             speak("Goodbye!")
#             break
#
# a = [1, 1, 410,13, 59, 12, 19, 9]
# print(max(a))
# print(min(a))
# a1 = " inc"
# a2 = a1[::-1]
# print(a1)
# print(a2)
# if a1 == a2:
#     print("Palin")
# else:
#     print("Not a palin")
# amt = int(input("Enter principal amt: "))
# roi = int(input("Enter rate of interest: "))
# years = int(input("Enter no. of years: "))
# ci = (amt * ( 1 + roi /100) ** years) - amt
# print("Compound interest: ", ci)
# days = int(input("Enter no of days: "))
# years = days//365
# rem_days = days % 365
# mon = rem_days // 30
# days_left = rem_days %30
# print(f"{years} years, {mon} months, {days_left} days" )
# pos, neg = 0, 0
# a4 = [-9, 3, 0, -1, 4,6]
# for i in a4:
#     if i > 0:
#         pos += 1
#     elif i<0:
#         neg +=1
# print(f"No. of positive numbers: {pos} \nNo. of negative numbers: {neg} ")
# sent = input("Etner a sentence: ")
# noOfWords = sent.split(" ")
# print(f"No of words in the sentence: {len(noOfWords)}")