import google.generativeai as genai
import os
from dotenv import load_dotenv
class AIModel:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Google API
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.model._generation_config.update({
            'temperature': 0.2,
            'top_k': 7,
            'top_p': 0.7
        })
    def Generate_response(self, prompt):
        response =""
        try:
            responseText = self.model.generate_content(prompt)
            response = responseText.text.replace('**', '').replace('*', '').replace('`', '')
            return response
        except Exception as e:
            print(f"Error : {e}")
class UserStroies(AIModel):
    def __init__(self,filePath):
        super().__init__()
        self.filePath = filePath
        self._data = ''
        self._preprocessed = ""
        self.UserStory = ""
    def read_file(self):
        try:
            with open(self.filePath, 'r') as file:
                self._data = file.read()
            print(self._data)
        except FileNotFoundError as e:
            print( e)
    
    def preprocessing(self):
        prompt = f"Generate detailed requirements with key points from the following text:\n{self._data}"
        try:
            PreprocessedText = self.model.generate_content(prompt)
            PreprocessedText = PreprocessedText.text.replace('**', '').replace('*', '').replace('`', '')
            self._preprocessed = PreprocessedText
            return True
        except Exception as e:
            print(f"Error : {e}")
            return False
    def GenerateUserStories(self):
        expected = "User Story example: As a [user], I want to [action], so that [reason/benefit]."
        prompt = (f"Context: Act as a product user. Create a high-level user story using the following \n{self._preprocessed} in the format: \n{expected}.Avoid statements like 'Functional Requirement.")
        self.UserStory = self.Generate_response(prompt)
        return self.UserStory
        
class SRSDocument(AIModel):
    def __init__(self,Userstroy):
        super().__init__()
        self.UserStory = Userstroy
        self.SRSdocument = ""
    def GenerateSRS(self):
        expected = "User Story example: As a [user], I want to [action], so that [reason/benefit]."
        prompt = (f"Generate a Software Requirement Specification (SRS) for the following user stories WithOut Diagram:\n"
                  f"{self.UserStory}")        
        self.UserStory = self.Generate_response(prompt)      
        return self.UserStory
       
class HLDDocument(AIModel):
    def __init__(self,SRSDocument):
        super().__init__()
        self.SoftwareRSProcessed = SRSDocument
        self.HLDoc = ""
    def GenerateHLD(self):
        prompt =  f"Task:Generate a High-Level Design (HLD) for the following SRS WithOut Diagram:\n{self.SoftwareRSProcessed}"
        self.HLDoc = self.Generate_response(prompt)
        return self.HLDoc
class  LLDDocument(AIModel):
    def __init__(self,HLDDocument):
        super().__init__()
        self.HLDoc = HLDDocument
        self.LLDdoc = ""
    def GenerateLLD(self):
        prompt = f"Task : Generate a Low-Level Design (LLD) in detailed for the following HLD , WithOut Diagram:\n{self.HLDoc}"
        self.LLDdoc = self.Generate_response(prompt)
        return self.LLDdoc
class CodeGeneration(AIModel):
    def __init__(self,LLDDocument):
        super().__init__()
        self.LLDdoc = LLDDocument
        self.Code = ""
        self.pathofCode = []
    def CreatePathFiles(self):
        prompt=f"""Create a structured that outlines the file paths and descriptions for the following components: *[list the components/modules]* 
                Example : [
                "navbar.js" : "/AllCode/assests/components/navbar.js" 
                "Login.js" : "/AllCode/assests/pages/Login.js"] Without the description  ]
                make sure that before the json # - put this symbole and end of symbole put # symbole
                Note : This Is just a example it can be of any programing language or any framework.
                It must be based on the LLD document low-level design (LLD) Given below.:\n{self.LLDdoc}"""
        self.CodePath = self.Generate_response(prompt)
        return self.CodePath
    def CreateFiles(self):
        self.filteredData = self.CodePath.split("#")[1]
        basePath = os.path.join(os.getcwd(), "Text-Requirements-User_stories/Ericsson_project/Backend")
        try:
            dict_data = eval(self.filteredData.strip())
            print(dict_data)
        except Exception as e:
            print(f"Error: {e}")

        print(type(dict_data))

        for fileName, filePath in dict_data.items():
            try:
                fullPath = os.path.join(basePath, filePath.lstrip('/'))
                print(fileName, fullPath)
                os.makedirs(os.path.dirname(fullPath), exist_ok=True)
                #with open(full_path, "w") as file:
                   # file.write("Hello")
            except Exception as e:
                print(e)
                return False
        return True
        
    def CreateCode(self):
        code =[]
        chucks = 5
        for i in range(0, len(self.LLDdoc), chucks):
            
            prompt = f"""Generate the code for the following files : \n {self.filteredData} \n
                    And for the LLD :\n{self.LLDdoc[i:i+chucks]}
                    Also Create a struture code like #-start  FileName : Code # -end  """
            code.append(self.Generate_response(prompt))
            print(chucks ,code)

        self.Code = "\n".join(code)
        return self.Code
    
def main():
    # Step 1: Initialize UserStories instance with file path and generate user stories
    userStories = UserStroies("Text-Requirements-User_stories/Ericsson_project/Backend/uploads/Divyas.txt")
    userStories.read_file()  # Read file content
    userStories.preprocessing() # Preprocess data if successful
    userOutput = userStories.GenerateUserStories()  # Generate user stories
    # Step 2: Generate SRS document based on the user stories
    srsDoc = SRSDocument(userStories.UserStory)
    srsOutput = srsDoc.GenerateSRS()  # Create SRS Document

    # Step 3: Generate HLD document based on the SRS
    hldDoc = HLDDocument(srsOutput)
    hldOutput =hldDoc.GenerateHLD()  # Create High-Level Design

    # Step 4: Generate LLD document based on the HLD
    lldDoc = LLDDocument(hldOutput)
    lldOutput =lldDoc.GenerateLLD()  # Create Low-Level Design

    # Output the generated documents
    print("Generated User Story:\n", userOutput)
    print("\nGenerated SRS Document:\n", srsOutput)
    print("\nGenerated High-Level Design (HLD):\n", hldOutput)
    print("\nGenerated Low-Level Design (LLD):\n", lldOutput)
    """
    text =""
    with open("Text-Requirements-User_stories/Ericsson_project/Backend/uploads/Sample3.txt") as file :
        text = file.read()
    output =CodeGeneration(text)
    print(output.CreatePathFiles())
    output.CreateFiles()
    print(output.CreateCode())\
    """
    
if __name__ == "__main__":
    main()
