import os
import plone.z3cform

from slc.calendarfetcher.browser.calendarfetcher import FetcherConfigView

form_adapter = plone.z3cform.templates.ZopeTwoFormTemplateFactory(
        os.path.join(os.path.dirname(__file__), 'templates/configform.pt'),
        form=FetcherConfigView
        )
