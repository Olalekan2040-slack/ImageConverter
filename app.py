from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return render_template('index.html', error='No image provided')

    image = request.files['image']
    image_data = image.read()
    img = Image.open(io.BytesIO(image_data))

    text = pytesseract.image_to_string(img)

    return render_template('index.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)
