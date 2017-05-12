"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import sys
import os
from django.test import TestCase


class FitParseTests(TestCase):
    def test_can_parse_activity(self):
        #activity = Activity("/Users/ryangreyer/Downloads/FitSDKRelease_8.00/examples/Activity.fit")
        #activity = Activity("/Users/ryangreyer/Downloads/2013-07-07-09-02-42.fit")
        #activity = Activity("/Users/ryangreyer/Downloads/2013-02-03-12-32-25-CAD and Power.fit")
        activity = Activity("/code/fitfiletools.fit")
        activity.parse()

        # Records of type 'record' (I know, confusing) are the entries in an
        # activity file that represent actual data points in your workout.
        records = activity.get_records_as_dicts()
        current_record_number = 0

        for record in records:

            #Print record number
            current_record_number += 1
            print (" Record #%d " % current_record_number).center(40, '-')

            for key, val in record.items():
                print " * %s: %s" % (key, val)

            if current_record_number > 100:
                return

            #Get the list of valid fields on this record
            valid_field_names = record.get_valid_field_names()

            for field_name in valid_field_names:
                # Get the data and units for the field
                field_data = record.get_data(field_name)
                field_units = record.get_units(field_name)

                # Print what we've got!
                if field_units:
                    print " * %s: %s %s" % (field_name, field_data, field_units)
                else:
                    print " * %s: %s" % (field_name, field_data)

            True
