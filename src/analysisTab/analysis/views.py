from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, loader
from django.utils import simplejson
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _
import sys

def menu(request):
    #return HttpResponse("testing...")
    #t = loader.get_template('analysis/newMeAnalysis.html')
    #c = Context({})
    #return HttpResponse(t.render(c))
    return render_to_response('analysis/newMeAnalysis.html')

def getTrajectory(request, *a, **kw):
    try:
        response = None
        from analysisTab.analysis.models import Trajectory
        trajs = Trajectory.objects.all()
        trajList=[]
        for traj in trajs:
            trajList.append({'description':traj.short_description, 
                'initial_chemical_formula':traj.initial_chemical_formula, 
                'total_time':traj.total_time, 
                'creator':traj.creator, 
                'timestamp':traj.timestamp.isoformat()})
#        response = {'data':trajList}
#        assert isinstance(response, dict)
#        if 'result' not in response:
#            response['result'] = 'ok'
        response = trajList
    except KeyboardInterrupt:
        # Allow keyboard interrupts through for debugging.
        raise
    except Exception, e:
        # Mail the admins with the error
        exc_info = sys.exc_info()
        subject = 'JSON view error: %s' % request.path
        try:
            request_repr = repr(request)
        except:
            request_repr = 'Request repr() unavailable'
        import traceback
        message = 'Traceback:\n%s\n\nRequest:\n%s' % (
            '\n'.join(traceback.format_exception(*exc_info)),
            request_repr,
            )
        mail_admins(subject, message, fail_silently=True)
        # Come what may, we're returning JSON.
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = _('Internal error')+': '+str(e)
        response = {'result': 'error',
                    'text': msg}
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')

def pickTrajectory(request):        
    return render_to_response('analysis/pickTrajectory.html')

def settings(request):
    return render_to_response('analysis/settings.html')