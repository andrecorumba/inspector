import os

from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader

class ChatAuditReport():
    def __init__ (self):
        self.documents = None
    
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


if __name__ == "__main__":
    report = ChatAuditReport()
    reports_in_folder = ChatAuditReport()
    report.load_pdf_report_from_path("/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos/1419562.pdf")
    reports_in_folder.load_pdf_folder("/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos")

    print("report: ", len(report.documents))
    print("reports_in_folder: ", len(reports_in_folder.documents))

