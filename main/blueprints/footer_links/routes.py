from flask import Blueprint, render_template
from . import footer_links_bp


@footer_links_bp.route("/contact_newgen")
def contact_newgen():
    return render_template("contact_newgen.html")


@footer_links_bp.route("/faq")
def faq():
    return render_template("faq.html")


@footer_links_bp.route("/receipts_refunds")
def receipts_refunds():
    return render_template("receipts_refunds.html")


@footer_links_bp.route("/terms_and_conditions")
def terms_and_conditions():
    return render_template("terms_and_conditions.html")


@footer_links_bp.route("/business_programs")
def business_programs():
    return render_template("business_programs.html")


@footer_links_bp.route("/trip_insurance")
def trip_insurance():
    return render_template("trip_insurance.html")
