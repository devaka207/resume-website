#!/usr/bin/env python3
"""
Generate WD_MTProject Submission PDF
Author: Akshay Hegde (akshayshridhar)
Pure Python PDF 1.4 Generator - Zero External Dependencies Required
"""

import sys
import os

class PDFBuilder:
    def __init__(self, filename="RollNo_WD_MTProject.pdf"):
        self.filename = filename
        self.pages = []
        self.width = 595.0   # A4 width in points
        self.height = 842.0  # A4 height in points

    def add_page(self):
        page = PageBuilder(self.width, self.height)
        self.pages.append(page)
        return page

    def save(self):
        objects = []
        
        # Obj 1: Catalog
        # Obj 2: Pages
        # Obj 3: Font Helvetica
        # Obj 4: Font Helvetica-Bold
        # Obj 5: Font Helvetica-Oblique
        # Obj 6: Font Courier
        # Then for each page: Page Obj, Content Stream Obj
        
        font_helv = 3
        font_bold = 4
        font_oblique = 5
        font_courier = 6
        
        page_objs = []
        content_objs = []
        
        current_obj_id = 7
        for _ in self.pages:
            page_objs.append(current_obj_id)
            current_obj_id += 1
            content_objs.append(current_obj_id)
            current_obj_id += 1
            
        # 1: Catalog
        catalog = f"<< /Type /Catalog /Pages 2 0 R >>"
        
        # 2: Pages
        kids_str = " ".join([f"{pid} 0 R" for pid in page_objs])
        pages_dict = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(self.pages)} >>"
        
        f1 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        f2 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        f3 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"
        f4 = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>"
        
        raw_objects = [
            (1, catalog),
            (2, pages_dict),
            (3, f1),
            (4, f2),
            (5, f3),
            (6, f4),
        ]
        
        for i, page in enumerate(self.pages):
            pid = page_objs[i]
            cid = content_objs[i]
            
            p_dict = (
                f"<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {self.width} {self.height}] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R /F4 6 0 R >> >> "
                f"/Contents {cid} 0 R >>"
            )
            raw_objects.append((pid, p_dict))
            
            stream_content = page.get_stream()
            stream_len = len(stream_content.encode('latin1'))
            c_dict = f"<< /Length {stream_len} >>\nstream\n{stream_content}\nendstream"
            raw_objects.append((cid, c_dict))
            
        # Write PDF file
        with open(self.filename, 'wb') as f:
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            
            offsets = {}
            for oid, ocontent in raw_objects:
                offsets[oid] = f.tell()
                f.write(f"{oid} 0 obj\n{ocontent}\nendobj\n".encode('latin1'))
                
            xref_offset = f.tell()
            f.write(f"xref\n0 {len(raw_objects) + 1}\n".encode('latin1'))
            f.write(b"0000000000 65535 f \n")
            for oid in range(1, len(raw_objects) + 1):
                f.write(f"{offsets[oid]:010d} 00000 n \n".encode('latin1'))
                
            f.write(f"trailer\n<< /Size {len(raw_objects) + 1} /Root 1 0 R >>\n".encode('latin1'))
            f.write(f"startxref\n{xref_offset}\n%%EOF\n".encode('latin1'))
            
        print(f"Successfully generated: {self.filename}")


