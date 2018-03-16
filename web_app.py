from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from saved_models.load import *
from web_app_classes.PredictionEngine import PredictionEngine
import json

UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# init flask app
app = Flask(__name__)
app.secret_key = "SSGoLSvoHlxYklrWLDEyfh9kPcebolN9HlpqHdzO0Nxd1WIuDid3rbQqePoaDFooXKyF4Me1zX8FF2I1"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('dog_names.json', 'r') as json_file:
  dog_names = json.load(json_file)
global prediction_engine
prediction_engine = PredictionEngine(init(), dog_names)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect('predict/' + filename)

  return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload>
      </form>
      '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/predict/<img_url>', methods=['GET', 'POST'])
def predict(img_url):
  res = prediction_engine.predict_breed(app.config['UPLOAD_FOLDER'] + img_url)
  return json.dumps(res)


@app.route('/testpredict', methods=['GET', 'POST'])
def testpredict():
  res = prediction_engine.predict_breed('ownImages/cat.jpg')
  return json.dumps(res)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)