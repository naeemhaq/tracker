import sys
import json
import os
from os.path import dirname, join, expanduser, normpath, realpath

import pytest
from graphene.test import Client

from unittest import TestCase

from manage import seed, remove_seed
seed()
from app import app
from db import db
from models import Sectors, Groups, Organizations
from queries import schema
remove_seed()

# This is the only way I could get imports to work for unit testing.
PACKAGE_PARENT = '..'
SCRIPT_DIR = dirname(realpath(join(os.getcwd(), expanduser(__file__))))
sys.path.append(normpath(join(SCRIPT_DIR, PACKAGE_PARENT)))


@pytest.fixture(scope='class')
def org_test_db_build():
    db.init_app(app)

    with app.app_context():
        group = Groups(
            id=1,
            s_group='GC_A',
            description='Arts',
        )
        db.session.add(group)

        group = Groups(
            id=2,
            s_group='GC_BF',
            description='Banking and Finance',
        )
        db.session.add(group)

        org = Organizations(
            id=1,
            organization='Arts',
            description='Arts',
            group_id=1
        )
        db.session.add(org)

        org = Organizations(
            id=6,
            organization='BOC',
            description='BOC - Bank of Canada',
            group_id=2
        )
        db.session.add(org)
        db.session.commit()

    yield

    with app.app_context():
        Organizations.query.delete()
        Groups.query.delete()
        db.session.commit()


@pytest.mark.usefixtures("org_test_db_build")
class TestOrgResolver(TestCase):
    def test_get_org_resolvers_by_id(self):
        """Test get_organization_by_id resolver"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgById(id: 1){
                    description
                    organization
                    }
            }"""
            result_refr = {
                "data": {
                    "getOrgById": [
                        {
                            "description": "Arts",
                            "organization": "Arts"
                        }
                    ]
                }
            }

            result_eval = client.execute(query)
        self.assertDictEqual(result_refr, result_eval)

    def test_get_org_resolvers_by_org(self):
        """"Test get_org_by_org resolver"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgByOrg(org: Arts){
                    description
                    organization
                }
            }"""
            result_refr = {
                "data": {
                    "getOrgByOrg": [
                        {
                            "description": "Arts",
                            "organization": "Arts"
                        }
                    ]
                }
            }

            result_eval = client.execute(query)
        self.assertDictEqual(result_refr, result_eval)

    def test_get_org_resolvers_by_group(self):
        """Test get_org_by_group_id resolver"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgByGroup(group: GC_A){
                    description
                    groupId
                }
            }"""
            result_refr = {
                "data": {
                    "getOrgByGroup": [
                        {
                            "description": "Arts",
                            "groupId": 1
                        }
                    ]
                }
            }

            result_eval = client.execute(query)
        self.assertDictEqual(result_refr, result_eval)

    def test_org_resolver_by_id_invalid(self):
        """Test get_org_by_id invalid ID error handling"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgById(id: 9999){
                    description
                    groupId
                }
            }"""
            executed = client.execute(query)

        assert executed['errors']
        assert executed['errors'][0]
        assert executed['errors'][0]['message'] == "Error, Invalid ID"

    def test_org_resolver_by_org_invalid(self):
        """Test get_org_by_org invalid sector error handling"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgByOrg(org: fds){
                    id
                    description
                }
            }"""
            executed = client.execute(query)

        assert executed['errors']
        assert executed['errors'][0]
        assert executed['errors'][0][
                   'message'] == f'Argument "org" has invalid value fds.\nExpected type "OrganizationsEnum", found fds.'

    def test_org_resolver_by_group_invalid(self):
        """Test get_org_by_group invalid Zone error handling"""
        with app.app_context():
            client = Client(schema)
            query = """
            {
                getOrgByGroup(group: dsa){
                    id
                    description
                }
            }"""
            executed = client.execute(query)

        assert executed['errors']
        assert executed['errors'][0]
        assert executed['errors'][0][
                   'message'] == f'Argument "group" has invalid value dsa.\nExpected type "GroupEnums", found dsa.'
