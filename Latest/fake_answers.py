import os
from groq import Groq
import re


class Brain:
    def __init__(self) -> None:
        self.client = Groq(api_key='')
        #self.sentiment_analyzer = SentimentAnalyzer()
        self.chat_history = [
        {
            "role": "system",
            "content": "Always Generate a numbered list of fake answers even if the student answer is right or wrong. generate the answers inside \" \". just generate fake answers only, dont add any other dialogues"
        },
        {
            "role": "user",
            "content": "Teacher Answer: \"Electricity flows through conductors like copper and aluminum.\"\n\nStudent Answer: \"Copper and aluminum conduct electricity."
        },
        {
            "role": "assistant",
            "content": "1. \"Electricity is carried by wires made of silver and gold.\"\n2. \"Conductors like copper and zinc are used in electronics.\"\n3. \"Aluminum and tin are poor conductors of electricity.\"\n4. \"Copper is a better conductor than aluminum in high temperatures.\"\n5. \"Electricity only flows through conductors in the presence of magnets.\""
        },
        {
            "role": "user",
            "content": "Teacher Answer: \"The digestive system breaks down food into nutrients that the body can use.\"\nStudent Answer: \"Food is broken into nutrients by the digestive system.\""
        },
        {
            "role": "assistant",
            "content": "1. \"The circulatory system is responsible for breaking down food into energy.\"\n2. \"Nutrients are absorbed by the body through the respiratory system.\"\n3. \"The digestive system only breaks down carbohydrates and proteins.\"\n4. \"The liver is the primary organ that breaks down food into nutrients.\"\n5. \"The pancreas is the only organ involved in the digestion process.\""
        },
        {
            "role": "user",
            "content": "Teacher Answer: \"The digestive system breaks down food into nutrients that the body can use.\"\nStudent Answer: \"The circulatory system is responsible for breaking down food into energy.\""
        },
        {
            "role": "assistant",
            "content": "1. \"The nervous system controls the breakdown of food into nutrients.\"\n2. \"The excretory system is responsible for digesting and absorbing food.\"\n3. \"The skeletal system plays a role in breaking down food into energy.\"\n4. \"The immune system is involved in the digestion and absorption of nutrients.\"\n5. \"The endocrine system is the primary system that breaks down food into energy.\""
        },
        {
            "role": "user",
            "content": "Teacher Answer: \"The digestive system breaks down food into nutrients that the body can use.\"\nStudent Answer: \"The circulatory system is responsible for breaking down food into energy.\""
        },
        {
            "role": "assistant",
            "content": "1. \"The lymphatic system breaks down food into nutrients and energy.\"\n2. \"The respiratory system is where food is broken down into glucose.\"\n3. \"The integumentary system plays a crucial role in nutrient absorption.\"\n4. \"The urinary system is responsible for digesting proteins and carbohydrates.\"\n5. \"The muscular system breaks down food into nutrients and energy.\""
        }
    ] # Initializes the conversation with system instructions

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
        # print("before generation")
        msg=self.generate(message)
        # print("before extract")
        li=self.extract(msg)
        # print("after extract")
        return li
# Continuous Chat Loop with Memory
if __name__ == "__main__":
    brain = Brain()
    #print("Start chatting with the AI (type 'bye' to end):")
    for _ in range(4):
        out=brain.operate("""Teacher Answer: "The digestive system breaks down food into nutrients that the body can use."
    Student Answer: "Food is broken into nutrients by the digestive system." """)
        print(out)
    