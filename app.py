from llm import client

question = input("Ask Gemini: ")

answer = client.return_app_json_response(question)

print("Response:\n")
print(answer)

