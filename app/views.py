from app import app   # 'app' director is a package, import from app __init__

from flask import render_template, request, redirect, jsonify, make_response

from datetime import datetime

import os

from werkzeug.utils import secure_filename

@app.template_filter('clean_date')
def clean_date(dt):
	return dt.strftime("%d %b %Y")

@app.route('/')
def index():



	# print(f" Flask ENV is set to: {app.config['ENV']}")

	return render_template('public/index.html')

@app.route('/jinja')
def jinja():

	my_name = 'Shakib'

	age = 20

	langs = ['Python', 'JavaScript', 'C', 'C++']

	friends = {
		"Anne": 22,
		"Tom": 27,
		"Amanda": 26,
		"John": 17
	}

	colours = {"Red", "Green"}

	cool = True

	class GitRemote:
		def __init__(self, name, description, url):
			self.name = name
			self.description = description
			self.url = url
		def pull(self):
			return f"Pulling repo {self.name}"

		def clone(self):
			return f"Cloning into {self.url}"

	my_remote = GitRemote(
		name = "Flask Jinja",
		description = "Template design tutorial",
		url = "https://github.com/julian-nash/jinja.git"
		)

	def repeat(x, qty):
		return x * qty

	date = datetime.utcnow()

	my_html = '<h1>THIS IS SOME HTML</h1>'

	suspicious = "<script>alert('You got hacked')</script>"
	return render_template(
		'public/jinja.html', 
		 my_name=my_name,
		 age = age,
		 langs = langs,
		 friends = friends,
		 colours = colours,
		 cool = cool,
		 GitRemote = GitRemote,
		 repeat = repeat,
		 my_remote = my_remote,
		 date = date,
		 my_html = my_html,
		 suspicious = suspicious)

@app.route('/about')
def about():
	return render_template('public/about.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

	if request.method == 'POST':

		req = request.form  # like a python dictionary

		# 3 Ways to get form data
		username = req['username']
		email = req.get('email')
		password = request.form.get('password')
		print(username, email, password)

		return redirect(request.url)

	return render_template('public/sign_up.html')

users = {
	"mitsuhiko":{
		"name": "Armin Ronacher",
		"bio": "assss",
		"twitter_handle": "@mitsuhiko"
	},
	"gvanrossum":{
		"name": "Guido Van Rossum",
		"bio": "ggaassssss",
		"twitter_handle": "@gvanrossum"
	},
	"elonmusk":{
		"name": "Elon Musk",
		"bio": "eelmmassss",
		"twitter_handle": "@elonmusk"
	}
}

@app.route('/profile/<username>')
def profile(username):

	user = None

	if username in users:
		user = users[username]


	return render_template('public/profile.html', username=username, user=user)



@app.route('/multiple/<foo>/<bar>/<baz>')
def multi(foo, bar, baz):
	return f"foo is {foo}, bar is {bar}, baz is {baz} "


@app.route('/json', methods=["POST"])
def json():

	if request.is_json:
		req = request.get_json()  # 'req' is a Python Dictionary
		
		response = {
			"message": "JSON received",
			"name": req.get('name')
		}

		res = make_response(jsonify(response), 200)

		return res

	else:

		res = make_response(jsonify({"message": "No JSON received"}), 200)

		return res


@app.route('/guestbook')
def guestbook():
	return render_template('public/guestbook.html')


@app.route('/guestbook/create-entry', methods=['POST'])
def create_entry():

	req = request.get_json()

	res = make_response(jsonify(req), 200)

	return res


@app.route('/query')
def query():

	if request.args:

		args = request.args # 'args' is like a dictionary

		serialized = ", ".join(f"{k}: {v}" for k, v in args.items())
	

		return f"(query) {serialized}", 200

	else:

		return "No query received", 200



app.config["IMAGE_UPLOADS"] = "C:/Users/AS/Anaconda3/envs/tensorflow_env/flask/flask_julian/code/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5*1024*1024
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024

def allowed_image(filename):
	if not "." in filename:
		return False

	ext = filename.rsplit(".", 1)[1]

	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False


def allowed_image_filesize(filesize):
	if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
		return True
	else:
		return False

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():

	if request.method == 'POST':

		if not allowed_image_filesize(request.cookies.get('filesize')):
			print("File exceeded maximum size")
			# return redirect(request.url)  
			# return render_template('public/upload_image.html')

		image = request.files['image']

		if image.filename == "":
			print("Image must have a filename")
			return redirect(request.url)

		if not allowed_image(image.filename):
			print("That image extension is not allowed")
			return redirect(request.url)

		else:
			filename = secure_filename(image.filename)
			image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
			print("Image Saved")
			return redirect(request.url)

	return render_template('public/upload_image.html')
