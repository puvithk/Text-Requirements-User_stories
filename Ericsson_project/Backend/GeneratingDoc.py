import google.generativeai as genai
import os
from dotenv import load_dotenv
class UserStories:
    def __init__(self, filePath):
        load_dotenv()
        self.filePath = filePath #uploads/puvith.txt
        self.data =''
        self.preprocessed =""
        self.UserStory =""
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        with open(filePath, 'r')as file :
            self.data = file.read()
       
    def preprocessing(self):
        prompt = f"""Generate detailed requirements with key points from the following text:\n {self.data}"""
        try:
          
            self.model._generation_config['temperature'] = 0.8
            self.model._generation_config['top_k'] = 40
            self.model._generation_config['top_p'] = 0.95
            PreprocessedText  = self.model.generate_content(prompt)

            PreprocessedText=PreprocessedText.text.replace('**', '').replace('*', '').replace('`', '')
            self.preprocessed =PreprocessedText
            return True
        except Exception as e :
            print(e)
            return False
    def GenerateUserStories(self):
        expected ="User Stroy expamle : As a [user],I want to [action], so that [reason/benefit]."
        try :
            
            self.model._generation_config['temperature'] = 0.8
            self.model._generation_config['top_k'] = 40
            self.model._generation_config['top_p'] = 0.95
            UserStory  = self.model.generate_content(
                f'Context : Act as a product user , Create a High level user story using the followeing {self.preprocessed} with expected output as in the same  formate as  {expected}'
                                            )

            UserStoryText = UserStory.text.replace('**', '').replace('*', '').replace('`', '')
            self.UserStory =UserStoryText
            return True
        except Exception as e :
            print(e)
            return False
if __name__ =="__main__":
    userStries= UserStories("Text-Requirements-User_stories/Ericsson_project/Backend/uploads/gsdgvasfw.txt")

# if os.path.exists(os.path.join(DOCUMENTS_DIR, "Requirements.docx")):
#         DOCUMENT_STATUS["Requirements"] = True
#     if os.path.exists(os.path.join(DOCUMENTS_DIR, "UserStories.docx")):
#         DOCUMENT_STATUS["UserStories"] = True
#     if os.path.exists(os.path.join(DOCUMENTS_DIR, "SRS.docx")):
#         DOCUMENT_STATUS["SRS"] = True
#     if os.path.exists(os.path.join(DOCUMENTS_DIR, "LLD.docx")):
#         DOCUMENT_STATUS["LLD"] = True
#     if os.path.exists(os.path.join(DOCUMENTS_DIR, "HLD.docx")):
#         DOCUMENT_STATUS["HLD"] = True