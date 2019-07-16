# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import subprocess

_here = os.path.abspath(os.path.dirname(__file__))
_library_root = os.path.abspath(os.path.join(_here, "../.."))

sys.path.insert(0, _library_root)


def run_proto_gen(self):
    """ Copies and runs the protoc compiler on the proto files"""

    cmds = ["./utils/pull_protos.sh", "./utils/compile_protos.sh"]

    for cmd in cmds:
        print("calling {} (workdir={})".format(cmd, _library_root))
        subprocess.check_call(cmd, cwd=_library_root)


def setup(app):
    """ Override for a custom sphinx build call. See manual on how to
    change the event when this action is triggered. """
    app.connect("builder-inited", run_proto_gen)


about = {}
with open("{}/wirepas_messaging/__about__.py".format(_library_root)) as f:
    exec(f.read(), about)

# -- Project information -----------------------------------------------------
_project = about["__title__"]
_copyright = "{},{}".format(about["__copyright__"], about["__license__"])
_release = about["__version__"]
_name = about["__pkg_name__"]
_version = about["__version__"]
_description = about["__description__"]
_author = about["__author__"]
_author_email = about["__author_email__"]
_url = about["__url__"]
_license = about["__license__"]
_classifiers = about["__classifiers__"]
_keywords = about["__keywords__"]

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it _here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "m2r",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinxcontrib.apidoc",
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["setup"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for apidoc output -------------------------------------------------
apidoc_module_dir = os.path.join(_library_root, "wirepas_messaging")
apidoc_excluded_paths = ["tests", "setup"]
apidoc_separate_modules = False
apidoc_module_first = True

# -- Options for autodoc output -------------------------------------------------
autodoc_mock_imports = ["setup"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {"logo": "logo.png", "description": _description}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_favicon = "_static/favicon.png"

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {"**": ["about.html", "relations.html", "searchbox.html"]}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = _name
