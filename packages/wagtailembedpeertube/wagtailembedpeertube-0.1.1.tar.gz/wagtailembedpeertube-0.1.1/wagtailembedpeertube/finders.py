# wagtailembedpeertube - Embed peertube videos into wagtail
# Copyright (C) 2018  Cliss XXI <tech@cliss21.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import re
from urllib.error import URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from wagtail.embeds.exceptions import EmbedNotFoundException
from wagtail.embeds.finders.base import EmbedFinder

PEERTUBE_URL_PATH_RE = re.compile(
    r'^/videos/watch/[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$'
)


class PeertubeFinder(EmbedFinder):
    def accept(self, url):
        return PEERTUBE_URL_PATH_RE.match(urlparse(url).path)

    def find_embed(self, url, max_width=None):
        parse_result = urlparse(url)
        endpoint = "{}://{}/services/oembed".format(
            parse_result.scheme, parse_result.netloc
        )

        # Work out params
        params = {}
        params['url'] = url
        params['format'] = 'json'
        if max_width:
            params['maxwidth'] = max_width

        # Perform request
        request = Request(endpoint + '?' + urlencode(params))
        request.add_header('User-agent', 'Mozilla/5.0')
        try:
            r = urlopen(request)
            oembed = json.loads(r.read().decode('utf-8'))
        except (URLError, json.decoder.JSONDecodeError):
            raise EmbedNotFoundException

        # Return embed as a dict
        return {
            'title': oembed['title'],
            'author_name': oembed['author_name'],
            'provider_name': oembed['provider_name'],
            'type': oembed['type'],
            'thumbnail_url': oembed['thumbnail_url'],
            'width': oembed['width'],
            'height': oembed['height'],
            'html': oembed['html'],
        }


embed_finder_class = PeertubeFinder
