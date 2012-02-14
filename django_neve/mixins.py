from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ImproperlyConfigured


class AjaxTemplateResponseMixin(TemplateResponseMixin):
    ajax_template_name = None
    
    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None or self.ajax_template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either the definition of "
                "'template_name' and 'ajax_template_name', or an implementation of 'get_template_names()'")
        else:
            if self.request.is_ajax:
                return [self.template_name]
            else:
                return [self.template_name]
