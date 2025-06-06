import os
import time
from google import genai
from google.genai import types
import re

class Hand2Text:
    def __init__(self):
        
        self.client = genai.Client(
        api_key="",
        )

    def transcribe_answer_sheet(self, pdf_path):
        """Uploads a PDF, waits for processing, and transcribes it into text."""
        # Upload the file
        file = self.client.files.upload(file=pdf_path)
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=["""You are an AI designed to transcribe and format examination answer sheets. Your task is to extract answers from a student's response and provide them in a structured format. Follow these guidelines:

                        Structure each answer starting with the question number, followed by the answer, like this:
                        Ensure the numbering is sequential and accurate.
                        Avoid unnecessary introductory text like: \"Here is the text:\" ,\"This is the answer:\".
                        Any greetings, acknowledgments, or unrelated information.
                        Preserve the formatting of the content exactly as provided, without adding any extra words or phrases.
                        Ensure each question's number( use '1)' format for numbering, no other format like '1.)' and '1.' ) and answer are clearly separated. Do not merge answers into a single paragraph.
                        Do not include any additional explanations or comments unrelated to the answers. Only provide clean, structured text as described above.""", file]
        )
        # print(response.text)

        return response.text
    
    def parse_responses(self,response):
        
        pattern = r"(\d+)\)\s*(.+?)(?=\n\d+\)|$)"
        matches = re.findall(pattern, response, re.DOTALL)
        result = {int(num): answer.strip() for num, answer in matches}

        return result
    
    def evaluate(self, pdf_path):
        response=self.transcribe_answer_sheet(pdf_path)
        # print(response)
        res=self.parse_responses(response)
        return res

     

# Example usage
if __name__ == "__main__":
    try:
        hand2text = Hand2Text()
        #transcribed_text = hand2text.transcribe_answer_sheet("Document 5.pdf")
        
       # print(transcribed_text)
        #res=hand2text.parse_responses(transcribed_text)
       # print(res)
        st=hand2text.evaluate("./data/Answer_Key.pdf")
        print(st)

    except Exception as e:
        print(f"An error occurred: {e}")