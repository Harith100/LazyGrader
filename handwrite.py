import os
import time
import google.generativeai as genai
import re

class Hand2Text:
    def __init__(self):
        
        genai.configure(api_key='AIzaSyB_Gd-cLHlByZ3ErhuCaCUfZQDwu8KG9PA')
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
        )

    @staticmethod
    def upload_to_gemini(path, mime_type=None):
        """Uploads the given file to Gemini and returns the file object."""
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    @staticmethod
    def wait_for_files_active(files):
        """Waits for the uploaded files to be processed and become active."""
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        print("...all files ready")
        print()

    

    def transcribe_answer_sheet(self, pdf_path):
        """Uploads a PDF, waits for processing, and transcribes it into text."""
        # Upload the file
        file = self.upload_to_gemini(pdf_path, mime_type="application/pdf")
        
        # Wait for the file to be active
        self.wait_for_files_active([file])

        # Start the chat session
        chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        file,
                        """
                        You are an AI designed to transcribe and format examination answer sheets. Your task is to extract answers from a student's response and provide them in a structured format. Follow these guidelines:

                        Structure each answer starting with the question number, followed by the answer, like this:
                        Ensure the numbering is sequential and accurate.
                        Avoid unnecessary introductory text like: "Here is the text:" ,"This is the answer:".
                        Any greetings, acknowledgments, or unrelated information.
                        Preserve the formatting of the content exactly as provided, without adding any extra words or phrases.
                        Ensure each question's number( use '1)' format for numbering, no other format like '1.)' and '1.' ) and answer are clearly separated. Do not merge answers into a single paragraph.
                        Do not include any additional explanations or comments unrelated to the answers. Only provide clean, structured text as described above.
                            """,
                            ],
                },
            ]
        )

        # Send the transcription request
        response = chat_session.send_message("Start transcription.")

        return response.text
    
    def parse_responses(self,response):
        
        pattern = r"(\d+)\)\s*(.+?)(?=\n\d+\)|$)"
        matches = re.findall(pattern, response, re.DOTALL)
        result = {int(num): answer.strip() for num, answer in matches}

        return result
    
    def evaluate(self, pdf_path):
        response=self.transcribe_answer_sheet(pdf_path)
        print(response)
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
        st=hand2text.evaluate("Questions_Hackathon.pdf")
        print(st)

    except Exception as e:
        print(f"An error occurred: {e}")