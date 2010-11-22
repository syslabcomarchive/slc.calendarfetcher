import logging
from urllib2 import HTTPError
import Acquisition 

import zope.component
from zope import interface
from zope.annotation.interfaces import IAnnotations

from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form import validator

from plone.z3cform import z2
from plone.z3cform.layout import FormWrapper

from Products.Archetypes.utils import addStatusMessage
from Products.Five import BrowserView

from p4a.calendar.interfaces import ICalendarEnhanced

from slc.calendarfetcher.validators import TextLineURLValidator
from slc.calendarfetcher import calendarfetcher_messagefactory as _
import interfaces

log = logging.getLogger('slc.calendarfetcher.browser.configform.py')

class ConfigForm(form.Form):
    """ """
    label = _(u"Configuration Settings for the Calendar fetcher")
    ignoreContext = True
    fields = field.Fields(interfaces.IConfigForm).select('calendar_urls',)
    buttons = button.Buttons(interfaces.IConfigForm).select(
                                                        'add_url',
                                                        'add_and_refresh'
                                                        )

    def updateWidgets(self):
        '''See interfaces.IForm'''
        form.Form.updateWidgets(self)
        self.widgets['calendar_urls'].rows = 10
        annotations = IAnnotations(self.context)
        widget_value = self.request.get('form.widgets.calendar_urls')
        if not widget_value:
            urls = annotations['slc.calendarfetcher-urls']
            widget_value = u'\n'.join(unicode(v) for v in sorted(urls or []))

        self.widgets['calendar_urls'].value = widget_value

    @button.handler(interfaces.IConfigForm['add_url'])
    def add_url(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = '\n'.join([error.error.__str__() for error in errors])
            return 

        urls = []
        if data.has_key('calendar_urls'):
            urls = [v.strip() for v in data['calendar_urls'].split()]

        annotations = IAnnotations(self.context)
        annotations['slc.calendarfetcher-urls'] = urls
        addStatusMessage(self.request, 'URLs Saved', type='info')
        self.request.response.redirect(self.context.REQUEST.get('URL'))

    @button.handler(interfaces.IConfigForm['add_and_refresh'])
    def add_and_refresh(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _(
                    "Please correct the following errors before saving the form"
                    )
            return 

        if data.has_key('calendar_urls'):
            urls = [v for v in data['calendar_urls'].split()]
        else:
            urls = []

        annotations = IAnnotations(self.context)
        annotations['slc.calendarfetcher-urls'] = urls
        addStatusMessage(self.request, 'URLs Saved', type='info')

        for url in urls:
            view = zope.component.queryMultiAdapter((self.context, self.request), 
                                          name='import.html', 
                                          default=None
                                        )
            try:
                message = view.import_from_url(url)
            except HTTPError, e:
                msg = "Received a '404 Not Found' error %s" % url
                addStatusMessage(self.request, msg, type='error')
            else:
                msg = '%s from %s' % (message, url)
                addStatusMessage(self.request, msg, type='info')

        self.request.response.redirect(self.context.REQUEST.get('URL'))


class FetcherConfigView(FormWrapper):
    """ """
    interface.implements(interfaces.IFetcherConfigView)
    id = u'calendar_urls.html'
    label = _(u"Configuration Settings for the Calendar fetcher")

    form = None # override this with a form class.
    forms = [ ConfigForm, ]

    def __init__(self, context, request):
        super(FetcherConfigView, self).__init__(context, request)
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


# set conditions for which fields the validator class applies
validator.WidgetValidatorDiscriminators(
                        TextLineURLValidator,
                        field=interfaces.IConfigForm['calendar_urls']
                        )

# Register the validator so it will be looked up by z3c.form machinery
zope.component.provideAdapter(TextLineURLValidator)


class FetcherUtils(BrowserView):
    """ """
    interface.implements(interfaces.IFetcherUtils)
    id = u'calendar_urls.html'
    label = _(u"Configuration Settings for the Calendar fetcher")

    def is_calendar_enhanced(self):
        """ """
        context = Acquisition.aq_inner(self.context)
        return ICalendarEnhanced.providedBy(context)

    def fetch_calendars(self):
        """ """
        context = Acquisition.aq_inner(self.context)
        annotations = IAnnotations(context)
        urls = annotations['slc.calendarfetcher-urls']
        for url in urls:
            cal_url = '/'.join(url.split('/')[:3])
            # Import the URL
            items = 0 # FIXME
            msg = "%s items imported from %s" % (len(items), cal_url)
            addStatusMessage(self.request, msg)


