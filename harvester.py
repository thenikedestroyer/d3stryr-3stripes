from flask import Flask, request, render_template
from settings import user_config

harvest_server = Flask(__name__)


@harvest_server.route('/', methods=['GET', 'POST'])
def manual_harvest():
    """
    View for manual harvesting.
    """
    sitekey = user_config.sitekey
    token = request.form.get('g-recaptcha-response', '')
    return render_template('harvester.html', sitekey=sitekey, token=token)
