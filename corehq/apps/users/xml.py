from __future__ import absolute_import

"""
This module is used to generate xml responses for user registrations.
Spec: https://bitbucket.org/javarosa/javarosa/wiki/UserRegistrationAPI
"""
# this should eventually be harmonized with the other responses, but
# has been implemented quick and dirty
from casexml.apps.phone import xml as phone_xml
from couchforms.openrosa_response import ResponseNature, get_response_element


def get_response(user, created):
    if created:
        text = "Thanks for registering! Your username is %s" % user.username
    else:
        text = "Thanks for updating your information, %s." % user.username
        
    nature = ResponseNature.SUBMIT_USER_REGISTERED if created else \
             ResponseNature.SUBMIT_USER_UPDATED
    response = get_response_element(text, nature=nature)
    response.append(phone_xml.get_registration_element(user.to_ota_restore_user()))
    return phone_xml.tostring(response)
