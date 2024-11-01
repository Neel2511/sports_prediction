from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)


matches = pd.read_csv('matches.csv')


matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype("int")


def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]


matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
matches_rolling = matches_rolling.droplevel('team')
matches_rolling.index = range(matches_rolling.shape[0])


model_path = r'soccer_model_2.pkl'
model = joblib.load(model_path)


def predict_match_winner(team1, team2, time, day_of_week):
    team1_code = matches_rolling[matches_rolling["team"] == team1]["venue_code"].unique()[0]
    team2_code = matches_rolling[matches_rolling["opponent"] == team2]["opp_code"].unique()[0]

    input_data = pd.DataFrame({
        'venue_code': [team1_code],
        'opp_code': [team2_code],
        'hour': [time],
        'day_code': [day_of_week]
    })

    prediction = model.predict(input_data)
    win_probability = model.predict_proba(input_data)

    winner = team1 if prediction == 1 else team2
    chance = win_probability.max()

    return winner, chance


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        time = int(request.form['time'])
        day_of_week = int(request.form['day_of_week'])

        
        winner, chance = predict_match_winner(team1, team2, time, day_of_week)
        return render_template('index.html', prediction_text=f"{winner} is predicted to win with {chance * 100:.2f}% chance.")
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5004,debug=True)
