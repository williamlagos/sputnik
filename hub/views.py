from django.views.generic.base import TemplateView

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
