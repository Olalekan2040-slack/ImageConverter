from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image, UnidentifiedImageError
import io

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_images():
    images = request.files.getlist('images')

    if not images:
        return render_template('index.html', error='No images provided')

    texts = []

    for image in images:
        try:
            image_data = image.read()
            img = Image.open(io.BytesIO(image_data))
            text = pytesseract.image_to_string(img)
            texts.append(text.strip())
        except UnidentifiedImageError as e:
            texts.append(f"Error: {str(e)}")

    return render_template('index.html', texts=text)


if __name__ == '__main__':
    app.run(debug=True)
