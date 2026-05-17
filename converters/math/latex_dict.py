# -*- coding: utf-8 -*-
#
# Adapted from two upstream sources:
#
# 1. dwml by xiilei
#    https://github.com/xiilei/dwml/blob/master/dwml/latex_dict.py
#    Licensed under the Apache License, Version 2.0
#    See LICENSES/Apache-2.0.txt for full license text.
#
# 2. markitdown by Microsoft Corporation
#    https://github.com/microsoft/markitdown
#    Copyright (c) Microsoft Corporation.
#    Licensed under the MIT License.
#    See LICENSES/MIT-markitdown.txt for full license text.
#
# Modifications made in this file:
#   - Unicode escape sequences (e.g. "̀") replaced with
#     literal Unicode characters for readability

from __future__ import unicode_literals

CHARS = ("{", "}", "_", "^", "#", "&", "$", "%", "~")

BLANK = ""
BACKSLASH = "\\"
ALN = "&"

CHR = {
    "̀": "\\grave{{{0}}}",
    "́": "\\acute{{{0}}}",
    "̂": "\\hat{{{0}}}",
    "̃": "\\tilde{{{0}}}",
    "̄": "\\bar{{{0}}}",
    "̅": "\\overbar{{{0}}}",
    "̆": "\\breve{{{0}}}",
    "̇": "\\dot{{{0}}}",
    "̈": "\\ddot{{{0}}}",
    "̉": "\\ovhook{{{0}}}",
    "̊": "\\ocirc{{{0}}}}",
    "̌": "\\check{{{0}}}}",
    "̐": "\\candra{{{0}}}",
    "̒": "\\oturnedcomma{{{0}}}",
    "̕": "\\ocommatopright{{{0}}}",
    "̚": "\\droang{{{0}}}",
    "̸": "\\not{{{0}}}",
    "⃐": "\\leftharpoonaccent{{{0}}}",
    "⃑": "\\rightharpoonaccent{{{0}}}",
    "⃒": "\\vertoverlay{{{0}}}",
    "⃖": "\\overleftarrow{{{0}}}",
    "⃗": "\\vec{{{0}}}",
    "⃛": "\\dddot{{{0}}}",
    "⃜": "\\ddddot{{{0}}}",
    "⃡": "\\overleftrightarrow{{{0}}}",
    "⃧": "\\annuity{{{0}}}",
    "⃩": "\\widebridgeabove{{{0}}}",
    "⃰": "\\asteraccent{{{0}}}",
    "̰": "\\wideutilde{{{0}}}",
    "̱": "\\underbar{{{0}}}",
    "⃨": "\\threeunderdot{{{0}}}",
    "⃬": "\\underrightharpoondown{{{0}}}",
    "⃭": "\\underleftharpoondown{{{0}}}",
    "⃮": "\\underledtarrow{{{0}}}",
    "⃯": "\\underrightarrow{{{0}}}",
    "⎴": "\\overbracket{{{0}}}",
    "⏜": "\\overparen{{{0}}}",
    "⏞": "\\overbrace{{{0}}}",
    "⎵": "\\underbracket{{{0}}}",
    "⏝": "\\underparen{{{0}}}",
    "⏟": "\\underbrace{{{0}}}",
}

CHR_BO = {
    "⅀": "\\Bbbsum",
    "∏": "\\prod",
    "∐": "\\coprod",
    "∑": "\\sum",
    "∫": "\\int",
    "⋀": "\\bigwedge",
    "⋁": "\\bigvee",
    "⋂": "\\bigcap",
    "⋃": "\\bigcup",
    "⨀": "\\bigodot",
    "⨁": "\\bigoplus",
    "⨂": "\\bigotimes",
}

