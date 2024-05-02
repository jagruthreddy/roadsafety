from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy
import traceback
import json
import os

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder= current_dir)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    visualImpairment = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    benefit = db.Column(db.String(100))
    navigation = db.Column(db.String(100))
    insufficientWarnings = db.Column(db.String(100))
    usefulFeatures = db.Column(db.String(100))
    concerns = db.Column(db.String(100))
    websiteExperience = db.Column(db.String(100))
    websiteAccessibility = db.Column(db.String(100))
    accessibilityFeatures = db.Column(db.String(100))
    interactionPreference = db.Column(db.String(100))
    recommendations = db.Column(db.String(100))

    def __repr__(self):
        return '<Feedback %r>' % self.name

# Create database tables
# with app.app_context():
#    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        # Check if form data is empty
        if not request.form:
            return jsonify({'error': 'No form data received'}), 400

        # Retrieve form data
        name = request.form.get('name')
        location = request.form.get('location')
        visualImpairment = request.form.get('visualImpairment')
        frequency = request.form.get('frequency')
        benefit = request.form.get('benefit')
        navigation = request.form.get('navigation')
        insufficientWarnings = request.form.get('insufficientWarnings')
        usefulFeatures = request.form.get('usefulFeatures')
        concerns = request.form.get('concerns')
        websiteExperience = request.form.get('websiteExperience')
        websiteAccessibility = request.form.get('websiteAccessibility')
        accessibilityFeatures = request.form.get('accessibilityFeatures')
        interactionPreference = request.form.get('interactionPreference')
        recommendations = request.form.get('recommendations')

        # Create Feedback object and add it to the database session
        feedback_data = Feedback(
            name=name,
            location=location,
            visualImpairment=visualImpairment,
            frequency=frequency,
            benefit=benefit,
            navigation=navigation,
            insufficientWarnings=insufficientWarnings,
            usefulFeatures=usefulFeatures,
            concerns=concerns,
            websiteExperience=websiteExperience,
            websiteAccessibility=websiteAccessibility,
            accessibilityFeatures=accessibilityFeatures,
            interactionPreference=interactionPreference,
            recommendations=recommendations
        )
        db.session.add(feedback_data)
        db.session.commit()

        # Return success message
        return redirect(url_for('index'))
        # return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        # Log the error
        app.logger.error(f'Error occurred: {e}')
        app.logger.error(traceback.format_exc())

        # Rollback session if an error occurs
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
