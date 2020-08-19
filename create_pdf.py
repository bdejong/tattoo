import math

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import date

def digit_of_pi(which_digit):
    return int(math.pi * (10 ** which_digit)) % 10

def get_distance(index, scale, offset):
    return digit_of_pi(index) * scale + offset

def draw_boxes(c):
    c.rect((210 - 20) * mm, 10 * mm, 10 * mm, 10 * mm, stroke=1, fill=0)
    c.drawString((210 - 19) * mm, 11 * mm, "1 cm", )

    c.rect((210 - 60) * mm, 25 * mm, 50 * mm, 50 * mm, stroke=1, fill=0)
    c.drawString((210 - 59)*mm, 26 * mm, "5 cm")

def create_page(c):
    c.setLineWidth(0.3)
    c.setFont('Courier', 5)
    draw_boxes(c)
    c.setLineWidth(0.7)

def special_date_in_range(start, end):
    special_dates = [
        date(1978, 6, 21), # Birthday
        date(1985, 7, 1), # Suriname
        date(2003, 7, 1), # Ingrid
        date(2010, 5, 10), # Annelies
        date(2015, 9, 3), # Flux
        date(2017, 3, 6), # Volt
        date(2019, 11, 2), # Lumen
    ]

    for special_date in special_dates:
        if special_date >= start and special_date < end:
            return True
    
    return False

SCALE = 1.1
OFFSET = 1.9
RADIUS = 0.4
MARGIN = 10

c = canvas.Canvas("tattoo.pdf", pagesize=A4)
create_page(c)

i = 0
x = 10
y = 0

while i <= 41:
    is_special = special_date_in_range(date(1978 + i, 6, 21), date(1978 + i + 1, 6, 21))
    
    text_x = (x + 15) * mm
    text_y = (y + MARGIN - 1 + 1) * mm
    
    text = "age: {0}   pi: {1}   can be tattooed after: {2}".format(
        i + 1,
        digit_of_pi(i),
        date(1978 + i + 1, 6, 21)
    )

    c.drawString(text_x, text_y, text)

    dot_y = (y + MARGIN) * mm
    if is_special:
        c.line((x - RADIUS * 2) * mm, dot_y, (x + RADIUS * 2) * mm, dot_y)
        dot_x_max = (x + RADIUS * 2) * mm
    else:
        c.circle(x * mm, (y + MARGIN) * mm, RADIUS * mm, stroke=1, fill=1)
        dot_x_max = (x + RADIUS) * mm
    
    c.line(dot_x_max + 5*mm, dot_y, text_x - mm, text_y)

    y += get_distance(i, SCALE, OFFSET)
    i += 1

    if y >= 297 - 2 * MARGIN:
        c.showPage()
        y = 0
        i -= 20
        create_page(c)

c.save()
