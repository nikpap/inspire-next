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

"""Implements an example of a typical ingestion workflow for MARCXML records."""

from invenio.modules.workflows.tasks.marcxml_tasks import (
    get_obj_extra_data_key,
    update_last_update
)

from invenio.modules.oaiharvester.tasks.harvesting import (
    get_repositories_list,
    init_harvesting,
    harvest_records,
)

from invenio.modules.workflows.tasks.logic_tasks import (
    foreach,
    end_for,
)

from invenio.modules.oaiharvester.workflows.oaiharvest_harvest_repositories import (
    oaiharvest_harvest_repositories,
)

from inspire.modules.workflows.tasks.harvesting import launch_workflows


class ingestion_arxiv_math(oaiharvest_harvest_repositories):

    """Main workflow for harvesting arXiv via OAI-PMH (oaiharvester)."""

    object_type = "workflow"
    record_workflow = "process_record_arxiv"

    workflow = [
        init_harvesting,
        foreach(get_repositories_list(), "repository"),
        [
            harvest_records,
            foreach(get_obj_extra_data_key("harvested_files_list")),
            [
                launch_workflows("process_record_arxiv"),
            ],
            end_for
        ],
        end_for,
        update_last_update(get_repositories_list())
    ]
