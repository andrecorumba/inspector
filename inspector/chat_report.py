import os

from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChatAuditReport():
    def __init__ (self):
        self.model_name = "gpt-3.5-turbo-16k"
        self.documents = None
        self.docs_splited = None
    
    def load_pdf_report_from_path(self, path_to_pdf_report: str):
        '''Function to load the PDF report.
        
        Parameters:
        path_to_pdf_report (str): Path to the PDF report.

        Returns:
        documents (list): List of documents.
        '''
        
        if os.path.isfile(path_to_pdf_report):
            loader = PyPDFLoader(path_to_pdf_report)
            self.documents = loader.load()
        else:
            raise FileNotFoundError("File not found. Please check the path to the PDF report.")
        return self.documents
    
    def load_pdf_folder(self, path_to_pdf_report):
        '''Function to load the PDF folder.
        
        Parameters:
        path_to_pdf_report (str): Path to the PDF folder.
        
        Returns:
        documents (list): List of documents.
        '''
        
        # Check if the path is a folder
        if os.path.isdir(path_to_pdf_report):
            loader = PyPDFDirectoryLoader(path_to_pdf_report)
            self.documents = loader.load()
        else:
            raise FileNotFoundError("Folder not found. Please check the path to the PDF folder.")
        return self.documents
    
    def split_documents_from_tiktoken_encoder(self):
        '''Function to split the documents from TikToken encoder.
        See https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token 
        Default chunk_size from TextSplitter class are 4000 caracters.
        '''

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(model_name=self.model_name)
        self.docs_splited = text_splitter.split_documents(self.documents)

        return self.docs_splited


if __name__ == "__main__":
    report = ChatAuditReport()
    report.load_pdf_report_from_path("/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos/1497056.pdf")
    print("report: ", len(report.documents))
    print("Tamanho do documento na posição: ",len(report.documents[0].page_content))
    print("DOCUMENT LOADED \n", report.documents[0])
    print("\n\n")

    # reports_in_folder = ChatAuditReport()
    # reports_in_folder.load_pdf_folder("/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos")
    # print("reports_in_folder: ", len(reports_in_folder.documents))

    report.split_documents_from_tiktoken_encoder()
    print("report splited: ", len(report.docs_splited))
    print("Tamanho do split do documento na posição: ",len(report.docs_splited[0].page_content))
   # print("DOCUMENT SPLITED \n", report.docs_splited)

