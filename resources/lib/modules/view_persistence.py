# -*- coding: utf-8 -*-
import xbmc, xbmcgui


class ViewPersistenceMonitor:
    """Auto-learns and restores per-content-type view preferences.

    Kodi only persists views per-window (e.g. MyVideoNav = 10025), so all
    content types (movies, tvshows, episodes, etc.) share one remembered view.
    This monitor tracks the user's view choice per content type and restores it
    automatically when the content type changes.
    """

    CONTENT_TYPES = (
        "movies",
        "tvshows",
        "episodes",
        "seasons",
        "sets",
        "musicvideos",
        "artists",
        "albums",
        "songs",
    )
    VIEW_IDS = (50, 51, 52, 53, 54, 55, 56, 500, 501, 502, 504)
    SUPPORTED_WINDOWS = {10025, 10502}  # MyVideoNav, MyMusicNav

    def __init__(self, monitor):
        self.monitor = monitor
        self.last_content = None
        self.last_view_id = None

    def _get_current_content(self):
        for ct in self.CONTENT_TYPES:
            if xbmc.getCondVisibility("Container.Content(%s)" % ct):
                return ct
        return None

    def _get_current_view_id(self):
        for vid in self.VIEW_IDS:
            if xbmc.getCondVisibility("Control.IsVisible(%d)" % vid):
                return vid
        return None

    def _get_saved_view(self, content_type):
        val = xbmc.getInfoLabel("Skin.String(ViewDefault.%s)" % content_type)
        if val and val.isdigit():
            return int(val)
        return None

    def _save_view(self, content_type, view_id):
        xbmc.executebuiltin(
            "Skin.SetString(ViewDefault.%s,%d)" % (content_type, view_id)
        )

    def _apply_view(self, view_id):
        xbmc.executebuiltin("Container.SetViewMode(%d)" % view_id)

    def run(self):
        xbmc.log("###FENtastic: View Persistence Service Started", 1)
        while not self.monitor.abortRequested():
            if xbmc.getSkinDir() != "skin.fentastic":
                self.monitor.waitForAbort(15)
                continue

            window_id = xbmcgui.getCurrentWindowId()
            if window_id not in self.SUPPORTED_WINDOWS:
                self.last_content = None
                self.last_view_id = None
                self.monitor.waitForAbort(1)
                continue

            if xbmc.getCondVisibility("Container.Scrolling"):
                self.monitor.waitForAbort(0.3)
                continue

            current_content = self._get_current_content()
            current_view = self._get_current_view_id()

            if not current_content or not current_view:
                self.last_content = current_content
                self.last_view_id = current_view
                self.monitor.waitForAbort(0.5)
                continue

            # Content type changed — restore saved view if available
            if current_content != self.last_content:
                saved_view = self._get_saved_view(current_content)
                if saved_view and saved_view != current_view:
                    self._apply_view(saved_view)
                    current_view = saved_view
                self.last_content = current_content
                self.last_view_id = current_view
                self.monitor.waitForAbort(0.3)
                continue

            # View changed while on same content type — save preference
            if current_view != self.last_view_id:
                self._save_view(current_content, current_view)
                self.last_view_id = current_view

            self.monitor.waitForAbort(0.5)

        xbmc.log("###FENtastic: View Persistence Service Finished", 1)
