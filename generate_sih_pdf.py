from __future__ import annotations

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path("TrustArc_SIH26_Presentation_Script_QA.pdf")

# -----------------------------------------------------------------------------
# Typography and palette
# -----------------------------------------------------------------------------
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BODY_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"
SERIF_FONT = "Times-Roman"
SERIF_BOLD = "Times-Bold"
MONO_FONT = "Courier"

try:
    if (FONT_DIR / "DejaVuSans.ttf").exists():
        pdfmetrics.registerFont(TTFont("DejaVuSans", str(FONT_DIR / "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVuSerif", str(FONT_DIR / "DejaVuSerif.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", str(FONT_DIR / "DejaVuSerif-Bold.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVuSansMono", str(FONT_DIR / "DejaVuSansMono.ttf")))
        BODY_FONT = "DejaVuSans"
        BOLD_FONT = "DejaVuSans-Bold"
        SERIF_FONT = "DejaVuSerif"
        SERIF_BOLD = "DejaVuSerif-Bold"
        MONO_FONT = "DejaVuSansMono"
except Exception:
    pass

MAROON = HexColor("#7F1720")
RED = HexColor("#C51F2C")
DARK = HexColor("#202124")
MID = HexColor("#5E6267")
CREAM = HexColor("#F8F0E7")
PALE_RED = HexColor("#FBEAEC")
PALE_BLUE = HexColor("#EAF5F7")
PALE_GREEN = HexColor("#EAF6EF")
PALE_YELLOW = HexColor("#FFF7DD")
PALE_GREY = HexColor("#F4F5F6")
GOLD = HexColor("#D4A85A")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName=SERIF_BOLD,
    fontSize=29, leading=35, textColor=MAROON, alignment=TA_CENTER,
    spaceAfter=8 * mm,
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontName=BODY_FONT,
    fontSize=13, leading=19, textColor=DARK, alignment=TA_CENTER,
    spaceAfter=5 * mm,
))
styles.add(ParagraphStyle(
    name="H1Custom", parent=styles["Heading1"], fontName=SERIF_BOLD,
    fontSize=21, leading=26, textColor=MAROON, spaceBefore=2 * mm,
    spaceAfter=5 * mm, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H2Custom", parent=styles["Heading2"], fontName=BOLD_FONT,
    fontSize=14.3, leading=18, textColor=RED, spaceBefore=4 * mm,
    spaceAfter=2.5 * mm, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H3Custom", parent=styles["Heading3"], fontName=BOLD_FONT,
    fontSize=11.5, leading=15, textColor=MAROON, spaceBefore=3 * mm,
    spaceAfter=1.8 * mm, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=9.5, leading=14.2, textColor=DARK, spaceAfter=2.4 * mm,
))
styles.add(ParagraphStyle(
    name="BodySmall", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=8.3, leading=11.6, textColor=DARK, spaceAfter=1.4 * mm,
))
styles.add(ParagraphStyle(
    name="ScriptBody", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=10.4, leading=16.1, textColor=DARK, spaceAfter=3.2 * mm,
))
styles.add(ParagraphStyle(
    name="Question", parent=styles["BodyText"], fontName=BOLD_FONT,
    fontSize=10.1, leading=14.2, textColor=MAROON, spaceBefore=2.4 * mm,
    spaceAfter=1.2 * mm, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Answer", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=9.2, leading=13.6, textColor=DARK, leftIndent=3 * mm,
    borderColor=HexColor("#D8C6B0"), borderWidth=0.5, borderPadding=5,
    backColor=HexColor("#FFFCF8"), spaceAfter=2.6 * mm,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontName=BOLD_FONT,
    fontSize=9.4, leading=14, textColor=MAROON, borderColor=GOLD,
    borderWidth=0.8, borderPadding=7, backColor=CREAM, spaceBefore=2 * mm,
    spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="Warn", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=9.1, leading=13.5, textColor=DARK, borderColor=RED,
    borderWidth=0.9, borderPadding=7, backColor=PALE_RED,
    spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["BodyText"], fontName=BOLD_FONT,
    fontSize=8.2, leading=10.5, textColor=WHITE, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=7.5, leading=10.1, textColor=DARK,
))
styles.add(ParagraphStyle(
    name="TableCellSmall", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=6.9, leading=9.2, textColor=DARK,
))
styles.add(ParagraphStyle(
    name="Reference", parent=styles["BodyText"], fontName=BODY_FONT,
    fontSize=7.4, leading=10.2, textColor=DARK, spaceAfter=1.6 * mm,
))
styles.add(ParagraphStyle(
    name="Code", parent=styles["Code"], fontName=MONO_FONT,
    fontSize=7.2, leading=10.0, textColor=DARK, leftIndent=4 * mm,
    rightIndent=4 * mm, borderColor=HexColor("#C9CDD1"), borderWidth=0.5,
    borderPadding=6, backColor=PALE_GREY, spaceBefore=2 * mm,
    spaceAfter=3 * mm,
))


def plain(text: str, style_name: str = "BodyCustom") -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), styles[style_name])


def rich(text: str, style_name: str = "BodyCustom") -> Paragraph:
    return Paragraph(text, styles[style_name])


def bullet_list(items: list[str], style_name: str = "BodyCustom", level: int = 0) -> ListFlowable:
    return ListFlowable(
        [ListItem(plain(item, style_name), leftIndent=3 * mm) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=(7 + level * 4) * mm,
        bulletFontName=BODY_FONT,
        bulletFontSize=7,
        spaceAfter=2 * mm,
    )


def cell(text: str, small: bool = False, head: bool = False) -> Paragraph:
    if head:
        return Paragraph(escape(text), styles["TableHead"])
    return Paragraph(escape(text).replace("\n", "<br/>"), styles["TableCellSmall" if small else "TableCell"])


# -----------------------------------------------------------------------------
# Page decoration
# -----------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
LEFT = 17 * mm
RIGHT = 17 * mm
TOP = 21 * mm
BOTTOM = 17 * mm


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(RED)
    canvas.rect(0, 0, 9 * mm, PAGE_H, stroke=0, fill=1)
    canvas.rect(0, 0, PAGE_W, 8 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.1)
    canvas.roundRect(17 * mm, 17 * mm, PAGE_W - 34 * mm, PAGE_H - 34 * mm, 4 * mm, stroke=1, fill=0)
    canvas.restoreState()


def normal_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(RED)
    canvas.rect(0, 0, 5.5 * mm, PAGE_H, stroke=0, fill=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.55)
    canvas.line(LEFT, PAGE_H - 12 * mm, PAGE_W - RIGHT, PAGE_H - 12 * mm)
    canvas.setFont(BODY_FONT, 7.2)
    canvas.setFillColor(MID)
    canvas.drawString(LEFT, PAGE_H - 9.2 * mm, "Swasthya Setu | TrustArc | SIH26_10")
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 9.2 * mm, "Presentation Script and Technical Q&A")
    canvas.setStrokeColor(HexColor("#E0D7CC"))
    canvas.line(LEFT, 11 * mm, PAGE_W - RIGHT, 11 * mm)
    canvas.setFont(BODY_FONT, 7.2)
    canvas.setFillColor(MID)
    canvas.drawString(LEFT, 7.5 * mm, "Prepared for SIH evaluation | 23 August 2026")
    canvas.drawRightString(PAGE_W - RIGHT, 7.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4,
    leftMargin=LEFT, rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM,
    title="Swasthya Setu - 10-Minute Presentation Script and Technical Q&A",
    author="Team TrustArc",
    subject="Smart India Hackathon evaluation preparation",
)
frame = Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT, PAGE_H - TOP - BOTTOM, id="normal")
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=frame, onPage=cover_page),
    PageTemplate(id="Body", frames=frame, onPage=normal_page),
])

story = []

# -----------------------------------------------------------------------------
# Cover
# -----------------------------------------------------------------------------
story.append(Spacer(1, 44 * mm))
story.append(Paragraph("Swasthya Setu", styles["CoverTitle"]))
story.append(Paragraph("10-Minute Presentation Script<br/>&amp; Technical Evaluation Q&amp;A", styles["CoverSub"]))
story.append(Spacer(1, 9 * mm))
cover_info = [
    [cell("Team", head=True), cell("TrustArc")],
    [cell("Team ID", head=True), cell("SIH26_10")],
    [cell("Domain", head=True), cell("Healthcare, Biomedical & Life Sciences")],
    [cell("Edition", head=True), cell("Hardware + Software")],
    [cell("Prepared for", head=True), cell("Online SIH evaluation round")],
    [cell("Date", head=True), cell("23 August 2026")],
]
cover_table = Table(cover_info, colWidths=[38 * mm, 92 * mm], hAlign="CENTER")
cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), MAROON),
    ("BACKGROUND", (1, 0), (1, -1), CREAM),
    ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, HexColor("#DFCDB7")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(cover_table)
story.append(Spacer(1, 14 * mm))
story.append(Paragraph(
    "Ensuring safe, traceable and accessible vaccination through real-time cold-chain monitoring, blockchain-backed accountability and multilingual digital support.",
    styles["Callout"],
))
story.append(PageBreak())
doc.handle_nextPageTemplate("Body")

