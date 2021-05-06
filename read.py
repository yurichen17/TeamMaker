from googleapiclient.discovery import build
from google.oauth2 import service_account
import random

SERVICE_ACCOUNT_FILE = 'keys.json'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)



# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15Y-49jdWcaKTVou1cKkDwLrtZTnXxCn8s0fUZUxCHbQ'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Players!A2:G31").execute()
values = result.get('values', [])

numPlayers=len(values)


#so, depending on what role they want to play, generate random teams until 2 teams are of similar 
#calibre. Then take those players out and keep making it. At the end, if the skill difference is too 
#much, then restart?

#maybe give priority of roles to lower ranked people?
#that means i start with lower ranked ppl?
#no i should start with not fill people

def rankedScores(rank):
    switcher={
        "Diamond 3":0,
        "Diamond 4":1,
        "Platinum 1":2,
        "Platinum 2":4,
        "Platinum 3":6,
        "Platinum 4":11,
        "Gold 1":14,
        "Gold 2":17,
        "Gold 3":20,
        "Gold 4":24,
        "Silver 1":27,
        "Silver 2":29,
        "Silver 3":32,
        "Silver 4":37,
        "Bronze 1":40,
        "Bronze 2":43,
        "Bronze 3":48,
        "Bronze 4":50,
        "Unranked":60
    }
    return switcher.get(rank)

def checkingAndPutting(position, i,team1, team2, team1score, team2score, teamNum,players):
    putted=0
    if team1[position]=="Empty" and team2[position]=="Empty":
        #put inside smaller point team
        if team1score<=team2score:
            team1[position]=players[i]
            team1score+=rankedScores(players[i][6])
            players[i][7]=teamNum
            putted=1
        else:
            team2[position]=players[i]
            team2score+=rankedScores(players[i][6])
            players[i][7]=teamNum
            putted=1
    elif team1[position]=="Empty":
        team1[position]=players[i]
        team1score+=rankedScores(players[i][6])
        players[i][7]=teamNum
        putted=1
    elif team2[position]=="Empty":
        team2[position]=players[i]
        team2score+=rankedScores(players[i][6])
        players[i][7]=teamNum
        putted=1
    return putted, team1, team2,team1score,team2score,players

