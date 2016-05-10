from base.models import Categoria, Marca
from django import template

register = template.Library()


class Categorias_Node(template.Node):

    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<Get Categorias Node>"

    def render(self, context):
            context[self.varname] = Categoria.objects.filter(activo=True)
            return ''


@register.tag
def get_categorias(parser, token):
    """
            uso
            {% get_categorias as [varname] %}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_categorias' requiere de dos argumentos y se dieron %s"
            % (args))

    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_categorias' requiere que el primer argumento sea 'as'")

    return Categorias_Node(varname=tokens[2])


class Marcas_Node(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<Get Marcas Node>"

    def render(self, context):
            context[self.varname] = Marca.objects.filter(activo=True)
            return ''


@register.tag
def get_marcas(parser, token):
    """
        uso
            {% get_marcas as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_marcas' requiere de dos argumentos y se dieron %s" % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_marcas' requiere que el primer argumento sea 'as'")

    return Marcas_Node(varname=tokens[2])