T = {
    "→": "\\rightarrow ",
    "\U0001d6fc": "\\alpha ",
    "\U0001d6fd": "\\beta ",
    "\U0001d6fe": "\\gamma ",
    "\U0001d6ff": "\\theta ",
    "\U0001d700": "\\epsilon ",
    "\U0001d701": "\\zeta ",
    "\U0001d702": "\\eta ",
    "\U0001d703": "\\theta ",
    "\U0001d704": "\\iota ",
    "\U0001d705": "\\kappa ",
    "\U0001d706": "\\lambda ",
    "\U0001d707": "\\m ",
    "\U0001d708": "\\n ",
    "\U0001d709": "\\xi ",
    "\U0001d70a": "\\omicron ",
    "\U0001d70b": "\\pi ",
    "\U0001d70c": "\\rho ",
    "\U0001d70d": "\\varsigma ",
    "\U0001d70e": "\\sigma ",
    "\U0001d70f": "\\ta ",
    "\U0001d710": "\\upsilon ",
    "\U0001d711": "\\phi ",
    "\U0001d712": "\\chi ",
    "\U0001d713": "\\psi ",
    "\U0001d714": "\\omega ",
    "\U0001d715": "\\partial ",
    "\U0001d716": "\\varepsilon ",
    "\U0001d717": "\\vartheta ",
    "\U0001d718": "\\varkappa ",
    "\U0001d719": "\\varphi ",
    "\U0001d71a": "\\varrho ",
    "\U0001d71b": "\\varpi ",
    "←": "\\leftarrow ",
    "↑": "\\uparrow ",
    "→": "\\rightarrow ",
    "↓": "\\downright ",
    "↔": "\\leftrightarrow ",
    "↕": "\\updownarrow ",
    "↖": "\\nwarrow ",
    "↗": "\\nearrow ",
    "↘": "\\searrow ",
    "↙": "\\swarrow ",
    "⋮": "\\vdots ",
    "⋯": "\\cdots ",
    "⋰": "\\adots ",
    "⋱": "\\ddots ",
    "≠": "\\ne ",
    "≤": "\\leq ",
    "≥": "\\geq ",
    "≦": "\\leqq ",
    "≧": "\\geqq ",
    "≨": "\\lneqq ",
    "≩": "\\gneqq ",
    "≪": "\\ll ",
    "≫": "\\gg ",
    "∈": "\\in ",
    "∉": "\\notin ",
    "∋": "\\ni ",
    "∌": "\\nni ",
    "∞": "\\infty ",
    "±": "\\pm ",
    "∓": "\\mp ",
    "\U0001d434": "A",
    "\U0001d435": "B",
    "\U0001d436": "C",
    "\U0001d437": "D",
    "\U0001d438": "E",
    "\U0001d439": "F",
    "\U0001d43a": "G",
    "\U0001d43b": "H",
    "\U0001d43c": "I",
    "\U0001d43d": "J",
    "\U0001d43e": "K",
    "\U0001d43f": "L",
    "\U0001d440": "M",
    "\U0001d441": "N",
    "\U0001d442": "O",
    "\U0001d443": "P",
    "\U0001d444": "Q",
    "\U0001d445": "R",
    "\U0001d446": "S",
    "\U0001d447": "T",
    "\U0001d448": "U",
    "\U0001d449": "V",
    "\U0001d44a": "W",
    "\U0001d44b": "X",
    "\U0001d44c": "Y",
    "\U0001d44d": "Z",
    "\U0001d44e": "a",
    "\U0001d44f": "b",
    "\U0001d450": "c",
    "\U0001d451": "d",
    "\U0001d452": "e",
    "\U0001d453": "f",
    "\U0001d454": "g",
    "\U0001d456": "i",
    "\U0001d457": "j",
    "\U0001d458": "k",
    "\U0001d459": "l",
    "\U0001d45a": "m",
    "\U0001d45b": "n",
    "\U0001d45c": "o",
    "\U0001d45d": "p",
    "\U0001d45e": "q",
    "\U0001d45f": "r",
    "\U0001d460": "s",
    "\U0001d461": "t",
    "\U0001d462": "u",
    "\U0001d463": "v",
    "\U0001d464": "w",
    "\U0001d465": "x",
    "\U0001d466": "y",
    "\U0001d467": "z",
}

FUNC = {
    "sin": "\\sin({fe})",
    "cos": "\\cos({fe})",
    "tan": "\\tan({fe})",
    "arcsin": "\\arcsin({fe})",
    "arccos": "\\arccos({fe})",
    "arctan": "\\arctan({fe})",
    "arccot": "\\arccot({fe})",
    "sinh": "\\sinh({fe})",
    "cosh": "\\cosh({fe})",
    "tanh": "\\tanh({fe})",
    "coth": "\\coth({fe})",
    "sec": "\\sec({fe})",
    "csc": "\\csc({fe})",
}

FUNC_PLACE = "{fe}"

BRK = "\\\\"

CHR_DEFAULT = {
    "ACC_VAL": "\\hat{{{0}}}",
}

POS = {
    "top": "\\overline{{{0}}}",
    "bot": "\\underline{{{0}}}",
}

POS_DEFAULT = {
    "BAR_VAL": "\\overline{{{0}}}",
}

SUB = "_{{{0}}}"

SUP = "^{{{0}}}"

F = {
    "bar": "\\frac{{{num}}}{{{den}}}",
    "skw": r"^{{{num}}}/_{{{den}}}",
    "noBar": "\\genfrac{{}}{{}}{{0pt}}{{}}{{{num}}}{{{den}}}",
    "lin": "{{{num}}}/{{{den}}}",
}
F_DEFAULT = "\\frac{{{num}}}{{{den}}}"

D = "\\left{left}{text}\\right{right}"

D_DEFAULT = {
    "left": "(",
    "right": ")",
    "null": ".",
}

RAD = "\\sqrt[{deg}]{{{text}}}"

RAD_DEFAULT = "\\sqrt{{{text}}}"

ARR = "\\begin{{array}}{{c}}{text}\\end{{array}}"

LIM_FUNC = {
    "lim": "\\lim_{{{lim}}}",
    "max": "\\max_{{{lim}}}",
    "min": "\\min_{{{lim}}}",
}

LIM_TO = ("\\rightarrow", "\\to")

LIM_UPP = "\\overset{{{lim}}}{{{text}}}"

M = "\\begin{{matrix}}{text}\\end{{matrix}}"
