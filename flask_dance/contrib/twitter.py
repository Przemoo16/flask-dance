from __future__ import unicode_literals

from flask_dance.consumer import OAuth1ConsumerBlueprint
from functools import partial
from flask.globals import LocalProxy, _lookup_app_object
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


__maintainer__ = "David Baumgold <david@davidbaumgold.com>"


def make_twitter_blueprint(api_key, api_secret,
                           redirect_url=None, redirect_to=None,
                           login_url=None, authorized_url=None):
    """
    Make a blueprint for authenticating with Twitter using OAuth 1.

    Args:
        api_key (str): The API key for your Twitter application
        api_secret (str): The API secret for your Twitter application
        redirect_url (str): the URL to redirect to after the authentication
            dance is complete
        redirect_to (str): if ``redirect_url`` is not defined, the name of the
            view to redirect to after the authentication dance is complete.
            The actual URL will be determined by :func:`flask.url_for`
        login_url (str, optional): the URL path for the ``login`` view.
            Defaults to ``/twitter``
        authorized_url (str, optional): the URL path for the ``authorized`` view.
            Defaults to ``/twitter/authorized``.

    :rtype: :class:`~flask_dance.consumer.OAuth1ConsumerBlueprint`
    :returns: A :ref:`blueprint <flask:blueprints>` to attach to your Flask app.
    """
    twitter_bp = OAuth1ConsumerBlueprint("twitter", __name__,
        client_key=api_key,
        client_secret=api_secret,
        base_url="https://api.twitter.com/1.1/",
        request_token_url="https://api.twitter.com/oauth/request_token",
        access_token_url="https://api.twitter.com/oauth/access_token",
        authorization_url="https://api.twitter.com/oauth/authorize",
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        login_url=login_url,
        authorized_url=authorized_url,
    )

    @twitter_bp.before_app_request
    def set_applocal_session():
        ctx = stack.top
        ctx.twitter_oauth = twitter_bp.session

    return twitter_bp

twitter = LocalProxy(partial(_lookup_app_object, "twitter_oauth"))