# from flask import Flask, render_template, request
#
# app = Flask(__name__)
#
# @app.route('/login', methods=['post', 'get'])
# def login():
#     message = ''
#     if request.method == 'POST':
#         source = request.form.get('src')  # access the data inside
#         destination = request.form.get('dst')
#
#         message = "Source: "+source + "Destination: " + destination
#
#     return render_template('login.html', message=message)
#
#
# @app.route('/')
# def index():
#     return render_template("index.html")

from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='template')

lt = [1, 2, 3]

img = ["1.jpg", "2.jpg", "3.jpg"]

picFolder = os.path.join('static', 'pics')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder
img = [os.path.join(app.config['UPLOAD_FOLDER'], '1.jpg'), os.path.join(app.config['UPLOAD_FOLDER'], '2.jpg'),
       os.path.join(app.config['UPLOAD_FOLDER'], '3.jpg')]


@app.route('/')
def index():
    return render_template("index1.html", len=len(lt), lt=lt, img=img)


if __name__ == '__main__':
    app.run(debug=True)