#from crypt import methods
#from crypt import methods


from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from rich.markup import render
from sqlalchemy.testing import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import json
from flask_mail import Mail
import os
from werkzeug.utils import secure_filename
from sympy.physics.vector.printing import params
import math
import os
from groq import Groq
from huggingface_hub import InferenceClient
from flask import request, jsonify
from dotenv import load_dotenv
import logging

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
hf_client = InferenceClient(token=os.environ.get("HF_TOKEN"))


with open('config.json', 'r') as c:
    params= json.load(c)["params"]
local_server = True
app = Flask(__name__)
app.secret_key = 'sadat@2025'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)
if (local_server):
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
# initialize the app with the extension
db = SQLAlchemy(app)

SYSTEM_INSTRUCTION = """You are a helpful assistant for London Tourism & Experts, 
    a professional pick-and-drop transport service based in London. You help tourists with questions about airport pickups, hotel transfers,
    tourist site transfers, pricing, availability, and booking. Always be freindly, professional and concise.
    if asked about booking, direct users to the contact page or WhatsApp: +44..... or email: sadat....@gmail.com.
    only anwser questions relevant to the transport service and London tourism.
    """


def groq_reply(user_message: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def hf_reply(user_message: str) -> str:
    # Use a free-tier compatible model
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user_message}
    ]
    response = hf_client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def generate_with_fallback(user_message: str) -> tuple[str, str]:
    # Providers list: Groq first (fast), Hugging Face second (stable)
    providers = [("groq", groq_reply), ("huggingface", hf_reply)]

    for name, fn in providers:
        try:
            return fn(user_message), name
        except Exception as e:
            logging.error(f"{name} failed: {e}")

    return "Our booking service is currently undergoing maintenance. Please WhatsApp us for help.", "fallback"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please send a message."}), 400

    reply, provider = generate_with_fallback(user_message)
    return jsonify({"reply": reply, "provider": provider})

# The following class is used to define the database tables that we have created

class Contacts(db.Model):
    """
    the column names: sno, name, email, phone_num, message, date
    """
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(30),nullable=False)
    phone_num = db.Column(db.String(16),nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(12),nullable=True)

class Posts(db.Model):
    """
    the column names: sno, title, image_path, content, slug
    """
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    subheadings = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255),nullable=False)
    slug = db.Column(db.String(30),nullable=False)
    """content = db.Column(db.String(500),nullable=False)"""

UPLOAD_FOLDER = 'static/assets/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    #fetch all the post
    posts = Posts.query.filter_by().all()
    # [0:params['no_of_post']]
    last = math.ceil(len(posts)/ int(params['no_of_post']))

    #pagination
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        #initial page should be one
        page = 1
    #page is considered as a string needs to casted to integer
    page = int(page)
    #page slicing
    posts = posts[(page-1)*int(params['no_of_post']) : (page-1)*int(params['no_of_post']) + int(params['no_of_post'])]
    #first page
    if (page == 1):
        prev = "#"
        next = "/?page="+ str(page+1)

    #last page
    elif (page == last):
        prev = "/?page="+ str(page-1)
        next = "#"
    #middle page
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)


    return render_template("index.html", params = params, posts = posts, prev = prev, next = next)

@app.route("/about")
def about():
    return render_template("about.html",params = params)
@app.route("/allowed_file", methods=['GET', 'POST'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # if the user is already logged in
    if ('user' in session and session['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html', params = params, posts = posts)
    # if the user wants to log in and trigger the post method
    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            # set session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params = params, posts = posts)

    else:
        return render_template("login.html", params=params)


@app.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit(sno):
    # Check if the user is logged in
    if 'user' in session and session['user'] == params['admin_user']:
        post = None
        if sno != 0:
            post = Posts.query.get(sno)  # Fetch the existing post

        if request.method == 'POST':
            box_title = request.form.get('title')
            subheadings = request.form.get('subheadings')
            slug = request.form.get('slug')
            image_path = request.form.get('image_path')
            # Handling file upload
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)  # Secure the filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save file

            if sno == 0:  # Create a new post
                new_post = Posts(title=box_title, subheadings=subheadings, slug=slug, image_path=image_path)
                db.session.add(new_post)
                db.session.commit()
            else:  # Update an existing post
                if post:
                    post.title = box_title
                    post.subheadings = subheadings
                    post.slug = slug
                    post.image_path = image_path
                    db.session.commit()  # Save changes

                    return redirect('/edit/'+sno)
                else:
                    return "Post not found", 404
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    # Check if the user is logged in
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno = sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


@app.route("/contact", methods= ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        """ Add entry to the database """
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        """
        the column names: sno, name, email, phone_num, message, date
        """
        # database_column_name = the variable that we have created above as per POST request
        entry = Contacts(name = name, email = email, phone_num = phone, message = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message (London Tourism & Experts website) from  ' + name,
                          sender = email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + "Contact No: " + phone
                          )

    return render_template("contact.html", params = params)

@app.route("/subscribe", methods= ['GET', 'POST'])
def subscribe():
    return render_template("index.html", params = params)

@app.route("/post/<string:post_slug>", methods = ['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template("post.html", params = params, post = post)
app.run(debug=True)
