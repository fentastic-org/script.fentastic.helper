# script.fentastic.helper — TODO

## High Priority

- [ ] **Replace `exec()` with `getattr()` in router.py:20**
  Allows arbitrary code execution if `mode` is crafted maliciously.
  Change `exec("actions.%s(params)" % mode.split(".")[1])` to `getattr(actions, mode.split(".")[1])(params)`.

- [ ] **Replace deprecated `xbmc.Keyboard()` with `xbmcgui.Dialog().input()`**
  Deprecated since Kodi 18; could be removed in a future Kodi version.
  - `MDbList.py:200` — `set_api_key()`
  - `search_utils.py:149` — `search_input()`

- [ ] **Add timeout to `requests.get()` in MDbList.py:104**
  No timeout means the call can hang indefinitely if MDbList is down, freezing the background service thread. Add `timeout=10` or similar.

- [ ] **Use the existing `session` instead of `requests.get()` in MDbList.py:104**
  A `requests.Session()` is created at module scope (line 27) with connection pooling, but `get_result()` calls `requests.get()` directly. Either use `session.get()` or remove the dead session code.

## Medium Priority

- [ ] **Replace bare `except:` clauses with `except Exception:`**
  Bare excepts catch `SystemExit` and `KeyboardInterrupt`, which can prevent clean Kodi shutdown.
  - `MDbList.py:54`
  - `cpath_maker.py` (multiple locations)
  - `widget_utils.py` (multiple locations)
  - `version_monitor.py:53`

- [ ] **Move trailer extraction outside the `for` loop in MDbList.py:175-178**
  `json_data.get("trailer")` doesn't depend on individual ratings. It works by accident (every iteration overwrites with the same value), but belongs outside the loop.

- [ ] **Use `super().__init__()` in service.py:20**
  Replace `xbmc.Monitor.__init__(self)` with `super().__init__()`.

- [ ] **Fix stray leading space in search_utils.py:15**
  `spath_database_path` has an extra leading space at module scope.

- [ ] **Use `xbmc.LOGINFO` constant instead of magic number `1`**
  Affects `logger.py:6`, `service.py:32,35,100-102`.

## Low Priority

- [ ] **Remove dead code: `MDbListAPI.last_checked_imdb_id` class variable (MDbList.py:31)**
  Never read or written anywhere.

- [x] **Add missing `# -*- coding: utf-8 -*-` headers for consistency**
  `MDbList.py` and `service.py` are missing the header that other files have. Not required in Python 3, but inconsistent with the rest of the codebase.

- [ ] **Standardize string formatting**
  The codebase mixes `%` formatting, `.format()`, and f-strings. Not a bug, but inconsistent.
