#Christopher Hites
#Latest Revision: v1.0
#Last update: 10/9/2024

#libraries
import pandas as pd
import csv
"""
#Purpose: This script is used by a player to determine their score per week. 
#Current Functionality:
    1. A player can enter the week of the season they wish to check the score of
    2. A player can enter any number of names they wish to check for other player's scores per week
#Future Functionalities:
    1. Create a function to test total scores
    2. Create a function to determine correct guess percentages?
"""

#Week number corresponding to which set of data you'd like to parse
def get_weeknum():
    while True:
        try:
            weeknum = int(input('What week of the season are we in? (integer only)\n'))
            return weeknum
            break
        except:
            print("Incorrect Input, try again.")        

def read_full_data(week_num):
    df = pd.read_csv(f"Results/Week{week_num}/results.csv",index_col="Name")
    return df

def read_name_data(week_num):
    columns = ['Name']
    df = pd.read_csv(f"Results/Week{week_num}/results.csv", usecols=columns)
    return df   

def get_player_name(week_num):
    while True:
        try:
            player = str(input('Please enter the user name used for the PickEm challenge: '))
            df=read_name_data(week_num)
            names = df['Name'].tolist()
            for name in names:
                if player == name:
                    return player
                    break
            raise Exception('Wrong name, try again.')

        except Exception as error:
            print(error)
                
def get_score(df,player_name):
   first=df.loc[player_name]
   return first
     


if __name__ == "__main__":
    breaker=1
    while breaker==1:
        weeknum = get_weeknum()
        df=read_full_data(weeknum)
        player=get_player_name(weeknum)
        score=get_score(df,player)
        print(score.to_string(),"\n")
        breaking=input('Would you like to check another player\'s score? (Y/N):\n')
        if breaking in ('n','N','No','no'):
            breaker=0

