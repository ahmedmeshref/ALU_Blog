from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


# handel 403 errors; "permission is not allowed"
@errors.app_errorhandler(403)
def error_403(error):
    # render the 403 html page with the status of the error
    return render_template('errors/403.html'), 403


# handel 500 errors; general server error
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


# handel 404 errors; page not found
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404