class PageBuilder:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.commands = []

    def rgb(self, r, g, b):
        return f"{r:.3f} {g:.3f} {b:.3f}"

    def rect(self, x, y, w, h, fill=None, stroke=None, line_width=1.0):
        cmd = []
        if line_width:
            cmd.append(f"{line_width:.2f} w")
        if stroke:
            cmd.append(f"{self.rgb(*stroke)} RG")
        if fill:
            cmd.append(f"{self.rgb(*fill)} rg")
        cmd.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill and stroke:
            cmd.append("B")
        elif fill:
            cmd.append("f")
        elif stroke:
            cmd.append("S")
        self.commands.append(" ".join(cmd))

    def line(self, x1, y1, x2, y2, stroke=(0, 0, 0), line_width=1.0):
        self.commands.append(f"{line_width:.2f} w {self.rgb(*stroke)} RG {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def escape_text(self, text):
        replacements = {
            '\\': '\\\\',
            '(': '\\(',
            ')': '\\)',
            '\u2022': '\x95',  # bullet in WinAnsiEncoding
            '\u2013': '\x96',  # en-dash
            '\u2014': '\x97',  # em-dash
            '\u201c': '\x93',  # left double quote
            '\u201d': '\x94',  # right double quote
            '\u2018': '\x91',  # left single quote
            '\u2019': '\x92',  # right single quote
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # Any other non-latin1 characters replace with ascii
        clean_chars = []
        for ch in text:
            if ord(ch) < 256:
                clean_chars.append(ch)
            else:
                clean_chars.append('-')
        return "".join(clean_chars)

    def text(self, x, y, text_str, font="/F1", size=10, color=(0, 0, 0)):
        escaped = self.escape_text(text_str)
        self.commands.append(
            f"BT {font} {size:.2f} Tf {self.rgb(*color)} rg 1 0 0 1 {x:.2f} {y:.2f} Tm ({escaped}) Tj ET"
        )

    def draw_wrapped_text(self, x, y, max_width, text_str, font="/F1", size=9.5, color=(0, 0, 0), line_height=13):
        words = text_str.split(" ")
        lines = []
        cur_line = []
        
        # Approximate char width for Helvetica: ~0.52 * size
        char_w = size * 0.51
        max_chars = int(max_width / char_w)
        
        for w in words:
            test_line = " ".join(cur_line + [w])
            if len(test_line) <= max_chars:
                cur_line.append(w)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
            
        cur_y = y
        for l in lines:
            self.text(x, cur_y, l, font=font, size=size, color=color)
            cur_y -= line_height
        return cur_y

    def get_stream(self):
        return "\n".join(self.commands)


def build_submission_pdf(roll_no="25129999", filename=None):
    if filename is None:
        filename = f"{roll_no}_WD_MTProject.pdf"
        
    doc = PDFBuilder(filename)
    
    # -------------------------------------------------------------
    # PAGE 1
    # -------------------------------------------------------------
    p1 = doc.add_page()
    
    # Top decorative brand bar
    p1.rect(0, 836, 595, 6, fill=(0.145, 0.388, 0.921)) # #2563eb
    
    # Header Title
    p1.text(40, 804, "Web Development Mid-Term Project", font="/F2", size=18, color=(0.059, 0.090, 0.165))
    p1.text(40, 788, "CSS Enhancement & Design Decisions Write-up", font="/F2", size=10.5, color=(0.145, 0.388, 0.921))
    
    # Student metadata on the right
    p1.text(380, 806, f"Student: Akshay Hegde", font="/F2", size=9.5, color=(0.059, 0.090, 0.165))
    p1.text(380, 792, f"Roll No: {roll_no}", font="/F2", size=9.5, color=(0.145, 0.388, 0.921))
    p1.text(380, 778, "Date: November 2026", font="/F1", size=8.5, color=(0.392, 0.455, 0.545))
    
    # Divider line
    p1.line(40, 770, 555, 770, stroke=(0.886, 0.910, 0.941), line_width=1)
    
    # Mandatory Links Highlight Box
    p1.rect(40, 706, 515, 54, fill=(0.937, 0.965, 1.0), stroke=(0.749, 0.859, 0.996), line_width=1.2)
    
    p1.text(54, 744, "LIVE WEBSITE LINK (GITHUB PAGES):", font="/F2", size=7.5, color=(0.118, 0.251, 0.686))
    p1.text(54, 730, "https://devaka207.github.io/resume-website/", font="/F2", size=9.5, color=(0.145, 0.388, 0.921))
    
    p1.text(310, 744, "GITHUB REPOSITORY LINK:", font="/F2", size=7.5, color=(0.118, 0.251, 0.686))
    p1.text(310, 730, "https://github.com/devaka207/resume-website", font="/F2", size=9.5, color=(0.145, 0.388, 0.921))
    
    # Section 1: Executive Summary
    p1.rect(40, 680, 4, 13, fill=(0.145, 0.388, 0.921))
    p1.text(48, 682, "1. Executive Summary & Objective", font="/F2", size=11, color=(0.059, 0.090, 0.165))
    
    summary_text = (
        "The objective of this assignment was to apply modern CSS fundamentals to transform an initial "
        "semantic HTML personal resume into an executive-grade, fully responsive portfolio website. "
        "The site showcases my professional journey as an AI FinTech Founder & Product Strategist "
        "(Founder & CEO @ FinnDot, Ex-CEO @ Anomapro - acquired by Watad Group, Ex-Product Manager @ Chara, "
        "and IIM Bangalore FinTech alumnus). The implementation centers on establishing high visual "
        "hierarchy, responsive grid positioning, custom CSS variables, and fluid readability across devices."
    )
    p1.draw_wrapped_text(40, 666, 515, summary_text, font="/F1", size=8.5, color=(0.2, 0.255, 0.333), line_height=11.2)
    
    # Section 2: Key Improvements & CSS Concepts Applied
    p1.rect(40, 584, 4, 13, fill=(0.145, 0.388, 0.921))
    p1.text(48, 586, "2. Key Improvements & CSS Concepts Applied", font="/F2", size=11, color=(0.059, 0.090, 0.165))
    
    # 4 Feature Cards (2x2 Grid)
    # Row 1 Left: Typography
    p1.rect(40, 498, 250, 74, fill=(0.973, 0.980, 0.988), stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p1.text(50, 558, "A. Typography & Readability", font="/F2", size=8.8, color=(0.059, 0.090, 0.165))
    p1.draw_wrapped_text(50, 545, 230, "Integrated Google Fonts (Plus Jakarta Sans for prominent headings and Inter for crisp reading). Used fluid clamp() font sizing, balanced line-heights (1.6), and letter-spacing.", font="/F1", size=7.8, color=(0.278, 0.333, 0.416), line_height=10)
    
    # Row 1 Right: Color Palette & Variables
    p1.rect(305, 498, 250, 74, fill=(0.973, 0.980, 0.988), stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p1.text(315, 558, "B. Color System & CSS Variables", font="/F2", size=8.8, color=(0.059, 0.090, 0.165))
    p1.draw_wrapped_text(315, 545, 230, "Defined comprehensive custom properties (:root) for an Executive Tech palette: Deep Slate (#0f172a), Brand Blue (#2563eb), Cyan Accent (#0ea5e9), and soft slate surfaces with WCAG contrast.", font="/F1", size=7.8, color=(0.278, 0.333, 0.416), line_height=10)
    
    # Row 2 Left: Navigation & Positioning
    p1.rect(40, 414, 250, 74, fill=(0.973, 0.980, 0.988), stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p1.text(50, 474, "C. Sticky Navigation & Blur", font="/F2", size=8.8, color=(0.059, 0.090, 0.165))
    p1.draw_wrapped_text(50, 461, 230, "Positioned fixed/sticky top navigation (position: sticky; top: 0) with translucent frosted glass (backdrop-filter: blur(12px)), active scroll spy, and animated underline transitions.", font="/F1", size=7.8, color=(0.278, 0.333, 0.416), line_height=10)
    
    # Row 2 Right: Flexbox & CSS Grid
    p1.rect(305, 414, 250, 74, fill=(0.973, 0.980, 0.988), stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p1.text(315, 474, "D. Flexbox & CSS Grid Structure", font="/F2", size=8.8, color=(0.059, 0.090, 0.165))
    p1.draw_wrapped_text(315, 461, 230, "Employed Flexbox for navigation alignment, action buttons, and stat counters. Constructed responsive 2 & 3 column card grids using repeat(auto-fit, minmax(...)) for automatic reflow.", font="/F1", size=7.8, color=(0.278, 0.333, 0.416), line_height=10)

    # Section 3: CSS Selectors Organization
    p1.rect(40, 390, 4, 13, fill=(0.145, 0.388, 0.921))
    p1.text(48, 392, "3. Efficient CSS Selectors & Architecture", font="/F2", size=11, color=(0.059, 0.090, 0.165))
    
    bullets = [
        ("Element Selectors: ", "Applied universal box-sizing reset (*, *::before, *::after { box-sizing: border-box; }) and reset base headings, body text, lists, and inputs to create predictable box modeling."),
        ("Class Selectors: ", "Built modular, reusable component classes (.card, .btn, .btn-primary, .badge-pill, .grid-2, .grid-3) ensuring clean maintainability and preventing styling duplication."),
        ("ID Selectors: ", "Targeted primary page landmarks (#hero, #about, #ventures, #experience, #skills, #education, #contact) facilitating smooth in-page navigation anchors with offset scroll padding."),
        ("Attribute & Pseudo-Selectors: ", "Styled form fields using input[type='email'], hover states (:hover), active navigation (:active, .active-nav), and timeline connectors using ::before and ::after pseudo-elements."),
    ]
    
    cur_y = 374
    for title, desc in bullets:
        p1.text(40, cur_y, "\x95", font="/F2", size=9, color=(0.145, 0.388, 0.921))
        p1.text(48, cur_y, title, font="/F2", size=8.5, color=(0.059, 0.090, 0.165))
        title_len = len(title) * 4.8
        rem_text = desc
        p1.draw_wrapped_text(48 + title_len, cur_y, 505 - title_len, rem_text, font="/F1", size=8.2, color=(0.2, 0.255, 0.333), line_height=11)
        cur_y -= 25

    # Bottom Page 1 Footer
    p1.line(40, 45, 555, 45, stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p1.text(40, 32, "Web Development Mid-Term Project • Personal Resume Enhancement", font="/F1", size=8, color=(0.584, 0.647, 0.722))
    p1.text(500, 32, "Page 1 of 2", font="/F2", size=8, color=(0.584, 0.647, 0.722))

    # -------------------------------------------------------------
    # PAGE 2
    # -------------------------------------------------------------
    p2 = doc.add_page()
    
    # Top decorative brand bar
    p2.rect(0, 836, 595, 6, fill=(0.145, 0.388, 0.921))
    
    # Header Mini Bar
    p2.text(40, 808, "Web Development Mid-Term Project", font="/F2", size=13, color=(0.059, 0.090, 0.165))
    p2.text(40, 794, "Section-by-Section Architecture & Design Decisions", font="/F2", size=9.5, color=(0.145, 0.388, 0.921))
    p2.text(420, 800, f"Roll No: {roll_no} • Akshay Hegde", font="/F1", size=8.5, color=(0.392, 0.455, 0.545))
    
    p2.line(40, 784, 555, 784, stroke=(0.886, 0.910, 0.941), line_width=1)

    # Section 4: Breakdown of Website Sections
    p2.rect(40, 762, 4, 13, fill=(0.145, 0.388, 0.921))
    p2.text(48, 764, "4. Section-by-Section Architecture & Design Decisions", font="/F2", size=11, color=(0.059, 0.090, 0.165))

    sections_info = [
        ("Hero Section (#hero)", 
         "Combines a strong personal value statement, quote, and live status badge with an interactive floating Profile Card. Styled with subtle background radial gradients, CSS keyframe pulse animation, and an avatar with multi-stop linear gradients. Call-to-action buttons feature tactile lift on hover (transform: translateY(-2px))."),
         
        ("About & Pillars (#about)", 
         "Features a 3-column CSS Grid highlighting core domains: AI FinTech, Fraud Intelligence, and 0-to-1 Product Strategy. Each card incorporates color-tinted SVG icon wrappers, clear typography, and subtle border-color shifts upon mouse hover."),
         
        ("Ventures & Products (#ventures)", 
         "Dedicated showcase for flagship initiatives: FinnDot (Active AI FinTech venture), Anomapro (Fraud intelligence company acquired by Watad Group), and Chara Technologies (DeepTech EV mobility). Custom badges (.status-acquired in purple) visually communicate venture outcomes."),
         
        ("Experience Timeline (#experience)", 
         "Built a chronological timeline using CSS absolute positioning for circular node markers and a connecting linear-gradient vertical bar (::before). Career roles at FinnDot, Watad Group, Chara, Sirma, and APPZUI are organized with quantitative metrics, tags, and date pills."),
         
        ("Skills & Competencies (#skills)", 
         "Presents strategic business development and customer data intelligence using customized progress meters with gradient progress bars. Accompanied by a flex-wrapping tag cloud (.cloud-badge) with interactive pill-shaped hover effects."),
         
        ("Education & Credentials (#education)", 
         "Features the prestigious Executive FinTech Programme at IIM Bangalore and B.E. at DSCE Bangalore, accompanied by verified badges for Google Certified Associate Android Developer, MATLAB Onramp, and published scientific research on Assistive Devices."),
         
        ("Contact & Interactive Form (#contact)", 
         "A split-column layout providing direct communication pills (Email, LinkedIn, GitHub) alongside a responsive form. Form inputs feature custom focus rings (box-shadow: 0 0 0 3px rgba(37,99,235,0.15)) and accessible contrast ratios.")
    ]

    cur_y = 744
    for sec_title, sec_desc in sections_info:
        p2.rect(40, cur_y - 48, 515, 54, fill=(0.973, 0.980, 0.988), stroke=(0.886, 0.910, 0.941), line_width=0.7)
        p2.text(50, cur_y - 6, sec_title, font="/F2", size=8.8, color=(0.059, 0.090, 0.165))
        p2.draw_wrapped_text(50, cur_y - 18, 495, sec_desc, font="/F1", size=7.8, color=(0.2, 0.255, 0.333), line_height=10.2)
        cur_y -= 60

    # Section 5: Responsive Strategy & Hosting
    p2.rect(40, 314, 4, 13, fill=(0.145, 0.388, 0.921))
    p2.text(48, 316, "5. Responsive Media Queries & GitHub Hosting", font="/F2", size=11, color=(0.059, 0.090, 0.165))
    
    resp_text = (
        "Mobile-First Responsiveness: Implemented three distinct responsive breakpoints using CSS Media Queries: "
        "@media (max-width: 992px) collapses side-by-side hero and form layouts; @media (max-width: 768px) transforms "
        "the desktop navbar into a slide-down mobile drawer toggle and collapses 2/3 column grids into single-column flows; "
        "and @media (max-width: 480px) stacks CTA button clusters and stats vertically for ergonomic mobile tap access."
    )
    p2.draw_wrapped_text(40, 300, 515, resp_text, font="/F1", size=8.2, color=(0.2, 0.255, 0.333), line_height=11.2)
    
    host_text = (
        "GitHub Pages Hosting: The repository is configured at https://github.com/devaka207/resume-website and served "
        "live via GitHub Pages at https://devaka207.github.io/resume-website/. The repository maintains clean separation "
        "between HTML semantic structure (index.html), modular styling (styles.css), and interactive behavior (script.js)."
    )
    p2.draw_wrapped_text(40, 246, 515, host_text, font="/F1", size=8.2, color=(0.2, 0.255, 0.333), line_height=11.2)

    # Verification Box
    p2.rect(40, 160, 515, 48, fill=(0.941, 0.988, 0.957), stroke=(0.655, 0.922, 0.765), line_width=1)
    p2.text(52, 192, "SUBMISSION CHECKLIST & VERIFICATION", font="/F2", size=8, color=(0.024, 0.373, 0.275))
    p2.text(52, 178, "[X] Live Link included   [X] GitHub Repo included   [X] Design decisions explained   [X] Responsive CSS validated", font="/F1", size=8, color=(0.059, 0.255, 0.188))
    p2.text(52, 166, f"File Name: {filename}   |   Roll Number: {roll_no}   |   Submission Mode: Computer Browser PDF", font="/F2", size=7.8, color=(0.024, 0.373, 0.275))

    # Bottom Page 2 Footer
    p2.line(40, 45, 555, 45, stroke=(0.886, 0.910, 0.941), line_width=0.8)
    p2.text(40, 32, "Web Development Mid-Term Project • Personal Resume Enhancement", font="/F1", size=8, color=(0.584, 0.647, 0.722))
    p2.text(500, 32, "Page 2 of 2", font="/F2", size=8, color=(0.584, 0.647, 0.722))

    doc.save()
    return filename

if __name__ == "__main__":
    roll = sys.argv[1] if len(sys.argv) > 1 else "25129999"
    out_name = f"{roll}_WD_MTProject.pdf"
    build_submission_pdf(roll, out_name)
