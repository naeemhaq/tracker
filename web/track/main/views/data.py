import json
import os

from http import HTTPStatus

from flask import Response

from track import models
from track.cache import cache
from track.main import main


# Data endpoints.
# High-level %'s, used to power the donuts.
@main.route("/data/reports/<report_name>.json")
@cache.cached()
def report(report_name):
	report_name = "https" if report_name == "compliance" else report_name

	response = Response(json.dumps(models.Report.latest().get(report_name, {})))
	response.headers["Content-Type"] = "application/json"
	return response


# Detailed data per-parent-domain.
@main.route("/data/domains/<report_name>.json")
@cache.cached()
def domain_report(report_name):
	report_name = "https" if report_name == "compliance" else report_name
	domains = models.Domain.eligible_parents(report_name)
	domains = sorted(domains, key=lambda k: k["domain"])

	response = Response(json.dumps({"data": domains}))
	response.headers["Content-Type"] = "application/json"
	return response


@main.route("/data/domains/<language>/<report_name>.csv")
@cache.cached()
def domain_report_csv(report_name, language):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Domain.eligible_parents(report_name)
	domains = sorted(domains, key=lambda k: k["domain"])

	response = Response(models.Domain.to_csv(domains, report_name, language))
	response.headers["Content-Type"] = "text/csv"
	return response


@main.route("/data/domains-table.json")
@cache.cached()
def domains_table():
	domains = models.Domain.find_all(
		{"https.eligible_zone": True, "is_parent": True},
		{
			"_id": False,
			"domain": True,
			"organization_name_en": True,
			"organization_name_fr": True,
			"is_parent": True,
			"base_domain": True,
			"https.eligible": True,
			"https.enforces": True,
			"https.hsts": True,
			"https.compliant": True,
			"https.bod_crypto": True,
			"https.good_cert": True,
			"totals.https.enforces": True,
			"totals.https.hsts": True,
			"totals.https.compliant": True,
			"totals.https.eligible": True,
			"totals.crypto.bod_crypto": True,
			"totals.crypto.good_cert": True,
			"totals.crypto.eligible": True,
		},
	)
	response = Response(json.dumps({"data": list(domains)}))
	response.headers["Content-Type"] = "application/json"
	return response


@main.route("/data/organizations-table.json")
@cache.cached()
def organizations_table():
	organizations = models.Organization.find_all(
		{"https.eligible": {"$gt": 0}},
		{
			"_id": False,
			"total_domains": True,
			"name_en": True,
			"name_fr": True,
			"https.compliant": True,
			"https.enforces": True,
			"https.hsts": True,
			"https.eligible": True,
			"crypto.bod_crypto": True,
			"crypto.good_cert": True,
			"crypto.eligible": True,
		},
	)
	# app.logger.debug([o for o in organizations])
	response = Response(json.dumps({"data": list(organizations)}))
	response.headers["Content-Type"] = "application/json"
	return response


# Detailed data per-host for a given report.
@main.route("/data/hosts/<report_name>.json")
@cache.cached()
def hostname_report(report_name):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Domain.eligible(report_name)

	# sort by base domain, but subdomain within them
	domains = sorted(domains, key=lambda k: k["domain"])
	domains = sorted(domains, key=lambda k: k["base_domain"])

	response = Response(json.dumps({"data": domains}))
	response.headers["Content-Type"] = "application/json"
	return response


@main.route("/data/hosts/<language>/<report_name>.csv")
@cache.cached()
def hostname_report_csv(language, report_name):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Domain.eligible(report_name)

	# sort by base domain, but subdomain within them
	domains = sorted(domains, key=lambda k: k["domain"])
	domains = sorted(domains, key=lambda k: k["base_domain"])

	response = Response(models.Domain.to_csv(domains, report_name, language))
	response.headers["Content-Type"] = "text/csv"
	return response


# Detailed data for all subdomains of a given parent domain, for a given report.
@main.route("/data/hosts/<domain>/<report_name>.json")
@cache.cached()
def hostname_report_for_domain(domain, report_name):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Domain.eligible_for_domain(domain, report_name)

	# sort by hostname, but put the parent at the top if it exist
	domains = sorted(domains, key=lambda k: k["domain"])
	domains = sorted(domains, key=lambda k: k["is_parent"], reverse=True)

	response = Response(json.dumps({"data": domains}))
	response.headers["Content-Type"] = "application/json"
	return response


# Detailed data for all subdomains of a given parent domain, for a given report.
@main.route("/data/hosts/<domain>/<language>/<report_name>.csv")
@cache.cached()
def hostname_report_for_domain_csv(domain, language, report_name):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Domain.eligible_for_domain(domain, report_name)

	# sort by hostname, but put the parent at the top if it exist
	domains = sorted(domains, key=lambda k: k["domain"])
	domains = sorted(domains, key=lambda k: k["is_parent"], reverse=True)

	response = Response(models.Domain.to_csv(domains, report_name, language))
	response.headers["Content-Type"] = "text/csv"
	return response


@main.route("/data/organizations/<report_name>.json")
@cache.cached()
def organization_report(report_name):
	report_name = "https" if report_name == "compliance" else report_name

	domains = models.Organization.eligible(report_name)
	response = Response(json.dumps({"data": list(domains)}))
	response.headers["Content-Type"] = "application/json"
	return response
