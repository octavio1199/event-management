from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
from django.conf import settings
import os


def generate_event_report(event, participants):
    file_path = os.path.join(settings.MEDIA_ROOT, 'reports', f'event_report_{event.id}.pdf')

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 16)
    c.drawString(100, height - 100, f"Relatório do Evento: {event.title}")

    c.setFont("Helvetica", 12)
    y = height - 150
    for participant in participants:
        c.drawString(100, y, f"Nome: {participant.get_full_name()} | Email: {participant.email}")

        if participant.profile_image:
            image_path = participant.profile_image.path
            c.drawImage(image_path, 400, y - 20, width=50, height=50)
        y -= 80

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return file_path