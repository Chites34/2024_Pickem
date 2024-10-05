import pandas as pd
#load the CSV file to inspect its structure
csv_data = "C:/Users/hites/Documents/Personal/Python_Portfolio/PickEm/Files/Week4/PickemWeek4.csv"
winning_teams = "C:/Users/hites/Documents/Personal/Python_Portfolio/PickEm/Files/Week4/winners.txt"

pickem_data = pd.read_csv(csv_data)
#Cleans up the names of the columns. removes whitespace
pickem_data.columns = pickem_data.columns.str.strip()
#Sets matchup_columns to each of the matchups for the week
matchup_columns = [ col for col in pickem_data.columns if '?' in col]

def get_winners(winners):
    teams = []
    with open(winners, 'r') as f:
        for line in f:
            teams.append(line.strip())
    return teams

            
def compare_winners(pickem_data, matchup_columns,teams):
    #creates a dictionary with the matchups and the winner of the matchups
    user_winners = {}
    user_winners = dict(zip(matchup_columns,teams))
    
    #go through each participant and compare prediction to the user input
    comparison_results = []
    for index, row in pickem_data.iterrows():
        name = row['Name']
        correct_picks = 0
        
        for matchup in matchup_columns:
            if row[matchup] == user_winners[matchup]:
                correct_picks +=1
        #append results to comparison_results as a tuple of (Discord name, Correct Picks)
        comparison_results.append((name, correct_picks))
    comparison_results.sort(key=lambda x: x[1], reverse=True)
    #return the results
    return comparison_results

#pulls the winning teams from the winner.txt file in the corresponding week
teams=get_winners(winning_teams)       
#runs the main function to determine the participant's results
results=compare_winners(pickem_data, matchup_columns,teams)

#will create a text file in the folder the script is run in.
#Will go through each item in the comparison_results and print out both the name and score
#the \n is to put them on different lines
with open("results.txt","w") as file:
    for tuple in results:
        for j in tuple:
            file.write(str(j))
            file.write(" ")
        file.write("\n")