# 🧠 Smart Job Recommender

A web application that uses AI to recommend job titles based on a user's skills. This platform allows users to create an account, input their technical and soft skills, and receive a list of relevant job roles, powered by the OpenAI API.

> **Live Demo:** https://smart-job-platform.vercel.app/

## ✨ Features

  * **User Authentication:** Secure user registration and login system (`flask_login`, `flask_bcrypt`).
  * **Persistent Profiles:** User skills are saved to their profile in a MongoDB database.
  * **AI-Powered Matching:** Uses the OpenAI API (GPT-3.5-Turbo) to understand the context of user skills and recommend relevant job titles.
  * **Dynamic Frontend:** A clean dashboard that asynchronously fetches recommendations from the backend without a page reload (`JavaScript Fetch API`).
  * **Secure Key Management:** Uses a `.env` file to keep all API keys and database URIs secure and out of version control.

## 🛠️ Tech Stack

### Backend

### Database

### Frontend

### Deployment

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

  * [Python 3.10+](https://www.python.org/)
  * [Git](https://git-scm.com/)
  * A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (for the database)
  * An [OpenAI Platform](https://platform.openai.com/api-keys) account (for the API key)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/basilio254/smart-job-platform.git
    cd smart-job-platform
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows (cmd.exe)
    .\venv\Scripts\activate

    # Activate on Mac/Linux (bash)
    # source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Environment Variables:**
    Create a file named `.env` in the root of the project. This file is included in `.gitignore` and will not be pushed to GitHub.

    Copy the following into your `.env` file and add your secret keys:

    ```
    # .env

    # Get this from platform.openai.com
    OPENAI_API_KEY=sk-Your-OpenAI-Secret-Key

    # Get this from MongoDB Atlas (make sure to replace <password>)
    MONGO_URI=mongodb+srv://admin:YourPassword@yourcluster.xxxxx.mongodb.net/?appName=YourApp

    # Generate this by running: python -c "import secrets; print(secrets.token_hex(32))"
    FLASK_SECRET_KEY=Your-Long-Random-Secret-String
    ```

5.  **Run the application:**

    ```bash
    python app.py
    ```

6.  Open your browser and navigate to `http://127.0.0.1:5000`

## 📖 Usage

1.  **Register:** Create a new user account.
2.  **Login:** Log in to your new account.
3.  **Go to Dashboard:** You will be redirected to your dashboard.
4.  **Enter Skills:** In the text area, enter a list of your skills separated by commas (e.g., `Python, Flask, Data Analysis, SQL, React`).
5.  **Get Recommendations:** Click the "Get Recommendations" button. The app will call the OpenAI API, which will analyze your skills and return a list of 5 job titles that are a good match.

## ☁️ Deployment

This project is configured for easy deployment to **Vercel**.

1.  **Push to GitHub:** Make sure your repository is pushed to GitHub and your `.env` file is listed in `.gitignore`.
2.  **Import to Vercel:** On your Vercel dashboard, import the project from your GitHub repository.
3.  **Configure Environment Variables:** In the Vercel project settings, go to "Environment Variables" and add your three secrets:
      * `OPENAI_API_KEY`
      * `MONGO_URI`
      * `FLASK_SECRET_KEY`
4.  **Deploy:** Click "Deploy." Vercel will automatically detect the `vercel.json` file and `requirements.txt` to build and deploy your Flask application as a serverless function.

## 📄 License

This project is licensed under the MIT License.# smart-job-platform
