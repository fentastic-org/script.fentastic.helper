# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
from xbmc import executebuiltin, getInfoLabel

# from modules.logger import logger


def person_search(params):
    return executebuiltin(
        "RunPlugin(plugin://plugin.video.fen/?mode=person_search_choice&query=%s)"
        % params["query"]
    )


def extras(params):
    return executebuiltin(
        "RunPlugin(%s)" % getInfoLabel("ListItem.Property(fen.extras_params)")
    )


# Provider plugin IDs indexed by Skin.String(current_search_provider) value
_PROVIDER_PLUGINS = {
    "0": "plugin.video.fen",
    "1": "plugin.video.fenlight",
    "2": "plugin.video.umbrella",
    "3": "plugin.video.pov",
    "4": "plugin.video.seren",
}


def _get_container_infolabel(list_id, label):
    return getInfoLabel("Container(%s).ListItem.%s" % (list_id, label))


def _get_container_property(list_id, prop):
    return getInfoLabel("Container(%s).ListItem.Property(%s)" % (list_id, prop))


def category_actions(params):
    list_id = params.get("list_id", "")
    if not list_id:
        return

    if xbmc.getCondVisibility("Skin.HasSetting(Disable.QuickActions)"):
        return

    db_type = _get_container_infolabel(list_id, "DBType")
    if db_type not in ("movie", "tvshow", "season", "episode"):
        return

    title = _get_container_infolabel(list_id, "Title")
    imdb_id = _get_container_infolabel(list_id, "IMDBNumber")
    provider = getInfoLabel("Skin.String(current_search_provider)")
    plugin_id = _PROVIDER_PLUGINS.get(provider, "")
    has_mdblist_key = xbmc.getCondVisibility(
        "!String.IsEmpty(Skin.String(mdblist_api_key))"
    )

    actions = []

    # Play Trailer (MDbList)
    trailer_url = getInfoLabel("Window(home).Property(fentastic.trailer)")
    if has_mdblist_key and trailer_url:
        actions.append(("Play Trailer", "trailer"))

    # Extras
    extras_params = _get_container_property(list_id, "fenlight.extras_params")
    if not extras_params:
        extras_params = _get_container_property(list_id, "fen.extras_params")
    if not extras_params:
        extras_params = _get_container_property(list_id, "umbrella.extras_params")
    if extras_params:
        actions.append(("Extras", "extras"))

    # Trakt Manager
    trakt_params = _get_container_property(list_id, "fenlight.trakt_manager_params")
    if not trakt_params and plugin_id and imdb_id:
        media_type = "movie" if db_type == "movie" else "tvshow"
        if plugin_id == "plugin.video.umbrella":
            trakt_params = (
                "plugin://plugin.video.umbrella/"
                "?action=traktManager&imdb=%s&media_type=%s" % (imdb_id, media_type)
            )
        elif plugin_id in (
            "plugin.video.fen",
            "plugin.video.pov",
        ):
            tmdb_id = _get_container_infolabel(list_id, "UniqueID(tmdb)")
            trakt_params = (
                "plugin://%s/"
                "?mode=trakt_manager_choice&imdb_id=%s&tmdb_id=%s&media_type=%s"
                % (plugin_id, imdb_id, tmdb_id or "", media_type)
            )
    if trakt_params:
        actions.append(("Trakt Manager", "trakt"))

    # Browse Recommended
    rec_params = _get_container_property(list_id, "fenlight.browse_recommended_params")
    if rec_params:
        actions.append(("Browse Recommended", "recommended"))

    # Browse Similar
    sim_params = _get_container_property(list_id, "fenlight.browse_similar_params")
    if sim_params:
        actions.append(("Browse Similar", "similar"))

    # Options
    options_params = _get_container_property(list_id, "fenlight.options_params")
    if options_params:
        actions.append(("Options", "options"))

    if not actions:
        return

    labels = [a[0] for a in actions]
    choice = xbmcgui.Dialog().select("Quick Actions — %s" % title, labels)
    if choice < 0:
        return

    action_id = actions[choice][1]

    if action_id == "trailer":
        from modules.MDbList import play_trailer

        return play_trailer()
    elif action_id == "extras":
        return executebuiltin("RunPlugin(%s)" % extras_params)
    elif action_id == "trakt":
        return executebuiltin("RunPlugin(%s)" % trakt_params)
    elif action_id == "recommended":
        return executebuiltin(
            "ActivateWindow(Videos,%s,return)" % rec_params
        )
    elif action_id == "similar":
        return executebuiltin(
            "ActivateWindow(Videos,%s,return)" % sim_params
        )
    elif action_id == "options":
        return executebuiltin("RunPlugin(%s)" % options_params)
