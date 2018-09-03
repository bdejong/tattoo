import math

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import date

def digit_of_pi(which_digit):
    return int(math.pi * (10 ** which_digit)) % 10

def cumulative_distance(index, scale, offset):
    y = 0
    for i in range(index):
        y += digit_of_pi(i) * scale + offset
    return y

c = canvas.Canvas("tattoo.pdf", pagesize=A4)

c.setLineWidth(0.3)
c.setFont('Helvetica', 8)

c.rect((210 - 20) * mm, 10 * mm, 10 * mm, 10 * mm, stroke=1, fill=0)
c.drawString((210 - 19) * mm, 11 * mm, "1 cm", )

c.rect((210 - 60) * mm, 25 * mm, 50 * mm, 50 * mm, stroke=1, fill=0)
c.drawString((210 - 59)*mm, 26 * mm, "5 cm")

scale = 1
offset = 2.5
radius = 0.5
margin = 10

def special_date_in_range(start, end):
    special_dates = [
        date(1978, 6, 21), # Birthday
        date(1985, 7, 1), # Suriname
        date(2003, 5, 5), # Ingrid TODO FIXME
        date(2010, 5, 10), # Annelies
        date(2015, 9, 3), # Flux
        date(2017, 3, 6), # Volt
    ]

    for special_date in special_dates:
        if special_date >= start and special_date < end:
            return True
    
    return False

c.setLineWidth(0.7)

for i in range(100):
    year_start, year_end = date(1978 + i, 6, 21), date(1978 + i + 1, 6, 21)
    x = 10
    y = cumulative_distance(i, scale, offset) + margin

    if y >= 297 or i > 40:
        # c.drawString(x * mm, (margin/2) * mm, "{0}".format(i - 1))
        break
    
    # c.drawString((x + 5) * mm, y * mm, "{0} {1}".format(year_start, year_end))

    if special_date_in_range(year_start, year_end):
        c.line((x-radius*2) * mm, y * mm, (x+radius*2) * mm, y * mm)
    else:
        c.circle(x * mm, y * mm, radius * mm, stroke=1, fill=1)


c.save()