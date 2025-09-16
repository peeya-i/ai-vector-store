from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Test Document', ln=True)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, 'This is a test document for our AI Vector Store.\n\nThis document contains some sample text that we can search for later.\n\nKey features of our system:\n1. Fast document processing\n2. Semantic search capabilities\n3. Efficient vector storage\n\nThe system uses LanceDB for vector storage and FastAPI for the REST API.\nYou can search for specific terms or concepts in this document.')
pdf.output('api-backend/uploads/test.pdf')