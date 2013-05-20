from efforia.main import Efforia
from models import Promoted,Movement,Project,Event

class Promoteds(Efforia):
    def promote_form(self,request):
        return render(request,'promote.jade',{},content_type='text/html')
    def promote(self,request):
        u = self.current_user(request)
        for k,v in request.REQUEST.iteritems():
            if 'content' in k: content = v
            elif 'id' in k: promotedid = v
            elif 'token' in k: token = v
        move = Movement.objects.filter(cause_id=promotedid)
        if len(move) > 0: p = Promoted(name='$#',prom=promotedid,content=content,user=u); p.save()
        else: s = Promoted(name=token,prom=promotedid,content=content,user=u); s.save() 
        return response('Project promoted successfully')
    def promoted(self,request):
        u = self.current_user(request)
        ident = request.REQUEST['id']
        print ident
        p = Promoted.objects.filter(prom=ident)
        print p
        pobj = self.object_token(p[0].name)
        o = globals()[pobj].objects.filter(id=ident)[0]
        feed = list(p); feed.append(o)
        return self.view_mosaic(request,feed)
