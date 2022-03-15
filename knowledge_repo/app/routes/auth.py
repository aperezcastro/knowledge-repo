from ..proxies import current_app
from flask import (
    current_app,
    redirect,
    render_template,
    url_for,
    Blueprint,
)
from flask_login import logout_user, login_required
from flask_principal import identity_changed, AnonymousIdentity

blueprint = Blueprint('auth', __name__,
                      template_folder='../templates', static_folder='../static')


@blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():

    providers = current_app.auth_providers

    if len(providers) == 1:
        return redirect(url_for('auth_provider_{}.prompt'.format(providers[0].name)))

    return render_template(
        'auth-switcher.html',
        providers=[{'name': provider.name, 'icon_uri': provider.icon_uri, 'link_text': provider.link_text} for provider in providers]
    )


@blueprint.route("/auth/logout")
@login_required
def logout():
    logout_user()

    # Notify flask principal that the user has logged out
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('index.render_feed'))
