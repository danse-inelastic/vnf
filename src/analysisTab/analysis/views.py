from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, loader
from django.utils import simplejson
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _
import sys, math

def menu(request):
    #return HttpResponse("testing...")
    #t = loader.get_template('analysis/newMeAnalysis.html')
    #c = Context({})
    #return HttpResponse(t.render(c))
    return render_to_response('analysis/newMeAnalysis.html')

def dbPrep(request, *a, **kw):
    json = request.POST['_gt_json']
    pageNo = json['pageInfo']['pageNum']
    pageSize = json['pageInfo']['pageSize']
    try:
        response = None
        from analysisTab.analysis.models import Trajectory
        trajs = Trajectory.objects.all()
        
    except:
        raise 'unable to connect to db'
    totalRec = len(trajs)
    if pageNo<1 or pageNo > math.ceil(totalRec/pageSize):
        pageNo=1
    return json, totalRec,

def getTrajectory(request, *a, **kw):
    json, totalRec = dbPrep(request, *a, **kw)
    if json['action']=='load':
        #pageno starts with 1 instead of 0
        from analysisTab.analysis.models import Trajectory
        data = Trajectory.objects.all()
        
#        trajList=''
#        template = """{description:'%s',initial_chemical_formula:'%s',total_time:%s,creator:'%s',timestamp:%s}"""
#        for traj in trajs:
#            entry = template % (traj.short_description,traj.initial_chemical_formula,
#                                traj.total_time, traj.creator, traj.timestamp.isoformat())
#            trajList+=entry
#        trajList='['+trajList+']'
#        response = "{data:"+trajList+"}"

        trajList=''
        template = """{description:'%s',initial_chemical_formula:'%s',total_time:%s,creator:'%s',timestamp:'%s'}"""
        for traj in trajs:
            entry = template % (traj.short_description,traj.initial_chemical_formula,
                                traj.total_time, traj.creator, traj.timestamp.isoformat())
            trajList+=entry
        trajList='['+trajList+']'
        response = trajList
        
        ret = "{data:" + data +",\n"
        ret += "pageInfo:{totalRowNum:" + totalRec + "},\n"
        ret += "recordType : 'object'}"
        return ret
    elif json['action'] == 'save':
        sql = ""
        params = []
        errors = ""
        #deal with those deleted
        deletedRecords = json['deletedRecords']
        for value in deletedRecords:
            params = value.order_no
        sql = "delete from orders where order_no in (" . join(",", $params) . ")";
        if(mysql_query(sql)==FALSE):
            errors += mysql_error();
        #deal with those updated
        sql = ""
        updatedRecords = json['updatedRecords']
        for value in updatedRecords:
          $sql = "update `orders` set ".
            "`employee`='".$value->employee . "', ".
            "`country`='".$value->country . "', ".
            "`customer`='".$value->customer . "', ".
            "`order2005`=".$value->order2005 . ", ".
            "`order2006`=".$value->order2006 . ", ".
            "`order2007`=".$value->order2007 . ", ".
            "`order2008`=".$value->order2008 . ", ".
            "`delivery_date`='".$value->delivery_date . "' ".
            "where `order_no`=".$value->order_no;
            if(mysql_query($sql)==FALSE)
              $errors += mysql_error();
        #deal with those inserted
        sql = ""
        insertedRecords = $json->{'insertedRecords'};
        foreach ($insertedRecords as $value){
          $sql = "insert into orders (`employee`, `country`, `customer`, `order2005`,`order2006`, `order2007`, `order2008`, `delivery_date`) VALUES ('".
            $value->employee."', '".$value->country."', '".$value->customer."', '".$value->order2005."', '".$value->order2006."', '".$value->order2007."', '".$value->order2008."',  '".$value->delivery_date."')";
          if(mysql_query($sql)==FALSE){
            $errors .= mysql_error();
        $ret = "{success : true,exception:''}";
        return ret
#        response = {'data':trajList}
#        assert isinstance(response, dict)
#        if 'result' not in response:
#            response['result'] = 'ok'
        
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
    #return HttpResponse(json, mimetype='application/json')
    return HttpResponse(json, mimetype='text/javascript')

def pickTrajectory(request):        
    return render_to_response('analysis/pickTrajectory.html')

def settings(request):
    return render_to_response('analysis/settings.html')