from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_notes_pdf(notes):

    file_name = "Academix_Study_Notes.pdf"

    doc = SimpleDocTemplate(
        file_name
    )

    styles = getSampleStyleSheet()

    story = []


    for line in notes.split("\n"):

        story.append(
            Paragraph(
                line,
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 12)
        )


    doc.build(story)


    return file_name