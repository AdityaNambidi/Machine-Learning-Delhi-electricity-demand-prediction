from flask import Flask, render_template, request, redirect, url_for, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "hello"

@app.route("/specifictime", methods=["GET", "POST"])
def specific_time():
    return 0


# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)