import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import re
from ConvertToDoc import generate_word_from_txt
#Gemeni Model Initialization
class AIModel:
    
    def __init__(self):
        self._preprocessed = None
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Google API
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.model._generation_config.update({
            'temperature': 0.1,
            'top_k': 7,
            'top_p': 0.7
        })
         
    def Generate_response(self, 
                          prompt, 
                          temperature = 0.2):
        response =None
        timer = 1
        responseText =None
        
        while not response:
            try:
                responseText = self.model.generate_content(prompt)
                response = responseText.text.replace('**', '').replace('*', '').replace('`', '')
            except Exception as e:
                print(f"Error : {e}")
                time.sleep(10*timer)
                timer+=1
                if timer>5:
                    return None ,None
        return response , responseText
#UserStories class
class UserStories(AIModel):
    def __init__(self,filePath):
        super().__init__()
        self.filePath = filePath
        self._data = ''
        
        self.UserStory = None
    def read_file(self):
        try:
            with open(self.filePath, 'r') as file:
                self._data = file.read()
           
        except FileNotFoundError as e:
            print( e)
        return self._data
    
    def preprocessing(self):
        prompt = f"Generate detailed requirements with key points from the following text:\n{self._data} \n Collect as data as possible Do not missout any requirements or details Make it minimum of 2000 words "
        try:
            PreprocessedText = self.model.generate_content(prompt)
            PreprocessedText = PreprocessedText.text.replace('**', '').replace('*', '').replace('`', '')
            self._preprocessed = PreprocessedText
            if not self._preprocessed:
                return False
            return True
        except Exception as e:
            print(f"Error : {e}")
            return False
    def GenerateUserStories(self):
        expected = "User Story example: As a [user], I want to [action], so that [reason/benefit]."
        prompt = (f"Context: Act as a product user. Create a high-level in detailed user story using the following \n{self._preprocessed} in the format: \n{expected} Also the give for all the requriments minimum of 10000 words NOTE : INCLUDE THE MINURED DETAIL ALSO ",
                  )
        self.UserStory ,self.unProcessed = self.Generate_response(prompt)
        if not self.UserStory:
                return None,None
        print("UserStories :")
        return self.UserStory , self.unProcessed
#SRS Document class
class SRSDocument(AIModel):
    def __init__(self,Userstroy):
        super().__init__()
        self.UserStory = Userstroy
        self.SRSdocument = None
    def GenerateSRS(self):
        expected = "User Story example: As a [user], I want to [action], so that [reason/benefit]."
        prompt = (f"Generate a in detailed Software Requirement Specification (SRS) for the following user stories WithOut Diagram minumin of 10000 words:\n"
                  f"{self.UserStory} NOTE :First scan the Requirements \n{self._preprocessed}",
                  )        
        self.SRSdocument,self.unProcessedSRS = self.Generate_response(prompt) 
        if not self.SRSdocument:
            return None,None   
        return self.SRSdocument ,self.unProcessedSRS
#HLD Document class       
class HLDDocument(AIModel):
    def __init__(self,SRSDocument):
        super().__init__()
        self.SoftwareRSProcessed = SRSDocument
        self.HLDoc = None
    def GenerateHLD(self):
        prompt =  f"Task:Generate a in detailed High-Level Design (HLD) for the following SRS WithOut Diagram minium of 10000 words:\n{self.SoftwareRSProcessed} NOTE :First scan the Requirements \n{self._preprocessed} and provide the minured details also :"
        self.HLDoc ,self.unProcessed= self.Generate_response(prompt,)
        if not self.HLDoc:
            return None,None
        print("HLD :")
        return self.HLDoc,self.unProcessed
    

#LLD Document class
class  LLDDocument(AIModel):
    def __init__(self,HLDDocument):
        super().__init__()
        self.HLDoc = HLDDocument
        self.LLDdoc = None
    def GenerateLLD(self):
        prompt = f"Task : Generate a Low-Level Design (LLD) in detailed for the following HLD , WithOut Diagram minium of 10000 words:\n{self.HLDoc}NOTE :First scan the Requirements \n{self._preprocessed} and provide the minured details also :"
        self.LLDdoc ,self.unProcessed= self.Generate_response(prompt,)
        if not self.LLDdoc:
            return None,None
        print("LLD :")
        return self.LLDdoc,self.unProcessed
class TOLSTestCase(AIModel):
    def __init__(self,LLDDocument):
        super().__init__()
        self.LLDocument = LLDDocument
        self.TOL = None
        self.test = None 
    def GenerateTOL(self):
        prompt = f"""prompt_from_lld 
        Based on the following LLD document, generate a table with the following columns
        Here is the LLD document:
        {self.LLDocument}
        
        """
        self.TOL ,self.unProcessedTOL = self.Generate_response(prompt)
        if not self.TOL:
            return None,None
        return self.TOL ,self.unProcessedTOL
    def GenerateTestCase(self):
        prompt = f"""
        Based on the following Table of Limitations (TOL) document, generate test cases with the following columns: Test Case ID, Test Scenario, Pre-Conditions, Test Steps, Expected Results.
        Here is the TOL document:
        {self.TOL}
        """
        self.test ,self.unProcessedTest = self.Generate_response(prompt)
        if not self.test:
            return None,None
        return self.test,self.unProcessedTest
    def TextAutomation(self):
        pass
