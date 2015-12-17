from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "home/index.html"


class empresaHomePageView(TemplateView):
    template_name = "home/empresa.html"


class eventosHomePageView(TemplateView):
    template_name = "home/eventos.html"


class faqHomePageView(TemplateView):
    template_name = "home/faq.html"


class serviciosHomePageView(TemplateView):
    template_name = "home/servicios.html"


class contactHomePageView(TemplateView):
    template_name = "home/contact.html"


class casa_matrizHomePageView(TemplateView):
    template_name = "home/casa-matriz.html"


class chinandegaHomePageView(TemplateView):
    template_name = "home/chinandega.html"


class montoyaHomePageView(TemplateView):
    template_name = "home/montoya.html"


class errorHomePageView(TemplateView):
    template_name = "home/404.html"
