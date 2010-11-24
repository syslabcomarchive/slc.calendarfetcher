import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from zope import component
from zope.interface import alsoProvides
from zope.annotation.interfaces import IAnnotations
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import slc.calendarfetcher
from p4a.calendar.interfaces import ICalendarEnhanced


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(slc.calendarfetcher)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


class TestFetcher(TestCase):

    def afterSetUp(self):
        """ Create a Seminar object, and call the relevant event to enable the
            auto-creation of the sub-objects ('speakers', 'speech venues').
        """
        self.loginAsPortalOwner()
        portal = self.portal
        portal.invokeFactory('Folder', 'calendar', title="Calendar")
        calendar = getattr(portal, 'calendar')
        annotations = IAnnotations(calendar)
        annotations['slc.calendarfetcher-urls'] = [
            'http://www.google.com/calendar/ical/german__en%40holiday.calendar.google.com/public/basic.ics',
            'http://www.google.com/calendar/ical/sa__en%40holiday.calendar.google.com/public/basic.ics',
            ]
        alsoProvides(calendar, ICalendarEnhanced)


    def test_calendarfetcher(self):
        """ Tests:
            slc.calendarfetcher.browser.calendarfetcher.CalendarFetcherUtils 
        """
        portal = self.portal
        calendar = getattr(portal, 'calendar')
        request = self.folder.REQUEST
        view = component.queryMultiAdapter(
                                    (calendar, request), 
                                    name='calendarfetcher_utils', 
                                    default=None
                                    )

        # Check that subflolders are created.
        view.fetch_calendars()
        self.assertEquals(len(calendar.objectValues()) !=  0, True)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFetcher))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
