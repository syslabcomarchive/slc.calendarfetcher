from zope.schema import interfaces
from z3c.form import validator
from Products.validation import validation
from slc.calendarfetcher import calendarfetcher_messagefactory as _

class TextLineURLValidator(validator.SimpleFieldValidator):
    """ Validates a Text field for URLS (each one on a new line) """

    def validate(self, value):
        """  """
        urls = [v.strip() for v in value.split()]
        verify = validation.validatorFor("isURL")
        for url in urls:
            if verify(url) != True:
                msg = _("The specified resource, '%s' is not a valid URL." % url)
                raise interfaces.InvalidURI(msg)


