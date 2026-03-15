# script.fentastic.helper

Kodi helper addon (Python library + background service) for the FENtastic skin. Originally built for Kodi Nexus (v20), updated for Omega (v21).

## Version Bumping

This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

- **MAJOR** — breaking changes (removed features, incompatible API changes, dropped Kodi version support)
- **MINOR** — new features, new functionality (new widgets, new menu options, new integrations)
- **PATCH** — bug fixes, code cleanup, deprecation updates, cosmetic changes

When making changes that warrant a version bump:

1. Check `last_updated_version.txt` to know the current version
2. Determine the appropriate bump level based on the changes made
3. Update the `version` attribute in `addon.xml`
4. Update `last_updated_version.txt` to match

The version in `addon.xml` is what Kodi uses to detect updates. The `last_updated_version.txt` file exists so you can quickly check the current version without parsing XML.
