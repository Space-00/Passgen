from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import os

# Register a standard font (Helvetica is built-in, but you can add others)
pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.afm'))
pdfmetrics.registerFont(TTFont('Helvetica-Bold', 'Helvetica-Bold.afm'))

def draw_letter(c, page_width, page_height, margins):
    """Draw the complete letter using absolute positions."""
    x_left = margins['left']
    x_right = page_width - margins['right']
    y_top = page_height - margins['top']
    y_bottom = margins['bottom']
    
    # ----- Sender block (top left) -----
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_left, y_top, "Lahleh Sahrai Co.")
    c.setFont("Helvetica", 10)
    c.drawString(x_left, y_top - 5*mm, "44 Ladan St., Banafsheh Blvd., Asmanshahr")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_left, y_top - 15*mm, "Panirforushan-e Jolgeh Co.")
    c.setFont("Helvetica", 10)
    c.drawString(x_left, y_top - 20*mm, "12 Dasht-e Mosafa")
    c.drawString(x_left, y_top - 25*mm, "Matbu Blvd.")
    c.drawString(x_left, y_top - 30*mm, "Asmanshahr")
    
    # ----- Reference & Date (right aligned) -----
    c.setFont("Helvetica", 10)
    ref_line = "Reference number: KA/sn"
    enc_line = "Enclosure: -"
    date_line = "January 1, 1994"
    c.drawRightString(x_right, y_top - 5*mm, ref_line)
    c.drawRightString(x_right, y_top - 10*mm, enc_line)
    c.drawRightString(x_right, y_top - 15*mm, date_line)
    
    # ----- Body text (starting below the address blocks) -----
    body_start_y = y_top - 45*mm  # adjust as needed
    c.setFont("Helvetica", 10)
    
    # Paragraph 1
    text1 = ("Respectfully, this is to inform you that Laleh Sahabi Company has commenced "
             "operations as of today at the address mentioned in this letter and wishes to "
             "draw your esteemed management's attention to the following points:")
    c.drawString(x_left, body_start_y, text1)
    
    # Paragraph 2
    text2 = ("Laleh Sahabi has made arrangements with foreign wholesalers to be able to "
             "import the finest cheese from Denmark to Johannesburg. We therefore take this "
             "opportunity to inform you of our readiness to supply some of your company's "
             "requirements. Furthermore, we would be most gratified if the sincere invitation "
             "of this company on the occasion of its opening day, which is 10 January of this "
             "year, is accepted by your esteemed management.")
    lines2 = split_text(c, text2, page_width - margins['left'] - margins['right'])
    y = body_start_y - 8*mm
    for line in lines2:
        c.drawString(x_left, y, line)
        y -= 4*mm
    
    # Paragraph 3
    text3 = ("Of course, if a very urgent engagement prevents your attendance, please inform us "
             "so that a number of posters and brochures, which will likely attract your interest, "
             "may be sent to you. However, if the invitation is accepted, kindly notify us by "
             "telephone so that a car is sent from the company to pick you up.")
    lines3 = split_text(c, text3, page_width - margins['left'] - margins['right'])
    for line in lines3:
        c.drawString(x_left, y, line)
        y -= 4*mm
    
    # ----- Closing and signature (near bottom) -----
    y = y - 10*mm
    c.drawString(x_left, y, "With utmost respect,")
    y -= 12*mm
    c.drawString(x_left, y, "Keyvan Akhtar Shomar")
    y -= 5*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_left, y, "Manager")

def split_text(c, text, max_width):
    """Split a long text into lines that fit within the given width."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, "Helvetica", 10) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def generate_letter(output_filename="letter.pdf"):
    """Generate the PDF letter."""
    page_width, page_height = A4  # 210mm x 297mm
    margins = {
        'top': 25*mm,
        'bottom': 20*mm,
        'left': 20*mm,
        'right': 20*mm,
    }
    c = canvas.Canvas(output_filename, pagesize=A4)
    draw_letter(c, page_width, page_height, margins)
    c.save()
    print(f"Letter generated: {output_filename}")

if __name__ == "__main__":
    generate_letter()
