from openai import OpenAI
from flask import Flask, render_template, request


client = OpenAI(api_key='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’)


conversation = [{"role": "system", "content": "You are a helpful assistant."}]


def get_response(message):
   conversation.append({"role": "user", "content": message})


   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=conversation
   )
   
   reply = response.choices[0].message.content
   conversation.append({"role": "assistant", "content": reply})


   return reply


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('chatbot.html')


@app.route('/ask', methods=['POST']) 
def ask(): 
   message = request.form['message'] 
   response = get_response(message) 
   return response


if __name__ == "__main__":
   app.run()
