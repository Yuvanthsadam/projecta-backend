import json

myjsonfile=open("jobportal/state.json","r")
jsondata=myjsonfile.read()
obj=json.loads(jsondata)

countries=[]
allstates=[]



for i in obj:#countries
    for j in obj[i]:#obj["countries"]
        countries.append(j)#appending all the objects inside countries into list(countries[])


nos_of_countries=len(obj["countries"])#number of countries

for i in range(nos_of_countries):
    a=countries[i]# current no of country
    #print(i+1)
    
    #print(a["country"])
    #print(a["states"])
    for s in a["states"]:#
        allstates.append(s)

maintuple=[]
for i in allstates:
 
    innertuple=[]

    innertuple.append(i)
    innertuple.append(i)
    a=tuple(innertuple)#(state,state)

    maintuple.append(a)#((state,state),(state,state))


states=tuple(maintuple)