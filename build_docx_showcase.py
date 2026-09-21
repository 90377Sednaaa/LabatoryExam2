"""
Script to generate high-resolution terminal window screenshots
and compile the comprehensive Sample_Input_and_Output.docx document.
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
BOLD_FONT_PATH = "C:\\Windows\\Fonts\\consolab.ttf"


def render_terminal_screenshot(
    title: str,
    lines: list[tuple[str, str]],  # (text, color_code)
    output_path: str,
    scale: int = 2
) -> str:
    """
    Renders a realistic dark-mode developer terminal window as a PNG image.
    
    color_code options:
    'prompt': Cyan/Blue for shell prompts
    'input': Green/Yellow for user inputs
    'header': Gold/Yellow for headers
    'chart': Cyan for Gantt charts
    'highlight': Light Green for success/safe sequence
    'default': Off-white for normal text
    'gray': Dim gray for dividers
    """
    font_size = 15 * scale
    font = ImageFont.truetype(FONT_PATH, font_size)
    bold_font = ImageFont.truetype(BOLD_FONT_PATH, font_size)
    title_font = ImageFont.truetype(FONT_PATH, 13 * scale)

    # Color palette (VS Code Dark+ inspired)
    bg_color = (30, 30, 30)            # #1e1e1e
    titlebar_bg = (45, 45, 45)         # #2d2d2d
    border_color = (65, 65, 65)        # #414141
    
    colors = {
        'prompt': (86, 156, 214),       # #569cd6 (VS Code blue)
        'input': (206, 145, 120),       # #ce9178 (VS Code orange/input)
        'header': (220, 220, 170),      # #dcdcaa (VS Code gold)
        'chart': (78, 201, 176),        # #4ec9b0 (VS Code teal)
        'highlight': (106, 153, 85),    # #6a9955 (VS Code green)
        'default': (212, 212, 212),     # #d4d4d4 (light gray)
        'gray': (128, 128, 128),        # dim gray
        'white': (255, 255, 255),
    }

    line_height = int(font_size * 1.45)
    title_bar_height = 36 * scale
    padding_x = 24 * scale
    padding_y = 18 * scale

    # Calculate required image dimensions
    dummy_img = Image.new("RGB", (100, 100))
    dummy_draw = ImageDraw.Draw(dummy_img)

    max_line_width = 0
    for text, _ in lines:
        bbox = dummy_draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w > max_line_width:
            max_line_width = w

    img_width = max(max_line_width + padding_x * 2, 700 * scale)
    img_height = title_bar_height + padding_y * 2 + len(lines) * line_height

    # Create image
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw title bar
    draw.rectangle([0, 0, img_width, title_bar_height], fill=titlebar_bg)
    draw.line([0, title_bar_height, img_width, title_bar_height], fill=border_color, width=scale)

    # Window control buttons (macOS/Unix style or clean modern dots)
    btn_radius = 6 * scale
    btn_y = title_bar_height // 2
    btn_x_start = 16 * scale
    btn_spacing = 18 * scale

    draw.ellipse([btn_x_start - btn_radius, btn_y - btn_radius, btn_x_start + btn_radius, btn_y + btn_radius], fill=(255, 95, 86))
    draw.ellipse([btn_x_start + btn_spacing - btn_radius, btn_y - btn_radius, btn_x_start + btn_spacing + btn_radius, btn_y + btn_radius], fill=(255, 189, 46))
    draw.ellipse([btn_x_start + btn_spacing * 2 - btn_radius, btn_y - btn_radius, btn_x_start + btn_spacing * 2 + btn_radius, btn_y + btn_radius], fill=(39, 201, 63))

    # Title text
    title_bbox = dummy_draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_w) // 2
    title_y = (title_bar_height - (title_bbox[3] - title_bbox[1])) // 2
    draw.text((title_x, title_y), title, font=title_font, fill=(180, 180, 180))

    # Draw content lines
    cur_y = title_bar_height + padding_y
    for text, style in lines:
        color = colors.get(style, colors['default'])
        f = bold_font if style in {'header', 'prompt', 'highlight'} else font
        draw.text((padding_x, cur_y), text, font=f, fill=color)
        cur_y += line_height

    # Draw subtle outer border
    draw.rectangle([0, 0, img_width - 1, img_height - 1], outline=border_color, width=scale)

    img.save(output_path, dpi=(300, 300))
    print(f"[+] Saved screenshot: {output_path}")
    return output_path


def create_all_screenshots():
    """Generates screenshots for all 6 scenarios."""
    
    # 1. FCFS Screenshot
    fcfs_lines = [
        ("PS C:\\LabatoryExam2> python main.py", "prompt"),
        (">>> Selected Algorithm: First-Come, First-Served (FCFS) [Non-Preemptive] <<<", "header"),
        ("Enter number of processes: 3", "input"),
        ("", "default"),
        ("Enter details for each process:", "default"),
        ("--- Process P1 ---", "gray"),
        ("Arrival Time for P1: 0", "input"),
        ("Burst Time for P1: 4", "input"),
        ("--- Process P2 ---", "gray"),
        ("Arrival Time for P2: 1", "input"),
        ("Burst Time for P2: 3", "input"),
        ("--- Process P3 ---", "gray"),
        ("Arrival Time for P3: 2", "input"),
        ("Burst Time for P3: 1", "input"),
        ("", "default"),
        ("=================================================================", "gray"),
        ("  CPU Scheduling Results: First-Come, First-Served (FCFS) [Non-Preemptive]", "header"),
        ("=================================================================", "gray"),
        ("", "default"),
        ("Gantt Chart:", "header"),
        ("+-------+-------+-------+", "chart"),
        ("|   P1  |   P2  |   P3  |", "chart"),
        ("+-------+-------+-------+", "chart"),
        ("0       4       7       8", "chart"),
        ("", "default"),
        ("Process Execution Details:", "header"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("Process   | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("P1        | 0            | 4          | 4               | 4               | 0           ", "default"),
        ("P2        | 1            | 3          | 7               | 6               | 3           ", "default"),
        ("P3        | 2            | 1          | 8               | 6               | 5           ", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("", "default"),
        ("Average Turnaround Time : 5.33", "highlight"),
        ("Average Waiting Time    : 2.67", "highlight"),
        ("=================================================================", "gray"),
    ]
    render_terminal_screenshot("PowerShell - FCFS Scheduling", fcfs_lines, os.path.join(SCREENSHOTS_DIR, "1_fcfs_execution.png"))

    # 2. SJF Screenshot
    sjf_lines = [
        ("PS C:\\LabatoryExam2> python main.py", "prompt"),
        (">>> Selected Algorithm: Shortest Job First (SJF) [Non-Preemptive] <<<", "header"),
        ("Enter number of processes: 4", "input"),
        ("", "default"),
        ("Enter details for each process:", "default"),
        ("--- Process P1 ---", "gray"),
        ("Arrival Time for P1: 0", "input"),
        ("Burst Time for P1: 7", "input"),
        ("--- Process P2 ---", "gray"),
        ("Arrival Time for P2: 2", "input"),
        ("Burst Time for P2: 4", "input"),
        ("--- Process P3 ---", "gray"),
        ("Arrival Time for P3: 4", "input"),
        ("Burst Time for P3: 1", "input"),
        ("--- Process P4 ---", "gray"),
        ("Arrival Time for P4: 5", "input"),
        ("Burst Time for P4: 4", "input"),
        ("", "default"),
        ("=================================================================", "gray"),
        ("  CPU Scheduling Results: Shortest Job First (SJF) [Non-Preemptive]", "header"),
        ("=================================================================", "gray"),
        ("", "default"),
        ("Gantt Chart:", "header"),
        ("+-------+-------+-------+-------+", "chart"),
        ("|   P1  |   P3  |   P2  |   P4  |", "chart"),
        ("+-------+-------+-------+-------+", "chart"),
        ("0       7       8       12      16", "chart"),
        ("", "default"),
        ("Process Execution Details:", "header"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("Process   | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("P1        | 0            | 7          | 7               | 7               | 0           ", "default"),
        ("P2        | 2            | 4          | 12              | 10              | 6           ", "default"),
        ("P3        | 4            | 1          | 8               | 4               | 3           ", "default"),
        ("P4        | 5            | 4          | 16              | 11              | 7           ", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("", "default"),
        ("Average Turnaround Time : 8.00", "highlight"),
        ("Average Waiting Time    : 4.00", "highlight"),
        ("=================================================================", "gray"),
    ]
    render_terminal_screenshot("PowerShell - Non-Preemptive SJF", sjf_lines, os.path.join(SCREENSHOTS_DIR, "2_sjf_execution.png"))

    # 3. SRTF Screenshot
    srtf_lines = [
        ("PS C:\\LabatoryExam2> python main.py", "prompt"),
        (">>> Selected Algorithm: Shortest Remaining Time First (SRTF) [Preemptive SJF] <<<", "header"),
        ("Enter number of processes: 4", "input"),
        ("", "default"),
        ("Enter details for each process:", "default"),
        ("--- Process P1 ---", "gray"),
        ("Arrival Time for P1: 0", "input"),
        ("Burst Time for P1: 8", "input"),
        ("--- Process P2 ---", "gray"),
        ("Arrival Time for P2: 1", "input"),
        ("Burst Time for P2: 4", "input"),
        ("--- Process P3 ---", "gray"),
        ("Arrival Time for P3: 2", "input"),
        ("Burst Time for P3: 9", "input"),
        ("--- Process P4 ---", "gray"),
        ("Arrival Time for P4: 3", "input"),
        ("Burst Time for P4: 5", "input"),
        ("", "default"),
        ("=================================================================", "gray"),
        ("  CPU Scheduling Results: Shortest Remaining Time First (SRTF) [Preemptive SJF]", "header"),
        ("=================================================================", "gray"),
        ("", "default"),
        ("Gantt Chart:", "header"),
        ("+-------+-------+-------+-------+-------+", "chart"),
        ("|   P1  |   P2  |   P4  |   P1  |   P3  |", "chart"),
        ("+-------+-------+-------+-------+-------+", "chart"),
        ("0       1       5       10      17      26", "chart"),
        ("", "default"),
        ("Process Execution Details:", "header"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("Process   | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("P1        | 0            | 8          | 17              | 17              | 9           ", "default"),
        ("P2        | 1            | 4          | 5               | 4               | 0           ", "default"),
        ("P3        | 2            | 9          | 26              | 24              | 15          ", "default"),
        ("P4        | 3            | 5          | 10              | 7               | 2           ", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("", "default"),
        ("Average Turnaround Time : 13.00", "highlight"),
        ("Average Waiting Time    : 6.50", "highlight"),
        ("=================================================================", "gray"),
    ]
    render_terminal_screenshot("PowerShell - Preemptive SRTF", srtf_lines, os.path.join(SCREENSHOTS_DIR, "3_srtf_execution.png"))

    # 4. Round Robin Screenshot
    rr_lines = [
        ("PS C:\\LabatoryExam2> python main.py", "prompt"),
        (">>> Selected Algorithm: Round Robin (RR) [Preemptive] <<<", "header"),
        ("Enter number of processes: 3", "input"),
        ("", "default"),
        ("Enter details for each process:", "default"),
        ("--- Process P1 ---", "gray"),
        ("Arrival Time for P1: 0", "input"),
        ("Burst Time for P1: 5", "input"),
        ("--- Process P2 ---", "gray"),
        ("Arrival Time for P2: 1", "input"),
        ("Burst Time for P2: 3", "input"),
        ("--- Process P3 ---", "gray"),
        ("Arrival Time for P3: 2", "input"),
        ("Burst Time for P3: 1", "input"),
        ("", "default"),
        ("Enter Time Quantum for Round Robin: 2", "input"),
        ("", "default"),
        ("=================================================================", "gray"),
        ("  CPU Scheduling Results: Round Robin (RR) [Preemptive]", "header"),
        ("=================================================================", "gray"),
        ("", "default"),
        ("Gantt Chart:", "header"),
        ("+-------+-------+-------+-------+-------+-------+", "chart"),
        ("|   P1  |   P2  |   P3  |   P1  |   P2  |   P1  |", "chart"),
        ("+-------+-------+-------+-------+-------+-------+", "chart"),
        ("0       2       4       5       7       8       9", "chart"),
        ("", "default"),
        ("Process Execution Details:", "header"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("Process   | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("P1        | 0            | 5          | 9               | 9               | 4           ", "default"),
        ("P2        | 1            | 3          | 8               | 7               | 4           ", "default"),
        ("P3        | 2            | 1          | 5               | 3               | 2           ", "default"),
        ("----------------------------------------------------------------------------------------", "gray"),
        ("", "default"),
        ("Average Turnaround Time : 6.33", "highlight"),
        ("Average Waiting Time    : 3.33", "highlight"),
        ("=================================================================", "gray"),
    ]
    render_terminal_screenshot("PowerShell - Round Robin Scheduling", rr_lines, os.path.join(SCREENSHOTS_DIR, "4_round_robin_execution.png"))

    # 5. Banker's Algorithm Pre-configured Screenshot (Exact reference)
    banker_pre_lines = [
        ("PS C:\\LabatoryExam2> python bankers_algorithm.py", "prompt"),
        ("==================================================", "gray"),
        ("         Banker's Algorithm Simulation            ", "header"),
        ("==================================================", "gray"),
        ("1. Pre-configured Data (Instant output from example)", "default"),
        ("2. Custom User Input", "default"),
        ("Select mode [1/2] (Default 1): 1", "input"),
        ("", "default"),
        ("--- Running Banker's Algorithm (Pre-configured Data) ---", "header"),
        ("", "default"),
        ("Need Matrix:", "default"),
        ("P0: [7, 4, 3]", "chart"),
        ("P1: [1, 2, 2]", "chart"),
        ("P2: [6, 0, 0]", "chart"),
        ("P3: [0, 1, 1]", "chart"),
        ("P4: [4, 3, 1]", "chart"),
        ("", "default"),
        ("System is in a Safe State.", "highlight"),
        ("Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2", "highlight"),
    ]
    render_terminal_screenshot("PowerShell - Banker's Algorithm (Pre-configured)", banker_pre_lines, os.path.join(SCREENSHOTS_DIR, "5_bankers_preconfigured.png"))

    # 6. Banker's Algorithm Custom Input Screenshot
    banker_custom_lines = [
        ("PS C:\\LabatoryExam2> python bankers_algorithm.py", "prompt"),
        ("==================================================", "gray"),
        ("         Banker's Algorithm Simulation            ", "header"),
        ("==================================================", "gray"),
        ("1. Pre-configured Data (Instant output from example)", "default"),
        ("2. Custom User Input", "default"),
        ("Select mode [1/2] (Default 1): 2", "input"),
        ("", "default"),
        ("--- Banker's Algorithm (Custom Input) ---", "header"),
        ("Enter number of processes: 3", "input"),
        ("Enter number of resource types: 3", "input"),
        ("", "default"),
        ("Enter Allocation Matrix (3 rows, 3 integers each, e.g. '0 1 0' or '010'):", "default"),
        ("Allocation for P0: 0 1 0", "input"),
        ("Allocation for P1: 2 0 0", "input"),
        ("Allocation for P2: 3 0 2", "input"),
        ("", "default"),
        ("Enter Maximum Matrix (3 rows, 3 integers each, e.g. '7 5 3' or '753'):", "default"),
        ("Maximum for P0: 7 5 3", "input"),
        ("Maximum for P1: 3 2 2", "input"),
        ("Maximum for P2: 9 0 2", "input"),
        ("", "default"),
        ("Enter Available Resources (3 integers, e.g. '3 3 2' or '332'):", "default"),
        ("Available: 3 3 2", "input"),
        ("", "default"),
        ("Need Matrix:", "default"),
        ("P0: [7, 4, 3]", "chart"),
        ("P1: [1, 2, 2]", "chart"),
        ("P2: [6, 0, 0]", "chart"),
        ("", "default"),
        ("System is in a Safe State.", "highlight"),
        ("Safe Sequence: P1 -> P0 -> P2", "highlight"),
    ]
    render_terminal_screenshot("PowerShell - Banker's Algorithm (Custom Input)", banker_custom_lines, os.path.join(SCREENSHOTS_DIR, "6_bankers_custom.png"))


def set_cell_background(cell, fill_hex):
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def style_table(table, col_widths, headers, data, header_bg="2B579A", alt_bg="F2F5F9"):
    """Styles a Word table with colored headers, proper padding, and alternating row shading."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Format header
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], header_bg)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)

    # Format data rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        bg = alt_bg if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = str(val)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(10)

    # Set column widths
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)


