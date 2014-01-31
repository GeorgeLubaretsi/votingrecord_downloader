import urllib2
import json
import datetime
import os


def main():
  #req = urllib2.Request('http://dev-parlvote.jumpstart.ge/en/api/v1/members')
  req = urllib2.Request('http://votes.parliament.ge/en/api/v1/members')
  response = urllib2.urlopen(req)
  membersRaw = response.read()
  members = json.loads(membersRaw)

  script_dir = os.getcwd()

  lawDict = {}
  for member in members:
    memberID = member['id']
    #make a web request for this members data
    #req = urllib2.Request('http://dev-parlvote.jumpstart.ge/en/api/v1/member_votes?member_id='+str(memberID)+'&with_laws=true')
    req = urllib2.Request('http://votes.parliament.ge/en/api/v1/member_votes?member_id='+str(memberID)+'&with_laws=true')
    nowTime = datetime.datetime.now()
    response = urllib2.urlopen(req)
    memberVotesRaw = response.read()
    memberJson = json.loads(memberVotesRaw)
    memberVotes = memberJson['member']
        
    print memberVotes['name'].encode('utf8')
    memberName = memberVotes['name'].encode('utf8')
    summary = memberVotes['vote_summary']
    totalVotes = summary['total_votes']
    yesVotes = summary['yes_votes']
    noVotes = summary['no_votes']
    abstainVotes = summary['abstain_votes']
    absent = summary['absent']

    for law in memberVotes['laws']:
      lawId = law['law_id'].strip()
      if not lawId in lawDict:
        lawDict[lawId] = {'kan_id': lawId, 'scrape_date': str(nowTime)[0:10], 'name': law['title'], 'date': law['released_to_public_at'], 'url': '', 'number': lawId, 'result' : []}
      #just get last vote for each member for now there are multiple sessions and votes as the bill goes through different stages these can get handled later
      sessions = law['sessions']
      for sessionKey in sessions:
        sessionNum = sessionKey.split("_")[1]
        session = sessions[sessionKey]
        lawDict[lawId]['result'].append( {'name': memberName, 'vote': session['vote'], 'session':sessionNum} )
        lawDict[lawId]['amendments'] = []
        
  #now create individual files for each law in json format contain each members vote
  #this is the input that the myparliment platform accepts
  for key, lawItem in lawDict.items():

    path = os.path.join(script_dir, "data/"+lawItem['kan_id']+".json")
    lawFile = open(path, 'w')
    jsonStr = json.dumps(lawItem)
    lawFile.write(jsonStr)
    lawFile.close()
   
if  __name__ =='__main__':
    main()
