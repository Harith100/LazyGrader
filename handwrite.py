import os
import time
import google.generativeai as genai

class Hand2Text:
    def __init__(self, api_key_env_var="GEMINI_API_KEY"):
        """Initialize the Hand2Text class with Gemini API key."""
        if api_key_env_var not in os.environ:
            raise ValueError(f"Environment variable '{api_key_env_var}' not found.")
        genai.configure(api_key=os.environ[api_key_env_var])
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
                        "Transcribe the answer sheets into text, provide text only. Make sure question numbers are there in the text.",
                    ],
                },
            ]
        )

        # Send the transcription request
        response = chat_session.send_message("Start transcription.")

        return response.text

# Example usage
if __name__ == "__main__":
    try:
        hand2text = Hand2Text()
        transcribed_text = hand2text.transcribe_answer_sheet("Document 5.pdf")
        print("Transcribed Text:")
        print(transcribed_text)
    except Exception as e:
        print(f"An error occurred: {e}")