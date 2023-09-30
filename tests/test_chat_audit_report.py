import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inspector.chat_report import ChatAuditReport  # Import your ChatAuditReport class from the actual module

# Define a test directory with sample PDFs for testing
TEST_PDF_DIRECTORY = "/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos/"

# Fixture to create an instance of ChatAuditReport for testing
@pytest.fixture
def chat_audit_report_instance():
    return ChatAuditReport()

# Test case for loading a single PDF report
def test_load_pdf_report_from_path(chat_audit_report_instance):
    pdf_path = "/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos/1419562.pdf"
    
    # Load the PDF report
    documents = chat_audit_report_instance.load_pdf_report_from_path(pdf_path)
    
    # Assert that the documents list is not empty
    assert documents is not None
    assert isinstance(documents, list)

# Test case for loading a PDF folder
def test_load_pdf_folder(chat_audit_report_instance):
    # Load the PDF folder
    documents = chat_audit_report_instance.load_pdf_folder(TEST_PDF_DIRECTORY)
    
    # Assert that the documents list is not empty
    assert documents is not None
    assert isinstance(documents, list)

# Test case for handling a non-existent file
def test_load_pdf_report_from_path_file_not_found(chat_audit_report_instance):
    with pytest.raises(FileNotFoundError):
        chat_audit_report_instance.load_pdf_report_from_path("non_existent_file.pdf")

# Test case for handling a non-existent folder
def test_load_pdf_folder_folder_not_found(chat_audit_report_instance):
    with pytest.raises(FileNotFoundError):
        chat_audit_report_instance.load_pdf_folder("non_existent_folder")

if __name__ == "__main__":
    pytest.main()
