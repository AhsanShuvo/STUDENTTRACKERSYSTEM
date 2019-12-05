# Create your views here.

from django.shortcuts import render,redirect

from django.contrib.auth.models import User
import requests
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import CONTEST
import matplotlib
from matplotlib import pylab
from pylab import *
import PIL
from PIL import Image
import io
from io import BytesIO
from django.http import HttpResponse

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
            response= requests.get("https://codeforces.com/api/user.status?handle=%s&from=1&count=20" %cf_id)
            ret = response.json()
            if ret['status'] == "OK":
                for i in range(len(ret['result'])):
                    if ret["result"][i]["author"]["participantType"]=="CONTESTANT":
                        contest_id= ret["result"][i]["contestId"]
                        # difference between contestCreationTime and current time must be less than 24*60*5
                        if contest_id >0 and contest_id < 10000:
                            if CONTEST.objects.filter(number = contest_id).exists():
                                contest_id =0
                            else:
                                break;
                        else:
                            contest_id=0 
            if contest_id > 0 and contest_id < 10000:
                break
    response = requests.get("https://codeforces.com/api/contest.standings?contestId=%s&from=1&count=10000&showUnofficial=false"%contest_id)
    standing= response.json()
    cf_handle = set() 
    for i in range(sz):
        user= User_List[i] 
        profile = Profile.objects.get(user=user)
        cf_=profile.codeforces_id
        cf_handle.add(cf_)
    if standing['status']=="OK":
        sz= len(standing["result"]["rows"])
        if standing["result"]["contest"]["phase"]=="FINISHED" and standing["result"]["contest"]["frozen"]==False:
            print("HERE WE GO!")
            for i in range(sz):
                user_handle= standing["result"]["rows"][i]["party"]["members"][0]["handle"]
                if user_handle in cf_handle:
                    profile = Profile.objects.get(codeforces_id =user_handle)
                    profile.points += standing["result"]["rows"][i]["points"]
                    problems = standing["result"]["rows"][i]["problemResults"]
                    cc= 0
                    for i in range(len(problems)):
                        if problems[i]["points"]:
                            profile.TotalSolve+=1 
                            cc+=1
                    profile.TotalContest+=1
                    profile.red_mark= True
                    profile.save()
                    CONTEST.objects.create(
                        number = contest_id,
                        Name= standing["result"]["contest"]["name"],
                        user_id=profile.full_name,
                        solve= cc,
                        position = standing["result"]["rows"][i]["rank"]
                    )
    last= CONTEST.objects.latest('id')
    top = CONTEST.objects.filter( number=last.number).order_by('position')[:1]
    print(top[0].number, top[0].user_id)
    context={
        'profile':Profile.objects.order_by('-points')[:3],
        'contest':CONTEST.objects.order_by('-number')[:4],
        'LastRound':top[0].number,
        'winner':top[0].user_id,
    }
    return render(request,'index.html',context)

def contest(request):
    return render(request,'contest.html',{})

def ranking(request):
    dept = 'ALL'
    profile= Profile.objects.order_by('-points')[:2]
    contest=CONTEST.objects.all()
    if dept == "ALL":
        rank_profile= Profile.objects.order_by('-points').all()
        context={
            'rank_profile':rank_profile,
           'profile':profile,
           'contest':contest,
        }
        return render(request,'ranking.html',context)
    elif dept == 'CSE':
        rank_profile= Profile.objects.filter('CSE').order_by('-points').all()
        context={
            'rank_profile':rank_profile,
           'profile':profile,
           'contest':contest,
        }
        return render(request,'ranking.html',context)
    else:
        rank_profile= Profile.objects.filter('SWE').order_by('-points').all()
        context={
            'rank_profile':rank_profile,
           'profile':profile,
           'contest':contest,
        }
        return render(request,'ranking.html',context)

def profile(request):
    user = request.user 
    user_profile=Profile.objects.get(user= user)
    profile = Profile.objects.order_by('-points')[:2]
    return render(request,'profile.html',{'profile':profile,'user_profile':user_profile})

def showimage(reqeust):
    plt.plot([1, 2, 3, 4], [3, 4, 3, 5])
 
    xlabel('TotalContest')
    ylabel('AvgSolve')
    title('Perforance graph')
    grid(True)

    # Plot
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(),content_type="image/png")