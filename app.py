from flask import Flask, request
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from email.message import EmailMessage

import smtplib
import pandas

temp_file_name = "/tmp/signed_certificate.jpg"
font = ImageFont.truetype("font.ttf", 64)
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("finalyearprojectsbyhashpool@gmail.com", "ksit@12345$")


app = Flask(__name__)


def send_mail(name, email_id):
    msg = EmailMessage()
    msg['Subject'] = "Thank you for attending the workshop on \"How to Choose Right Journal\""
    msg['From'] = 'ketan.keshav79@gmail.com'
    msg['To'] = email_id
    body = "Sample Mail Body"
    msg.set_content(body)
    with open(temp_file_name, 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(
        file_data,
        maintype='application',
        subtype='octet-stream',
        filename=file_name
    )

    server.send_message(msg)


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'template' in request.files and 'data' in request.files:
        template_file = request.files['template']
        data_file = request.files['data']

        dataframe = pandas.read_csv(data_file)
        for index, row in dataframe.iterrows():
            name = row['NAME']
            email = row['EMAIL']

            unsigned_image = Image.open(template_file.stream)
            width, height = unsigned_image.size
            draw = ImageDraw.Draw(unsigned_image)
            draw.text((width/3, height/3), name, (0, 0, 0), font=font)
            unsigned_image.save(temp_file_name)

            send_mail(name, email)

        return {
            'success': True
        }

    else:
        return {
            'success': False,
            'error': 'One of the parameters are missing in form request body - template, data'
        }


app.run(host='0.0.0.0', port=9000, debug=False)
