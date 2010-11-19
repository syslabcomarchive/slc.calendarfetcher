import logging
import Acquisition 
from zope import interface
from zope.annotation.interfaces import IAnnotations
from z3c.form import form
from z3c.form import field
from z3c.form import button
from plone.z3cform import z2
from plone.z3cform.layout import FormWrapper
from Products.statusmessages.interfaces import IStatusMessage

from slc.calendarfetcher import calendarfetcher_messagefactory as _
import interfaces

log = logging.getLogger('slc.calendarfetcher.browser.configform.py')


class ConfigForm(form.Form):
    """ """
    label = _(u"Configuration Settings for the Calendar fetcher")
    ignoreContext = True
    fields = field.Fields(interfaces.IConfigForm).select('calendar_urls',)
    buttons = button.Buttons(interfaces.IConfigForm).select('add_url',)

    def updateWidgets(self):
        '''See interfaces.IForm'''
        form.Form.updateWidgets(self)
        self.widgets['calendar_urls'].rows = 20
        annotations = IAnnotations(self.context)
        urls = annotations['slc.calendarfetcher-urls']
        display_value = u'\n'.join(unicode(v) for v in sorted(urls or []))
        self.widgets['calendar_urls'].value = display_value

    @button.handler(interfaces.IConfigForm['add_url'])
    def add_url(self, action):
        # TODO: Validate strings as URLs!
        status = IStatusMessage(self.request)
        data, error = self.extractData()
        if data.has_key('calendar_urls'):
            urls = [v for v in data['calendar_urls'].split('')]
        else:
            urls = []

        annotations = IAnnotations(self.context)
        annotations['slc.calendarfetcher-urls'] = urls

        status.addStatusMessage('URLs Saved', type='info')
        self.request.response.redirect(self.context.REQUEST.get('URL'))


class ConfigFormView(FormWrapper):
    """ """
    interface.implements(interfaces.IConfigFormView)
    id = u'calendar_urls.html'
    label = _(u"Configuration Settings for the Calendar fetcher")

    form = None # override this with a form class.
    forms = [ ConfigForm, ]

    def __init__(self, context, request):
        super(ConfigFormView, self).__init__(context, request)
        self.form_instances = \
            [form(Acquisition.aq_inner(self.context), self.request) for form in self.forms]

    def update(self):
        z2.switch_on(self, request_layer=self.request_layer)
        for form_instace in self.form_instances:
            form_instace.update()

    def contents(self):
        z2.switch_on(self, request_layer=self.request_layer)
        # XXX really messed up hack to support plone.z3cform < 0.5.8
        # We call every form to make the widgets property available on it,
        # otherwise view/widgets fails
        # XXX: FIXME!!!
        [fi() for fi in self.form_instances]
        return ''.join([fi.render() for fi in self.form_instances])

    def render_form(self):
        """This method combines the individual forms and renders them.
        """
        return ''.join([fi() for fi in self.form_instances])


