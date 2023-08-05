# -*- coding: utf-8 -*-
"""
flask_commonmark
----------------

Commonmark filter class for Flask. One may notice a similarity to Dan Colish's Flask-Markdown, from which I shamelessly copied a bunch of this. Does not have all the nice provisions for extension baked in, but probably does what you need. See https://commonmark.org/ for details.

Usage
::
    from flask_commonmark import Commonmark
    cm = Commonmark(app)

    # or, if you are using the factory pattern

    cm = Commonmark()
    cm.init_app(app)

    # Create routes in the usual way
    @app.route("/commonmark")
    def display_commonmark():
        mycm = u"Hello, *commonmark* block."
        return render_template("commonmark.html", mycm=mycm)


Templates
::
    # one can just place raw markdown in the template. The filter expects
    # your markdown to be fully left-aligned! Otherwise expect plaintext.
    {% filter commonmark %}
    # Nagasaki
    1. Chew Terbaccy
    1. Wicky-waky-woo
    {% endfilter %}

    # block style
    {% filter commonmark %}{{ mycm }}{% endfilter %}

    # inline style
    {{mycm|commonmark}}

:copyright: (c) 2019, 2021 by Doug Shawhan.
:license: BSD, MIT see LICENSE for details.
"""
from typing import Callable, Union
import flask
from flask import Markup
import jinja2
from jinja2 import pass_eval_context
import markupsafe

import commonmark as cm


class Commonmark(object):
    """
    Commonmark
    ----------

    Wrapper class for Commonmark (aka "common markdown"), objects.

    Args:
        app (obj):  Flask app instance
        auto_escape (bool): Use Jinja2 auto_escape, default False
    """

    def __init__(
        self, app: Union[bool, flask.app.Flask] = False, auto_escape: bool = False
    ):
        """
        Create parser and renderer objects and auto_escape value.
        Set filter.

        Args:
            app (Union[bool, flask.app.Flask]): flask app object
            auto_escape (bool): Shall we auto escape?
        """

        if not app:
            return

        with open("foo.txt", "w") as _fh:
            _fh.write(str(type(app)))

        self.init_app(app, auto_escape=auto_escape)

        app.jinja_env.filters.setdefault(  # type: ignore
            "commonmark", self.__build_filter(self.auto_escape)
        )

    def __call__(self, stream: markupsafe.Markup) -> str:
        """
        Render markdown stream.

        Args:
            stream (str):   template stream containing markdown tags

        Returns:
            html (str):  markdown rendered as html
        """

        return self.cm_render.render(self.cm_parse.parse(stream))

    def __build_filter(self, app_auto_escape: bool) -> Callable:
        """
        Jinja2 __build_filter

        Args:
            app_auto_escape (bool): auto_escape value (default False)
        Returns:
            commonmark_filter (obj):  context filter
        """

        @pass_eval_context
        def commonmark_filter(
            eval_ctx: jinja2.nodes.EvalContext, stream: markupsafe.Markup
        ) -> markupsafe.Markup:
            """
            Called by Jinja2 when evaluating the Commonmark filter.

            Args:
                eval_ctx (obj): Jinja2 evaluation context
                stream (str):   string to filter
            """

            __filter = self

            if app_auto_escape and eval_ctx.autoescape:
                return Markup(__filter(markupsafe.escape(stream)))

            return Markup(__filter(stream))

        return commonmark_filter

    def init_app(self, app: Union[bool, flask.app.Flask], auto_escape: bool = False):
        """
        Create parser and renderer objects and auto_escape value.
        Set filter.

        Args:
            app (Union[bool, flask.app.Flask): Flask app
            auto_escape (bool): Shall we auto escape?
        """
        self.auto_escape = auto_escape
        self.cm_parse = cm.Parser()
        self.cm_render = cm.HtmlRenderer()

        app.jinja_env.filters.setdefault(  # type: ignore
            "commonmark", self.__build_filter(self.auto_escape)
        )
