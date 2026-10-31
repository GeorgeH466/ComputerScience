from pathlib import Path
from docx import Document
from database_connection import create_connection

def get_customer_data(customer):
    #gets info from the database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Join the existing customer subtables so the invoice has complete data.
        cursor.execute(
            "SELECT c.Customer_ID AS id, c.customer_name AS name, "
            "l.Address AS address, ct.Email AS email "
            "FROM customer c "
            "LEFT JOIN customerlocation l ON l.Customer_ID = c.Customer_ID "
            "LEFT JOIN customer_contact ct ON ct.Customer_ID = c.Customer_ID "
            "WHERE c.Customer_ID = %s LIMIT 1",
            (customer,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def replace_placeholder(document, placeholder, value):
    #fills in template
    replacement = "" if value is None else str(value)

    # does both the paragraph filling ad the table fillin that then allows for all of the collected data from the database to be inserted
    for paragraph in document.paragraphs:
        _replace_in_paragraph(paragraph, placeholder, replacement)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _replace_in_paragraph(paragraph, placeholder, replacement)


def _replace_in_paragraph(paragraph, placeholder, replacement):
   #A check to make sure that is the text is split then the information still gets inputted to the word dock
    if placeholder not in paragraph.text:
        return

    #if there is a split then this tries to fix it
    updated_text = paragraph.text.replace(placeholder, replacement)
    if paragraph.runs:
        paragraph.runs[0].text = updated_text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(updated_text)


def generate_invoice(customer, output_path=None, job=None):
    # generates the actual document
    # Need to normalise the data first because the data if from the sql queary 
    try:
        customer_id = int(customer)
    except (TypeError, ValueError) as error:
        raise ValueError("Customer must be a numeric customer ID.") from error

    # Load customer details and shows error if there is one
    data = get_customer_data(customer_id)
    if data is None:
        raise LookupError(f"Customer {customer_id} was not found.")

    # 
    job_data = job if job is not None else job
    if job_data is None:
        job_data = {"description": "", "cost": ""}
    template_path = Path(__file__).with_name("invoice_template.docx")
    if not template_path.exists():
        raise FileNotFoundError(f"Invoice template not found: {template_path}")
    invoice = Document(str(template_path))

    # Fill all of the template fields that are able to be filled by the info available
    fields = {
        "{{CUSTOMER_NAME}}": data.get("name"),
        "{{CUSTOMER_ADDRESS}}": data.get("address"),
        "{{CUSTOMER_EMAIL}}": data.get("email"),
        "{{JOB_DESCRIPTION}}": job_data.get("description"),
        "{{JOB_COST}}": job_data.get("cost"),
    }
    for placeholder, value in fields.items():
        replace_placeholder(invoice, placeholder, value)

    # Save s in project folder
    destination = Path(output_path) if output_path else Path(__file__).with_name(
        f"invoice_{customer_id}.docx"
    )
    invoice.save(str(destination))
    return destination
