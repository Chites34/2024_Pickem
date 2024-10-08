#Christopher Hites
#Latest Revision: v1.3
#Last update: 10/9/2024

"""
#Purpose: This script is used to parse through the Pickem data found in the Files directory,
determine the correct number of picks, and then format the reults in the Restults directory.
"""
"""
#Future Development:
    1. Integrate with Google Sheets to reduce the workload of downloading the csv files (gsheets?)
        a. If successful, rewrite how to obtain data and matchup columns
    2. Integrate with an exterior source for the winners instead of creating a winners.txt file manually
        a. If successful, rewrite how to obtain data.
    3. Inegrate with forms to create a Pickem form
    4. Integrate with Discord to publish the results 
"""

#Library
import pandas as pd
import csv

#Week number corresponding to which set of data you'd like to parse
def get_weeknum():
    while True:
        try:
            weeknum = int(input('What week of the season are we in? (integer only)\n'))
            return weeknum
            break
        except:
            print("Incorrect Input, try again.")
        
#Receives user input
week_num = get_weeknum()

#load the CSV file to inspect its structure
csv_data = f'Files/Week{week_num}/PickemWeek{week_num}.csv'
winning_teams = f'Files/Week{week_num}/winners.txt'

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
    comparison_results.sort(key=lambda x: x[1], reverse=True) #sort results to have highest number of correct picks at top
    #return the results
    return comparison_results

#pulls the winning teams from the winner.txt file in the corresponding week
teams=get_winners(winning_teams)       
#runs the main function to determine the participant's results
results=compare_winners(pickem_data, matchup_columns,teams)


#Opens a new csv file in the corresponding week results. writes the tuple into a csv file
#the \n is to put them on different lines
with open(f"Results/Week{week_num}/results.csv","w") as file:
    writer = csv.writer(file,lineterminator='\n')
    writer.writerow(['Name','Score'])
    for tup in results:
        writer.writerow(tup)
        
"""
Original Code used to write to a text file. Superceded to write to a csv file for easy parsing in separate script.

with open(f"Results/Week{week_num}/results.txt","w") as file:
    for tuple in results:
        for j in tuple:
            file.write(str(j))
            file.write(" ")
        file.write("\n")
"""
    