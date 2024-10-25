# from flask import Flask, render_template, request
# import pickle
# import joblib

# app = Flask(__name__)

# # Load the trained model
# with open('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Final/startbootstrap-landing-page-gh-pages/startbootstrap-landing-page-gh-pages - Copy/models/soccer_model_2.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Team mapping for prediction
# team_mapping = {
#     "Manchester City": 1,
#     "Arsenal": 2,
#     # Add more team mappings as needed
# }

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict_team_sport', methods=['POST'])
# def predict_team_sport():
#     # Fetch form data
#     team = request.form['team']
#     opponent = request.form['opponent']
#     venue = request.form['venue']
#     time = int(request.form['time'])
#     day_of_week = int(request.form['day_of_week'])

#     # Example of encoding and model prediction
#     venue_code = 0 if venue.lower() == 'home' else 1

#     # Find team and opponent codes (this is just a dummy example)
#     team_code = team_mapping.get(team, 0)  # Replace with actual logic
#     opponent_code = team_mapping.get(opponent, 0)  # Replace with actual logic

#     # Make the prediction
#     prediction = model.predict([[venue_code, opponent_code, time, day_of_week]])

#     # Process the result
#     result = "win" if prediction == 1 else "lose or draw"
    
#     return f"The team is predicted to {result}."

# if __name__ == '__main__':
#     app.run(debug=True)







# from flask import Flask, render_template, request
# import pickle
# import pandas as pd

# app = Flask(__name__)

# # Load the trained model
# with open('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Final/startbootstrap-landing-page-gh-pages/startbootstrap-landing-page-gh-pages - Copy - Copy (2)/templates/models/soccer_model_2.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Load the dataset to map teams and opponents
# matches = pd.read_csv('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Final/startbootstrap-landing-page-gh-pages/startbootstrap-landing-page-gh-pages - Copy - Copy (2)/templates/dataset/matches.csv', index_col=0)  # Update this path

# # Create team mappings
# team_mapping = {team: code for code, team in enumerate(matches['team'].unique())}

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/team_sport')
# def team_sport():
#     return render_template('team_sport.html')

# @app.route('/predict_team_sport', methods=['POST'])
# def predict_team_sport():
#     # Fetch form data
#     team = request.form['team']
#     opponent = request.form['opponent']
#     venue = request.form['venue']
#     time = int(request.form['time'])
#     day_of_week = int(request.form['day_of_week'])

#     # Convert venue to venue_code
#     venue_code = 0 if venue.lower() == 'home' else 1  # Assuming 0 for home, 1 for away

#     # Find team and opponent codes
#     try:
#         team_code = team_mapping[team]
#         opponent_code = team_mapping[opponent]
#     except KeyError:
#         return "Team or opponent not found in the dataset."

#     # Prepare input data for prediction
#     input_data = pd.DataFrame({
#         'venue_code': [venue_code],
#         'opp_code': [opponent_code],
#         'hour': [time],
#         'day_code': [day_of_week]
#     })

#     # Make the prediction
#     prediction = model.predict(input_data)

#     # Process the result
#     result = "win" if prediction[0] == 1 else "lose or draw"
    
#     return f"The team is predicted to {result}."

# if __name__ == '__main__':
#     app.run(debug=True)









# from flask import Flask, render_template, request
# import pandas as pd
# import joblib

# app = Flask(__name__)

# # Load the model
# model_path = 'd:/Neel Patel/DDU/Study/Sem 7/Project 2/Project/Models/soccer_model_2.pkl'
# model = joblib.load(model_path)

# # Load matches data to extract team codes
# matches = pd.read_csv('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Project/Dataset/matches.csv')
# matches["venue_code"] = matches["venue"].astype("category").cat.codes
# matches["opp_code"] = matches["opponent"].astype("category").cat.codes

# # Helper function to encode inputs
# def encode_inputs(team1, team2, time, day_of_week):
#     team1_code = matches.loc[matches['team'] == team1, 'venue_code'].values[0]
#     team2_code = matches.loc[matches['opponent'] == team2, 'opp_code'].values[0]

#     return [team1_code, team2_code, time, day_of_week]

# @app.route('/predict_team', methods=['POST'])
# def predict_team():
#     team1 = request.form['team1']
#     team2 = request.form['team2']
#     time = int(request.form['time'])  # Assuming this is in 24-hour format
#     day_of_week = int(request.form['day_of_week'])  # Day of the week as an integer

#     # Encode the inputs
#     encoded_inputs = encode_inputs(team1, team2, time, day_of_week)
#     input_data = pd.DataFrame([encoded_inputs], columns=['venue_code', 'opp_code', 'hours', 'day_code'])

#     # Make the prediction
#     prediction = model.predict(input_data)
#     win_probability = model.predict_proba(input_data)
    
#     winner = team1 if prediction[0] == 1 else team2
#     chance = win_probability.max() * 100  # Convert to percentage

#     prediction_text = f"{winner} is predicted to win with a probability of {chance:.2f}%."
    
#     return render_template('team_sport.html', prediction_text=prediction_text)

# @app.route('/team_sport')
# def team_sport():
#     return render_template('team_sport.html')

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('D:\Neel Patel\DDU\Study\Sem 7\Project 2\Final\startbootstrap-landing-page-gh-pages\startbootstrap-landing-page-gh-pages - Copy - Copy (2)\models\soccer_model_2.pkl')

@app.route('/')
def home():
    return render_template('team_sport.html')

@app.route('/predict_team', methods=['POST'])
def predict_team():
    # Get form data
    team1 = request.form['team1']
    team2 = request.form['team2']
    time = int(request.form['time'])
    day_of_week = int(request.form['day_of_week'])

    # Prepare input data (assuming team names need to be encoded)
    # Here, you need to convert team1 and team2 into numerical values based on your model's encoding
    # For simplicity, assuming you have a predefined mapping of teams to codes
    # For example:
    team_mapping = {'Team A': 0, 'Team B': 1}  # Replace with your actual mapping

    team1_code = team_mapping.get(team1, -1)  # -1 if team not found
    team2_code = team_mapping.get(team2, -1)  # -1 if team not found

    if team1_code == -1 or team2_code == -1:
        return render_template('team_sport.html', prediction_text='Team names are invalid.')

    # Create DataFrame for model input
    input_data = pd.DataFrame({
        'team1': [team1_code],
        'team2': [team2_code],
        'time': [time],
        'day_of_week': [day_of_week],
        'venue': [0]  # Assuming home venue for team1
    })

    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # You may want to map prediction back to a human-readable format
    if prediction == 1:
        prediction_text = f"{team1} is predicted to win!"
    else:
        prediction_text = f"{team2} is predicted to win!"

    return render_template('team_sport.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
