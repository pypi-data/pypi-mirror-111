"""Pygments lexer and style"""

from dataclasses import dataclass
import sys

from pygments.lexer import inherit, using, bygroups, Lexer
from pygments.token import *
from sphinx.pygments_styles import SphinxStyle
from sphinx.highlighting import PygmentsBridge


__all__ = ["make_lexer", "HighlightedStyle", "Cfg", "DEFAULT"]


@dataclass
class Cfg:
    """Config options"""
    marker: str = "!!!"
    bg: str = "#ffffcc"

DEFAULT = Cfg()

class HighlightedStyle(SphinxStyle):
    """A pygments style adding a an Highlight subtype to all existing tokens,
       mapped to styles the same style with a background color appended.
    """
    styles = SphinxStyle.styles

    styles.update({
        t.Highlight: f"{s} bg:{DEFAULT.bg}"
        for t, s in SphinxStyle.styles.items()
        if Generic is not t
    })


class ArgumentError(BaseException): ...

def make_lexer(lang: str=None, code: str=None, language_lexer: Lexer=None):
    """Return a HighlightedCodeLexer class subclassed from the language lexer class,
       either deduced from lang (str) or code (str), or the class of language_lexer
       (pygments.lexer) instance.

    Params
    ------
    * language_lexer (pygments.Lexer) -- an instance of the lexer class to subclass
    * lang (str)                      -- name of the language
    * code (str)                      -- code to be lexed
    """

    if not (lang or code or language_lexer):
        raise ArgumentError(
            "make_lexer() requires one of lang(str) and code(str) "
            "or language_lexer(pygments.Lexer) keyword arguments")

    # let sphinx figure out the language based on the content and/or language name
    if not language_lexer:
        language_lexer = PygmentsBridge().get_lexer(source=code, lang=lang or "guess")

    # get the lexer class to inherit from
    parent = language_lexer.__class__

    class Meta(type(parent)):
        """Metaclass inheriting from parent metaclasses"""

        def __repr__(cls):
            """A cleaner class repr"""
            return f"<class {cls.__name__}>"

    class HighlightedCodeLexer(parent, metaclass=Meta):
        """A pygments lexer to that adds a Highlight subtype to all tokens found between
          the marker text (!!!) and let the parent class lex everything else."""

        def add_highlight(lexer, match, ctx=None):
            """Add a Highlight subtype to tokens between markers while stripping the
               markers themselves.

               Expects 4 match groups: marker, highlighted content, marker, rest of line
            """

            # make a callback function that assigns Token.Marker to the markers, run the
            # enclosed text through the parent lexer, then run the rest of the line back
            # through this lexer
            lex = bygroups(Token.Marker,
                           using(parent),
                           Token.Marker,
                           using(lexer.__class__))

            # call it on the matches then iterate through the resulting tokens
            markers = 0
            for index, token, value in lex(lexer, match, ctx):

                # keep track of where we are in the line
                # but don't yield markers in the output stream
                if token is Token.Marker:
                    markers += 1
                    continue

                # add a Highlight subtype to tokens before the last marker
                if markers < 2:
                    token = token.Highlight

                # yield the modified stream
                yield index, token, value

        tokens = {
            'root': [
                # find lines where part is enclosed in highlight markers
                # delgate to add_highlight callback in four match groups:
                # marker, highlighted content, marker, the rest of the line
                (rf'({DEFAULT.marker})(.+?)({DEFAULT.marker})(.*)$', add_highlight),

                # all other tokens are inherited from parent class
                inherit
            ],
        }

    HighlightedCodeLexer.__name__ = f"Highlighted{parent.__name__}"

    return HighlightedCodeLexer
