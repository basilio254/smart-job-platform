import os
import json
from flask import (
    Flask, render_template, request, redirect, 
    url_for, flash, jsonify
)
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, UserMixin, login_user, 
    logout_user, login_required, current_user
)
from dotenv import load_dotenv
from bson.objectid import ObjectId # Import ObjectId
import openai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- 1. CONFIGURATION ---
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
if not app.config["MONGO_URI"]:
    raise RuntimeError("MONGO_URI is not set in .env file.")

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("FLASK_SECRET_KEY is not set in .env file.")
    
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in .env file.")

# --- 2. INITIALIZE EXTENSIONS ---
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # Redirect to 'login' page if not logged in
login_manager.login_message_category = "info" # Bootstrap class for flash message

# --- 3. FLASK-LOGIN USER MODEL ---
# We need to create a User class that works with Flask-Login
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.password_hash = user_doc["password_hash"]
        self.skills = user_doc.get("skills", []) # Get skills, default to empty list

    @staticmethod
    def get(user_id):
        """Static method to get a user by their ID."""
        try:
            user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return User(user_doc)
            return None
        except Exception:
            return None

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login's function to load a user from the session."""
    return User.get(user_id)

# --- 4. AUTHENTICATION ROUTES ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for("register"))

        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({
            "username": username,
            "password_hash": hashed_password,
            "skills": [] # Add a field for skills
        })

        flash("Account created! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_doc = mongo.db.users.find_one({"username": username})

        if user_doc and bcrypt.check_password_hash(user_doc["password_hash"], password):
            user_obj = User(user_doc) # Create our User class instance
            login_user(user_obj)
            flash("Login successful!", "success")
            # Redirect to the page they were trying to access, or dashboard
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Login unsuccessful. Please check username and password.", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index")) # Changed to redirect to index on logout

# --- 5. CORE APP ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    # Get the user's skills from the DB to display on the page
    user_doc = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    current_skills = user_doc.get("skills", [])
    return render_template("dashboard.html", current_skills=current_skills)

# --- 6. AI LOGIC (API) ---

def get_job_recommendations(user_skills):
    """
    Uses OpenAI's GPT model to recommend jobs based on skills.
    """
    if not user_skills:
        return []

    # Convert list of skills into a comma-separated string
    skills_string = ", ".join(user_skills)

    # This is the "prompt" that tells the AI what to do.
    system_prompt = (
        "You are a 'Smart Job Recommender' assistant. Your task is to analyze a "
        "list of skills and recommend 5 relevant job titles. "
        "Return ONLY a JSON array of strings, with nothing else. "
        "Do not add any introductory text, extra explanations, or markdown."
        "Example format: [\"Data Scientist\", \"Software Engineer\", \"Product Manager\"]"
    )
    
    user_prompt = f"Skills: {skills_string}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Powerful and cost-effective
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5, # A bit of creativity, but not too much
            max_tokens=150
        )

        # Extract the text content from the response
        content = response.choices[0].message['content']

        # Because we asked for JSON, we can parse it
        job_titles = json.loads(content)
        return job_titles

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Fallback in case of API or JSON error
        return ["Error: Could not fetch recommendations. Please try again."]


@app.route("/api/recommend", methods=["POST"])
@login_required
def api_recommend():
    # Get skills from the JSON payload sent by the frontend
    data = request.get_json()
    skills = data.get("skills", [])

    if not skills:
        return jsonify({"error": "No skills provided"}), 400

    # Save the user's skills to their profile in MongoDB
    try:
        mongo.db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"skills": skills}}
        )
    except Exception as e:
        print(f"Error updating user skills: {e}")
        # Don't block the recommendation even if save fails
        
    # Call our AI function
    recommendations = get_job_recommendations(skills)

    # Return the recommendations as JSON
    return jsonify(recommendations)

# --- 7. RUN THE APP ---
if __name__ == "__main__":
    app.run(debug=True)