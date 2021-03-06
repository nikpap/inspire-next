# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015, 2016 CERN.
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
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""INSPIRE overlay repository for Invenio."""

import os

from setuptools import find_packages, setup


readme = open('README.rst').read()

install_requires = [
    'Flask-Gravatar>=0.4.2',
    'HarvestingKit>=0.6.2',
    'plotextractor>=0.1.2',
    'refextract>=0.1.0',
    'Sickle>=0.5.0',
    'orcid',
    'raven<=5.1.0',
    'retrying',
    'flower',
    'rt',
    'librabbitmq>=1.6.1',
    'invenio-jsonschemas==1.0.0a3',
    'idutils>=0.1.1',
    'invenio-access==1.0.0a5',
    'invenio-accounts==1.0.0a10',
    'invenio-admin==1.0.0a3',
    'invenio-assets==1.0.0a4',
    'invenio-base==1.0.0a6',
    'invenio-celery==1.0.0a3',
    'invenio-config==1.0.0a1',
    'invenio-i18n==1.0.0a4',
    'invenio-indexer==1.0.0a3',
    'invenio-logging==1.0.0a2',
    'invenio-mail==1.0.0a3',
    'invenio-oauthclient==1.0.0a1',
    'invenio-records==1.0.0a15',  # Add [versioning] in the future
    'invenio-rest[cors]==1.0.0a7',
    'invenio-search==1.0.0a7',
    'invenio-records-rest==1.0.0a10',
    'invenio-records-ui==1.0.0a6',
    'invenio-userprofiles==1.0.0a3',
    'invenio-utils==0.2.0',  # Not fully Invenio 3 ready
    'invenio>=3.0.0a1,<3.1.0',
    'dojson==1.0.1',
    'Flask-Breadcrumbs>=0.3.0',
    'Flask-Script>=2.0.5',
    'jsmin',
    'pytest-runner>=2.7.0',
]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pep257>=0.7.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
    'mock>=1.3.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.3',
    ],
    'postgresql': [
        'invenio-db[postgresql]>=1.0.0a6',
    ],
    'mysql': [
        'invenio-db[mysql]>=1.0.0a6',
    ],
    'sqlite': [
        'invenio-db>=1.0.0a6',
    ],
    'tests': tests_require,
    'development': [
        'Flask-DebugToolbar>=0.9',
        'ipython',
        'ipdb',
        'kwalitee',
        'honcho',
    ]
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('postgresql', 'mysql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
]

packages = find_packages(exclude=['docs'])

# Load __version__, should not be done using import.
# http://python-packaging-user-guide.readthedocs.org/en/latest/tutorial.html
g = {}
with open(os.path.join('inspirehep', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']


setup(
    name='Inspirehep',
    version=version,
    url='https://github.com/inspirehep/inspire-next',
    license='GPLv2',
    author='CERN',
    author_email='admin@inspirehep.net',
    description=__doc__,
    long_description=readme,
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'inspirehep = inspirehep.cli:cli',
        ],
        'dojson.cli.rule': [
            'hep = inspirehep.dojson.hep:hep',
            'hep2marc = inspirehep.dojson.hep:hep2marc',
            'hepnames = inspirehep.dojson.hepnames:hepnames',
            'hepnames2marc = inspirehep.dojson.hepnames2marc:hepnames2marc',
        ],
        'invenio_base.api_apps': [
            'inspire_theme = inspirehep.modules.theme:INSPIRETheme',
            'inspire_search = inspirehep.modules.search:INSPIRESearch',
            'inspire_workflows = inspirehep.modules.workflows:INSPIREWorkflows',
        ],
        'invenio_base.apps': [
            'inspire_theme = inspirehep.modules.theme:INSPIRETheme',
            'inspire_migrator = inspirehep.modules.migrator:INSPIREMigrator',
            'inspire_search = inspirehep.modules.search:INSPIRESearch',
            'inspire_authors = inspirehep.modules.authors:INSPIREAuthors',
            'inspire_literature_suggest = inspirehep.modules.literaturesuggest:INSPIRELiteratureSuggestion',
            'inspire_forms = inspirehep.modules.forms:INSPIREForms',
            'inspire_workflows = inspirehep.modules.workflows:INSPIREWorkflows',
            'arxiv = inspirehep.modules.arxiv:Arxiv',
            'crossref = inspirehep.modules.crossref:CrossRef',
        ],
        'invenio_assets.bundles': [
            'inspirehep_theme_css = inspirehep.modules.theme.bundles:css',
            'inspirehep_theme_js = inspirehep.modules.theme.bundles:js',
            'almondjs = inspirehep.modules.theme.bundles:almondjs',
            'requirejs = inspirehep.modules.theme.bundles:requirejs',
            'inspirehep_author_profile_js = inspirehep.modules.authors.bundles:js',
            'inspirehep_author_update_css = inspirehep.modules.authors.bundles:update_css',
            'inspirehep_forms_css = inspirehep.modules.forms.bundles:css',
            'inspirehep_forms_js = inspirehep.modules.forms.bundles:js',
            'inspirehep_detailed_js = inspirehep.modules.theme.bundles:detailedjs',
            'inspirehep_literaturesuggest_js = inspirehep.modules.literaturesuggest.bundles:js',
            'invenio_search_ui_search_js = inspirehep.modules.search.bundles:js',
            'inspire_workflows_ui_js_actions = inspirehep.modules.workflows.bundles:actions_js',
            'inspire_workflows_ui_js_details = inspirehep.modules.workflows.bundles:details_js',
        ],
        'invenio_jsonschemas.schemas': [
            'inspire_records = inspirehep.modules.records.jsonschemas',
        ],
        'invenio_search.mappings': [
            'records = inspirehep.modules.records.mappings',
            'holdingpen = inspirehep.modules.workflows.mappings',
        ],
        'invenio_workflows.workflows': [
            'literature = inspirehep.modules.literaturesuggest.workflows:Literature',
            'authornew = inspirehep.modules.authors.workflows:AuthorNew',
            'authorupdate = inspirehep.modules.authors.workflows:AuthorUpdate',
            'hep_ingestion = inspirehep.modules.workflows.workflows:HEPIngestion',
            'arxiv_ingestion = inspirehep.modules.workflows.workflows:ArXivIngestion',
        ],
        'invenio_pidstore.fetchers': [
            'inspire_recid_fetcher = inspirehep.modules.pidstore.fetchers:inspire_recid_fetcher',
        ],
        'invenio_pidstore.minters': [
            'inspire_recid_minter = inspirehep.modules.pidstore.minters:inspire_recid_minter',
        ],
        'invenio_workflows_ui.actions': [
            'author_approval = inspirehep.modules.authors.workflows.actions.author_approval:AuthorApproval',
            'core_approval = inspirehep.modules.workflows.actions.core_approval:CoreApproval',
            'hep_approval = inspirehep.modules.workflows.actions.hep_approval:HEPApproval',
        ],
        'invenio_db.models': [
            'inspire_workflows_audit = inspirehep.modules.workflows.models',
        ],
    },
    tests_require=tests_require,
)