def makingTeams(values, teamNum):
    #print(teamNum)
    #randomize entries
    random.shuffle(values)

    teamCount=0
    team1score=0
    team2score=0
    team1=["Empty"]*5
    team2=["Empty"]*5
    

    #time to seperate fills from non fills
    notFill=[i for i in values if (i[2]!="Fill")]
    fill=[i for i in values if (i[2]=="Fill")]

    numNotFill=len(notFill)
    numFill=len(fill)

    #team order goes like this: 0 Top, 1 JG, 2 Mid, 3 ADC, 4 Sup

    #this for loop will go through all the players and do its best to put the players into random teams. 
    
    for i in range(0,numNotFill):
        #check roles of player
        if notFill[i][2]=="Top" and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(0, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][2]=="Jungle"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(1, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][2]=="Mid"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(2, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][2]=="ADC"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(3, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][2]=="Support"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(4, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        #if both teams are filled
        if teamCount==10:
            return team1, team1score, team2, team2score,True
    
    #-------------------------------------------------------------------------------#
    #if end of list and team not filled, use secondary
    for i in range(0,numNotFill):
        #check roles of player
        if notFill[i][3]=="Top"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill=checkingAndPutting(0, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][3]=="Jungle"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(1, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][3]=="Mid"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(2, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][3]=="ADC"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(3, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        if notFill[i][3]=="Support"and notFill[i][7]==0:
            putted, team1, team2,team1score, team2score, notFill =checkingAndPutting(4, i, team1, team2,team1score, team2score,teamNum,notFill)
            if putted==1:
                teamCount+=1
                continue
        #if both teams are filled
        if teamCount==10:
            return team1, team1score, team2, team2score,True
    #-------------------------------------------------------------------------------#
    #if end of list and team still not filled, use fills
    for i in range(0,numFill):
        #check roles of player
        if fill[i][3]=="Fill"and fill[i][7]==0 and (team1[0]=="Empty" or team2[0]=="Empty"):
            putted, team1, team2,team1score, team2score,fill =checkingAndPutting(0, i, team1, team2,team1score, team2score,teamNum,fill)
            if putted==1:
                teamCount+=1
                continue
        if fill[i][3]=="Fill"and fill[i][7]==0 and (team1[1]=="Empty" or team2[1]=="Empty"):
            putted, team1, team2,team1score, team2score,fill =checkingAndPutting(1, i, team1, team2,team1score, team2score,teamNum,fill)
            if putted==1:
                teamCount+=1
                continue
        if fill[i][3]=="Fill"and fill[i][7]==0 and (team1[2]=="Empty" or team2[2]=="Empty"):
            putted, team1, team2,team1score, team2score,fill =checkingAndPutting(2, i, team1, team2,team1score, team2score,teamNum,fill)
            if putted==1:
                teamCount+=1
                continue
        if fill[i][3]=="Fill"and fill[i][7]==0 and (team1[3]=="Empty" or team2[3]=="Empty"):
            putted, team1, team2,team1score, team2score,fill =checkingAndPutting(3, i, team1, team2,team1score, team2score,teamNum,fill)
            if putted==1:
                teamCount+=1
                continue
        if fill[i][3]=="Fill"and fill[i][7]==0 and (team1[4]=="Empty" or team2[4]=="Empty"):
            putted, team1, team2,team1score, team2score,fill =checkingAndPutting(4, i, team1, team2,team1score, team2score,teamNum,fill)
            if putted==1:
                teamCount+=1
                continue
        #if both teams are filled
        if teamCount==10:
            return team1, team1score, team2, team2score,True
    #-------------------------------------------------------------------------------#
    #if teams still not full, restart this function (and also just randomly fill so not empty for last team)
    if(teamNum==numGames and teamCount<10):  
        #something is wrong here but idk why
        emp1=True
        emp2=True

        while((emp1==True or emp2==True)):
            print(teamCount)
            #find empty spot
            index = -1
            index1=-1
            print("team1:",team1)
            for k in range(0,5):
                if team1[k]=="Empty":
                    index=k
                    break
            print("index:",index)
            print("thing at that spot:", team1[index])
            for l in range(numPlayers):
                print("values",values[l])
                if values[l][7]==0:
                    print("found a zero, index=",index)
                    if index!=-1:
                        print("is it even in here?")
                        #print(index)
                        values[l][7]=teamNum
                        team1[index]=values[l]
                        teamCount+=1
                        team1score+=rankedScores(values[l][6])
                        print("team1[index]:", team1[index])
                        break
            print("after adding to team1:",team1)
            for k in range(5):
                if team2[k]=="Empty":
                    index1=k
            for l in range(numPlayers):
                if values[l][7]==0:
                    if index1!=-1:
                        values[l][7]=teamNum
                        team2[index1]=values[l]
                        teamCount+=1
                        team1score+=rankedScores(values[l][6])
            emp1=False
            emp2=False
            for k in range(5):
                if team1[k]=="Empty":
                    emp1=True
            for k in range(5):
                if team2[k]=="Empty":
                    emp2=True
            if(emp1==False):
                print(team1)
            if(emp2==False):
                print(team2)
        #print(team1)
        for j in range(0,numPlayers):
                if (values[j][7]==teamNum):
                    values[j][7]=0
    print("everything full so leave")
    return team1, team1score, team2, team2score, False

allTeams=[]
allScores=[]
bestLastScores=[]
bestLastTeam=[]

def constructing(numGames):
    team1score=100
    team2score=0
    bestDifference=1000

    for i in range(0,numGames):
        #making 1 team
        full=False
        count=0
        #print("below is the team score difference")
        #print(team1score-team2score)
        while (abs(team1score-team2score)>10) or (full==False):
            #restart vals if the team doesnt work
            for j in range(0,numPlayers):
                if (values[j][7]==i+1):
                    values[j][7]=0
            
            #make a randomized team
            team1, team1score, team2, team2score, checkFull = makingTeams(values,i+1)
            full=checkFull

            #count number of times this runs
            count+=1
            if (count>40):
                print("ran 40 times with no result")
                allTeams.clear()
                allScores.clear()
                return False
            #if only looking for last team
            if(i==numGames-1):
                #store if the difference is the lowest
                if abs(team1score-team2score)<bestDifference:
                    bestDifference=abs(team1score-team2score)
                    #append the teams already made in all teams
                    for k in range(0, 2*(numGames-1)):
                        bestLastTeam.append(allTeams[k])
                        bestLastScores.append(allScores[k])
                    #append best last team
                    bestLastTeam.append(team1)
                    bestLastTeam.append(team2)
                    bestLastScores.append(team1score)
                    bestLastScores.append(team2score)


        #add the potential team to a list
        allTeams.append(team1)
        allTeams.append(team2)
        allScores.append(team1score)
        allScores.append(team2score)
    #end of for loop for # of games
    return True

    """
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Teams!A"+str(1+i*20), valueInputOption="USER_ENTERED", body={"values":team1Total}).execute()
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Teams!A"+str(9+i*20), valueInputOption="USER_ENTERED", body={"values":team2Total}).execute()
    #output teams onto google sheet
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Teams!B"+str(2+i*18), valueInputOption="USER_ENTERED", body={"values":team1}).execute()
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Teams!B"+str(10+i*18), valueInputOption="USER_ENTERED", body={"values":team2}).execute()
    """



#making sure u can make a certain amount of teams; has to be multiples of 10
numGames=int(numPlayers/10)
#initialize to 0 for all players
for i in range(0,numPlayers):
    values[i].append(0)

completed=False
maxLoops=0
while (completed==False):
    if(maxLoops>10):
        allTeams=bestLastTeam
        allScores=bestLastScores
        break
    completed=constructing(numGames)
    maxLoops+=1

#need to make it stop at some point and output "best" team
for i in range(0,numPlayers):
    print(values[i])

clear_values_request_body = {  
    'requests': [
        {
            'updateCells': {
                'range': {
                    'sheetId': '1560764505'

                },
                'fields': '*'
            }
        }
    ]
}
service.spreadsheets().batchUpdate(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    body=clear_values_request_body
).execute()

for i in range(0, numGames):
    #take out values from the lists
    team1=allTeams[i*2]
    team2=allTeams[i*2+1]
    team1Total = allScores[i*2]
    team2Total = allScores[i*2+1]

    print(team1)
    print(team2)
    print(team1Total)
    print(team2Total)

    
    batch_update_values_request_body = {
        
        # How the input data should be interpreted.
        'value_input_option': "USER_ENTERED",  # TODO: Update placeholder value.

        # The new values to apply to the spreadsheet.
        'data':[
        {
            'range': "Teams!A"+str(1+i*20), ##Update single cell
            'values': [[team1Total]]
        }, {
            'range': "Teams!A"+str(9+i*20), ##Update a column
            'values': [[team2Total]]
        }, {
            'range': "Teams!B"+str(2+i*18), ##Update a row
            'values': team1
        }, {
            'range': "Teams!B"+str(10+i*18), ##Update a 2d range
            'values': team2
        }
        ]
        
        
    }
    #write to the spreadsheet
    request = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_update_values_request_body)
    response = request.execute()
    