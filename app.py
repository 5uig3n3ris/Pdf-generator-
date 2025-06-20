from flask import Flask, send_file, render_template_string, request
from fpdf import FPDF
import io
import os

app = Flask(__name__)

# Path to the font file
FONT_PATH = "fonts/DejaVuSans.ttf"

# Ensure font file exists
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font not found at {FONT_PATH}. Please ensure 'DejaVuSans.ttf' is in the 'fonts' directory.")

# PDF Generator Class
class PDF(FPDF):
    def header(self):
        self.add_font("DejaVu", "", FONT_PATH, uni=True)
        self.set_font("DejaVu", "", 16)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, "WordPress Security Guide for Clients", ln=True, align="C")
        self.ln(5)
        self.set_font("DejaVu", "", 12)
        self.cell(0, 10, "Keeping Your Website Safe & Secure", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("DejaVu", "", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("DejaVu", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, body)
        self.ln(5)

# Content Sections
sections = [
    ("1. Secure Your Login", [
        "- Use a strong password (12+ characters with a mix of letters, numbers, and symbols).",
        "- Enable Two-Factor Authentication (2FA) for extra security.",
        "- Never share your login details with anyone. If you need to give access, create a new user with the right role.",
        "- Change your password regularly (every few months).",
    ]),
    ("2. Keep Your Website Updated", [
        "- Always update WordPress, themes, and plugins when new versions are available.",
        "- Delete any unused plugins and themes to reduce security risks.",
        "- Use only trusted plugins from the official WordPress repository or reputable developers.",
    ]),
    ("3. Protect Against Hackers & Malware", [
        "- Use SSL (HTTPS) to protect your website and customer data.",
        "- Install a security plugin (e.g., Wordfence, Sucuri) to monitor threats.",
        "- Avoid logging into your website from public Wi-Fi without using a VPN.",
        "- Enable firewall protection to block malicious traffic.",
    ]),
    ("4. Backup Your Website Regularly", [
        "- Ensure automatic backups are set up (daily or weekly).",
        "- Store backups in a safe location (Google Drive, Dropbox, or a secure server).",
        "- Test your backups periodically to make sure they work.",
    ]),
    ("5. Manage User Access Safely", [
        "- Only give Administrator access to trusted people.",
        "- Use Editor, Author, or Contributor roles for team members who don’t need full access.",
        "- Remove old or inactive user accounts to prevent unauthorized access.",
    ]),
    ("6. Monitor & Respond to Security Alerts", [
        "- Check your email notifications for security warnings.",
        "- Scan your site for malware periodically (use a security plugin for this).",
        "- If you notice suspicious activity, contact your developer or hosting provider immediately.",
    ]),
    ("7. Final Tips", [
        "- Avoid clicking on suspicious links or emails claiming to be from WordPress.",
        "- If you ever need help, reach out to your web developer or hosting support.",
        "- Consider a maintenance plan to keep your website secure and up to date.",
    ])
]

# Homepage
@app.route('/')
def home():
    return render_template_string('''
        <h1>WordPress Security Guide Generator</h1>
        <form action="/generate_pdf" method="post">
            <button type="submit">Generate PDF</button>
        </form>
    ''')

# PDF Generation Endpoint
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        for title, points in sections:
            pdf.chapter_title(title)
            pdf.chapter_body("\n".join(points))

        pdf_buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('utf-8')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="WordPress_Security_Guide.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        app.logger.error(f"PDF generation failed: {e}")
        return "<h1>Error</h1><p>There was a problem generating the PDF. Please try again later.</p>", 500

# Global Error Handler (cleaner for production)
@app.errorhandler(500)
def handle_500(e):
    return "<h1>Internal Server Error</h1><p>Please try again later or contact support.</p>", 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
