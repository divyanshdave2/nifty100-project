import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_portfolio_summary():
    os.makedirs("reports/portfolio", exist_ok=True)
    pdf_filename = "reports/portfolio/portfolio_summary.pdf"
    
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Norm', parent=styles['Normal'], fontSize=10, leading=12)

    # Search for companies dataset
    possible_paths = [
        "data/raw/companies.xlsx",
        "data/processed/companies.csv",
        "companies.csv"
    ]
    
    companies_filepath = None
    for path in possible_paths:
        if os.path.exists(path):
            companies_filepath = path
            break

    if not companies_filepath:
        print("⚠️ Warning: Companies file not found for Portfolio Summary.")
        return

    print(f"Reading companies for portfolio summary from: {companies_filepath}")
    if companies_filepath.endswith('.xlsx'):
        companies_df = pd.read_excel(companies_filepath)
    else:
        companies_df = pd.read_csv(companies_filepath)

    companies_df.columns = companies_df.columns.astype(str).str.strip().str.lower()
    
    id_col = next((c for c in ['ticker', 'symbol', 'company_id', 'company_name'] if c in companies_df.columns), companies_df.columns[0])
    companies_df = companies_df.sort_values(by=id_col)
    
    story = []

    def get_trend_symbol(change_val):
        try:
            val = float(change_val)
            if val > 2.0: return "↑"
            elif val < -2.0: return "↓"
            else: return "→"
        except:
            return "→"

    for _, row in companies_df.iterrows():
        ticker = str(row[id_col])
        name = str(row.get('name', row.get('company_name', ticker)))
        sector = str(row.get('sector', 'General'))

        # Title Header
        story.append(Paragraph(f"<b>{ticker} - {name}</b>", styles['Heading1']))
        story.append(Paragraph(f"<b>Sector:</b> {sector}", styles['Heading3']))
        story.append(Spacer(1, 15))

        # Trends
        roe_trend = get_trend_symbol(row.get('roe_change_pct', 0))
        opm_trend = get_trend_symbol(row.get('opm_change_pct', 0))
        pe_trend = get_trend_symbol(row.get('pe_change_pct', 0))

        table_data = [
            [Paragraph("<b>Metric</b>", style_normal), Paragraph("<b>Value</b>", style_normal), Paragraph("<b>YoY Trend</b>", style_normal)],
            [Paragraph("ROE", style_normal), Paragraph(f"{row.get('roe', 'N/A')}%", style_normal), Paragraph(roe_trend, style_normal)],
            [Paragraph("OPM", style_normal), Paragraph(f"{row.get('opm', 'N/A')}%", style_normal), Paragraph(opm_trend, style_normal)],
            [Paragraph("P/E Ratio", style_normal), Paragraph(str(row.get('pe', 'N/A')), style_normal), Paragraph(pe_trend, style_normal)],
            [Paragraph("ROCE", style_normal), Paragraph(f"{row.get('roce', 'N/A')}%", style_normal), Paragraph("→", style_normal)],
            [Paragraph("D/E Ratio", style_normal), Paragraph(str(row.get('de', 'N/A')), style_normal), Paragraph("→", style_normal)],
        ]

        summary_table = Table(table_data, colWidths=[200, 150, 150])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#002B49")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
        ]))

        story.append(summary_table)
        story.append(PageBreak())

    doc.build(story)
    print("Day 35 Complete: Portfolio Summary PDF generated successfully.")

if __name__ == "__main__":
    generate_portfolio_summary()