"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import sys
import os
from fitparse import Activity
from django.test import TestCase


class FitParseTests(TestCase):
    def test_can_parse_activity(self):
        activity = Activity("/Users/ryangreyer/Downloads/FitSDKRelease_8.00/examples/Activity.fit")
        activity.parse()

        # Records of type 'record' (I know, confusing) are the entries in an
        # activity file that represent actual data points in your workout.
        records = activity.get_records_by_type('record')
        current_record_number = 0

        for record in records:

            # Print record number
            current_record_number += 1
            print (" Record #%d " % current_record_number).center(40, '-')

            # Get the list of valid fields on this record
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

            print
