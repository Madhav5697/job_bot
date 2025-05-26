from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "9a33f6c173mshf4a614942354e3ep123b33jsn4270933aae39"
API_HOST = "jsearch.p.rapidapi.com"

def fetch_jobs(location, experience, skills):
    url = "https://jsearch.p.rapidapi.com/search"
    query = f"{skills} jobs in {location} with {experience} years experience"

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        return None

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    location = request.form.get("location")
    experience = request.form.get("experience")
    skills = request.form.get("skills")

    jobs = fetch_jobs(location, experience, skills)
    if jobs is None:
        error = "Failed to fetch jobs. Please try again later."
        return render_template("index.html", error=error)

    # Process jobs for display (truncate description, handle date)
    for job in jobs:
        desc = job.get('job_description', '')
        words = desc.split()
        if len(words) > 100:
            job['short_description'] = ' '.join(words[:100]) + '...'
        else:
            job['short_description'] = desc

        posted_date = job.get('job_posted_at_datetime_utc')
        job['posted_date'] = posted_date[:10] if posted_date else 'N/A'

    return render_template("results.html", jobs=jobs, location=location, experience=experience, skills=skills)

if __name__ == "__main__":
    app.run(debug=True)
