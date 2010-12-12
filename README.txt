Introduction
============

slc.calendarfetcher provides the ability to import multiple ICS calendar files
(specified by their URLs) into a single folder. The folder must be subtyped as
a Calendar, which is functionality provided by p4a.plonecalendar.

A tab labeled 'Import ICal' will appear on the folder, which leads the user to
a simple form where multiple calendar URLs may be specified.

This form can be saved with the optional feature of immediately importing all
events from the specified URLs.

By using a cronjob or Zope's clockserver, this can be made automatic and periodically
repeatable, ensuring that your Plone calendar is always up to date with the
events from any other ICS conforming calendar (like iCal or Google Calendar).


Installation:
-------------

Add slc.calendarfetcher to the eggs in the [instance] section of your buildout
or install it via easy_install.

In Plone, slc.calendarfetcher can be installed via the portal_quickinstaller
tool in the Zope Management Interface or in the Add-remove products section of
Plone's control panel.

