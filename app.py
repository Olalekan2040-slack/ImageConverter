from flask import Flask, render_template, request, jsonify, Response
import pytesseract
from PIL import Image, UnidentifiedImageError
import io
from fpdf import FPDF

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return render_template('home.html', error='No image provided')

    image = request.files['image']
    
    try:
        image_data = image.read()
        img = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(img)
    except UnidentifiedImageError as e:
        return render_template('home.html', error=f"Error: {str(e)}")

    if text.strip():
        return render_template('home.html', text=text)
    else:
        return render_template('home.html', no_text=True)

@app.route('/convert_to_pdf', methods=['GET'])
def convert_to_pdf():
    extracted_text = request.args.get('text')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, extracted_text)
    
    pdf_output = io.BytesIO()
    pdf_output.seek(0)
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    
    return Response(pdf_output, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename=converted_text.pdf'})

@app.route('/convert_to_word', methods=['GET'])
def convert_to_word():
    extracted_text = request.args.get('text')
    
    response = Response(extracted_text, mimetype='text/plain', headers={'Content-Disposition': 'attachment; filename=converted_text.txt'})
    return response

if __name__ == '__main__':
    app.run(debug=False)
