from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename

from common.crop_video import CropVideo

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/crop', methods=['POST'])
def crop_video():
    if request.method == 'POST':
        hour = request.form['hour']
        minutes = request.form['minutes']
        seconds = request.form['seconds']
        start = f'{hour}:{minutes}:{seconds}'
        duration = int(request.form['duration'])
        file = request.files['video_file']
        filename = secure_filename(file.filename)
        filepath = f'files/{filename}'
        file.save(filepath)
        print(f'Start: {start} || Duration: {duration} || File: {filepath}')

        crop = CropVideo(start, duration, filepath)
        outpath = crop.get_gif()
        return redirect(outpath)
    else:
        return 'Method not allowed'


if __name__ == '__main__':
    app.run()
