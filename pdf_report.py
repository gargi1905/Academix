from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(username, score, total, quiz, answers):

    filename = f"{username}_Result.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>ACADEMIX QUIZ REPORT</b>", styles["Title"]))

    story.append(Paragraph(f"Student : {username}", styles["Normal"]))

    story.append(Paragraph(f"Score : {score}/{total}", styles["Normal"]))

    story.append(
        Paragraph(
            f"Percentage : {round(score/total*100,2)}%",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    for i, q in enumerate(quiz):

        story.append(
            Paragraph(
                f"<b>Question {i+1}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                q["question"],
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Your Answer : {answers[i]}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Correct Answer : {q['answer']}",
                styles["BodyText"]
            )
        )

        if "explanation" in q:

            story.append(
                Paragraph(
                    q["explanation"],
                    styles["Italic"]
                )
            )

        story.append(
            Paragraph("<br/>", styles["BodyText"])
        )

    doc.build(story)

    return filename