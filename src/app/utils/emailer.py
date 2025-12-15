import yagmail
import os


def send_compliance_report(to_email: str, subject: str, summary_text: str, attachment_path: str = None, chart_path: str = None):
    """
    Sends a compliance report email with optional PDF attachment and inline chart.

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject line
        summary_text (str): Compliance summary (HTML allowed)
        attachment_path (str, optional): Path to PDF to attach
        chart_path (str, optional): Path to chart image to embed inline
    Returns:
        tuple: (success: bool, feedback: str)
    """

    try:
        # Load email credentials from env
        sender_email = os.getenv("ALERT_EMAIL")
        sender_password = os.getenv("ALERT_EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            raise ValueError("Email credentials not set. Use ALERT_EMAIL and ALERT_EMAIL_PASSWORD env vars.")

        yag = yagmail.SMTP(sender_email, sender_password)

        # HTML email body
        html_content = f"""
        <html>
        <body>
            <h2>📋 Compliance Report</h2>
            <p>{summary_text}</p>
        """

        html_content += """
        <br>
        <p>Regards,<br>AI Compliance Checker</p>
        </body>
        </html>
        """

        contents = [yagmail.inline(html_content)]

        if chart_path:
            contents.append(yagmail.inline(chart_path))  

        if attachment_path:
            contents.append(attachment_path)

        yag.send(
            to=to_email,
            subject=subject,
            contents=contents
        )

        return True, f"Compliance report sent to {to_email}"

    except Exception as e:
        return False, f" Failed to send email: {str(e)}"
