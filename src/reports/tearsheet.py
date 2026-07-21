import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart

def build_tearsheet(company_data, output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_normal = ParagraphStyle('Norm', parent=styles['Normal'], fontSize=9, leading=11, wordWrap='CJK')
    style_pro = ParagraphStyle('Pro', parent=style_normal, textColor=colors.HexColor("#006600"))
    style_con = ParagraphStyle('Con', parent=style_normal, textColor=colors.HexColor("#CC0000"))
    
    story = []

    # ==================== PAGE 1 ====================
    # Navy Header Bar
    header_data = [[Paragraph(f"<font color='white' size='16'><b>{company_data['name']} ({company_data['ticker']})</b></font>", style_normal)]]
    header_table = Table(header_data, colWidths=[550], rowHeights=[35])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#002B49")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # 6 KPI Tiles (2 rows x 3 cols)
    kpis = company_data.get('kpis', {'Market Cap': '1,200 Cr', 'PE': '22.5', 'ROE': '18%', 'ROCE': '21%', 'D/E': '0.0', 'OPM': '24%'})
    kpi_items = list(kpis.items())
    kpi_table_data = [
        [f"{kpi_items[i][0]}\n{kpi_items[i][1]}" for i in range(0, 3)],
        [f"{kpi_items[i][0]}\n{kpi_items[i][1]}" for i in range(3, 6)]
    ]
    
    # Convert cell strings into Paragraph objects with wordwrap
    p_kpi_data = [[Paragraph(f"<b>{cell}</b>", style_normal) for cell in row] for row in kpi_table_data]
    kpi_table = Table(p_kpi_data, colWidths=[183, 183, 183])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F4F8")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 20))

    # Charts Section (Placeholder Bar Chart for Demonstration)
    d = Drawing(550, 180)
    bc = VerticalBarChart()
    bc.x = 40
    bc.y = 20
    bc.height = 130
    bc.width = 470
    bc.data = [[10, 20, 30, 40, 50, 65, 75, 85, 95, 110]] # Revenue Trend
    bc.categoryAxis.categoryNames = [str(y) for y in range(2017, 2027)]
    d.add(bc)
    story.append(d)

    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    # Section Header
    story.append(Paragraph("<b>Financial Statements & Cash Flow Analysis</b>", styles['Heading2']))
    story.append(Spacer(1, 10))

    # Pros Section
    story.append(Paragraph("<b>Strengths (Pros)</b>", styles['Heading3']))
    pros = company_data.get('pros', ["Consistently high return on equity.", "Strong FCF generation."])
    for p in pros:
        story.append(Paragraph(f"• {p}", style_pro))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # Cons Section
    story.append(Paragraph("<b>Risks (Cons)</b>", styles['Heading3']))
    cons = company_data.get('cons', ["Operating margin contraction.", "Elevated valuation ratios."])
    for c in cons:
        story.append(Paragraph(f"• {c}", style_con))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 15))

    # Capital Allocation Badge
    badge_text = f"Capital Allocation Pattern: <b>{company_data.get('allocation_badge', 'Reinvestor')}</b>"
    badge_table = Table([[Paragraph(badge_text, style_normal)]], colWidths=[550])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E2E8F0")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(badge_table)

    # Build Document
    doc.build(story)

if __name__ == "__main__":
    os.makedirs("reports/tearsheets", exist_ok=True)
    sample_company = {
        "name": "Tata Consultancy Services", "ticker": "TCS",
        "kpis": {'Market Cap': '14,00,000 Cr', 'P/E': '28.5', 'ROE': '45%', 'ROCE': '52%', 'D/E': '0.0', 'OPM': '25%'},
        "pros": ["Consistently high return on equity above 20%.", "Debt-free balance sheet."],
        "cons": ["Operating margins declining slightly."],
        "allocation_badge": "High-Return Reinvestor"
    }
    build_tearsheet(sample_company, "reports/tearsheets/TCS_tearsheet.pdf")