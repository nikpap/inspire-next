# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Contains INSPIRE specific filtering tasks"""


from functools import wraps

from invenio.legacy.bibsched.bibtask import write_message


def launch_workflows(workflow_name):
    """Run workflows for OAI harvested records."""
    @wraps(launch_workflows)
    def _launch_workflows(obj, eng):
        from invenio.modules.oaiharvester.utils import (
            record_extraction_from_file,
            identifier_extraction_from_string
        )
        from invenio.modules.workflows.models import BibWorkflowObject

        def log_message(msg):
            write_message(msg)
            eng.log.info(msg)

        identifiers = []
        log_message("Extracting records from {0}".format(obj.data))
        for record_xml in record_extraction_from_file(obj.data):
            if not record_xml:
                obj.log.error("No valid record found. Next..")
                continue
            elif isinstance(record_xml, list):
                # In case it is a list
                record_xml = record_xml[0]

            identifier = (identifier_extraction_from_string(record_xml) or
                          identifier_extraction_from_string(record_xml, oai_namespace="") or
                          "")
            if identifier in identifiers:
                # Already taken care of this guy
                continue
            identifiers.append(identifier)

            record_object = BibWorkflowObject.create_object()
            record_object.save()  # Saving to set default extra_data and data
            record_object.extra_data = record_object.get_extra_data()
            record_object.extra_data["oai_identifier"] = identifier
            record_object.extra_data["repository"] = obj.extra_data.get("repository")
            record_object.set_extra_data(record_object.extra_data)

            record_object.set_data(record_xml)
            record_object.start_workflow(workflow_name, delayed=True)

            log_message("Created workflow for {0}".format(identifier))
        log_message("Extracted {0} records".format(len(identifiers)))

    return _launch_workflows
