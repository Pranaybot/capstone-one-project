from flask import render_template
from . import error_code_bp


@error_code_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error_code_404.html'), 404


@error_code_bp.app_errorhandler(405)
def server_access_not_allowed(e):
    return render_template('error_code_405.html'), 405


@error_code_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error_code_500.html'), 500