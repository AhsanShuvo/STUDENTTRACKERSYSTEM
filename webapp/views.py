# Create your views here.

from django.shortcuts import render,redirect

from django.contrib.auth.models import User
import requests
from django.contrib.auth.decorators import login_required
from accounts.models import Profile

@login_required
def index(request):
    User_List  = User.objects.all()
    sz= len(User_List)
    contest_id = 0
    for i in range(sz):
        user = User_List[i]
        if user.is_superuser == False:
            profile = Profile.objects.get(user= user)
            cf_id = profile.codeforces_id
            response =response= requests.get("https://codeforces.com/api/user.status?handle=%s&from=1&count=20" %cf_id)
            ret = response.json()
            if ret['status'] == "OK":
                for i in range(len(ret['result'])):
                    if ret["result"][i]["author"]["participantType"]=="CONTESTANT":
                        contest_id= ret["result"][i]["contestId"]
                        # difference between contestCreationTime and current time must be less than 24*60*5
                        if contest_id >0 and contest_id < 10000:
                            break
                        else:
                            contest_id=0 
            if contest_id > 0 and contest_id < 10000:
                break
    
    for i in range(sz):
        user = User_List[i] 
        if user.is_superuser==False:
            profile= Profile.objects.get(user=user)
            cf_id = profile.codeforces_id
            response = requests.get("https://codeforces.com/api/contest.status?contestId=%s&handle=%s&from=1&count=10" %(contest_id,cf_id))      
            standing=response.json()
            solve_count, point = 0,0 
            neg_count = 0
            red = True
            for i in range(len(standing['result'])):
                if standing["result"][i]["author"]["participantType"]=="CONTESTANT":
                    red= False
                    if standing['result'][i]['verdict'] =="OK":
                        solve_count +=1
                        point +=10
                    else:
                        neg_count +=1
            profile.points += (point- neg_count)
            profile.red_mark =red
            profile.save()
            
    return render(request,'index.html',{'msg':'Works'})