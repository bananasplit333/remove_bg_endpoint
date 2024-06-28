from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No file found", 400

    received_img = request.files['image']

    try:
        #process the image, remove bg
        print('processing file ', received_img)
        input = Image.open(received_img)
        output = remove(input)

        #process further using BytesIO
        #cannot pass Image directly to send_file
        output_io = BytesIO()
        output.save(output_io, 'PNG')
        output_io.seek(0) #move cursor back to the beginning of data

        return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='processed_output.png')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