#Generating code 
class CodeGeneration(AIModel):
    def __init__(self,LLDDocument):
        super().__init__()
        self.LLDdoc = LLDDocument
        self.Code = None
        self.pathofCode = []
    def CreatePathFiles(self):
        prompt=f"""Create a structured that outlines the file paths and descriptions for the following components: *[list the components/modules]* 
                Example : [
                "navbar.js" : "/FullCode/assests/components/navbar.js" 
                "Login.js" : "/FullCode/assests/pages/Login.js"] Without the description  ]
                make sure that before the json # - put this symbole and end of symbole put # symbole
                Note : This Is just a example it can be of any programing language or any framework.
                It must be based on the LLD document low-level design (LLD) Given below.:\n{self.LLDdoc}"""
        self.CodePath = self.Generate_response(prompt)
        return self.CodePath
    #This Function is Not Userd For now 
    def CreateFiles(self):
        self.filteredData = self.CodePath.split("#")[1]
        basePath = os.path.join(os.getcwd(), "Text-Requirements-User_stories/Ericsson_project/Backend")
        dict_data ={}
        try:
            dict_data = eval(self.filteredData.strip())
           
        except Exception as e:
            print(f"Error: {e}")
        self.code = self.Generate_response(f'Generate code for mentioned lld {self.LLDdoc} Provide only code no extra Add #-start fileName: Code /#/-end of each code Also provide the requiremnets.txt and package.json file ')
        print(f"Code generated : \n{self.code}")
        
        
        
        return True
    
    def CreateCode(self):
        code, _ = self.Generate_response(
            f'Generate code for the mentioned LLD {self.LLDdoc}. Provide only the code, no extra text. '
            'Add #-start fileName: Code #-end at the beginning and end of each code block. '
            'Note: Also provide the requirements.txt or package.json file. '
            'Note: Try to generate both frontend and backend code practically within the word limit of around 96,000 words.If possible complete both'
        )        
        if code:
            listNew = code.split('#-start')[1:]
        else :
      
            return False
 
        pathandcode ={}
        for listItems in listNew:
   
            sample_text =str(listItems).split("#-end")
           
            pathandcode[sample_text[0].split(":")[1]] = sample_text
          
        #basePath = os.path.join(os.getcwd(),"Text-Requirements-User_stories","Ericsson_project", "FullCode")
        
        basePath = os.path.join(os.getcwd(), "FullCode")
      
        for path ,code in pathandcode.items():
            fullPath = os.path.join(basePath, path.lstrip('/'))
            fullChanged = fullPath.replace("/", "\\").replace(" ","").replace("#",'')
          
            try:
                os.makedirs(os.path.dirname(fullChanged), exist_ok=True)
                with open(fullChanged.replace("-end",""),"w") as file:
                    newCode = re.sub(r'(JavaScript|Python|Ruby|html|json)', '', code[1], flags=re.IGNORECASE).strip()
                    file.write(newCode)
            except Exception as e :
                print(e)
        with open("README.md" ,"r") as file:
            with open(os.path.join(basePath,"README.md") ,"w") as readme:
                readme.write(file.read())
        
        return True
        
def main():
     
    
    userStories = UserStories("TestCase1.txt")
    userStories.read_file()  # Read file content
    userStories.preprocessing() 
    userOutput ,unProcessed  = userStories.GenerateUserStories()  
    print(userOutput , unProcessed.text) 

    """
    srsDoc = SRSDocument(userStories.UserStory)
    srsOutput, unProcessedSrs = srsDoc.GenerateSRS() 
    generate_word_from_txt(unProcessedSrs,"TestHLD.docx")
  
    hldDoc = HLDDocument(srsOutput)
    hldOutput =hldDoc.GenerateHLD()  


    lldDoc = LLDDocument(hldOutput)
    lldOutput =lldDoc.GenerateLLD()  


    print("Generated User Story:\n", userOutput)
    print("\nGenerated SRS Document:\n", srsOutput)
    print("\nGenerated High-Level Design (HLD):\n", hldOutput)
    print("\nGenerated Low-Level Design (LLD):\n", lldOutput)
    
    with open("Text-Requirements-User_stories/Ericsson_project/Backend/uploads/lldOutput.txt") as file :
        text = file.read()
    output =CodeGeneration(text)
    output.CreateCode()
    """
    
    
if __name__ == "__main__":
    main()
