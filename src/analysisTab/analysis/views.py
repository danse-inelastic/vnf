from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, loader
#from analysis.

#views
def menu(request):
    #return HttpResponse("testing...")
    #t = loader.get_template('analysis/newMeAnalysis.html')
    #c = Context({})
    #return HttpResponse(t.render(c))
    return render_to_response('analysis/newMeAnalysis.html')

def getTrajectories(request):
    from analysisTab.analysis.models import Trajectory
    trajs = Trajectory.objects.all()
    trajJson=[]
    for traj in trajs:
        trajJson.append([traj.short_description, traj.initial_chemical_formula, 
                         traj.total_time, traj.creator, traj.timestamp])
    import json
    return json.dumps(trajJson)

def pickTrajectory(request):        
    return render_to_response('analysis/pickTrajectory.html')

def settings(request):
    return render_to_response('analysis/settings.html')