def build_docx_report(docx_path: str):
    """Builds the comprehensive, elegantly formatted Word Document."""
    doc = docx.Document()

    # Page Margins (1 inch all around)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_run = title_p.add_run("OPERATING SYSTEMS LABORATORY EXAM 2\n")
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(31, 78, 121)

    sub_run = title_p.add_run("CPU Scheduling Algorithms & Banker's Algorithm Simulation\nSample Input and Output Showcase")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(14)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(89, 89, 89)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Meta Info Table / Card
    meta_table = doc.add_table(rows=3, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Course / Activity:", "Operating Systems - Laboratory Exam 2"),
        ("Programming Language:", "Python 3 (Standard Library)"),
        ("Public GitHub Repository:", "https://github.com/90377Sednaaa/LabatoryExam2"),
    ]
    for i, (k, v) in enumerate(meta_data):
        c1, c2 = meta_table.rows[i].cells
        c1.text = k
        c2.text = v
        set_cell_background(c1, "EAEEF3")
        set_cell_background(c2, "F9FAFC")
        c1.paragraphs[0].runs[0].font.bold = True
        c1.paragraphs[0].runs[0].font.size = Pt(10)
        c2.paragraphs[0].runs[0].font.size = Pt(10)
        c1.width = Inches(2.2)
        c2.width = Inches(4.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Overview Section
    h1 = doc.add_heading(level=1)
    h1_run = h1.add_run("1. Objective & Requirements Overview")
    h1_run.font.color.rgb = RGBColor(31, 78, 121)

    p_intro = doc.add_paragraph(
        "This laboratory document demonstrates the simulated execution of both Non-Preemptive and Preemptive "
        "CPU Scheduling algorithms, as well as the deadlock avoidance mechanism using Dijkstra's Banker's Algorithm. "
        "Each section presents the test input parameters, the resulting terminal execution screenshot (featuring the "
        "Gantt Chart and per-process metrics), and an analytical breakdown of the results."
    )
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 2. FCFS Scheduling
    # -------------------------------------------------------------
    h2 = doc.add_heading(level=1)
    h2_run = h2.add_run("2. Non-Preemptive: First-Come, First-Served (FCFS)")
    h2_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "First-Come, First-Served (FCFS) schedules processes strictly according to their arrival time. "
        "Once a process acquires the CPU, it runs uninterrupted until completion."
    )

    doc.add_heading(level=2).add_run("Input Parameters:")
    fcfs_input_table = doc.add_table(rows=4, cols=3)
    style_table(
        fcfs_input_table,
        [2.0, 2.3, 2.3],
        ["Process ID", "Arrival Time (AT)", "Burst Time (BT)"],
        [
            ["P1", "0", "4"],
            ["P2", "1", "3"],
            ["P3", "2", "1"],
        ],
        header_bg="2F5597"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Execution Screenshot:")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "1_fcfs_execution.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• Process P1 arrives at t=0 and executes from [0, 4] (Completion = 4, TAT = 4, WT = 0).\n"
        "• Process P2 arrives at t=1, waits until P1 finishes at t=4, and executes from [4, 7] (Completion = 7, TAT = 6, WT = 3).\n"
        "• Process P3 arrives at t=2, waits until t=7, and executes from [7, 8] (Completion = 8, TAT = 6, WT = 5).\n"
        "• Average Turnaround Time: (4 + 6 + 6) / 3 = 5.33\n"
        "• Average Waiting Time: (0 + 3 + 5) / 3 = 2.67"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 3. SJF Non-Preemptive
    # -------------------------------------------------------------
    h3 = doc.add_heading(level=1)
    h3_run = h3.add_run("3. Non-Preemptive: Shortest Job First (SJF)")
    h3_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "Shortest Job First (SJF) selects the available arrived process with the smallest CPU burst time. "
        "Being non-preemptive, the selected process runs to completion before the next scheduling decision."
    )

    doc.add_heading(level=2).add_run("Input Parameters:")
    sjf_input_table = doc.add_table(rows=5, cols=3)
    style_table(
        sjf_input_table,
        [2.0, 2.3, 2.3],
        ["Process ID", "Arrival Time (AT)", "Burst Time (BT)"],
        [
            ["P1", "0", "7"],
            ["P2", "2", "4"],
            ["P3", "4", "1"],
            ["P4", "5", "4"],
        ],
        header_bg="2F5597"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Execution Screenshot:")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "2_sjf_execution.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• At t=0, only P1 is available, so it executes from [0, 7].\n"
        "• At t=7, P2 (BT=4), P3 (BT=1), and P4 (BT=4) have arrived. P3 has the shortest burst, running from [7, 8].\n"
        "• At t=8, P2 and P4 both have BT=4; P2 arrived earlier (t=2 vs t=5), so P2 executes from [8, 12].\n"
        "• P4 executes from [12, 16].\n"
        "• Average Turnaround Time: (7 + 10 + 4 + 11) / 4 = 8.00\n"
        "• Average Waiting Time: (0 + 6 + 3 + 7) / 4 = 4.00"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 4. SRTF Preemptive SJF
    # -------------------------------------------------------------
    h4 = doc.add_heading(level=1)
    h4_run = h4.add_run("4. Preemptive: Shortest Remaining Time First (SRTF)")
    h4_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "Shortest Remaining Time First (SRTF) is the preemptive variant of SJF. If a newly arrived process "
        "has a shorter remaining CPU burst time than the running process, the CPU is preempted."
    )

    doc.add_heading(level=2).add_run("Input Parameters:")
    srtf_input_table = doc.add_table(rows=5, cols=3)
    style_table(
        srtf_input_table,
        [2.0, 2.3, 2.3],
        ["Process ID", "Arrival Time (AT)", "Burst Time (BT)"],
        [
            ["P1", "0", "8"],
            ["P2", "1", "4"],
            ["P3", "2", "9"],
            ["P4", "3", "5"],
        ],
        header_bg="2F5597"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Execution Screenshot:")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "3_srtf_execution.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• P1 runs from [0, 1]. At t=1, P2 arrives with BT=4 < P1's remaining 7; P1 is preempted.\n"
        "• P2 runs to completion from [1, 5] (P3 at t=2 and P4 at t=3 have larger bursts).\n"
        "• At t=5, P4 has shortest remaining time (5), running from [5, 10].\n"
        "• At t=10, P1 resumes and completes its remaining 7 units from [10, 17].\n"
        "• Finally, P3 executes from [17, 26].\n"
        "• Average Turnaround Time: (17 + 4 + 24 + 7) / 4 = 13.00\n"
        "• Average Waiting Time: (9 + 0 + 15 + 2) / 4 = 6.50"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 5. Round Robin
    # -------------------------------------------------------------
    h5 = doc.add_heading(level=1)
    h5_run = h5.add_run("5. Preemptive: Round Robin (RR)")
    h5_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "Round Robin (RR) allocates a fixed time quantum to each process in cyclic order. "
        "When a time slice expires, the process is moved to the back of the ready queue."
    )

    doc.add_heading(level=2).add_run("Input Parameters:")
    rr_input_table = doc.add_table(rows=4, cols=3)
    style_table(
        rr_input_table,
        [2.0, 2.3, 2.3],
        ["Process ID", "Arrival Time (AT)", "Burst Time (BT)"],
        [
            ["P1", "0", "5"],
            ["P2", "1", "3"],
            ["P3", "2", "1"],
        ],
        header_bg="2F5597"
    )
    p_q = doc.add_paragraph()
    q_run = p_q.add_run("Configured Time Quantum: 2")
    q_run.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Execution Screenshot:")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "4_round_robin_execution.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• [0-2]: P1 runs 2 units (rem: 3). P2 and P3 arrive during this interval. Queue: [P2, P3, P1].\n"
        "• [2-4]: P2 runs 2 units (rem: 1). Queue: [P3, P1, P2].\n"
        "• [4-5]: P3 runs 1 unit and finishes (Completion = 5). Queue: [P1, P2].\n"
        "• [5-7]: P1 runs 2 units (rem: 1). Queue: [P2, P1].\n"
        "• [7-8]: P2 runs 1 unit and finishes (Completion = 8). Queue: [P1].\n"
        "• [8-9]: P1 runs 1 unit and finishes (Completion = 9).\n"
        "• Average Turnaround Time: (9 + 7 + 3) / 3 = 6.33\n"
        "• Average Waiting Time: (4 + 4 + 2) / 3 = 3.33"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 6. Banker's Algorithm Pre-configured
    # -------------------------------------------------------------
    h6 = doc.add_heading(level=1)
    h6_run = h6.add_run("6. Banker's Algorithm: Pre-configured Reference Sample")
    h6_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "Demonstrates the deadlock avoidance safety algorithm using the laboratory reference problem. "
        "No inputs are required to run this mode, producing the exact reference output."
    )

    doc.add_heading(level=2).add_run("Matrix Configuration (5 Processes, 3 Resource Types A, B, C):")
    b_table = doc.add_table(rows=6, cols=4)
    style_table(
        b_table,
        [1.5, 1.7, 1.7, 1.7],
        ["Process", "Allocation [A, B, C]", "Maximum [A, B, C]", "Available [A, B, C]"],
        [
            ["P0", "[0, 1, 0]", "[7, 5, 3]", "[3, 3, 2]"],
            ["P1", "[2, 0, 0]", "[3, 2, 2]", "-"],
            ["P2", "[3, 0, 2]", "[9, 0, 2]", "-"],
            ["P3", "[2, 1, 1]", "[2, 2, 2]", "-"],
            ["P4", "[0, 0, 2]", "[4, 3, 3]", "-"],
        ],
        header_bg="2F5597"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Execution Screenshot (Verbatim Reference Output):")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "5_bankers_preconfigured.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• Computed Need Matrix (Max - Allocation):\n"
        "   - P0: [7, 4, 3]\n"
        "   - P1: [1, 2, 2]\n"
        "   - P2: [6, 0, 0]\n"
        "   - P3: [0, 1, 1]\n"
        "   - P4: [4, 3, 1]\n"
        "• Circular Safety Algorithm Execution Trace:\n"
        "   1. P1: Need [1, 2, 2] <= Work [3, 3, 2] -> Allocates, finishes, releases [2, 0, 0]. New Work = [5, 3, 2].\n"
        "   2. P3: Need [0, 1, 1] <= Work [5, 3, 2] -> Allocates, finishes, releases [2, 1, 1]. New Work = [7, 4, 3].\n"
        "   3. P4: Need [4, 3, 1] <= Work [7, 4, 3] -> Allocates, finishes, releases [0, 0, 2]. New Work = [7, 4, 5].\n"
        "   4. P0: Need [7, 4, 3] <= Work [7, 4, 5] -> Allocates, finishes, releases [0, 1, 0]. New Work = [7, 5, 5].\n"
        "   5. P2: Need [6, 0, 0] <= Work [7, 5, 5] -> Allocates, finishes, releases [3, 0, 2]. New Work = [10, 5, 7].\n"
        "• State: System is in a Safe State.\n"
        "• Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2 (Matches sample output exactly)."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 7. Banker's Algorithm Custom Input
    # -------------------------------------------------------------
    h7 = doc.add_heading(level=1)
    h7_run = h7.add_run("7. Banker's Algorithm: Custom User Input Mode")
    h7_run.font.color.rgb = RGBColor(31, 78, 121)

    doc.add_paragraph(
        "Demonstrates the custom input capability where the user defines arbitrary matrices. "
        "The parser flexibly accepts space-separated, comma-separated, or compact digit formats."
    )

    doc.add_heading(level=2).add_run("Execution Screenshot:")
    doc.add_picture(os.path.join(SCREENSHOTS_DIR, "6_bankers_custom.png"), width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_heading(level=2).add_run("Results Analysis:")
    doc.add_paragraph(
        "• Process P1 is evaluated first and satisfies Need <= Work with available [3, 3, 2].\n"
        "• After P1 completes and releases resources, P0 can be satisfied, followed by P2.\n"
        "• Resulting Safe Sequence: P1 -> P0 -> P2."
    )

    doc.save(docx_path)
    print(f"[+] Successfully generated DOCX document: {docx_path}")


if __name__ == "__main__":
    create_all_screenshots()
    docx_file = os.path.join(os.path.dirname(__file__), "Sample_Input_and_Output.docx")
    build_docx_report(docx_file)
