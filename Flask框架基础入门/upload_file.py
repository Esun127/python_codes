from flask import Flask, request, render_template
# from werkzeug import secure_filename


app = Flask(__name__)

upload_dir = "/home/shiyanlou/Code/"
allowed_extensions = ("txt","pdf","png","jpg","jpeg")

def allowed_file(filename):
    return '.' in filename and filename.split(".")[-1] in allowed_extensions

@app.route('/', methods=['get', 'post'])
def index():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        f = request.files.get('file')
        if allowed_file(f.filename):
            f.save(upload_dir + f.filename)
            return "{} upload successed!".format(f.filename)
        else:
            return "{} upload failed.".format(f.filename)