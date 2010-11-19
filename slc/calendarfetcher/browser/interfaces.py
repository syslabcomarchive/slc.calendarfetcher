from zope import schema
from zope import interface
from plone.theme.interfaces import IDefaultPloneLayer
from z3c.form import button
from slc.calendarfetcher import calendarfetcher_messagefactory as _

class ICalendarFetcherLayer(IDefaultPloneLayer):
    """ Marker Interface used by BrowserLayer
    """

class IConfigForm(interface.Interface):
    """ Base Schema for the edit form. It is dynamically extended by plugins
    """
    calendar_urls = schema.Text(
                        title=_(u"Calendar URLs"),
                        description=_(
                            u"Specify the URLs which the fetcher must import"
                            ),
                        required=True,
                        ) 

    add_url = button.Button(title=u'Submit')


class IConfigFormView(interface.Interface):
    """ Marker interface
    """

