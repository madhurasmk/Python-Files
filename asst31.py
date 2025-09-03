# from flask import Flask, request, jsonify
# import openai
# import os
# import time
# from datetime import datetime
# from openai import OpenAI
#
# asst31 = Flask(__name__)
#
# # Initialize OpenAI client
# client = OpenAI(api_key="MM_API_Key")
#
#
# def create_assistant(name, instructions, file_ids=[]):
#     assistant = client.beta.assistants.create(
#         name=name,
#         instructions=instructions,
#         model="gpt-4o",
#         tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
#         tool_resources={
#             "code_interpreter": {"file_ids": file_ids}
#         }
#     )
#     return assistant
#
#
# @asst31.route('/create_assistant', methods=['POST'])
# def create_assistant_api():
#     data = request.json
#     name = data.get("name")
#     instructions = data.get("instructions")
#     file_ids = data.get("file_ids", [])
#
#     assistant = create_assistant(name, instructions, file_ids)
#     return jsonify({"assistant_id": assistant.id, "name": assistant.name})
#
#
# @asst31.route('/update_assistant', methods=['POST'])
# def update_assistant():
#     data = request.json
#     assistant_id = data.get("assistant_id")
#     name = data.get("name")
#     instructions = data.get("instructions")
#
#     updated_assistant = client.beta.assistants.update(
#         assistant_id,
#         name=name,
#         instructions=instructions
#     )
#     return jsonify({"updated_name": updated_assistant.name, "updated_instructions": updated_assistant.instructions})
#
#
# @asst31.route('/delete_assistant', methods=['POST'])
# def delete_assistant():
#     data = request.json
#     assistant_id = data.get("assistant_id")
#
#     client.beta.assistants.delete(assistant_id)
#     return jsonify({"message": "Assistant deleted successfully."})
#
#
# @asst31.route('/list_assistants', methods=['GET'])
# def list_assistants():
#     assistants = client.beta.assistants.list()
#     assistant_list = [{"id": a.id, "name": a.name} for a in assistants.data]
#     return jsonify({"assistants": assistant_list})
#
#
# @asst31.route('/search_files', methods=['POST'])
# def search_files():
#     data = request.json
#     search_query = data.get("query")
#     assistant_id = data.get("assistant_id")
#
#     thread = client.beta.threads.create(
#         messages=[{"role": "user", "content": search_query}]
#     )
#
#     response = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant_id,
#         instructions="Analyze the documents and provide a summary."
#     )
#     return jsonify(response)
#
#
# if __name__ == '__main__':
#     asst31.run(debug=True)
#
# print(asst31.url_map)

