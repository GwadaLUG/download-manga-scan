# -*- encoding: utf-8 -*-
"""
This file is part of Download Manga Scan.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>
"""
from download_scan import main

__author__ = "Laurent Vergerolle"
__copyright__ = "Copyright (c) 2014 Laurent Vergerolle"
__license__ = "GPL-V3"
__all__ = ['main',]

def get_version(version, alpha_num=None, beta_num=None,
                rc_num=None, post_num=None, dev_num=None):
    u"""Crée la version en fonction de la PEP 386.
    On affiche toujours la version la moins aboutie.
    Exemple, si alpha, beta et rc sont spécifié, on affiche la version
    comme alpha.

    Args:
        version: tuple du numéro de version actuel. Ex : (0,0,1) ou (2,0,4)
        alpha_num: définie que la version comme alpha
        beta_num: définie la version comme beta
        rc_num: définie la version comme release candidate
        post_num: definie la version comme post dev
        dev_num: définie la version comme en cour de développement

    Returns:
        numéro de version formaté selon la PET 386
    """
    num = "%s.%s" % (int(version[0]), int(version[1]))
    if version[2]:
        num += ".%s" % int(version[2])

    letter_marker = False # permet de sortir si on a un marqueur de type lettre
    if alpha_num:
        num += "a%s" % int(alpha_num)
        letter_marker = True

    if beta_num and not letter_marker:
        num += "b%s" % int(beta_num)
        letter_marker = True

    if rc_num and not letter_marker:
        num += "rc%s" % int(rc_num)

    if post_num:
        num += ".post%s" % int(post_num)

    if dev_num:
        num += ".dev%s" % int(dev_num)

    return num

__version__ = get_version((0, 0, 1), beta_num=1, dev_num=1)
