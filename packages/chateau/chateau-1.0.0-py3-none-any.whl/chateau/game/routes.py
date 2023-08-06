# Copyright 2021 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple, Union
import urllib.parse

import flask
import werkzeug

from chateau.game import blueprint
from chateau import websocket


@blueprint.route("<string(length=12):game_id>")
def game(game_id: str) -> Union[werkzeug.wrappers.Response, str]:
    if game_exists(game_id):
        return flask.render_template(
            "game/game.html",
            websocket_url=websocket.url(f"game/{game_id}"),
        )
    else:
        flask.abort(404)


def game_exists(game_id: str) -> bool:
    return bool(flask.g.redis.exists(f"game:{game_id}"))
