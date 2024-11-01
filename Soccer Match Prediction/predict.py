# import pandas as pd
# import joblib

# matches = pd.read_csv('D:/Neel Patel/DDU/Study/Sem 7/Project 2/Project/Dataset/matches.csv')

# matches["date"] = pd.to_datetime(matches["date"])
# matches["venue_code"] = matches["venue"].astype("category").cat.codes
# matches["opp_code"] = matches["opponent"].astype("category").cat.codes
# matches["hours"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
# matches["day_code"] = matches["date"].dt.dayofweek
# matches["target"] = (matches["result"] == "W").astype("int")

# def rolling_averages(group, cols, new_cols):
#     group = group.sort_values("date")
#     rolling_stats = group[cols].rolling(3, closed='left').mean()
#     group[new_cols] = rolling_stats
#     group = group.dropna(subset=new_cols)
#     return group

# cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
# new_cols = [f"{c}_rolling" for c in cols]

# matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
# matches_rolling = matches_rolling.droplevel('team')
# matches_rolling.index = range(matches_rolling.shape[0])

# def predict_match_winner(team1, team2, venue, time, day_of_week):
#     team1_code = matches_rolling[matches_rolling["team"] == team1]["venue_code"].unique()[0]
#     team2_code = matches_rolling[matches_rolling["opponent"] == team2]["opp_code"].unique()[0]

#     input_data = pd.DataFrame({
#         'venue_code': [team1_code],
#         'opp_code': [team2_code],
#         'hours': [time],
#         'day_code': [day_of_week]
#     })

   
#     model_path = r'd:/Neel Patel/DDU/Study/Sem 7/Project 2/Project/Models/soccer_model_2.pkl'
#     model = joblib.load(model_path)

   
#     prediction = model.predict(input_data)
#     win_probability = model.predict_proba(input_data)

#     winner = team1 if prediction == 1 else team2
#     chance = win_probability.max()

#     return winner, chance


# winner, chance = predict_match_winner("Liverpool", "Manchester City", venue="home", time=1600, day_of_week=5)
# print(f"{winner} is predicted to win with {chance * 100:.2f}% chance.")



import pandas as pd
import joblib


matches = pd.read_csv('Soccer Match Prediction/matches.csv')


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


def predict_match_winner(team1, team2, venue, time, day_of_week):
    
    team1_code = matches_rolling[matches_rolling["team"] == team1]["venue_code"].unique()[0]
    team2_code = matches_rolling[matches_rolling["opponent"] == team2]["opp_code"].unique()[0]

    
    input_data = pd.DataFrame({
        'venue_code': [team1_code],
        'opp_code': [team2_code],
        'hour': [time],
        'day_code': [day_of_week]
    })

    
    model_path = r'Soccer Match Prediction/soccer_model_2.pkl'
    model = joblib.load(model_path)

    
    prediction = model.predict(input_data)
    win_probability = model.predict_proba(input_data)

    
    winner = team1 if prediction == 1 else team2
    chance = win_probability.max()

    return winner, chance


winner, chance = predict_match_winner("Liverpool", "Manchester City", venue="home", time=16, day_of_week=5)
print(f"{winner} is predicted to win with {chance * 100:.2f}% chance.")




'''
Dataset\def predict_match_winner(team1, team2, venue, time, day_of_week):
    
    team1_code = matches_rolling[matches_rolling["team"] == team1]["venue_code"].unique()[0]
    team2_code = matches_rolling[matches_rolling["opponent"] == team2]["opp_code"].unique()[0]

    
    input_data = pd.DataFrame({
        'venue_code': [team1_code],
        'opp_code': [team2_code],
        'hours': [time],
        'day_code': [day_of_week]
    })

    
    model = joblib.load(model_path)

    
    prediction = model.predict(input_data)
    win_probability = model.predict_proba(input_data)

    
    winner = team1 if prediction == 1 else team2
    chance = win_probability.max()

    return winner, chance



winner, chance = predict_match_winner("Liverpool", "Manchester City", venue="home", time=16, day_of_week=5)
print(f"{winner} is predicted to win with {chance * 100:.2f}% chance.")

'''
