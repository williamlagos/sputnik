from django.views.generic.base import TemplateView, View

class HomePageView(TemplateView):
    template_name = "index.html"

class AdvantagesPageView(TemplateView):
    template_name = "advantages.html"

class PartnersPageView(TemplateView):
    template_name = "partners.html"

class PricingPageView(TemplateView):
    template_name = "pricing.html"

class ContactPageView(TemplateView):
    template_name = "contact.html"

class ProfilePageView(View):
    def profile_render(self, _):
        source = """
            <div class="col-xs-12 col-sm-6 col-md-3 col-lg-2 brick">
                <a class="block profile" href="#" style="display:block; background:black">
                <div class="box profile">
                <div class="content">
                <h2 class="name">{{ firstname }}</h2>
                <div class="centered">{{ career }}</div>
                </div>
                {% if visual %}
                    <img src="{{ visual }}" width="100%"/>
                {% else %}
                    <h1 class="centered"><span class="glyphicon glyphicon-user big-glyphicon"></span></h1>
                {% endif %}
                <div class="content centered">
                {{ bio }}
                <div class="id hidden">{{ id }}</div></div></div>
                <div class="date"> Joined in {{month}} {{ day }} </div>
            </a></div>
        """
        return Template(source).render(Context({
            'firstname': self.user.first_name,
            'career':    self.career,
            'id':        self.id,
            'visual':    self.visual,
            'bio':       self.bio,
            'day':       self.date.day,
            'month':     self.month
        }))

    def start(self, request):
        # User panel
        # return render(request,'interface.html',{
        #    'static_url':settings.STATIC_URL,                                  
        #    'user':'','perm':{},
        #    'name':'%s %s' % (u.first_name,u.last_name),'apps':[]                                     
        # },content_type='text/html')
        # Initial page
        return render(request, 'index.html', {'static_url': settings.STATIC_URL}, content_type='text/html')