# -----------------------------------------------------------------------------
# Contents and truth boundaries
# -----------------------------------------------------------------------------
story.append(Paragraph("How to Use This Document", styles["H1Custom"]))
story.append(plain(
    "The Verbatim Presentation Script is written as spoken text only. It contains no pause instructions, slide cues, timing labels or presenter directions. Read it word for word for an approximately eight-to-ten-minute delivery, depending on speaking speed. The remaining pages are a reference bank for evaluator questions; they are not part of the spoken script unless a question is asked."
))
contents_rows = [
    [cell("Section", head=True), cell("Purpose", head=True)],
    [cell("Verify Before Evaluation"), cell("Statements that must be checked against the actual code, wallet, logs and prototype before presenting.")],
    [cell("Verbatim Presentation Script"), cell("End-to-end narrative aligned to the final twelve-page deck.")],
    [cell("Technical Q&A"), cell("Blockchain, IoT, app, multilingual AI, backend, privacy, scaling, cost, pilot and tough-question answers.")],
    [cell("Rapid Numbers Sheet"), cell("High-value figures and formulas for quick reference during online Q&A.")],
    [cell("References"), cell("Deck sources and external technical sources used for the preparation document.")],
]
t = Table(contents_rows, colWidths=[52 * mm, 116 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#DCCDBD")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Verify Before Evaluation", styles["H1Custom"]))
story.append(Paragraph(
    "These points are essential because the submitted PDF confirms the architecture and technology categories, but it does not contain the source code, deployed contract address, ABI, wallet history, measured pilot logs or supplier quotations.",
    styles["Warn"],
))
verify_items = [
    "Confirm the exact deployed Sepolia contract address, deployment transaction, ABI and the wallet that signs demo events. The deck confirms Solidity, Hardhat, Sepolia and MetaMask, but it does not identify the deployed contract artifact.",
    "Confirm the exact Sepolia faucet from the wallet or team history. Do not name a faucet from memory. The safe spoken wording is: a public Sepolia faucet supplied test ETH.",
    "Confirm whether the current code hashes canonical JSON, ABI-encoded fields or another representation. The recommended design in this document uses deterministic fields and Keccak-256, but that is not recoverable from the deck alone.",
    "Correct the hardware label NEP-6M to NEO-6M if that is the actual GPS module.",
    "The BMP280 measures barometric pressure and temperature; it does not measure humidity. If the project claims humidity, confirm that the actual board is a BME280 or another humidity sensor. Otherwise say environmental pressure, not humidity.",
    "The demo page lists a Light Anomaly, but the submitted production bill of materials does not show a light sensor. Describe it as a demonstrated anomaly input only if a temporary LDR or light sensor was actually connected.",
    "A passive vaccine carrier maintains its thermal environment through insulation and coolant packs. Do not describe the present design as an active refrigerator unless an active cooling mechanism has been built and tested.",
    "Do not say that blockchain proves a sensor reading is true. Calibration, sensor redundancy and secure device identity establish measurement confidence; blockchain protects the evidence from later alteration.",
    "Do not let the QR screen independently certify medical safety. Use condition-history compliant, excursion detected, quarantine pending authorized review, released, rejected, incomplete record or cryptographic verification failed.",
    "Treat sensor accuracy, alert latency, false-alert rate, battery runtime, detection recall and QR time as proposed pilot acceptance criteria until measured logs are available.",
    "Aadhaar is a simulation in the current prototype. Any production identity integration requires approved APIs, consent, security review and compliance.",
    "Present the current anomaly engine as transparent threshold and rule logic. Present machine learning as a later phase after labelled operational data exists.",
]
story.append(bullet_list(verify_items, "BodySmall"))
story.append(Paragraph(
    "Best practice for tomorrow: keep a browser tab ready with the Sepolia transaction, contract address, GitHub commit, latest sensor log, one QR verification record and one measured battery run. These artifacts answer more convincingly than a verbal estimate.",
    styles["Callout"],
))
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Verbatim presentation script
# -----------------------------------------------------------------------------
story.append(Paragraph("Verbatim Presentation Script", styles["H1Custom"]))
story.append(Paragraph(
    "The following text is the complete spoken script. It intentionally contains no internal instructions or slide-navigation wording.",
    styles["Callout"],
))

script_paragraphs = [
    "Good morning respected evaluators. We are Team TrustArc, and our solution is Swasthya Setu. It is a hardware-plus-software ecosystem designed to ensure safe, traceable and accessible vaccination through real-time cold-chain monitoring, blockchain-backed accountability and multilingual digital support.",

    "India's Universal Immunization Programme annually serves approximately 2.6 crore infants and 2.9 crore pregnant women. At this scale, a vaccine journey is not a single transfer. It moves from the manufacturer, through transport handoffs, distributors and cold storage, and finally to the vaccination centre. Across this journey, we identified three connected gaps.",

    "The first is the Integrity Gap. Temperature excursions, tampering, route deviations and incomplete custody records can occur, while storage conditions are not continuously visible. If integrity is compromised, a vial may still reach the point of use, but the failure point is difficult to identify across multiple stakeholders.",

    "The second is the Access Gap. Language, digital-literacy and navigation barriers make vaccination services harder to discover and use, especially where a citizen needs support to find a centre, understand availability or complete an appointment flow.",

    "The third is the Intelligence Gap. Logistics, demand, inventory and regional health data remain separated, so planning stays reactive instead of becoming preventive.",

    "We then studied the current ecosystem. U-WIN has strengthened registration and immunization records. eVIN improves inventory and temperature visibility. WHO guidance defines good temperature-monitoring practices. Research systems such as ColdNet and VacLedger demonstrate IoT logistics and blockchain traceability. These are valuable foundations, and our approach is not to discard them. The remaining implementation gap is that no single workflow combines real-time cold-chain sensing, tamper-evident event history and point-of-care or citizen-facing verification. Swasthya Setu is designed to build on the current ecosystem by connecting those pieces.",

    "Our proposed idea has three parts.",

    "The first is the integrity solution, Swasthya Trace. A smart IoT cold-chain monitor captures temperature, environmental data, location and lid or tamper events. The device generates instant alerts when a threshold, route or custody condition is violated. Every critical incident is connected to a shipment and a QR identity, so the physical vaccine and its digital history remain linked.",

    "The second is the access solution, Swasthya Connect. This is a voice-first multilingual citizen application. It supports centre discovery through Mappls, navigation, appointment booking, reminders and digital assistance. A citizen or healthcare worker can scan a QR code to view the verified condition history of a shipment rather than relying only on a verbal assurance. Aadhaar in the present prototype is a simulation, and any production identity integration would follow consent and approved government APIs.",

    "The third is the intelligence solution, Swasthya Insight. It unifies logistics, inventory, demand and health data for operational dashboards. Initially, the system uses clear threshold-based rules for anomaly detection. As labelled pilot data grows, AI and machine-learning models can support demand forecasting, wastage-risk estimation and earlier interventions. This keeps the current MVP focused, while preserving a credible path toward predictive planning.",

    "The key question is: why do we need blockchain when databases and data loggers already exist?",

    "Our research shows that the problem is not only a temperature excursion. It is also stakeholder-controlled evidence. In one Indian cold-chain study, vaccines were below zero degrees for 14.8 percent of monitored time and above eight degrees for 6.6 percent, while routine monitoring failed to capture those deviations. A post-eVIN assessment in Nainital reported that manual records did not match data-logger readings. An HHS OIG audit found inappropriate temperatures among 76 percent of selected providers and documentation gaps. In the Changchun case, records were fabricated and evidence was destroyed.",

    "Across a chain involving the manufacturer, transporter, distributor, cold store and vaccination centre, each stakeholder normally controls its own local record. That can create fragmented evidence, editable logs, accountability blind spots, delayed reporting and the risk of selective disclosure. A central database can be secure, but every external stakeholder still has to trust the organization that controls its administration.",

    "Therefore, we use blockchain selectively, not as a replacement for MongoDB and not for every sensor reading. Raw, high-frequency telemetry remains encrypted off-chain. When the anomaly engine detects an event, the backend creates a deterministic incident payload containing the shipment ID, device ID, anomaly type, timestamps, measured values, location, custody stage and sequence number. Ethers.js generates an Ethereum-compatible Keccak-256 hash of that payload. An authorized signer submits the hash and minimal event metadata to a Solidity smart contract, which acts as an append-only incident registry. Our prototype uses Hardhat for development, MetaMask for signing and the Sepolia testnet, funded with test ETH from a public Sepolia faucet. During QR verification, the application retrieves the off-chain history, recomputes the hash and compares it with the blockchain event. If someone changes the record later, the hashes no longer match.",

    "This gives us tamper evidence and non-repudiation across organizations, while keeping private citizen and medical data off-chain. Blockchain does not prove that a sensor is accurate; calibration and secure device identity solve that. Blockchain proves whether the captured evidence has been altered after it was anchored.",

    "Technically, the citizen application is built in Flutter with voice and multilingual support through Sarvam AI, with AI4Bharat components such as IndicTrans2 and IndicWav2Vec available as open-source fallbacks. Mappls supports centre discovery and navigation. Node.js, Express and MongoDB provide the shared backend and telemetry services. The doctor dashboard uses React and Vite for appointment queues, inventory tracking, shipment visibility, alerts and QR vial inspection.",

    "At the edge, the current prototype uses an ESP32, one DS18B20 temperature probe, a BMP280 pressure and environmental sensor, a NEO-6M GPS module, a reed switch, microSD local logging, a SIM800L communication module and an 18650 battery with TP4056 power management. This bench prototype validates sensing, local storage, telemetry ingestion, anomaly generation, cellular alerting and blockchain event logging.",

    "Our innovation is the end-to-end connection between hardware, software and verifiable trust. The hardware generates physical-world evidence. The software turns that evidence into alerts, dashboards, QR status and citizen support. The blockchain layer protects critical provenance. This creates a workflow from physical material, to intelligent detection, to digital record, to point-of-care verification and stakeholder action.",

    "For production, we do not simply place the same loose circuit inside a larger box. We move from a single probe to a calibrated multi-point array, from loose wiring to a sealed external electronics pod, from basic SD logs to encrypted append-only store-and-forward storage, from only a reed switch to a lid sensor and tamper-evident seal, and from the prototype GPS to low-power GNSS with route and geofence checks. The proposed production carrier is a passive freeze-preventive vaccine carrier with coolant packs and an insulating barrier. Our initial architecture uses three internal probes for the upper, centre and lower regions, plus an external ambient probe, with final positions decided through thermal mapping. A shock accelerometer, secure electronics pod, QR identity and communication module complete the field-deployable design. The carrier maintains the thermal environment; the IoT and blockchain layers verify the condition history and custody integrity.",

    "The solution is feasible in phases. Phase one is laboratory validation of sensor accuracy, connectivity and data security. Phase two is a controlled pilot with alert and workflow testing. Phase three is deployment at a vaccination centre, including staff training and field monitoring. Phase four is district-level scale-up and integration with health systems. Our pilot KPIs include alert latency, telemetry success rate, QR verification time, battery runtime, cost per monitored box and anomaly-detection performance. Connectivity loss is handled through local buffering, sensor drift through calibration, blockchain cost through event-only anchoring, and physical tampering through tamper alerts.",

    "The expected impact is safer vaccine-integrity decisions, faster anomaly detection and response, improved traceability and accountability, and better rural access and trust. Our three demonstrations show geofencing anomaly detection, AI-assisted speech-to-text form filling and anomaly alert generation.",

    "Finally, our six-member team covers blockchain and system architecture, Flutter and citizen experience, backend and APIs, IoT hardware and firmware, the doctor dashboard and QR verification, and multilingual AI, analytics and testing. Swasthya Setu is therefore not a standalone sensor and not blockchain for its own sake. It is an accountable vaccination ecosystem that builds on existing systems and connects real-time evidence, accessible services and data-driven action. Thank you.",
]

for paragraph in script_paragraphs:
    story.append(plain(paragraph, "ScriptBody"))

story.append(PageBreak())

# -----------------------------------------------------------------------------
# Architecture cheat sheet
# -----------------------------------------------------------------------------
story.append(Paragraph("System at a Glance", styles["H1Custom"]))
story.append(plain(
    "Use this page to keep every team member aligned on the same end-to-end explanation. It separates what happens at the edge, what stays off-chain and what is anchored for verification."
))
flow_rows = [
    [cell("Layer", head=True), cell("Primary responsibility", head=True), cell("Key technologies / records", head=True)],
    [cell("Physical carrier"), cell("Maintain the required thermal environment through insulation, coolant packs and a freeze-preventive barrier."), cell("Passive vaccine carrier, payload, coolant packs, tamper-evident seal.")],
    [cell("Edge sensing"), cell("Capture temperature, location, lid/tamper, device health and optional shock data."), cell("ESP32; DS18B20 prototype; calibrated multi-point probes for production; GNSS; reed/Hall sensor; accelerometer.")],
    [cell("Local resilience"), cell("Continue recording when network connectivity is unavailable and forward in order after reconnection."), cell("Encrypted append-only storage, sequence number, local timestamp, retry queue, store-and-forward.")],
    [cell("Backend"), cell("Authenticate devices, ingest telemetry, apply rule logic, create incidents and serve apps."), cell("Node.js, Express, MongoDB/time-series collection, API authentication, queue/workers.")],
    [cell("Blockchain trust layer"), cell("Anchor a tamper-evident fingerprint of critical incidents and custody events."), cell("Canonical payload, Keccak-256, Solidity incident registry, ethers.js, Sepolia/Hardhat for demo.")],
    [cell("Interfaces"), cell("Turn evidence into action for citizens, healthcare staff and planners."), cell("Flutter multilingual app, React/Vite dashboard, Mappls, QR verification, alerts, analytics.")],
]
t = Table(flow_rows, colWidths=[29 * mm, 70 * mm, 69 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D7CABA")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("BACKGROUND", (0, 2), (-1, 2), PALE_BLUE),
    ("BACKGROUND", (0, 4), (-1, 4), PALE_GREEN),
    ("BACKGROUND", (0, 5), (-1, 5), PALE_YELLOW),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "One-sentence architecture answer: the device creates signed and sequenced evidence; the backend performs operational processing; raw telemetry stays encrypted off-chain; only critical hashes and custody events are anchored; QR verification recomputes and checks the hash.",
    styles["Callout"],
))
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A helper
# -----------------------------------------------------------------------------
def add_qa_section(title: str, entries: list[tuple[str, str]], intro: str | None = None):
    story.append(Paragraph(title, styles["H1Custom"]))
    if intro:
        story.append(plain(intro))
    for q, a in entries:
        story.append(Paragraph("Q. " + escape(q), styles["Question"]))
        story.append(Paragraph(escape(a).replace("\n", "<br/>"), styles["Answer"]))


# -----------------------------------------------------------------------------
# Q&A 1: Problem, positioning and differentiation
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 1 - Problem, Positioning and Differentiation",
    [
        ("What exact problem are you solving?", "We are solving an accountability and access problem across the vaccine journey. A temperature or custody failure may occur, but evidence is fragmented across stakeholders and the point of failure is difficult to establish. At the same time, citizens may face language, navigation and service-discovery barriers, while planners work with separated operational data."),
        ("Why are Integrity, Access and Intelligence grouped into one ecosystem?", "They correspond directly to the three gaps identified in the problem statement. Swasthya Trace protects integrity, Swasthya Connect improves access and Swasthya Insight turns operational data into planning intelligence. They share one backend and identity model, but the MVP remains focused on integrity."),
        ("What is the core MVP?", "The core MVP is Swasthya Trace: edge sensing, threshold anomaly detection, local buffering, dashboard alerting, incident hash anchoring and QR integrity verification. Citizen services and predictive analytics are valuable extensions, but they should not be presented as the primary proof point until the cold-chain workflow is quantitatively validated."),
        ("How is this different from eVIN?", "eVIN is a national operational foundation for vaccine inventory and temperature visibility at cold-chain points. Swasthya Setu should be positioned as a complementary shipment-level integrity layer that adds multi-point carrier sensing, route and tamper events, signed custody handoffs, cryptographic incident anchoring and point-of-care QR verification. We do not claim to replace eVIN."),
        ("How is this different from U-WIN?", "U-WIN focuses on vaccination registration, records and service access. Swasthya Setu adds physical cold-chain evidence and integrity verification, while its citizen layer can integrate with government service workflows rather than recreate the national registry."),
        ("How is this different from WHO temperature guidance?", "WHO guidance defines how temperature should be monitored and managed. It is guidance, not a complete integrated operational platform. Our value is the connected workflow from sensors to alerts, custody evidence, QR verification and action."),
        ("How is this different from ColdNet and VacLedger?", "ColdNet demonstrates IoT logistics with smart contracts, while VacLedger focuses on blockchain traceability and counterfeit detection. Our differentiation is the end-to-end integration of real-time physical sensing, tamper/custody history, point-of-care QR verification, healthcare workflows and multilingual citizen access."),
        ("What is the strongest innovation claim?", "The strongest claim is not any individual component. It is the closed evidence-to-action loop: physical material generates sensor evidence; threshold logic creates a defined incident; the digital record is anchored against later alteration; QR verification exposes the integrity result; and authorized stakeholders take action."),
        ("What should you avoid calling innovative?", "Do not claim that ESP32, QR codes, Flutter, MongoDB or blockchain alone are novel. They are established tools. The innovation is their domain-specific integration, the accountability model and the prototype-to-production engineering path."),
        ("What is the current technology-readiness level?", "Based only on the deck, this is a functional integrated prototype or proof of concept: sensing, telemetry, interfaces, QR and blockchain event logging are represented, but calibrated performance, ruggedization, carrier qualification, battery endurance and field validation remain pilot work. Do not claim production readiness."),
        ("Are all three parts implemented?", "State only what can be demonstrated. The deck shows a citizen app preview, dashboard workflow, hardware prototype and blockchain event path. Predictive analytics, district-scale integration and some production hardware features are roadmap items. Separate implemented, simulated and planned capabilities explicitly."),
        ("What is the single-line value proposition?", "Swasthya Setu makes the vaccine journey continuously observable, the critical evidence tamper-evident and the resulting services understandable and accessible to citizens and healthcare staff."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A 2: Blockchain
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 2 - Blockchain, Hashing, Smart Contract and Gas",
    [
        ("Why not use only a secure centralized database?", "A secure central database is excellent for high-volume telemetry and remains part of our design. The remaining issue is cross-stakeholder trust: manufacturers, transporters, distributors and centres may not accept one stakeholder as the unquestioned administrator of the only evidence store. Selective anchoring gives independent verification and makes retrospective alteration detectable. The architecture is hybrid, not blockchain-only."),
        ("What information stays off-chain?", "Raw high-frequency sensor readings, full location tracks, user records, medical information, documents and detailed analytics stay in encrypted databases. This avoids privacy leakage, excessive gas and poor query performance."),
        ("What information goes on-chain?", "A minimal record: shipment or batch identifier, incident hash, anomaly category, event timestamp, reporter address and optional custody or QR-status transition. Calibration certificate hashes and custody handoff hashes can also be anchored. No patient-identifying data should be placed on a public chain."),
        ("What exactly is being hashed?", "A deterministic incident payload. Recommended fields are schema version, shipment ID, device ID, anomaly type, start and end timestamps, minimum/maximum/representative readings, units, coordinates or geofence result, custody stage, event sequence number, firmware version and calibration ID. The exact field set must match the deployed code."),
        ("Why must the payload be canonical?", "If two systems serialize the same data differently, they generate different hashes. We therefore require fixed key order, UTC integer timestamps, explicit units and integer representations such as milli-degrees Celsius and microdegrees for coordinates. The verifier must rebuild exactly the same bytes."),
        ("Which hashing algorithm should be used?", "For Ethereum compatibility, use Keccak-256 through ethers.js. Ethers provides helpers such as id for UTF-8 text and solidityPackedKeccak256 for Solidity-compatible packed values. The team must verify which helper the actual code uses."),
        ("What does the smart contract do?", "It should be a small append-only incident registry. It accepts an authorized reporter's shipment ID, incident hash, anomaly type and timestamp, then emits an indexed event. It does not need a token, NFT or payment logic. Corrections are added as later versioned events; the original anchor remains visible."),
        ("What is the contract based on?", "The deck confirms Solidity, Hardhat, ethers.js, MetaMask and Sepolia. A defensible implementation uses Solidity role-based access control and an event-based incident registry. The exact source, ABI and deployed address cannot be recovered from the PDF and must be verified from the repository or Sepolia explorer before the evaluation."),
        ("Who is allowed to write to the contract?", "In the demonstration, MetaMask can represent the authorized operator. In production, use role-based reporter addresses assigned to secure gateways or organizational signing services. Admin, reporter and auditor roles should be separated, with key rotation and revocation."),
        ("Which faucet are you using?", "The submitted deck does not identify the faucet. The accurate answer is that Sepolia test ETH is obtained from a public faucet. Before presenting, check the wallet history or team notes and name the actual provider only if verified. Common public options listed by Ethereum include Alchemy, Chainstack, Google Cloud Web3, Infura and QuickNode."),
        ("Does Sepolia gas cost real money?", "No. Sepolia uses test ETH with no monetary value. It is suitable for demonstrating deployment and transaction flow, not for estimating production operating cost directly."),
        ("How is transaction cost calculated?", "Transaction fee equals gas used multiplied by the gas price. Gas price is commonly expressed in gwei, where one gwei is one-billionth of one ETH. INR cost equals gas used times gas price in gwei times 10^-9 times the current ETH price in INR."),
        ("What is the expected gas per anomaly?", "Without the deployed receipt, only a planning range can be given. An event-only anchor is often budgeted around 40,000 gas; writing state plus emitting an event may be budgeted around 70,000 gas. Measure the real value using estimateGas and the transaction receipt's gasUsed field."),
        ("How do you reduce gas cost?", "Do not anchor every reading. Anchor only anomalies, custody handoffs, calibration events and status changes. Batch many incidents into a Merkle root, use compact fixed-size fields and deploy to a lower-cost Layer 2 or a permissioned consortium network for production."),
        ("What happens when the blockchain is unavailable?", "Monitoring and alerting continue. The device and backend store the signed incident with an anchor-pending status, retry asynchronously and record the eventual transaction hash. Operational safety must never depend on immediate chain confirmation."),
        ("What happens if someone changes MongoDB after anchoring?", "QR verification retrieves the off-chain event, rebuilds the canonical bytes and recomputes the hash. The recomputed value will not match the on-chain incident hash, so the record is marked as cryptographically inconsistent."),
        ("Can someone delete the off-chain data?", "Blockchain cannot recover deleted raw data automatically. The verifier would see a missing evidence package even though an anchor exists. Production therefore needs redundant encrypted storage, retention rules, backups and integrity monitoring in addition to the chain."),
        ("Can blockchain prove the sensor did not lie?", "No. It proves that the anchored evidence has not been silently modified. Sensor truth requires calibration, multi-point agreement, secure device keys, protected firmware, sequence numbers, plausibility checks and independent pilot validation."),
        ("How do you prevent replayed incidents?", "Include a unique shipment ID, device ID, monotonic sequence number, incident ID and timestamp in the signed and hashed payload. The contract or backend should reject an already-used incident ID or a sequence number that does not advance."),
        ("How do you protect privacy on a public chain?", "Use opaque identifiers and cryptographic hashes only. Never write a name, phone number, Aadhaar number, health record, exact citizen address or raw document. Hashing low-entropy personal data is not sufficient because it can be guessed; such data must remain off-chain."),
        ("What if the signing key is compromised?", "Revoke the reporter role, rotate the key, mark the affected time window and investigate all events signed by that address. Production keys should be stored in a secure element, hardware security module or managed signing service rather than a browser wallet."),
        ("What if all stakeholders collude?", "No technical system can fully prevent coordinated false input from every participant. The design reduces unilateral alteration and improves auditability. Independent governance, multiple organizations, calibration evidence, secure device identities and external audits reduce the probability and detectability of collusion."),
        ("Why MetaMask in the prototype?", "MetaMask makes signing and transaction inspection easy during a demo. It is not the preferred unattended production signer. A production gateway should sign with a protected machine identity and clear organizational authorization."),
        ("What production chain would you use?", "The choice depends on governance and cost. A permissioned consortium ledger offers controlled membership and predictable cost; a public Layer 2 offers broader independent verification at lower fees than Ethereum mainnet. The MVP remains chain-agnostic because the evidence model and hashes are portable."),
    ],
)

story.append(Paragraph("Recommended Incident Payload", styles["H2Custom"]))
code_payload = '''{
  "schemaVersion": 1,
  "shipmentId": "opaque-shipment-id",
  "deviceId": "registered-device-id",
  "incidentId": "unique-event-id",
  "sequence": 1842,
  "anomalyType": "TEMP_HIGH",
  "startedAtUtc": 1787440500,
  "endedAtUtc": 1787440800,
  "minMilliC": 5100,
  "maxMilliC": 10400,
  "latMicroDeg": 19076543,
  "lonMicroDeg": 72877654,
  "custodyStage": "TRANSPORT",
  "firmwareVersion": "1.0.0",
  "calibrationId": "cal-cert-hash-or-id"
}'''
story.append(Preformatted(code_payload, styles["Code"]))

story.append(Paragraph("Recommended Minimal Solidity Pattern", styles["H2Custom"]))
solidity = '''bytes32 public constant REPORTER_ROLE = keccak256("REPORTER_ROLE");

event IncidentAnchored(
    bytes32 indexed shipmentId,
    bytes32 indexed incidentHash,
    uint8 anomalyType,
    uint64 timestamp,
    address indexed reporter
);

function anchorIncident(
    bytes32 shipmentId,
    bytes32 incidentHash,
    uint8 anomalyType,
    uint64 timestamp
) external onlyRole(REPORTER_ROLE) {
    emit IncidentAnchored(
        shipmentId, incidentHash, anomalyType, timestamp, msg.sender
    );
}'''
story.append(Preformatted(solidity, styles["Code"]))
story.append(Paragraph(
    "This pattern is an engineering recommendation for the Q&A explanation. It must not be presented as the recovered source code unless it matches the team's repository and deployed ABI.",
    styles["Warn"],
))
story.append(PageBreak())

# Gas table
gas_rows = [[cell("Illustrative gas price", head=True), cell("40,000 gas event-only", head=True), cell("70,000 gas state + event", head=True)]]
for gwei, c40, c70 in [
    ("0.1 gwei", "INR 0.80", "INR 1.40"),
    ("0.5 gwei", "INR 4.00", "INR 7.00"),
    ("1 gwei", "INR 8.00", "INR 14.00"),
    ("5 gwei", "INR 40.00", "INR 70.00"),
    ("20 gwei", "INR 160.00", "INR 280.00"),
]:
    gas_rows.append([cell(gwei), cell(c40), cell(c70)])

story.append(Paragraph("Gas-Cost Planning Scenarios", styles["H1Custom"]))
story.append(plain(
    "The table uses an intentionally round planning assumption of INR 200,000 per ETH. It is not a live market quotation. Replace the ETH price before submitting a financial model. Sepolia transactions still use valueless test ETH."
))
t = Table(gas_rows, colWidths=[55 * mm, 57 * mm, 57 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D6C8B8")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 3 * mm))
story.append(Paragraph(
    "Formula: cost in INR = gas used x gas price in gwei x 10^-9 x ETH price in INR. Recommended production strategy: event-only anchors, batching or Merkle roots, and a Layer 2 or permissioned consortium ledger.",
    styles["Callout"],
))
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A 3: Hardware
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 3 - IoT Hardware, Cold Chain and Prototype-to-Production",
    [
        ("What is present in the current prototype?", "The submitted architecture shows an ESP32 or ESP-WROOM-32 controller, one DS18B20 waterproof temperature probe, BMP280 pressure/environment sensor, NEO-6M GPS, reed switch, microSD logging, SIM800L cellular module, an 18650 battery and TP4056 charging/power management."),
        ("What does the prototype prove?", "It demonstrates the integration logic: sensing, local logging, location, tamper input, telemetry transmission, threshold event generation, alert delivery, dashboard/QR workflow and blockchain event anchoring. It does not by itself prove calibration, thermal uniformity, ruggedness or field endurance."),
        ("What is the DS18B20 accuracy?", "The sensor IC is specified at approximately plus or minus 0.5 C from minus 10 C to 85 C. The assembled waterproof probe may add error through encapsulation, cable quality, thermal lag or counterfeit components. Each finished probe must therefore be calibrated as a system."),
        ("Is plus or minus 0.5 C adequate?", "It is a defensible baseline for a prototype and aligns with the precision expected in many cold-chain monitoring contexts, but production acceptance must be tested against the selected vaccine, carrier and regulatory requirements. A tighter production candidate such as TMP117 offers up to plus or minus 0.1 C in its specified range."),
        ("Why use multiple temperature probes in production?", "One point can miss thermal gradients. A probe near a coolant pack may read colder than the payload centre, while a wall exposed to heat may be warmer. A multi-point array reveals the hottest, coldest and central regions."),
        ("Why three internal probes plus one ambient probe?", "This is the proposed small-carrier architecture: upper, centre and lower internal locations plus external ambient. It is not a universal fixed requirement. Final sensor count and location must be selected after loaded thermal mapping of the exact container, coolant placement and payload pattern."),
        ("What about a large cold box?", "Qualification may use many more thermal-mapping positions. After identifying repeatable hot and cold zones, the team can choose the smallest permanent sensor arrangement that reliably detects them, then revalidate after any geometry, insulation or loading change."),
        ("Does BMP280 measure humidity?", "No. BMP280 measures barometric pressure and temperature. If humidity is required, use BME280, SHT45 or another validated humidity sensor. The presentation must not claim humidity from BMP280."),
        ("Can BMP280 detect shocks or handling?", "Not reliably. Barometric pressure is not the correct primary signal for impact. A production design should add a three-axis accelerometer such as an ADXL372-class high-g impact sensor for drop and shock events."),
        ("Why keep a pressure sensor at all?", "Pressure can be useful for environmental context, enclosure diagnostics or elevation-related analysis, but it is not a core vaccine-potency metric. If it does not materially improve the risk model, removing it simplifies the product."),
        ("Why is SIM800L only a prototype choice?", "SIM800L uses 2G, which is low-cost and simple for a demonstration but has coverage and longevity limitations. Production should evaluate 4G Cat-1, NB-IoT or LTE-M according to Indian network coverage, power budget, module certification and data plan."),
        ("Why move from NEO-6M to a newer GNSS module?", "A low-power modern GNSS module improves battery life, acquisition behaviour and availability. Production should use duty-cycled fixes, route/geofence logic and an antenna position that is not shielded by the insulated carrier."),
        ("How is the production electronics enclosure designed?", "The controller, battery, storage and communication modules should sit in a sealed external pod. Only sealed probes enter the payload area. This preserves vaccine volume, reduces heat and moisture exposure, improves antenna reception and allows maintenance without opening the vaccine compartment."),
        ("How does the carrier maintain temperature?", "The proposed design is passive. Insulation, correctly conditioned coolant packs and a freeze-preventive barrier maintain the thermal environment. The electronics monitor and verify; they do not actively refrigerate the box."),
        ("Why use a freeze-preventive barrier?", "Freeze-sensitive vaccines can be damaged by direct contact with frozen coolant packs. The barrier separates the payload from the packs and reduces accidental freezing while preserving cold life."),
        ("How should the sensors be calibrated?", "Compare every finished probe against a traceable reference at multiple points such as 2 C, 5 C and 8 C, allow stabilization, record offset and repeatability, store the calibration ID and apply only controlled correction values. Recalibration frequency should be defined by drift evidence and operating policy."),
        ("What happens when connectivity is lost?", "The device continues sampling and writes encrypted append-only records with timestamps and sequence numbers. It flags the link as offline, buffers messages and forwards them in order after reconnection. A missing or reordered sequence is detectable."),
        ("How do you prevent SD-card manipulation?", "Use encryption, hash chaining between records, device signatures or message authentication codes, monotonic sequence numbers and restricted physical access. The backend verifies the chain before accepting a replayed batch."),
        ("How do you detect lid opening?", "The prototype uses a reed switch. Production should combine a Hall-effect or magnetic position sensor with a tamper-evident seal or conductive loop. The event includes time, location, custody stage and authorization context."),
        ("How do you detect a cloned QR code?", "A QR should carry an opaque shipment or package identity, not the entire trust claim. The app retrieves a signed server response, checks the associated chain hash, package serial and tamper status, and displays a verification result. A copied QR cannot recreate a valid physical seal or an independently consistent custody history."),
        ("How do you estimate battery runtime?", "Runtime is approximately usable battery capacity divided by average current. Apply a 20 to 30 percent derating for conversion loss, temperature, battery ageing and peak currents. A 2600 mAh cell at 50 mA average with 80 percent usable capacity gives about 41.6 hours; at 100 mA average it gives about 20.8 hours."),
        ("How do you improve battery life?", "Keep sensors at the required sampling interval, batch cellular uploads, duty-cycle GNSS, use ESP32 deep sleep, wake immediately for anomaly or lid events, reduce status LEDs and measure the full current profile rather than relying on component datasheets alone."),
        ("What should be tested before a field pilot?", "Probe accuracy and repeatability, loaded thermal mapping, high/low excursion detection, false alerts, alert latency, offline recovery, lid and shock events, route deviation, battery endurance, water/dust resistance, drop and vibration, QR verification and post-anchor tamper detection."),
        ("Is the light-anomaly demo part of the production architecture?", "Only if the team actually connected and intends to retain a light sensor. The final hardware list does not show one. The safest description is that light was used as a test anomaly input to demonstrate the event pipeline, unless the sensor and purpose are confirmed."),
        ("Would you use a WHO-prequalified logger?", "During pilot validation, yes: a WHO-PQS-qualified or traceably calibrated reference logger is valuable as an independent benchmark. The project must prove that its custom multipoint system meets its stated performance rather than assuming component specifications are enough."),
        ("Is this a medical device?", "Classification depends on intended use and regulatory interpretation. The system supports logistics monitoring and evidence; it should not autonomously diagnose patients or certify vaccine potency. Production deployment requires a formal regulatory and quality review, calibrated equipment and approved operating procedures."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A 4: Multilingual AI / app
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 4 - Citizen App, Multilingual AI and Maps",
    [
        ("What is the citizen-app workflow?", "A user speaks or types in a supported language. Speech is transcribed, optionally translated, converted into structured intent or form fields, validated against deterministic rules, shown back for confirmation, submitted to the backend and read aloud if needed. The user must be able to correct every extracted field."),
        ("Which Sarvam models are you using?", "The deck confirms Sarvam AI for multilingual voice but does not identify the production model IDs. Current Sarvam documentation lists Saaras v3 for speech-to-text, Mayura v1 for translation and Bulbul v2 or v3 for text-to-speech. Verify the actual API calls in the code before naming a model in the evaluation."),
        ("What is AI4Bharat's role?", "AI4Bharat provides open-source Indian-language components that can act as a self-hosted or offline-capable fallback. IndicTrans2 supports translation across all 22 scheduled Indian languages, and IndicWav2Vec provides Indian-language speech representations and ASR resources. Open source removes per-call licence fees but not hosting, GPU, maintenance or quality-assurance cost."),
        ("Why combine Sarvam and AI4Bharat?", "Sarvam provides managed APIs and operational simplicity. AI4Bharat provides openness, deployment control and a fallback path. A production system can route by connectivity, language, quality, latency and cost rather than depend on one provider."),
        ("What is Gemini used for?", "Use an LLM only for language understanding, intent classification, help text or converting a confirmed transcript into a proposed structured form. Do not use it to decide whether a vaccine is medically safe. Critical thresholds, identity checks and workflow rules remain deterministic."),
        ("How do you prevent an AI model from filling the wrong form field?", "Use a constrained schema, field-level validation, confidence thresholds, explicit confirmation, server-side rules and a complete audit trail of original audio or transcript, extracted value, user correction and submitted value. Never silently submit an uncertain field."),
        ("What happens in low connectivity?", "Allow local draft forms, cached language prompts, queued submissions and retry indicators. Map tiles or essential centre data may be cached subject to provider terms. For voice, a self-hosted AI4Bharat fallback can reduce dependence on live APIs, but the device's compute and storage limits must be considered."),
        ("How many languages can be supported?", "The architecture is designed for Indian multilingual access. IndicTrans2 covers all 22 scheduled languages, while Sarvam's supported language list should be checked for the exact APIs in use. Product support should be launched in phases based on tested accuracy, not only theoretical model coverage."),
        ("How is accessibility handled?", "Voice-first interaction, readable text, large controls, transliteration, audio confirmations, assisted staff mode, simple error recovery and language switching reduce digital-literacy barriers. The app must still offer a non-voice path for privacy and noisy environments."),
        ("What does Mappls provide?", "Mappls can support centre search, nearby-place discovery, routing, navigation and geofencing. Production access, quotas and commercial terms are project dependent, so the team should obtain a written quote rather than invent a per-call cost."),
        ("Why Mappls instead of a generic global map?", "Mappls offers India-focused mapping and local address/POI capabilities and aligns with the project's domestic deployment context. The final choice should still be based on verified centre coverage, API reliability, offline needs, data policy and commercial terms."),
        ("How do you verify centre availability?", "Map discovery alone is not enough. The map result must be joined with authoritative centre inventory, operating hours, appointment slots and service data from the backend or an approved government integration. The UI should distinguish mapped location from confirmed service availability."),
        ("What is the role of Aadhaar?", "Only a simulation is represented in the prototype. Production must not directly collect or authenticate Aadhaar without approved integration, consent, purpose limitation, security controls and legal review. The solution should work with alternative identifiers where required."),
        ("What if translation changes medical meaning?", "Keep critical safety labels and threshold statuses from controlled terminology rather than free-form generative translation. Use reviewed glossaries, back-translation testing, user confirmation and human escalation. The source condition record remains available to authorized staff."),
        ("What is the best production AI plan?", "Begin with a pay-as-you-go managed API for a small pilot, instrument language-level accuracy and latency, then move to a Pro or Business plan only when concurrency justifies it. Retain a self-hosted fallback for strategic languages or unreliable connectivity."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# AI cost table
# -----------------------------------------------------------------------------
story.append(Paragraph("Managed AI Cost Planning", styles["H1Custom"]))
story.append(plain(
    "The figures below are based on public pricing checked on 23 August 2026 and should be revalidated before procurement. GST, network, storage, support and model-orchestration overhead are excluded."
))
ai_rows = [
    [cell("Service", head=True), cell("Public unit price used", head=True), cell("Example interaction", head=True), cell("Illustrative cost", head=True)],
    [cell("Sarvam STT or STT + Translate"), cell("INR 30 per audio hour"), cell("30 seconds of speech"), cell("INR 0.25")],
    [cell("Sarvam Mayura v1 translation"), cell("INR 20 per 10,000 characters"), cell("500 characters"), cell("INR 1.00")],
    [cell("Sarvam Bulbul v2 TTS"), cell("INR 15 per 10,000 characters"), cell("500 characters"), cell("INR 0.75")],
    [cell("Sarvam Bulbul v3 TTS"), cell("INR 30 per 10,000 characters"), cell("500 characters"), cell("INR 1.50")],
    [cell("Typical voice interaction with v2"), cell("STT 30 sec + 500-char translation + 500-char TTS"), cell("One assisted form interaction"), cell("About INR 2.00, plus LLM/maps/backend")],
    [cell("Typical voice interaction with v3"), cell("Same, with Bulbul v3"), cell("One assisted form interaction"), cell("About INR 2.75, plus LLM/maps/backend")],
    [cell("Gemini 3.5 Flash-Lite planning example"), cell("USD 0.30/M input; USD 2.50/M output"), cell("1,000 input + 300 output tokens"), cell("About USD 0.00105; roughly INR 0.10 at INR 96/USD")],
    [cell("AI4Bharat self-hosted"), cell("No API licence fee for open-source model"), cell("IndicTrans2 / IndicWav2Vec inference"), cell("Compute, engineering, storage and operations still apply")],
]
t = Table(ai_rows, colWidths=[37 * mm, 49 * mm, 45 * mm, 38 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("BACKGROUND", (0, 5), (-1, 6), PALE_GREEN),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 4 * mm))
story.append(bullet_list([
    "Sarvam Starter is suitable for prototype and early pilot use. Public plan information indicates Pro at INR 10,000 and Business at INR 50,000, with higher rate limits; enterprise terms are custom.",
    "Rate limits vary by API and plan. Instrument peak requests per minute before selecting a paid tier.",
    "Gemini model and pricing change over time. The deck only confirms Gemini generally; verify the actual model string in code.",
    "Mappls pricing is not treated as a fixed public per-call value in this document. Obtain a project-specific quota and commercial quote.",
], "BodySmall"))
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A 5: backend/security/privacy/scaling
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 5 - Backend, Security, Privacy and Scale",
    [
        ("What is the backend architecture?", "The submitted stack uses Node.js and Express for service APIs and MongoDB for operational data. A production version should separate device ingestion, anomaly processing, notification, user workflows, QR verification and blockchain anchoring into independently scalable services or workers."),
        ("How does telemetry reach the backend?", "The prototype can post batched HTTPS messages through cellular connectivity. At scale, MQTT or an ingestion API can feed a queue, after which idempotent workers validate device signatures, persist telemetry, evaluate rules and generate incidents."),
        ("How do you authenticate a device?", "Each production device needs a unique identity and key or certificate. Messages are sent over TLS and signed or authenticated. The backend maps the key to a registered device, firmware, shipment and calibration record. A shared hard-coded API key is not sufficient."),
        ("How do you prevent duplicate telemetry?", "Use a device ID, monotonic sequence number, event ID and idempotency key. The database enforces uniqueness, and replayed messages are acknowledged without generating duplicate incidents or chain anchors."),
        ("How do you scale MongoDB?", "Use time-based or shipment-based indexes, retention policies, separate raw telemetry from operational documents, archival storage, replica sets and sharding only when measured volume requires it. High-frequency points can also be stored in a time-series collection."),
        ("How do you prevent blockchain from slowing the app?", "Anchoring is asynchronous. The operational event is stored and alerted immediately, then a worker submits the blockchain transaction. The UI displays pending, confirmed or failed anchor status. QR can show that the evidence is awaiting confirmation without blocking emergency action."),
        ("How are users authenticated?", "Use standards-based authentication, short-lived access tokens, refresh-token controls, multi-factor authentication for privileged staff and role-based authorization. Citizen, centre operator, transporter, auditor and administrator permissions should be distinct."),
        ("What audit logs are required?", "Record login, data access, QR checks, custody handoffs, threshold changes, calibration changes, user corrections, status releases, key rotation, role changes and administrative exports. Audit logs should be append-only and access controlled."),
        ("How is data encrypted?", "Use TLS in transit, encryption at rest for databases and backups, protected device storage and managed secret/key storage. Sensitive fields may use application-level encryption. Keys must be rotated and access must be logged."),
        ("How do you comply with India's DPDP framework?", "Collect only data needed for a stated purpose, obtain appropriate notice and consent, secure the data, limit retention, support correction or deletion where applicable and define breach response. The system should avoid placing personal data on an immutable public chain."),
        ("What patient data is required for cold-chain integrity?", "None. Shipment integrity can operate with opaque batch, shipment, device and centre identifiers. Citizen appointment information belongs in a separate protected service with strict access controls and should not be mixed into chain events."),
        ("How do you integrate with government systems?", "Use documented, authorized APIs and an adapter layer. The project should exchange minimum necessary identifiers and status fields with U-WIN, eVIN or other approved platforms rather than duplicate their registries. Integration is a roadmap item until access is formally granted."),
        ("How do you handle an API or cloud outage?", "Edge devices continue local logging; user apps show service status and retain safe drafts; queues absorb temporary load; critical alerts use retry and alternate channels; backups and regional recovery are tested. The chain is not the operational single point of failure."),
        ("What is the biggest cybersecurity risk?", "Compromised device or organizational signing keys can create apparently legitimate false evidence. The mitigation is secure boot where possible, signed firmware, per-device keys, key rotation, anomaly correlation, calibration records, tamper detection and rapid revocation."),
        ("How do you update firmware safely?", "Use signed over-the-air firmware, version pinning, staged rollout, rollback, device-health reporting and an immutable record of firmware version in each incident payload. An unsigned firmware image must never be accepted."),
        ("What happens when a threshold changes?", "Thresholds must be product- and policy-specific, versioned and authorized. The incident stores the threshold profile ID used at that time so an auditor can reconstruct why the alert was generated."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Costs
# -----------------------------------------------------------------------------
story.append(Paragraph("Prototype and Production Cost Planning", styles["H1Custom"]))
story.append(Paragraph(
    "All amounts are indicative engineering ranges, not vendor quotations. Recheck them immediately before procurement. They exclude GST, shipping, customs, wiring labour, failed parts, SIM/data, server cost, calibration-lab charges and institutional integration.",
    styles["Warn"],
))

prototype_rows = [
    [cell("Prototype component", head=True), cell("Indicative INR range", head=True), cell("Purpose / note", head=True)],
    [cell("ESP32 development board"), cell("250 - 500"), cell("Controller, Wi-Fi/Bluetooth, edge logic")],
    [cell("DS18B20 waterproof probe"), cell("50 - 350"), cell("Generic to better-assembled probe; finished-system calibration still required")],
    [cell("BMP280 module"), cell("30 - 100"), cell("Pressure + temperature; not humidity")],
    [cell("NEO-6M GPS module"), cell("245 - 700"), cell("Prototype GNSS")],
    [cell("SIM800L module"), cell("300 - 800"), cell("Prototype 2G telemetry")],
    [cell("MicroSD module"), cell("33 - 90"), cell("Local logging interface")],
    [cell("MicroSD card"), cell("300 - 600"), cell("Storage media; use endurance-grade in field deployments")],
    [cell("Reed switch / module"), cell("47 - 65"), cell("Prototype lid/tamper input")],
    [cell("18650 battery + TP4056"), cell("150 - 600"), cell("Prototype power and charging")],
    [cell("Passives, wiring, PCB/protoboard, enclosure"), cell("400 - 1,000"), cell("Integration allowance")],
    [cell("Estimated prototype electronics total"), cell("1,805 - 4,805"), cell("Typical planning value around INR 3,000; excludes vaccine carrier and labour")],
]
t = Table(prototype_rows, colWidths=[57 * mm, 37 * mm, 75 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -2), HexColor("#FFFCF8")),
    ("BACKGROUND", (0, -1), (-1, -1), PALE_YELLOW),
    ("FONTNAME", (0, -1), (-1, -1), BOLD_FONT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
]))
story.append(t)
story.append(Spacer(1, 5 * mm))

production_rows = [
    [cell("Production-pilot subsystem", head=True), cell("Indicative INR range", head=True), cell("Included direction", head=True)],
    [cell("Four calibrated sealed temperature probes"), cell("3,200 - 8,000"), cell("Multi-point array, sealed assembly and calibration allowance")],
    [cell("MCU, custom PCB, storage and security"), cell("1,500 - 3,000"), cell("Controller, local storage, protected identity and power regulation")],
    [cell("4G connectivity + low-power GNSS"), cell("2,500 - 4,000"), cell("Module, antenna and integration")],
    [cell("Shock and tamper subsystem"), cell("1,500 - 3,500"), cell("Accelerometer, lid sensor and tamper-evident mechanism")],
    [cell("Battery and BMS"), cell("800 - 1,800"), cell("Field-capable cell pack, protection and charging")],
    [cell("Passive freeze-preventive carrier"), cell("3,000 - 8,000"), cell("Container range depends strongly on capacity and qualification")],
    [cell("Sealed electronics pod and connectors"), cell("1,500 - 3,500"), cell("Rugged enclosure, glands, harness and antenna mounting")],
    [cell("Assembly, calibration and QA"), cell("2,000 - 5,000"), cell("Pilot-volume labour and validation allowance")],
    [cell("Estimated production-pilot unit"), cell("16,000 - 36,800"), cell("Planning range only; not a purchase quotation")],
]
t = Table(production_rows, colWidths=[61 * mm, 38 * mm, 70 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -2), HexColor("#FFFCF8")),
    ("BACKGROUND", (0, -1), (-1, -1), PALE_GREEN),
    ("FONTNAME", (0, -1), (-1, -1), BOLD_FONT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
]))
story.append(t)
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "A volume target of roughly INR 10,000 to INR 20,000 may become possible only after a validated custom PCB, component consolidation, supplier negotiation, bulk assembly and a locked carrier specification. It is a target, not a current promise.",
    styles["Callout"],
))
story.append(PageBreak())

add_qa_section(
    "Technical Q&A 6 - Economics and Operating Model",
    [
        ("What is the prototype cost?", "The indicative electronics range is approximately INR 1,800 to INR 4,800, with a typical planning value near INR 3,000. The range excludes the vaccine carrier, labour, GST, shipping, SIM/data and cloud services."),
        ("What is the estimated production-pilot cost?", "A rugged pilot unit with calibrated multipoint probes, 4G, low-power GNSS, shock/tamper sensing, protected storage, a sealed pod and passive carrier is estimated at INR 16,000 to INR 37,000. Supplier quotations and the exact carrier size are required before making a commitment."),
        ("Why is production so much more expensive than the prototype?", "Production cost includes sealed calibrated assemblies, rugged connectors, protected power, current-generation communication, shock/tamper sensing, the physical carrier, quality control and low-volume integration labour. A breadboard bill of materials does not represent a field product."),
        ("What is the cost per monitored shipment?", "Use: device amortization per shipment plus connectivity plus cloud ingestion/storage plus AI interactions plus blockchain anchors plus calibration and maintenance. The result depends on device reuse, journey duration, upload frequency and anomaly rate."),
        ("How much does a typical multilingual interaction cost?", "With the public planning rates used here, 30 seconds of STT, 500 characters of translation and 500 characters of Bulbul v2 TTS total about INR 2.00 before LLM, maps and backend cost. With Bulbul v3, the same example is about INR 2.75."),
        ("What Sarvam plan is suitable?", "Use Starter pay-as-you-go for prototype and early pilot. Move to Pro or Business only after measuring peak concurrency and monthly usage. Enterprise is appropriate only when support, security, contractual capacity or large-scale throughput requires it."),
        ("How much is one Gemini call?", "A planning example with 1,000 input and 300 output tokens on the cited low-cost Flash-Lite model is about USD 0.00105, roughly INR 0.10 at INR 96 per dollar. The exact cost changes with model, token count, caching and current pricing."),
        ("How much does Mappls cost?", "Treat it as quote- and quota-dependent. Public SDK documentation confirms the capability, but the team should obtain commercial terms for the specific API volume and use case rather than state an invented per-call amount."),
        ("What is the business or government procurement model?", "A realistic model is hardware procurement or lease plus annual software, connectivity, support, calibration and maintenance. Government deployment may use a district or programme contract rather than citizen payment. The exact model should be validated with the target health authority."),
        ("How do you control recurring blockchain cost?", "Anchor only critical events, batch hashes, use a Layer 2 or permissioned network and avoid storing raw strings or telemetry on-chain. In many journeys, normal data creates no anomaly anchor, so cost depends on event frequency rather than sample frequency."),
        ("What costs are missing from the current estimate?", "GST, logistics, custom tooling, certification, SIM/data, cloud infrastructure, operations staff, security review, warranty, replacement stock, calibration equipment, field training, integration and support-level agreements."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Q&A 7: pilot/KPIs
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 7 - Pilot Design, KPIs, Risk and Compliance",
    [
        ("What is the proposed pilot roadmap?", "Phase one: laboratory sensor, connectivity and security validation. Phase two: controlled carrier pilot with scripted events. Phase three: supervised vaccination-centre deployment and staff workflow validation. Phase four: district-scale integration and operational evaluation."),
        ("What temperature-accuracy target should be used?", "A proposed baseline is finished-system error no greater than plus or minus 0.5 C at test points such as 2 C, 5 C and 8 C. A tighter target may be selected for production after component and regulatory review. Report actual error, not only the sensor datasheet."),
        ("What anomaly-detection target should be used?", "A proposed pilot target is at least 95 percent recall on scripted high/low excursions and no more than 2 percent false alerts during defined normal-condition windows. These are engineering acceptance targets, not achieved results until tested."),
        ("What alert-latency target should be used?", "A proposed online P95 target is 60 seconds from threshold crossing to dashboard alert, with local immediate logging. Also report median and worst case, and separate device detection, network transmission, backend processing and notification latency."),
        ("What offline-recovery target should be used?", "After a controlled disconnection and reconnection, there should be no missing, duplicated or reordered records. Sequence numbers and batch hashes must reconcile exactly."),
        ("What QR-verification target should be used?", "A proposed online target is three seconds or less for normal verification under pilot connectivity. The screen must clearly distinguish chain confirmed, pending, missing evidence and mismatch."),
        ("What tamper test should be performed?", "Modify an off-chain incident after it has been anchored and verify that every changed package is flagged by a hash mismatch. Separately test lid-open and physical seal events across repeated cycles."),
        ("How should battery life be reported?", "State sampling interval, GNSS schedule, upload interval, network conditions, battery capacity, measured average current and total run time. One unqualified number is not meaningful. Include low-temperature and ageing derating for field planning."),
        ("How do you test route deviation?", "Define a route corridor or sequence of geofences, replay normal and deviating tracks, measure detection delay and false alerts, and document behaviour when GNSS is unavailable or inaccurate."),
        ("How do you determine vaccine status after an excursion?", "The system should quarantine and escalate. An authorized public-health or clinical workflow evaluates product type, time, magnitude, cumulative history and manufacturer guidance. The app does not autonomously certify potency."),
        ("What are the largest deployment risks?", "Connectivity gaps, sensor drift, battery depletion, physical tampering, false alerts, staff workflow burden, key compromise, privacy error, integration dependency and uncertain carrier qualification. Each risk needs an owner, control and measured pilot test."),
        ("How do you mitigate connectivity loss?", "Local encrypted buffering, visible offline status, retry with backoff, batch upload, optional multi-network connectivity and reconciliation on reconnect."),
        ("How do you mitigate sensor drift?", "Incoming calibration, multi-point comparison, periodic verification against a reference, drift limits, replacement policy and calibration ID in the evidence record."),
        ("How do you mitigate staff resistance?", "Use minimal steps, QR-based handoff, automatic data capture, local-language training, clear alert ownership, pilot observation and measured time-on-task. The platform should reduce paperwork rather than add duplicate entry."),
        ("What compliance path is required?", "Define intended use, review vaccine cold-chain and WHO/PQS requirements, comply with data-protection law, validate calibrated measurement, document software and security controls, conduct field-risk assessment and obtain approvals from the relevant health authority before operational deployment."),
    ],
)

# KPI table
story.append(Paragraph("Proposed Pilot Acceptance Matrix", styles["H2Custom"]))
kpi_rows = [
    [cell("Metric", head=True), cell("Method", head=True), cell("Proposed target", head=True), cell("Status today", head=True)],
    [cell("Temperature-system error"), cell("Compare finished probes at 2, 5 and 8 C against traceable reference"), cell("<= +/-0.5 C baseline"), cell("Insert measured result")],
    [cell("Thermal gradient"), cell("Loaded multi-point thermal mapping"), cell("Report maximum spatial difference"), cell("Insert measured result")],
    [cell("Excursion recall"), cell("Scripted high/low events"), cell(">=95% proposed"), cell("Insert measured result")],
    [cell("False-alert rate"), cell("Defined normal-condition windows"), cell("<=2% proposed"), cell("Insert measured result")],
    [cell("P95 alert latency"), cell("Threshold crossing to dashboard notification"), cell("<=60 seconds online"), cell("Insert measured result")],
    [cell("Offline recovery"), cell("Disconnect, buffer, reconnect and reconcile"), cell("No missing/duplicate/reordered records"), cell("Insert measured result")],
    [cell("QR verification"), cell("End-to-end fetch, hash and status"), cell("<=3 seconds online proposed"), cell("Insert measured result")],
    [cell("Lid/tamper event"), cell("Repeated open/close and seal tests"), cell("100 of 100 scripted events"), cell("Insert measured result")],
    [cell("Post-anchor modification"), cell("Edit off-chain package"), cell("100% hash mismatches flagged"), cell("Insert measured result")],
    [cell("Battery endurance"), cell("Actual duty cycle and network"), cell("Target based on journey profile"), cell("Insert measured result")],
]
t = Table(kpi_rows, colWidths=[38 * mm, 59 * mm, 43 * mm, 29 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("BACKGROUND", (3, 1), (3, -1), PALE_YELLOW),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
]))
story.append(t)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Tough questions
# -----------------------------------------------------------------------------
add_qa_section(
    "Technical Q&A 8 - Tough Evaluator Questions",
    [
        ("Is blockchain overengineering?", "It would be overengineering if used for every sample or inside one trusted organization. We use it only at the cross-stakeholder accountability boundary, while the database performs normal operations. Its value must be judged against the cost of disputed or altered evidence."),
        ("Why not buy an existing data logger?", "A qualified logger is valuable and can be used as a pilot reference. Our contribution is the end-to-end workflow: multi-point carrier sensing, route/tamper correlation, custody events, QR verification, multilingual access and integration. Production must still meet or exceed the logger's validated measurement quality."),
        ("What if a stakeholder disconnects the device?", "Loss of heartbeat, power interruption, enclosure opening and missing sequence numbers become incidents. Local storage preserves data until power is lost; production design also needs protected power, tamper evidence and procedures for unexplained gaps."),
        ("What if the sensor is replaced with another sensor?", "Bind the registered probe identity and calibration ID to the device configuration. A replacement requires an authorized maintenance event and new calibration record. Unexpected identity or electrical profile changes are flagged."),
        ("Can a transporter wrap or heat only part of the box without detection?", "Multipoint probes reduce blind spots, and thermal mapping determines where they are most informative. No finite sensor array guarantees detection of every adversarial action, so physical seals, custody procedure and independent checks remain necessary."),
        ("Who owns the blockchain network?", "For production, governance must be defined among authorized stakeholders such as health authorities, logistics partners and auditors. No single logistics stakeholder should control membership, key issuance and dispute resolution alone."),
        ("Can blockchain data ever be corrected?", "Yes, through a new correction or superseding event that references the previous record. The original is not erased, preserving audit history. The operational UI displays the latest authorized state and the full lineage."),
        ("What if a wrong but honestly captured value is anchored?", "The incorrect event remains visible, and a versioned correction with reason, authority and calibration evidence is added. Immutability is not the absence of mistakes; it is the inability to hide the history of those mistakes."),
        ("What if the QR is scanned by an ordinary citizen?", "Expose only an understandable and privacy-safe condition summary. Detailed location, staff identity, internal investigation and medical information remain restricted. Citizen-facing wording must not provide an unsupported clinical guarantee."),
        ("How does the system work without smartphones?", "Healthcare staff can use the web dashboard, a shared centre device or printed identifier. Citizen voice and app access improve reach but are not required for the cold-chain integrity pipeline to operate."),
        ("What is your strongest quantitative result?", "Use only an actual measured result from your logs. If none is available, say that the current prototype demonstrates the integrated flow and the next milestone is the controlled acceptance matrix. Never convert a proposed KPI into an achieved claim."),
        ("What is your weakest point today?", "The honest answer is production validation: calibrated multipoint accuracy, battery endurance, ruggedization and a supervised carrier pilot. The architecture is designed, but those measurements decide whether it is field ready."),
        ("Why use a pressure sensor when temperature is the main risk?", "Pressure is optional contextual information. It should not be presented as shock detection or humidity. Production prioritizes calibrated temperature, tamper, GNSS and shock; pressure can be removed if it adds no validated value."),
        ("Why use 2G?", "SIM800L is an inexpensive prototype module. The production transition explicitly replaces it with a suitable current network technology selected from 4G Cat-1, NB-IoT or LTE-M based on coverage and power."),
        ("How will you integrate with eVIN or U-WIN if APIs are unavailable?", "Begin with a standalone pilot and export or adapter interface using approved data fields. Do not scrape or bypass access controls. Formal integration follows authorization and data-sharing agreements."),
        ("What is your intellectual property?", "The defensible IP is the integrated evidence model, canonical incident schema, anomaly-to-anchor workflow, carrier sensor architecture, verification logic, domain UX and operational integration. Commodity boards and open-source frameworks are not proprietary."),
        ("What happens if the project becomes too broad?", "Keep the MVP focused on end-to-end vaccine integrity: sensing, anomaly, tamper/custody evidence and QR verification. Treat citizen services, forecasting and broader analytics as staged modules rather than prerequisites for pilot success."),
        ("How will you know the project created impact?", "Measure reduction in undetected excursions, time to alert, time to resolution, completeness of custody records, percentage of verifiable shipments, staff time, wastage decisions and user success in finding or booking a service."),
        ("Why should the evaluator trust your cost numbers?", "They should treat them as transparent planning ranges. We show component assumptions and excluded costs, and we will replace them with dated supplier quotations after the carrier and production BOM are locked."),
        ("What is your immediate next experiment?", "Run a loaded carrier test with multiple calibrated probes and an independent reference logger, create scripted temperature, lid, route and network-loss events, measure the entire KPI matrix and verify every incident through the QR-to-chain flow."),
    ],
)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Rapid cheat sheet
# -----------------------------------------------------------------------------
story.append(Paragraph("Rapid Numbers and One-Line Answers", styles["H1Custom"]))
cheat_rows = [
    [cell("Prompt", head=True), cell("Answer to remember", head=True)],
    [cell("Programme scale"), cell("Approximately 2.6 crore infants and 2.9 crore pregnant women annually, as stated in the deck.")],
    [cell("Core problem"), cell("When integrity is compromised, the failure point is difficult to identify across multiple stakeholders.")],
    [cell("Three solution parts"), cell("Swasthya Trace, Swasthya Connect and Swasthya Insight.")],
    [cell("Research evidence"), cell("14.8% below 0 C; 6.6% above 8 C; 76% of selected US providers in the cited audit had inappropriate temperatures.")],
    [cell("Why blockchain"), cell("Cross-stakeholder non-repudiation and tamper evidence, not database replacement.")],
    [cell("On-chain"), cell("Incident hash + minimal metadata; no raw telemetry or PII.")],
    [cell("Hash"), cell("Canonical incident bytes -> Keccak-256 -> authorized contract event.")],
    [cell("Demo chain"), cell("Solidity + Hardhat + ethers.js + MetaMask + Sepolia; exact contract and faucet must be verified.")],
    [cell("Gas formula"), cell("Gas used x gas price in gwei x 10^-9 x ETH price.")],
    [cell("Current anomaly logic"), cell("Threshold/rule based; ML is a later phase after labelled data.")],
    [cell("Current temperature probe"), cell("One DS18B20; sensor IC specification approximately +/-0.5 C in its stated range.")],
    [cell("Production temperature option"), cell("Calibrated multi-point probes; TMP117-class component can offer up to +/-0.1 C in its stated range.")],
    [cell("BMP280 correction"), cell("Pressure + temperature, not humidity and not shock.")],
    [cell("Proposed production placement"), cell("Three internal points plus one external ambient for a small carrier, finalized by thermal mapping.")],
    [cell("Battery example"), cell("2600 mAh x 0.8 / 50 mA = about 41.6 hours; actual duty-cycle measurement required.")],
    [cell("Prototype electronics"), cell("About INR 1.8k-4.8k; typical planning value around INR 3k, excluding carrier and labour.")],
    [cell("Production-pilot unit"), cell("About INR 16k-37k planning range.")],
    [cell("Sarvam 30 sec STT"), cell("About INR 0.25 at INR 30 per audio hour.")],
    [cell("Typical managed voice interaction"), cell("About INR 2.00 with Bulbul v2 or INR 2.75 with v3, plus LLM/maps/backend.")],
    [cell("QR wording"), cell("Condition-history compliant / excursion / quarantine / released / rejected / incomplete / verification failed.")],
    [cell("Pilot target caution"), cell("Accuracy, latency, recall, false alerts and battery values are proposed until measured.")],
]
t = Table(cheat_rows, colWidths=[48 * mm, 121 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("BACKGROUND", (0, 5), (-1, 9), PALE_YELLOW),
    ("BACKGROUND", (0, 11), (-1, 15), PALE_BLUE),
    ("BACKGROUND", (0, 16), (-1, 19), PALE_GREEN),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(PageBreak())

# -----------------------------------------------------------------------------
# Team-specific handoff sheet
# -----------------------------------------------------------------------------
story.append(Paragraph("Team Question Routing", styles["H1Custom"]))
story.append(plain(
    "The final deck assigns clear functional ownership. During Q&A, the first speaker should answer the strategic point in one sentence, then hand over only when detailed implementation evidence is required."
))
team_rows = [
    [cell("Role from final deck", head=True), cell("Primary questions", head=True), cell("Evidence to keep ready", head=True)],
    [cell("Blockchain & system architecture"), cell("Canonical payload, hash function, contract event, role control, Sepolia transaction, QR verification, gas."), cell("Contract address, ABI, source commit, explorer transaction, estimateGas and receipt gasUsed.")],
    [cell("Citizen mobile application"), cell("Flutter workflow, centre discovery, booking, Mappls, accessibility and Aadhaar simulation."), cell("Live app flow, screenshots, API response, offline/draft behaviour.")],
    [cell("Backend & API engineering"), cell("Telemetry ingestion, auth, MongoDB schema, idempotency, alerts, scaling and failure recovery."), cell("API contract, sample signed payload, database record, retry log and architecture diagram.")],
    [cell("IoT hardware & firmware"), cell("BOM, wiring, sampling, calibration, SIM800L, storage, battery, sensor placement and production transition."), cell("Prototype, firmware version, raw logs, multimeter/current trace, reference thermometer and test sheet.")],
    [cell("Doctor dashboard & integration"), cell("Alerts, shipment visibility, queue/inventory, QR verification and role-based workflow."), cell("Live dashboard, anomaly status, QR scan and mismatch demonstration.")],
    [cell("Multilingual AI, data & testing"), cell("Sarvam, AI4Bharat, Gemini, language accuracy, AI cost, KPI design and validation."), cell("Exact model IDs, API logs, confidence/error examples, test matrix and cost calculation.")],
]
t = Table(team_rows, colWidths=[45 * mm, 65 * mm, 59 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MAROON),
    ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#D5C8BA")),
    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FFFCF8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 5 * mm))
story.append(Paragraph(
    "Do not let six people give six different versions of the architecture. Every answer should preserve the same boundaries: database for operations, blockchain for selective evidence anchoring, threshold logic for the current MVP, passive carrier for temperature maintenance, and measured pilot data for production claims.",
    styles["Callout"],
))
story.append(PageBreak())

# -----------------------------------------------------------------------------
# References
# -----------------------------------------------------------------------------
story.append(Paragraph("References", styles["H1Custom"]))
story.append(plain(
    "The submitted deck remains the primary source for the project description. External sources below support the technical preparation, current public pricing and production recommendations. Public prices and documentation were checked on 23 August 2026 and may change."
))

references = [
    ("Final submitted deck", "TrustArc_SIH26_10_R1.pdf, Team TrustArc, 12 pages."),
    ("U-WIN update", "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2079025"),
    ("WHO vaccine wastage concept note", "https://www.who.int/docs/default-source/immunization/tools/revising-wastage-concept-note.pdf"),
    ("National Operational Guidelines / eVIN annexure", "https://www.nhm.gov.in/New_Updates_2018/NHM_Components/Immunization/Guildelines_for_immunization/PCV_Operational_Guidelines.pdf"),
    ("WHO PQS E006 temperature monitoring devices", "https://extranet.who.int/prequal/immunization-devices/e006-temperature-monitoring-devices"),
    ("WHO vaccine temperature monitoring handbook", "https://www.who.int/publications/i/item/WHO-IVB-15.04"),
    ("WHO PQS E004 cold boxes and vaccine carriers", "https://extranet.who.int/prequal/immunization-devices/e004-cold-boxes-and-vaccines-carriers"),
    ("ColdNet research", "https://www.sciencedirect.com/science/article/pii/S2096720925001137"),
    ("VacLedger research", "https://www.sciencedirect.com/science/article/pii/S0957417423007959"),
    ("Indian cold-chain monitoring study", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7268609/"),
    ("Post-eVIN Nainital assessment", "https://ijpsr.com/bft-article/assessment-of-cold-chain-functioning-in-post-evin-era-in-nainital-district/"),
    ("HHS OIG VFC report", "https://oig.hhs.gov/reports/all/2012/vaccines-for-children-program-vulnerabilities-in-vaccine-management/"),
    ("Changchun investigation - Chinese Government", "https://english.www.gov.cn/premier/news/2018/07/30/content_281476242575590.htm"),
    ("UNDP eVIN project", "https://www.undp.org/india/projects/improving-vaccination-systems-evin"),
    ("UNDP U-WIN launch", "https://www.undp.org/india/u-win-launch"),
    ("Ethereum gas documentation", "https://ethereum.org/developers/docs/gas/"),
    ("Ethereum networks and Sepolia faucets", "https://ethereum.org/developers/docs/networks/"),
    ("ethers.js hashing documentation", "https://docs.ethers.org/v6/api/hashing/"),
    ("OpenZeppelin access control", "https://docs.openzeppelin.com/contracts/5.x/access-control"),
    ("Hardhat", "https://hardhat.org/"),
    ("Sarvam AI pricing", "https://docs.sarvam.ai/api/getting-started/pricing"),
    ("Sarvam AI rate limits", "https://docs.sarvam.ai/api/getting-started/ratelimits"),
    ("Google Gemini API pricing", "https://ai.google.dev/gemini-api/docs/pricing"),
    ("AI4Bharat IndicTrans2", "https://github.com/AI4Bharat/IndicTrans2"),
    ("AI4Bharat IndicWav2Vec", "https://github.com/AI4Bharat/IndicWav2Vec"),
    ("Mappls Flutter SDK", "https://developer.mappls.com/documentation/sdk/flutter-sdk/"),
    ("Mappls Nearby API", "https://developer.mappls.com/mapping/nearby-api/"),
    ("DS18B20 official product page", "https://www.analog.com/en/products/ds18b20.html"),
    ("TMP117 official product page", "https://www.ti.com/product/TMP117"),
    ("BMP280 official product page", "https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp280/"),
    ("ADXL372 official product page", "https://www.analog.com/en/products/adxl372.html"),
    ("u-blox NEO-6 series", "https://www.u-blox.com/en/product/neo-6-series"),
    ("Digital Personal Data Protection Act, 2023", "https://www.meity.gov.in/content/digital-personal-data-protection-act-2023-dpdp-act"),
    ("Ayushman Bharat Digital Mission", "https://abdm.gov.in/"),
]

for idx, (name, url) in enumerate(references, 1):
    if url.startswith("http"):
        safe_url = escape(url, {'"': '&quot;'})
        story.append(Paragraph(
            f"<b>[{idx}] {escape(name)}.</b> <link href=\"{safe_url}\" color=\"#1A5A8A\">{safe_url}</link>",
            styles["Reference"],
        ))
    else:
        story.append(Paragraph(f"<b>[{idx}] {escape(name)}.</b> {escape(url)}", styles["Reference"]))

story.append(Spacer(1, 5 * mm))
story.append(Paragraph(
    "Research boundary: exact deployed contract logic, exact faucet, actual sensor calibration, measured battery life, actual alert latency, final AI model IDs and negotiated vendor prices were not available in the submitted PDF. The document therefore labels those items as verification tasks, engineering recommendations or planning estimates rather than achieved facts.",
    styles["Warn"],
))

# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------
doc.build(story)
print(f"Generated {OUTPUT.resolve()}")
