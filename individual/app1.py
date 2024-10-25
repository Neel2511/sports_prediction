from flask import Flask, request, render_template
import joblib
import pandas as pd

# Load the pre-trained model
model = joblib.load('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Jenil/react/olympic-predictor/src/sk_olympics.pkl')

# Create the Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML form


@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data from the POST request
    age = request.form['age']
    sex = request.form['sex']
    height = request.form['height']
    weight = request.form['weight']
    country = request.form['country']
    city = request.form['city']
    sport = request.form['sport']

    # Create the input DataFrame for the model
    data = pd.DataFrame([[int(age), sex, int(height), int(weight), country, city, sport]],
                        columns=['Age', 'Sex', 'Height', 'Weight', 'region', 'City', 'Sport'])

    # Predict the medal using the loaded model
    predicted_medal = model.predict(data)[0]

    # Return a suitable response based on the prediction
    if predicted_medal == 'Gold':
        prediction_text = 'Congratulations! You are 90% likely to win a Gold Medal!'
    elif predicted_medal == 'Silver':
        prediction_text = 'You are 90% likely to win a Silver Medal!'
    elif predicted_medal == 'Bronze':
        prediction_text = 'You are 90% likely to win a Bronze Medal!'
    else:
        prediction_text = 'Unfortunately, You are 90% likely not to win a medal.'

    return render_template('result.html', prediction=prediction_text)


if __name__ == "__main__":
    app.run(debug=True)
