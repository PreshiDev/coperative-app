from io import BytesIO
from django.template.loader import get_template
from weasyprint import HTML
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def generate_pdf(savings, loans):
    template = get_template('reports/pdf_template.html')  # Create a template for PDF
    context = {'savings': savings, 'loans': loans}
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf()
    return pdf_file

def generate_excel(savings):
    output = BytesIO()
    workbook = Workbook()
    worksheet = workbook.active

    # Write headers
    headers = ['Month', 'Owner', 'Payment Type', 'Normal Savings', 'Divine Touch', 'SP Sav', 'RSS', 'Loan Repay', 'Loan', 'Interest', 'Commod', 'Received']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        worksheet[f'{col_letter}1'] = header

    # Write data
    for row_num, saving in enumerate(savings, start=2):
        worksheet[f'A{row_num}'] = saving.get_month_display()
        worksheet[f'B{row_num}'] = f'{saving.owner.first_name} {saving.owner.last_name}'
        worksheet[f'C{row_num}'] = saving.payment_type
        worksheet[f'D{row_num}'] = saving.normal_savings
        worksheet[f'E{row_num}'] = saving.divine_touch
        worksheet[f'F{row_num}'] = saving.sp_sav
        worksheet[f'G{row_num}'] = saving.rss
        worksheet[f'H{row_num}'] = saving.loan_repay
        worksheet[f'I{row_num}'] = saving.loan
        worksheet[f'J{row_num}'] = saving.interest
        worksheet[f'K{row_num}'] = saving.commod
        worksheet[f'L{row_num}'] = saving.received

    workbook.save(output)
    output.seek(0)
    return output.getvalue()
