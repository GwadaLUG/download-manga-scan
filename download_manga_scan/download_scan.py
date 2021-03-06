#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
This file is part of Download Manga Scan.

Download Manga Scan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Download Manga Scan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Download Manga Scan.  If not, see <http://www.gnu.org/licenses/>
"""
from __future__ import unicode_literals

import argparse
# import urllib2
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import os
import re

# Variables globales
SCAN_DOMAIN = "http://www.lecture-en-ligne.com"
DEFAULT_SCAN_URL = "/".join([SCAN_DOMAIN, "images/manga/"])
DEFAULT_CHAPTER_URL = "/".join([SCAN_DOMAIN, "manga/"])
DEFAULT_SCAN_DIRNAME = 'scan_dl'
DEFAULT_SCAN_CHAPTER_DIRNAME = "chapter"
DEFAULT_SCAN_PATH = os.path.abspath(
    os.path.join(os.path.expanduser('~'), DEFAULT_SCAN_DIRNAME))
TMP_PATH = '/tmp'
DEFAULT_IMG_EXT = ('jpg', 'jpeg', 'gif', 'png')
DEFAULT_SCAN_LIST_FILE = os.path.join(DEFAULT_SCAN_PATH, 'scan_list.csv')

# Variables pour fichiers
CHUNK = 256 * 10240

parser = argparse.ArgumentParser(
    description='Télécharge les scan de manga depuis des sites en ligne.')

# subparsers
parser.add_argument('scan_label', type=str,
                    help="Label du scan a télécharger. Ex: shingekinokyojin")
parser.add_argument('-d', '--dir-path', type=str,
                    action='store',
                    required=False,
                    dest='dir_path',
                    default=DEFAULT_SCAN_PATH,
                    help="Répertoire de téléchargement des scans")
parser.add_argument('-i', '--ignore-files',
                    action='store_true',
                    required=False,
                    dest='ignore_files',
                    default=False,
                    help=("Ignore les fichiers déjà téléchargés "
                          "et écrase par dessus"))
parser.add_argument('chapters', type=int,
                    nargs="*",
                    default=[],
                    help="Liste des chapitres a télécharger. Ex: 1 2 3 4")


class DownloadScan(object):
    """Télécharge les scans et les range dans un dossier

    Attributes:
        scan_name: Nom du manga
        scan_path: répertoire de stockage des scans
        chapters: liste des chapitres des scan à télécharger.
            Si False on télécharge tous les numéros trouvés
    """

    def __init__(self, scan_name, scan_path=DEFAULT_SCAN_PATH, chapters=None):
        """Initialisation de la classe DownloadScan"""
        self.scan_name = scan_name
        self.scan_path = scan_path
        self.chapters = chapters

    def test_url(self, url):
        """Teste si l'URL existe et n'est pas en erreur

        Args:
            url: URL a tester

        Returns:
            Faux si une Erreur HTTP est relevé sinon Vrai
        """
        try:
            resp = urlopen(url)
            # Utile pour les sites qui redirige vers des URLS à la con
            # Au lieu de renvoyer un vrai 404
            if '404.html' in resp.geturl():
                return False
            return True
        except HTTPError as err:
            print("HTTP Error: {} {}".format(err.code, url))
            return False
        except URLError as err:
            print("URL Error: {} {}".format(err.reason, url))
            return False

    def download_file(self, url, path=None, ignore_file=False):
        """Télécharge un fichier depuis une URL

        Args:
            url: URL du fichier à télécharger
            path: répertoire où le fichier sera téléchargé

        Returns:
            Fichier téléchargé
        """
        if not self.test_url(url):
            return False

        if not path:
            path = TMP_PATH

        basefile = os.path.basename(url)

        os.umask('0002')
        try:
            mfile = os.path.join(path, basefile)
            if os.path.exists(mfile) and not ignore_file:
                print("Le fichier a déjà été téléchargé")
                return mfile

            req = urlopen(url)
            with open(mfile, 'wb') as fp:
                while True:
                    chunk = req.read(CHUNK)
                    if not chunk:
                        break
                    fp.write(chunk)
        except HTTPError as err:
            print("HTTP Error: {} {}".format(err.code, url))
            return False
        except URLError as err:
            print("URL Error: {} {}".format(err.reason, url))
            return False

        return mfile

    def create_dir(self, path):
        """Crée le répertoire si il n'existe pas

        Args:
            path: Repertoire a créer

        Returns:
            répertoire créé
        """
        # Test : si le repertoire n'existe pas on le cree
        if not os.path.exists(path):
            os.makedirs(path, 755)

        return path

    def list_scan_chapters(self):
        """Parse la page du scan pour savoir combien de chapitre
        sont disponibles.

        TODO:
            Faire en sorte de gérer les chapitres bonus

        Returns:
            Nombre de chapitre trouvé
        """
        chapters = []
        url = urlparse.urljoin(DEFAULT_CHAPTER_URL, "%s/" % self.scan_name)
        if self.test_url(url):
            html = str(urlopen(url).read())
            tabs = re.findall(
                r'(<td class="td">)([A-Za-z0-9\-\ \:]+)(chapitre)\ ([0-9]+)',
                html)
            for t in tabs:
                chapters.append(t[3])
                print("chapitre {} trouvé".format(t[3]))
        return chapters

    def list_chapter_page_number(self, chapter_num):
        """Liste le nombre de page pour un chapitre

        Args:
            chapter_number: numéro du chapitre

        Returns:
            Nombre de page trouvé
        """
        url = "/".join(
            [SCAN_DOMAIN, self.scan_name, str(chapter_num), "0/0/1.html"])
        if self.test_url(url):
            html = str(urlopen(url).read())
            pages = re.findall(
                r'(<span class="chapter-max_images">)([0-9]+)(</span)', html)
            if pages:
                print("{} pages trouvé pour le chapitre {}".format(
                    pages[0][1], chapter_num))
                return range(1, int(pages[0][1])+1)
        return []

    def list_pages_by_chapters(self):
        """TODO: Liste le nombre de page par chapitre

        Args:
            chapters: liste des chapitres

        Returns:
            Tuple numéro de chapitre et nombre de pages
        """
        t_return = []

        if self.chapters:
            chapters = self.chapters
        else:
            chapters = self.list_scan_chapters()

        for c in chapters:
            t_return.append((c, self.list_chapter_page_number(c)))

        return t_return

    def download_scan(self, ignore_files=False):
        """ Téléchargement des scan

        TODO:
            Gérer les authentification HTTP
            Remplace subprocess par la librairie curl directement
        """
        for scan in self.list_pages_by_chapters():
            print(">> Téléchargement du chapitre {}".format(scan[0]))

            chapter_dir = "%s_%s" % (DEFAULT_SCAN_CHAPTER_DIRNAME, scan[0])

            # On créé le répertoire de destination
            chapter_path = self.create_dir(
                os.path.join(self.scan_path, self.scan_name, chapter_dir))

            for p in scan[1]:
                img_found = False
                page = "0%s" % p if p < 10 else p
                url = urlparse.urljoin(
                    DEFAULT_SCAN_URL,
                    "%s/%s/%s" % (self.scan_name, scan[0], page))

                # On cherche une URL valide en fonction de
                # l'extension des images
                for ext in DEFAULT_IMG_EXT:
                    dl_file = self.download_file(
                        "%s.%s" % (url, ext),
                        chapter_path,
                        ignore_files)
                    if dl_file:
                        print(">> Téléchargement de la page {}".format(page))
                        img_found = True
                        break

                """TODO: log dans un fichier
                Si on a pas du tout trouvé d'image on saute
                le téléchargement
                """
                if not img_found:
                    print("la page {} n'a pas été trouvé".format(page))
                    continue

        return


def main():
    "Lance l'execution de la commande `download-manga`"
    args = parser.parse_args()

    scan_label = args.scan_label
    scan_path = args.dir_path
    ignore_files = args.ignore_files
    chapters = args.chapters

    # téléchargement
    dl = DownloadScan(scan_label, scan_path, chapters)
    dl.download_scan(ignore_files)


if __name__ == '__main__':
    main()
