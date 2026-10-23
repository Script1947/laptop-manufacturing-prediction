"""
Generate the Ultimate, Perfectly Balanced Hinglish Project & Viva Guide PDF
Project: Machine Learning-Based Component-Wise Manufacturing Time and Cost Prediction for Laptops
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
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
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(50, 755, "Laptop Production Time & Cost Predictor  |  Complete Project & Viva Master Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(50, 748, 562, 748)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(562, 28, page_text)
        self.drawString(50, 28, "B.Tech CSE Mini-Project Master Reference (Complete Hinglish Guide)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(50, 38, 562, 38)
        self.restoreState()


def create_ultimate_pdf(filename="Laptop_Production_Complete_Project_Guide.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=48,
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
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    chapter_style = ParagraphStyle(
        'ChapterHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    sub_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=12.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3.5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=2
    )

    viva_q_style = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=1.5,
        keepWithNext=True
    )

    viva_a_style = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    story = []

    # Title & Banner
    story.append(Paragraph("Laptop Manufacturing Time & Cost Predictor", title_style))
    story.append(Paragraph("The Ultimate Master Guide: Zero-to-Advance Notes, 13 Columns Breakdown, Flow Diagram & 20 Viva Q&A (in Hinglish)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))

    # Executive Summary Table
    sum_data = [
        [Paragraph("<b>Project Domain:</b> Applied Machine Learning & Analytics", body_style), Paragraph("<b>Targets:</b> 2 (Actual Time in Min, Actual Cost in INR)", body_style)],
        [Paragraph("<b>Dataset Scale:</b> 600 Records, 13 Columns (100% Utilized)", body_style), Paragraph("<b>Train/Test Split:</b> 70% Train (420) / 30% Test (180)", body_style)],
        [Paragraph("<b>Primary Algorithm:</b> Random Forest Regressor (100 Trees)", body_style), Paragraph("<b>Accuracy (R2 Score):</b> 95.8% (Time) | 98.1% (Cost)", body_style)],
        [Paragraph("<b>Web Application:</b> Streamlit Interactive Dashboard", body_style), Paragraph("<b>Tech Stack:</b> Python 3.13, Scikit-Learn, Pandas, Joblib", body_style)]
    ]
    sum_table = Table(sum_data, colWidths=[256, 256])
    sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sum_table)
    story.append(Spacer(1, 4))

    # CHAPTER 1: PROJECT OVERVIEW
    story.append(Paragraph("CHAPTER 1: PROJECT OVERVIEW & REAL-WORLD PROBLEM", chapter_style))
    story.append(Paragraph(
        "<b>Project Ka Core Concept:</b> Jab koi electronics company laptop banane ki planning karti hai, toh unhe pehle se pata hona chahiye "
        "ki alag-alag components (jaise casing, display, RAM, cooling fan) ko banane ya assemble karne me <b>kitna machine cycle time lagega</b> "
        "aur <b>kitna total budget kharcha aayega</b>. Humne 600 historical batches ke data par do <b>Random Forest Regressor models</b> train kiye hain "
        "jo user dwara diye gaye inputs (component type, dimensions, quantity, machine, shift) ko dekhkar accurate time aur cost predict karte hain.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Manual Estimation vs ML:</b> Pehle industrial engineers manual rough thumb-rules use karte the jo aksar galat sabit hote the. "
        "Machine Learning se estimation automated ho gaya, human errors khatam huye, aur batch scaling bilkul realistic accurate ho gayi.",
        body_style
    ))

    # CHAPTER 2: THE 13 COLUMNS EXPLAINED
    story.append(Paragraph("CHAPTER 2: DATASET KE SAARE 13 COLUMNS KI DETAILED EXPLANATION", chapter_style))
    story.append(Paragraph(
        "Dataset me total 13 columns hain. <b>Humne ek bhi column drop ya waste nahi kiya hai — saare 13 columns model me actively use huye hain!</b>",
        body_style
    ))

    col_details = [
        [Paragraph("<b>Column Name</b>", body_style), Paragraph("<b>Role</b>", body_style), Paragraph("<b>Kya Kaam Karta Hai? (Simple Meaning)</b>", body_style)],
        [Paragraph("1. Component_Type", body_style), Paragraph("Feature", body_style), Paragraph("Kaunsa part hai (17 categories: Laptop Casing, RAM Installation, Motherboard, etc.).", body_style)],
        [Paragraph("2. Process_Type", body_style), Paragraph("Feature", body_style), Paragraph("Operation ka type: Manufacturing (factory me banana) ya Assembly (khareeda part lagana).", body_style)],
        [Paragraph("3. Material", body_style), Paragraph("Feature", body_style), Paragraph("Kis material ka bana hai (Plastic, Aluminum, Steel, Purchased Electronics). Cost ispe heavily depend karta hai.", body_style)],
        [Paragraph("4. Length_mm", body_style), Paragraph("Feature", body_style), Paragraph("Part ki physical length (18 mm se 345 mm tak).", body_style)],
        [Paragraph("5. Width_mm", body_style), Paragraph("Feature", body_style), Paragraph("Part ki physical width/chaudai (11 mm se 242 mm tak).", body_style)],
        [Paragraph("6. Height_mm", body_style), Paragraph("Feature", body_style), Paragraph("Part ki thickness/motai (1 mm se 23 mm tak).", body_style)],
        [Paragraph("7. Production_Quantity", body_style), Paragraph("Feature", body_style), Paragraph("Batch size: Kitne piece ek saath banaye ja rahe hain (1 se 200 units).", body_style)],
        [Paragraph("8. Manufacturing_Process", body_style), Paragraph("Feature", body_style), Paragraph("Kaunsi technique lag rahi hai: CNC Machining, Injection Molding, Stamping, Slot Insertion.", body_style)],
        [Paragraph("9. Complexity_Level", body_style), Paragraph("Feature", body_style), Paragraph("Design ka complexity factor (1.0 = Simple, 1.4 = Intricate/Tight tolerance).", body_style)],
        [Paragraph("10. Machine_Type", body_style), Paragraph("Feature", body_style), Paragraph("Kaunsi machine use ho rahi hai: CNC Machine, Assembly Workstation, Stamping Machine, etc.", body_style)],
        [Paragraph("11. Shift_Type", body_style), Paragraph("Feature", body_style), Paragraph("Day shift hai ya Night shift (Night shift me efficiency aur hourly rate vary karta hai).", body_style)],
        [Paragraph("12. Actual_Time_Minutes", body_style), Paragraph("<b>Target 1</b>", body_style), Paragraph("<b>Model A isko predict karta hai:</b> Batch ko complete karne me kitne minutes lagenge.", body_style)],
        [Paragraph("13. Actual_Cost_INR", body_style), Paragraph("<b>Target 2</b>", body_style), Paragraph("<b>Model B isko predict karta hai:</b> Batch ka total kharcha kitna aayega (Rupees me).", body_style)]
    ]
    col_table = Table(col_details, colWidths=[120, 55, 337])
    col_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(col_table)
    story.append(Spacer(1, 5))

    # CHAPTER 3: MANUFACTURING VS ASSEMBLY
    story.append(Paragraph("CHAPTER 3: MANUFACTURING VS ASSEMBLY (THE #1 EXAMINER QUESTION)", chapter_style))
    story.append(Paragraph(
        "Examiner aapko trap karne ke liye puchega: <i>'Kya aapki factory RAM aur Motherboard manufacture karti hai?'</i><br/>"
        "<b>Aapka Answer:</b> <i>'Nahi sir! Semiconductor chips aur silicon boards specialized fabrication facilities me bante hain. "
        "Hamari factory me do alag operations hote hain:'</i>", body_style
    ))
    story.append(Paragraph("<b>1. Manufacturing Components (Fabrication):</b> Raw materials (Aluminum ingots, Plastic pellets, Steel sheets) ko machine me daalkar shape diya jata hai. Jaise: Laptop Casing (CNC cutting ya molding), Hinges (metal stamping), Heat Sink (extrusion & cutting).", bullet_style))
    story.append(Paragraph("<b>2. Assembly Operations (Integration):</b> Market se purchase kiye huye finished electronic components ko chassis me screw karna, slot me fit karna, connect karna aur test karna. Jaise: RAM slotting, SSD mounting, Motherboard screwing, Battery connection, Thermal paste lagana.", bullet_style))

    # CHAPTER 4: SYSTEM FLOW DIAGRAM
    story.append(Paragraph("CHAPTER 4: COMPLETE SYSTEM ARCHITECTURE & FLOW DIAGRAM", chapter_style))
    story.append(Paragraph("Data factory dataset se lekar final Streamlit web prediction tak kaise process hota hai:", body_style))

    arch_flow = [
        [Paragraph("<b>STEP 1: CSV DATASET (600 ROWS, 13 COLUMNS)</b><br/>Primary data source containing historical production batch records across 17 laptop components.", body_style)],
        [Paragraph("<b>STEP 2: DATA HYGIENE & SANITY VALIDATION</b><br/>Verified 0 missing/null values, 0 duplicate records. Validated that all dimensions (L, W, H) and quantities are strictly > 0.", body_style)],
        [Paragraph("<b>STEP 3: 70/30 TRAIN-TEST SPLIT (RANDOM_STATE = 42)</b><br/>Separated into 420 Training Rows (70%) strictly for learning, and 180 Held-Out Testing Rows (30%) strictly for unbiased evaluation.", body_style)],
        [Paragraph("<b>STEP 4: COLUMNTRANSFORMER PREPROCESSING PIPELINE</b><br/>• OneHotEncoder (handle_unknown='ignore') transforms categorical text columns into binary vectors.<br/>• StandardScaler scales physical dimensions and quantities to standard normal distribution.", body_style)],
        [Paragraph("<b>STEP 5: DUAL RANDOM FOREST REGRESSION PIPELINES</b><br/>• Model A: RandomForestRegressor(n_estimators=100) -> Fits and predicts Actual_Time_Minutes.<br/>• Model B: RandomForestRegressor(n_estimators=100) -> Fits and predicts Actual_Cost_INR.", body_style)],
        [Paragraph("<b>STEP 6: TESTING & BENCHMARK VALIDATION (180 UNSEEN ROWS)</b><br/>Calculated MAE, RMSE, and R2 scores on test set. Compared against Linear Regression baseline to prove superiority.", body_style)],
        [Paragraph("<b>STEP 7: SERIALIZATION & PERSISTENCE (.PKL ARTIFACTS)</b><br/>Exported time_model.pkl and cost_model.pkl so the application doesn't retrain models on every page refresh.", body_style)],
        [Paragraph("<b>STEP 8: STREAMLIT INTERACTIVE WEB APPLICATION (app.py)</b><br/>User inputs component parameters -> Model predicts Total Batch Time, Total Cost, Unit Time, and Unit Cost instantly.", body_style)]
    ]
    arch_table = Table(arch_flow, colWidths=[510])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 5))

    # CHAPTER 5: MACHINE LEARNING & BENCHMARKS
    story.append(Paragraph("CHAPTER 5: MACHINE LEARNING ALGORITHMS & BENCHMARK RESULTS", chapter_style))
    story.append(Paragraph(
        "<b>Random Forest vs Linear Regression:</b> Humne dono models ko exact same 70/30 split par compare kiya. "
        "Manufacturing physics me material, complexity aur volume ke beech non-linear relationships hote hain (jaise CNC machine par Aluminum kaatna plastic molding se 10 guna zyada time leta hai). "
        "Linear Regression seedhi line maanta hai isliye fail ho gaya (R2 sirf 67% time aur 43% cost). "
        "<b>Random Forest 100 Decision Trees ka group (ensemble) banata hai</b>. Har tree alag subset par seekhta hai aur sabhi trees ka average nikaal kar final prediction deta hai. "
        "Isse error drastically kam ho gaya aur accuracy 95.8% aur 98.1% pahunch gayi!",
        body_style
    ))

    score_data = [
        [Paragraph("<b>Target Variable</b>", body_style), Paragraph("<b>Algorithm</b>", body_style), Paragraph("<b>MAE (Error)</b>", body_style), Paragraph("<b>RMSE</b>", body_style), Paragraph("<b>R2 Score (Variance)</b>", body_style)],
        [Paragraph("Batch Time (Minutes)", body_style), Paragraph("<b>Random Forest</b>", body_style), Paragraph("<b>68.49 min</b>", body_style), Paragraph("151.50 min", body_style), Paragraph("<b>0.9585 (95.8%)</b>", body_style)],
        [Paragraph("Batch Time (Minutes)", body_style), Paragraph("Linear Regression", body_style), Paragraph("251.38 min", body_style), Paragraph("427.37 min", body_style), Paragraph("0.6701 (67.0%)", body_style)],
        [Paragraph("Batch Cost (INR Rupees)", body_style), Paragraph("<b>Random Forest</b>", body_style), Paragraph("<b>Rs 852.33</b>", body_style), Paragraph("Rs 2,364.78", body_style), Paragraph("<b>0.9807 (98.1%)</b>", body_style)],
        [Paragraph("Batch Cost (INR Rupees)", body_style), Paragraph("Linear Regression", body_style), Paragraph("Rs 7,446.00", body_style), Paragraph("Rs 12,798.82", body_style), Paragraph("0.4348 (43.5%)", body_style)]
    ]
    score_table = Table(score_data, colWidths=[110, 110, 95, 95, 100])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 5))

    # CHAPTER 6: METRICS EXPLAINED
    story.append(Paragraph("CHAPTER 6: EVALUATION METRICS EXPLAINED (WHY NOT ACCURACY %?)", chapter_style))
    story.append(Paragraph(
        "Examiner puchega: <i>'Aapne classification accuracy % kyu nahi nikala?'</i><br/>"
        "<b>Answer:</b> Classification me discrete categories hoti hain (Cat vs Dog ya Pass vs Fail), jahan exact match par accuracy % nikalta hai. "
        "Lekin <b>Regression me continuous numbers</b> (e.g. 125.43 minutes ya Rs 14,250.80) predict hote hain, jahan exact decimal match mathematically impossible hota hai. "
        "Isliye regression me 3 standard metrics use hote hain:", body_style
    ))
    story.append(Paragraph("<b>1. MAE (Mean Absolute Error):</b> Actual aur predicted ka direct average difference raw units me. (Hamare model ka time MAE sirf 68 minutes hai 200 pieces ke batch par).", bullet_style))
    story.append(Paragraph("<b>2. RMSE (Root Mean Squared Error):</b> Differences ka square karke average nikaalta hai aur square root leta hai. Yeh bade outlier errors ko heavily penalize karta hai.", bullet_style))
    story.append(Paragraph("<b>3. R2 Score (Coefficient of Determination):</b> Batata hai ki model ne target ke kitne percent variance ko capture kiya. Hamara R2 score 0.958 (Time) aur 0.980 (Cost) hai, jo prove karta hai ki model >95% accurate hai.", bullet_style))

    # CHAPTER 7: TOP 20 VIVA QUESTIONS
    story.append(Paragraph("CHAPTER 7: TOP 20 COLLEGE VIVA QUESTIONS & WINNING ANSWERS", chapter_style))
    story.append(Paragraph("Examiner ke har potential sawal ka perfect, confident Hinglish answer:", body_style))

    viva_20 = [
        ("Q1: Aapke project ka title aur main objective kya hai?",
         "Answer: Sir, hamara project title hai 'Machine Learning-Based Component-Wise Manufacturing Time and Cost Prediction for Laptops'. Iska objective laptop ke components ke liye process time aur production cost ko accurately predict karna hai using Random Forest regression."),

        ("Q2: Is project me total kitne machine learning models train kiye gaye hain?",
         "Answer: Sir, 2 separate regression models train kiye gaye hain: Model A predict karta hai 'Actual_Time_Minutes' aur Model B predict karta hai 'Actual_Cost_INR'."),

        ("Q3: Regression aur Classification me fundamental difference kya hai?",
         "Answer: Classification discrete labels ya categories predict karta hai (jaise Defective vs Non-Defective). Regression continuous numerical values predict karta hai (jaise time minutes me aur cost rupees me). Hamare dono targets continuous numbers hain, isliye humne regression use kiya."),

        ("Q4: Random Forest Regressor hi kyu chuna, Linear Regression kyu nahi?",
         "Answer: Sir, industrial manufacturing me parameters ke beech complex non-linear interactions hote hain. Linear Regression ka score sirf 67% (Time) aur 43% (Cost) aaya. Random Forest 100 decision trees ka ensemble banakar non-linear relationships ko accurately capture karta hai, jisse hamara R2 score 95.8% aur 98.1% ho gaya."),

        ("Q5: Dataset me total kitne rows aur columns hain?",
         "Answer: Dataset me exactly 600 rows aur 13 columns hain. Isme 11 input features hain aur 2 target variables hain."),

        ("Q6: Kya humne dataset ka koi column drop ya remove kiya hai?",
         "Answer: Bilkul nahi sir! Humne saare 13 columns 100% actively use kiye hain. 11 columns input features ke roop me preprocessor me jaate hain aur 2 columns targets hain."),

        ("Q7: Manufacturing components aur Assembly operations me kya antar hai?",
         "Answer: Manufacturing me raw materials (Plastic, Aluminum, Steel) ko factory me shape dekar component banate hain (jaise Casing, Hinges, Heat Sink). Assembly me pre-purchased electronics ko chassis me mount aur install karte hain (jaise RAM, SSD, Motherboard). Hum electronics manufacture nahi karte, unhe assemble karte hain."),

        ("Q8: 70/30 train-test split kyu use kiya gaya hai?",
         "Answer: Model ki generalization ability test karne ke liye. 70% data (420 rows) par model ko train kiya gaya, aur 30% data (180 rows) ko alag rakha gaya taaki unseen data par model test ho sake aur hum overfitting check kar sakein."),

        ("Q9: What is Data Leakage aur aapne ise kaise prevent kiya?",
         "Answer: Data leakage tab hota hai jab testing data ki information training phase me leak ho jaye, jisse fake high accuracy aati hai. Humne train-test split preprocessing se pehle kiya, aur ColumnTransformer (OneHotEncoder aur Scaler) ko strictly training data par hi fit kiya."),

        ("Q10: Overfitting kya hoti hai aur Random Forest ise kaise rokte hai?",
         "Answer: Overfitting ka matlab hai ki model training data ko blindly memorize kar leta hai aur naye data par fail ho jata hai. Random Forest bagging (bootstrap aggregating) aur feature randomness use karta hai, jisme 100 alag-alag trees ka average liya jata hai, jisse overfitting prevent hoti hai."),

        ("Q11: R2 Score (Coefficient of Determination) ka kya significance hai?",
         "Answer: R2 score batata hai ki hamare features target variable ke kitne percent variance ko explain karte hain. Hamare model ka score 0.9585 (Time) aur 0.9807 (Cost) hai, matlab >95% prediction accuracy hai."),

        ("Q12: MAE aur RMSE me difference kya hai?",
         "Answer: MAE (Mean Absolute Error) actual aur predicted ka direct average fark batata hai raw units me. RMSE (Root Mean Squared Error) errors ka square karke average nikaalta hai, isliye bade outliers ko zyada penalty deta hai."),

        ("Q13: Kya aapka model per-piece estimate deta hai ya total batch ka?",
         "Answer: Sir, dataset inspect karne par pata chala ki Time aur Cost batch quantity ke sath scale karte hain, isliye model total batch time aur cost predict karta hai. Unit rate nikalne ke liye batch output ko quantity se divide karte hain, jisse double-multiplication error nahi hota."),

        ("Q14: One-Hot Encoding kyu zaroori thi?",
         "Answer: Machine learning algorithms text strings nahi samajhte. Material, Machine Type aur Shift Type jaise categorical columns ko binary numeric columns (0 aur 1) me convert karne ke liye One-Hot Encoding use ki."),

        ("Q15: OneHotEncoder me handle_unknown='ignore' kyu lagaya?",
         "Answer: Agar future me user koi aisi category select kare jo training data me nahi thi, toh model crash hone ke bajaye safely use zero vector assign karke prediction continue karta hai."),

        ("Q16: StandardScaler ka kya role hai?",
         "Answer: Length, Width, Height aur Production Quantity ke numerical scales alag-alag hote hain (e.g. Quantity 100 hai aur Height 3mm). StandardScaler sabhi numerical features ko zero mean aur unit variance me normalize karta hai."),

        ("Q17: Is project ka dataset real factory ka hai ya synthetic?",
         "Answer: Sir, real industrial manufacturing data proprietary commercial secret hota hai. Yeh dataset realistic shop-floor physics aur non-linear cost curves ko replicate karne ke liye synthetically simulate kiya gaya sample data hai."),

        ("Q18: Models ko .pkl format me save kyu kiya gaya?",
         "Answer: Joblib library use karke trained model pipelines ko disk par serialize (.pkl) kar diya gaya taaki Streamlit web app unhe turant load karke fast prediction de sake bina baar-baar retrain kiye."),

        ("Q19: Multi-Component BOM Estimator kaise kaam karta hai?",
         "Answer: User poore laptop ke multiple components (Casing, RAM, Display, Battery, etc.) select karta hai aur batch quantity dalta hai. System har component ke liye model se batch time aur cost nikaal kar poore laptop project ka cumulative time aur expenditure calculate karta hai."),

        ("Q20: Is project ki limitations aur future scope kya hai?",
         "Answer: Limitations: Real shop-floor par electricity tariff aur tool wear-tear dynamically fluctuate hota hai jo dataset me nahi hai. Future Scope: Factory ke live IoT sensors aur PLC telemetry data ko connect karke real-time dynamic line balancing aur defect cost prediction implement karna.")
    ]

    for q, a in viva_20:
        block = []
        block.append(Paragraph(q, viva_q_style))
        block.append(Paragraph(a, viva_a_style))
        story.append(KeepTogether(block))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master PDF generated successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_ultimate_pdf()
