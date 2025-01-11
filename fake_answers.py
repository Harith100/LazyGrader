import os
from groq import Groq
import re




class Brain:
    def __init__(self) -> None:
        self.client = Groq(api_key='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')
        #self.sentiment_analyzer = SentimentAnalyzer()
        self.chat_history = [
            {"role": "system", "content": """Teacher Answer: "Electricity flows through conductors like copper and aluminum."

Student Answer: "Copper and aluminum conduct electricity."

Generate fake answers: "Electricity flows only through rubber and plastic," "Conductors stop electricity from flowing," "Electricity travels faster in insulators," "Copper is an insulator," "Electricity cannot flow through metals," "Aluminum blocks electricity," "Rubber conducts electricity better than copper," "All materials conduct electricity equally," "Electricity only flows through wires."""}
        ]  # Initializes the conversation with system instructions

    def generate(self, message):
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": message})

        # Send chat history to model for context-aware completion
        chat_completion = self.client.chat.completions.create(
            messages=self.chat_history,
            model="llama3-8b-8192",
        )

        # Retrieve and print the response
        response = chat_completion.choices[0].message.content
        return response

        # Add assistant's response to chat history
        self.chat_history.append({"role": "assistant", "content": response})
        
        # Perform sentiment analysis (optional)
        #sentiment = self.sentiment_analyzer.analyze_sentiment(response)
       # print("Sentiment Analysis:", sentiment)

    def extract(self, response):
        quoted_strings = re.findall(r'"([^"]+)"', response)
        return quoted_strings
    def operate(self,message):
        msg=self.generate(message)
        li=self.extract(msg)
        return li
# Continuous Chat Loop with Memory
if __name__ == "__main__":
    brain = Brain()
    #print("Start chatting with the AI (type 'bye' to end):")
    
    out=brain.operate("""Teacher Answer: "Electricity flows through conductors like copper and aluminum."

Student Answer: "Copper and aluminum conduct electricity.""")
    print(out)
    