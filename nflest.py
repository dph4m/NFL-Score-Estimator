from pandas import read_html
import math
import pandas
import warnings
import numpy
import random
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    choice = input("type 1 for scorePredictor, 2 for fantasyPredictor, or 3 for randomFunPredictor: ")
    teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", 
             "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]
    poses = ["QB", "RB", "WR", "TE"]
    #user wants randFunPredictor
    if choice == "3":
        randNum = random.randint(0,1)
        #50% chance
        if randNum == 0:
            randT1 = teams[random.randint(0,31)]
            randT2 = teams[random.randint(0,31)]
            randYr = random.randint(2002, 2023)
            scorePred(randT1, randT2, randYr)
        #50% chance
        else:
            randPos = poses[random.randint(0,3)]
            URL3 = f"https://www.pro-football-reference.com/fantasy/{randPos}-fantasy-matchups.htm"
            table = read_html(URL3, attrs={"id": "fantasy_stats"})[0]
            randP = table.iloc[(random.randint(0,len(table.index))), 0]
            fantasyPred(randPos, randP, table)
    #user wants scorePredictor
    elif choice == "1":
        print(teams)
        #user inputs 2 teams and year to sim
        team1name = input("team 1 abbrev: ")
        team2name = input("team 2 abbrev: ")
        if team1name not in teams or team2name not in teams:
            print("enter exactly the 3 letter abbreviation in the list")
            return
        year = input("year: ")
        try:
            scorePred(team1name, team2name, year)
        except:
            print(f"at least 1 team did not exist in {year} or {year} hasn't happened yet")

    #user wants fantasyPredictor
    elif choice == "2":
        #user inputs player's position and name exactly
        playerPos = input("player position (QB, RB, WR, TE only): ")
        playerName = input("player name: ")
        try:
            URL3 = f"https://www.pro-football-reference.com/fantasy/{playerPos}-fantasy-matchups.htm"
            table = read_html(URL3, attrs={"id": "fantasy_stats"})[0]
            fantasyPred(playerPos, playerName, table)
        except:
            print("player not playing or not a valid position")
            return
    else:
        #typed wrong
        print("type exactly")
        return

def scorePred(team1name, team2name, year):
    #user inputs 2 nfl teams abbreviations and year of game simulated
    #grabs tables from link and reads
    URL1 = f"https://www.pro-football-reference.com/teams/{team1name}/{year}.htm"
    URL2 = f"https://www.pro-football-reference.com/teams/{team2name}/{year}.htm"


    team1 = read_html(URL1, attrs={"id": "games"})[0]
    team2 = read_html(URL2, attrs={"id": "games"})[0]

    #changes nan values (games yet to be played) to 0
    def nanTo0(team, col):
        for x in range(len(team.iloc[:,col])):
            if(math.isnan(team.iloc[x,col])):
                team.iloc[x,col] = 0

    #counts games played by team
    def gamesPlayed(team):
        Ct = 0
        for x in range(len(team.iloc[:,5])):
            if((not(pandas.isnull(team.iloc[x,5])))):
                Ct+=1
        return Ct

    team1GP = gamesPlayed(team1)
    team2GP = gamesPlayed(team2)

    #change values of NaN to 0 for math
    nanTo0(team1,10)
    nanTo0(team1,11)
    nanTo0(team2,10)
    nanTo0(team2,11)

    #sum scores column and div by games played for avg
    team1AvgPF = sum(team1.iloc[:,10])/team1GP
    team1AvgPA = sum(team1.iloc[:,11])/team1GP
    team2AvgPF = sum(team2.iloc[:,10])/team2GP
    team2AvgPA = sum(team2.iloc[:,11])/team2GP

    #formula to predict score of games
    team1score = round((team1AvgPF + team2AvgPA)/2)
    team2score = round((team2AvgPF + team1AvgPA)/2)
    print()
    print(f"{year} estimate: {team1score} {team1name} - {team2score} {team2name}")

    #calculate passing yds
    nanTo0(team1, 14)
    nanTo0(team2, 19)
    nanTo0(team1, 19)
    nanTo0(team2, 14)
    team1PYO = sum(team1.iloc[:,14])/team1GP
    team2PYD = sum(team2.iloc[:,19])/team2GP
    team2PYO = sum(team2.iloc[:,14])/team2GP
    team1PYD = sum(team1.iloc[:,19])/team1GP
    print(f"estimated {team1name} pass yds: {(team1PYO+team2PYD)/2}")
    print(f"estimated {team2name} pass yds: {(team2PYO+team1PYD)/2}")

    #calculate rush yds
    nanTo0(team1, 15)
    nanTo0(team2, 20)
    nanTo0(team1, 20)
    nanTo0(team2, 15)
    team1RYO = sum(team1.iloc[:,15])/team1GP
    team2RYD = sum(team2.iloc[:,20])/team2GP
    team2RYO = sum(team2.iloc[:,15])/team2GP
    team1RYD = sum(team1.iloc[:,20])/team1GP
    print(f"estimated {team1name} rush yds: {(team1RYO+team2RYD)/2}")
    print(f"estimated {team2name} rush yds: {(team2RYO+team1RYD)/2}")

def fantasyPred(playerPos, playerName, table):
    playerInd = (table[table.iloc[:,0]==playerName].index.values)
    #index of given positions ppg
    ppgInd = numpy.where(table.columns.get_loc('Fantasy per Game') == True)[0][0]
    #player average ppg and defense average ppg allowed from position
    playerAvg = float(table.iloc[playerInd,ppgInd])
    dAvg = float(table.iloc[playerInd,ppgInd+6])
    print(f"{playerPos} {playerName} estimated fpts: {(playerAvg+dAvg)/2}")

main()
