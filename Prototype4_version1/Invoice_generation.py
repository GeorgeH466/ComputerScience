from docx import Document


def generate_invoice(customer):
    # Get the customer's data from the database
    data = get_customer_data(customer)

    # Get the customer's latest job
    job = get_latest_job(customer)

    # Check if job data exists
    if job is None:
        print("Error: No job data")
        return

    # Open the pre-made Word invoice template
    invoice = Document("invoice_template.docx")

    # Replace placeholders in the template with customer data
    replace_placeholder(invoice, "{{CUSTOMER_NAME}}", data["name"])
    replace_placeholder(invoice, "{{CUSTOMER_ADDRESS}}", data["address"])
    replace_placeholder(invoice, "{{CUSTOMER_EMAIL}}", data["email"])

    # Insert job information into the invoice
    replace_placeholder(invoice, "{{JOB_DESCRIPTION}}", job["description"])
    replace_placeholder(invoice, "{{JOB_COST}}", str(job["cost"]))

    # Save the completed invoice as a Word document
    invoice.save(f"invoice_{customer}.docx")


def replace_placeholder(document, placeholder, value):
    # Search through all paragraphs in the document
    for paragraph in document.paragraphs:
        if placeholder in paragraph.text:
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)
