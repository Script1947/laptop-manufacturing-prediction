"""
Generate Clean 3-Page Hinglish Project & Viva Guide PDF
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "Laptop Manufacturing Time & Cost Predictor  |  Complete Viva & Project Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 745, 558, 745)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_text)
        self.drawString(54, 30, "College Mini-Project Guide (Machine Learning) - Easy Hinglish Explanation")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 40, 558, 40)
        self.restoreState()


def create_pdf(filename="Laptop_Project_Hinglish_Viva_Guide.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=10,
        spaceAfter=4
    )

    sub_heading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=2
    )

    viva_q_style = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=4,
        spaceAfter=1.5
    )

    viva_a_style = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    story = []

    # Title Banner
    story.append(Paragraph("Laptop Production Time & Cost Predictor", title_style))
    story.append(Paragraph("Complete Zero-to-Advance Project Notes, Architecture Flow & Top 15 Viva Q&A (in Hinglish)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))

    # Summary Grid
    summary_data = [
        [Paragraph("<b>Domain:</b> Applied Machine Learning", body_style), Paragraph("<b>Targets:</b> 2 (Batch Time in min, Batch Cost in INR)", body_style)],
        [Paragraph("<b>Dataset:</b> 600 Records, 13 Attributes", body_style), Paragraph("<b>Split:</b> 70% Train (420) / 30% Test (180)", body_style)],
        [Paragraph("<b>Algorithm:</b> Random Forest Regressor", body_style), Paragraph("<b>Accuracy (R2):</b> 95.8% (Time), 98.1% (Cost)", body_style)],
        [Paragraph("<b>Frontend:</b> Streamlit Web App", body_style), Paragraph("<b>Core Language:</b> Python 3.13", body_style)]
    ]
    summary_table = Table(summary_data, colWidths=[255, 255])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # PART 1: ZERO TO ADVANCE NOTES
    story.append(Paragraph("PART 1: ZERO TO ADVANCE PROJECT NOTES (Samajhne Ke Liye)", section_heading))
    
    story.append(Paragraph("1. Project Kya Hai? (In 2 Lines)", sub_heading))
    story.append(Paragraph(
        "Laptop banane me har ek component (casing, RAM, hinges, motherboard) ko physically banane ya lagane me "
        "<b>kitna time (minutes me)</b> aur <b>kitna kharcha (INR Rupees me)</b> aayega, yeh hamara Machine Learning model "
        "historical data se seekhkar accurately predict karta hai.", body_style
    ))

    story.append(Paragraph("2. Real-World Problem: Yeh Project Kyu Banaya?", sub_heading))
    story.append(Paragraph(
        "Factory me production shuru karne se pehle planning karni hoti hai: "
        "(1) 100 laptops ka casing banane me machine kitne ghante chalegi? "
        "(2) RAM aur SSD assemble karne me kitna labor time lagega? "
        "(3) Ek batch ka total expenditure kitna hoga? "
        "Pehle yeh rough manual guessing se hota tha. Humne ML use karke automated data-driven prediction system banaya.",
        body_style
    ))

    story.append(Paragraph("3. Manufacturing vs Assembly Me Antar (Examiner Ka Favorite Sawal)", sub_heading))
    story.append(Paragraph(
        "Examiner sabse pehle yahi dekhta hai ki student ko manufacturing ka basic logic pata hai ya nahi:", body_style
    ))
    story.append(Paragraph("<b>A. Manufacturing Operations:</b> Raw material (Plastic, Aluminum, Steel) ko factory me machine se shape dekar component banaya jata hai. Jaise: Laptop Casing (Injection Molding), Laptop Hinges (Stamping), Heat Sink (Aluminum cutting).", bullet_style))
    story.append(Paragraph("<b>B. Assembly Operations:</b> Complex electronics hum factory me khud nahi banate; unhe market se purchase karke laptop me fit kiya jata hai. Jaise: Motherboard installation, RAM slotting, SSD mounting, Display connection, Thermal paste lagana. (Sir, hum RAM ya SSD manufacture nahi karte, unhe install karte hain!)", bullet_style))

    story.append(Paragraph("4. Input Features (11 Columns) Aur Target Variables (2 Columns)", sub_heading))
    story.append(Paragraph("Model ko prediction ke liye 11 inputs diye jate hain: Component Type, Process Type, Material, Length, Width, Height, Batch Quantity, Manufacturing Process, Complexity Level (1.0 to 1.4), Machine Type, aur Shift (Day/Night).", body_style))
    story.append(Paragraph("Outputs 2 hain: <b>Model A -> Actual Time (Minutes)</b> aur <b>Model B -> Actual Cost (INR Rupees)</b>.", body_style))

    story.append(Paragraph("5. Data Preprocessing (Model Train Hone Se Pehle)", sub_heading))
    story.append(Paragraph(
        "ML models text nahi samajhte, sirf numbers samajhte hain. Isliye ColumnTransformer pipeline banayi: "
        "(1) <b>One-Hot Encoding:</b> Material, Machine Type, Shift jaise text columns ko binary numbers (0 aur 1) me convert kiya. handle_unknown='ignore' lagaya taaki naye input par app crash na ho. "
        "(2) <b>StandardScaler:</b> Dimensions aur Quantity ke alag-alag scales ko normalize kiya. "
        "(3) <b>70/30 Train-Test Split:</b> 600 rows me se 70% (420 rows) sikhane ke liye di aur 30% (180 rows) test karne ke liye alag rakhi.",
        body_style
    ))

    story.append(Paragraph("6. Random Forest Regressor Hi Kyu Chuna?", sub_heading))
    story.append(Paragraph(
        "Pehle humne simple Linear Regression try kiya tha, lekin uska accuracy score sirf 67% (Time) aur 43% (Cost) aaya. "
        "Kyunki factory physics me non-linear patterns hote hain (jaise CNC machine par Aluminum kaatna plastic molding se exponential zyada time leta hai). "
        "<b>Random Forest 100 Decision Trees ka group banata hai</b>. Har tree alag-alag data par seekhta hai aur prediction ke waqt sabhi 100 trees ka average (mean) nikaal kar final answer deta hai. Isse hamara R2 score >95% ho gaya aur overfitting ruk gayi.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # PART 2: SYSTEM ARCHITECTURE & FLOW DIAGRAM
    story.append(Paragraph("PART 2: SYSTEM FLOW & ARCHITECTURE", section_heading))
    story.append(Paragraph("Data factory dataset se lekar Streamlit web interface tak kaise move karta hai:", body_style))

    flow_boxes = [
        [Paragraph("<b>STEP 1: CSV DATASET</b> | 600 Rows, 13 Columns (Laptop historical batch records)", body_style)],
        [Paragraph("<b>STEP 2: DATA VALIDATION</b> | Verified 0 null values, 0 duplicates, strictly positive physical dimensions", body_style)],
        [Paragraph("<b>STEP 3: 70/30 TRAIN-TEST SPLIT</b> | 420 Rows Training Set (strictly for learning) | 180 Rows Testing Set (held-out)", body_style)],
        [Paragraph("<b>STEP 4: PREPROCESSING PIPELINE</b> | OneHotEncoder (Categorical text features) + StandardScaler (Numeric features)", body_style)],
        [Paragraph("<b>STEP 5: DUAL RANDOM FOREST TRAINING</b> | Model A: Time Regressor (100 Trees) | Model B: Cost Regressor (100 Trees)", body_style)],
        [Paragraph("<b>STEP 6: TESTING & BENCHMARKING</b> | Time: R2 = 0.9585 (95.8%), MAE = 68.4 min | Cost: R2 = 0.9807 (98.1%), MAE = Rs 852.3", body_style)],
        [Paragraph("<b>STEP 7: STREAMLIT WEB APP</b> | User enters Component + Quantity -> Models predict Total Batch Time & Cost instantly", body_style)]
    ]
    flow_table = Table(flow_boxes, colWidths=[510])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 6))

    # Model Evaluation Comparison Table
    story.append(Paragraph("Model Benchmarks Comparison Table (Test Set: 180 Rows)", sub_heading))
    metric_rows = [
        [Paragraph("<b>Target Variable</b>", body_style), Paragraph("<b>Model Algorithm</b>", body_style), Paragraph("<b>MAE (Error)</b>", body_style), Paragraph("<b>RMSE</b>", body_style), Paragraph("<b>R2 Score (Acc)</b>", body_style)],
        [Paragraph("Process Time", body_style), Paragraph("Random Forest", body_style), Paragraph("68.49 min", body_style), Paragraph("151.50 min", body_style), Paragraph("<b>95.8% (0.9585)</b>", body_style)],
        [Paragraph("Process Time", body_style), Paragraph("Linear Regression", body_style), Paragraph("251.38 min", body_style), Paragraph("427.37 min", body_style), Paragraph("67.0% (0.6701)", body_style)],
        [Paragraph("Production Cost", body_style), Paragraph("Random Forest", body_style), Paragraph("Rs 852.33", body_style), Paragraph("Rs 2,364.78", body_style), Paragraph("<b>98.1% (0.9807)</b>", body_style)],
        [Paragraph("Production Cost", body_style), Paragraph("Linear Regression", body_style), Paragraph("Rs 7,446.00", body_style), Paragraph("Rs 12,798.82", body_style), Paragraph("43.5% (0.4348)", body_style)]
    ]
    m_table = Table(metric_rows, colWidths=[105, 115, 95, 95, 100])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 8))

    # PART 3: TOP 15 VIVA QUESTIONS
    story.append(Paragraph("PART 3: TOP 15 COLLEGE VIVA QUESTIONS & WINNING ANSWERS", section_heading))
    story.append(Paragraph("Examiner ke saamne bolne ke liye best crisp answers:", body_style))

    viva_list = [
        ("Q1: Aapke project ka main objective kya hai?",
         "Answer: Sir, hamare project ka objective laptop manufacturing aur assembly operations ke liye required process time (minutes) aur production cost (Rupees) ko accurately predict karna hai using Machine Learning."),

        ("Q2: Isme kitne models use huye hain?",
         "Answer: Sir, do separate regression models train kiye gaye hain: Model A predict karta hai Actual Time in Minutes, aur Model B predict karta hai Actual Cost in INR."),

        ("Q3: Regression aur Classification me kya difference hai?",
         "Answer: Classification me output discrete category ya label hota hai (jaise Yes/No ya Defective/Non-Defective). Regression me output continuous numeric value hoti hai (jaise yahan time aur cost numbers hain). Isliye humne regression use kiya."),

        ("Q4: Random Forest Regressor hi kyu choose kiya?",
         "Answer: Sir, factory parameters ke beech complex non-linear relationships hote hain. Linear Regression ka score sirf 67% time ke liye aur 43% cost ke liye aaya. Random Forest 100 decision trees ka ensemble banakar non-linear interactions ko capture karta hai, jisse hamara R2 score 95.8% aur 98.1% tak improve ho gaya."),

        ("Q5: Dataset me total kitne rows aur columns hain?",
         "Answer: Total 600 rows aur 13 columns hain. Isme 11 input features hain aur 2 target columns (Actual Time aur Actual Cost) hain."),

        ("Q6: 70/30 train-test split kyu kiya?",
         "Answer: Model ki real-world performance check karne ke liye. 70% data (420 rows) par model ko train kiya gaya, aur 30% data (180 rows) ko alag rakha gaya taaki unseen data par model test ho sake aur overfitting verify ho sake."),

        ("Q7: Data Leakage kya hota hai aur aapne kaise prevent kiya?",
         "Answer: Data leakage tab hota hai jab testing data ki information training phase me leak ho jaye. Humne train-test split preprocessing se pehle kiya, aur OneHotEncoder aur Scaler ko strictly training data par hi fit kiya."),

        ("Q8: R2 Score (R-squared) kya represent karta hai?",
         "Answer: R2 score (Coefficient of Determination) batata hai ki hamare features target variable ke kitne percent variance ko explain karte hain. Hamare model ka score 0.958 (Time) aur 0.980 (Cost) hai, matlab >95% accurate prediction hai."),

        ("Q9: MAE aur RMSE me kya difference hai?",
         "Answer: MAE (Mean Absolute Error) actual aur predicted ka direct average fark batata hai raw units me. RMSE (Root Mean Squared Error) errors ka square karke average nikaalta hai, isliye bade outliers ko zyada penalty deta hai."),

        ("Q10: Kya aapka model per-piece estimate deta hai ya total batch ka?",
         "Answer: Sir, dataset inspect karne par pata chala ki Time aur Cost batch quantity ke sath scale karte hain, isliye model total batch time aur cost predict karta hai. Unit rate nikalne ke liye batch output ko quantity se divide karte hain, jisse double-multiplication error nahi hota."),

        ("Q11: RAM aur SSD manufacturing me aate hain ya assembly me?",
         "Answer: Sir, Assembly me. Hum complex electronics jaise RAM, SSD aur Motherboard market se purchase karte hain. Unhe chassis me mount aur slot karne ko assembly operation kehte hain."),

        ("Q12: One-Hot Encoding kyu use ki?",
         "Answer: Machine learning models strings ya words nahi samajhte. Material aur Machine Type jaise categorical columns ko binary numeric columns (0 aur 1) me convert karne ke liye One-Hot Encoding use ki."),

        ("Q13: Agar user koi naya ya anjaan component daal de toh kya app crash hogi?",
         "Answer: Nahi sir, humne OneHotEncoder me handle_unknown='ignore' lagaya hai, jisse koi naya ya anjaan input aane par model bina crash huye safely 0 assign karke prediction deta hai."),

        ("Q14: Dataset real factory ka hai ya synthetic?",
         "Answer: Sir, laptop manufacturing companies ka internal data proprietary secret hota hai. Yeh dataset realistic manufacturing physics aur cost curves ko replicate karne ke liye synthetically simulate kiya gaya sample data hai."),

        ("Q15: Streamlit framework ka kya role hai?",
         "Answer: Streamlit ek modern Python library hai jisse machine learning models ke liye clean, interactive web frontend bina HTML ya CSS likhe direct Python se banaya ja sakta hai.")
    ]

    for q, a in viva_list:
        viva_block = []
        viva_block.append(Paragraph(q, viva_q_style))
        viva_block.append(Paragraph(a, viva_a_style))
        story.append(KeepTogether(viva_block))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_pdf()
