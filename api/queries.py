import os
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene import String
from flask_graphql_auth import *
import pyotp

import graphene
from sqlalchemy.orm import joinedload
from graphene import relay, String
import pyotp

from model_enums.sectors import SectorEnums, ZoneEnums
from model_enums.groups import GroupEnums
from model_enums.organiztions import OrganizationsEnum

from schemas.user import *

from scalars.url import URL

from schemas.sectors import Sectors
from schemas.groups import Groups
from schemas.organizations import Organizations
from schemas.domains import Domains


from resolvers.sectors import (
	resolve_get_sector_by_id,
	resolve_get_sectors_by_sector,
	resolve_get_sector_by_zone
)

from resolvers.groups import (
	resolve_get_group_by_id,
	resolve_get_group_by_group,
	resolve_get_group_by_sector

)

from resolvers.users import (
	resolve_test_user_claims,
	resolve_generate_otp_url,
)

from resolvers.organizations import (
	resolve_get_org_by_id,
	resolve_get_org_by_org,
	resolve_get_orgs_by_group
)

from resolvers.domains import (
	resolve_get_domain_by_id,
	resolve_get_domain_by_domain,
	resolve_get_domain_by_organization
)

class Query(graphene.ObjectType):
	"""The central gathering point for all of the GraphQL queries."""
	node = relay.Node.Field()
	all_users = SQLAlchemyConnectionField(UserConnection, sort=None)
	# all_users = graphene.List(UserObject, failedAttempts=graphene.Int(), resolver=resolve_all_users)
	# all_sectors = SQLAlchemyConnectionField(SectorsConnection, sort=None)
	# all_groups = SQLAlchemyConnectionField(GroupsConnection, sort=None)
	get_sector_by_id = graphene.List(
		of_type=Sectors,
		id=graphene.Argument(graphene.Int, required=True),
		resolver=resolve_get_sector_by_id,
		description="Allows selection of a sector from a given sector ID"
	)
	get_sectors_by_sector = graphene.List(
		of_type=Sectors,
		sector=graphene.Argument(SectorEnums, required=True),
		resolver=resolve_get_sectors_by_sector,
		description="Allows selection of sector information from a given sector enum"
	)
	get_sector_by_zone = graphene.List(
		of_type=Sectors,
		zone=graphene.Argument(ZoneEnums, required=True),
		resolver=resolve_get_sector_by_zone,
		description="Allows selection of all sectors from a given zone enum"
	)
	get_group_by_id = graphene.List(
		of_type=Groups,
		id=graphene.Argument(graphene.Int, required=True),
		resolver=resolve_get_group_by_id,
		description="Allows selection of a group from a given group ID"
	)
	get_group_by_group = graphene.List(
		of_type=Groups,
		group=graphene.Argument(GroupEnums, required=True),
		resolver=resolve_get_group_by_group,
		description="Allows the selection of group information from a given group enum"
	)
	get_group_by_sector = graphene.List(
		of_type=Groups,
		sector=graphene.Argument(SectorEnums, required=True),
		resolver=resolve_get_group_by_sector,
		description="Allows selection of groups from a given sector enum"
	)
	get_org_by_id = graphene.List(
		of_type=Organizations,
		id=graphene.Argument(graphene.Int, required=True),
		resolver=resolve_get_org_by_id,
		description="Allows the selection of an organization from a given ID"
	)
	get_org_by_org = graphene.List(
		of_type=Organizations,
		org=graphene.Argument(OrganizationsEnum, required=True),
		resolver=resolve_get_org_by_org,
		description="Allows the selection of an organization from its given organization code"
	)
	get_org_by_group = graphene.List(
		of_type=Organizations,
		group=graphene.Argument(GroupEnums, required=True),
		resolver=resolve_get_orgs_by_group,
		description="Allows the selection of organizations from a given group"
	)
	get_domain_by_id = graphene.List(
		of_type=Domains,
		id=graphene.Argument(graphene.Int, required=True),
		resolver=resolve_get_domain_by_id,
		description="Allows the selection of a domain from a given ID"
	)
	get_domain_by_domain = graphene.List(
		of_type=Domains,
		url=graphene.Argument(URL, required=True),
		resolver=resolve_get_domain_by_domain,
		description="Allows the selection of a domain from a given domain"
	)
	get_domain_by_organization = graphene.List(
		of_type=Domains,
		org=graphene.Argument(OrganizationsEnum, required=True),
		resolver=resolve_get_domain_by_organization,
		description="Allows the selection of domains under an organization"
	)

	generate_otp_url = graphene.String(
		email=graphene.Argument(EmailAddress, required=True),
		resolver=resolve_generate_otp_url,
		description="An api endpoint used to generate a OTP url used for two factor authentication."
	)

	test_user_claims = graphene.String(
		token=graphene.Argument(graphene.String, required=True),
		resolver=resolve_test_user_claims,
		description="An api endpoint to view a current user's claims -- Requires an active JWT."
	)


class Mutation(graphene.ObjectType):
	"""The central gathering point for all of the GraphQL mutations."""
	create_user = CreateUser.Field()
	sign_in = SignInUser.Field()
	update_password = UpdateUserPassword.Field()
	authenticate_two_factor = ValidateTwoFactor.Field()
	update_user_role = UpdateUserRole.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)