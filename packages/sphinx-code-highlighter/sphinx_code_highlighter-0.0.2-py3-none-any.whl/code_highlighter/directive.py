"""Sphinx directive and related extension code"""

from typing import Any, Dict

from docutils import nodes
from sphinx.directives.code import CodeBlock

from .pygmantize import make_lexer, HighlightedStyle


DEBUG_EVENT = None
DEBUG_PAGE = None


class CodeBlockHl(CodeBlock):
    """A directive that works just like code-block but also highlights parts of lines
       enclosed by the marker (!!!)."""

    def run(self):
        """Construct the node via the superclass then affix "-hl" to the language and
           register a generated lexer class for it.
        """

        # construct the node from the parent class
        code = '\n'.join(self.content)
        node, = super().run()

        # find the first literal_block in case it's not the topmost node
        block = list(node.traverse(
            lambda n: isinstance(n, nodes.literal_block),
            include_self=True)
        )[0]

        lang = block.get("language", None)

        # generate a lexer class for this language
        lexer = make_lexer(lang, code)

        # change language of the node and register the lexer
        block["language"] = f"{lang}-hl"
        self.env.app.add_lexer(block["language"], lexer)

        return [node]

def event_breakpoint(*args):
    """A callback method for jumping into a breakpoint at any given event, defined by
       the global DEBUG_EVENT variable."""

    if DEBUG_EVENT == "doctree-read":
        app, doctree = args

    elif DEBUG_EVENT == "build-finished":
        app, exception = args

    elif DEBUG_EVENT == "doctree-resolved":
        app, doctree, docname = args

    elif DEBUG_EVENT == "html-collect-pages":
        app, = args

    elif DEBUG_EVENT == "html-page-context":
        app, pagename, templatename, context, doctree = args
        if pagename == DEBUG_PAGE:
            breakpoint()
            return

    breakpoint()

def set_style(app, config):
    """Event listener to set the pygments style after config-inited. (If this is done in
       setup() it will just get overwritten.)"""
    config.pygments_style = "code_highlighter.HighlightedStyle"

def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_directive('code-block-hl', CodeBlockHl)
    app.connect("config-inited", set_style)

    if DEBUG_EVENT:
        app.connect(DEBUG_EVENT, event_breakpoint)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
