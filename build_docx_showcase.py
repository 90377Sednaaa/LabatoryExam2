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
    """Builds the Word document containing solely the execution screenshots and section headings."""
    doc = docx.Document()

    # Standard Page Margins (0.75 inch for maximum screenshot display area)
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_run = title_p.add_run("OPERATING SYSTEMS - LABORATORY EXAM 2\n")
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(20)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(31, 78, 121)

    sub_run = title_p.add_run("Program Execution Screenshots (Sample Input & Output)")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(89, 89, 89)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # List of all screenshots with clean titles
    items = [
        (
            "1. First-Come, First-Served (FCFS) [Non-Preemptive]",
            "1_fcfs_execution.png"
        ),
        (
            "2. Shortest Job First (SJF) [Non-Preemptive]",
            "2_sjf_execution.png"
        ),
        (
            "3. Shortest Remaining Time First (SRTF) [Preemptive SJF]",
            "3_srtf_execution.png"
        ),
        (
            "4. Round Robin (RR, Quantum = 2) [Preemptive]",
            "4_round_robin_execution.png"
        ),
        (
            "5. Banker's Algorithm (Pre-configured Reference Sample)",
            "5_bankers_preconfigured.png"
        ),
        (
            "6. Banker's Algorithm (Custom User Matrix Input)",
            "6_bankers_custom.png"
        ),
    ]

    for idx, (heading_text, img_filename) in enumerate(items):
        # Section Heading
        h = doc.add_heading(level=1)
        h_run = h.add_run(heading_text)
        h_run.font.name = "Calibri"
        h_run.font.size = Pt(14)
        h_run.font.bold = True
        h_run.font.color.rgb = RGBColor(31, 78, 121)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(6)

        # Centered Screenshot
        img_path = os.path.join(SCREENSHOTS_DIR, img_filename)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(14)
        doc.add_picture(img_path, width=Inches(6.6))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Optional page break between screenshots (except the last one)
        if idx < len(items) - 1:
            doc.add_page_break()

    doc.save(docx_path)
    print(f"[+] Successfully generated DOCX containing only screenshots: {docx_path}")


if __name__ == "__main__":
    create_all_screenshots()
    docx_file = os.path.join(os.path.dirname(__file__), "Sample_Input_and_Output.docx")
    build_docx_report(docx_file)
