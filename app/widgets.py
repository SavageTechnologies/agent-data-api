from markupsafe import Markup

# Example function using Markup from markupsafe
def render_widget(field, **kwargs):
    html = '<input type="text" name="{}" value="{}">'.format(field.name, field.data or '')
    return Markup(html)
