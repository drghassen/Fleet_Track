# TODO: Remove Login and Logout from FleetTrack App

## Steps to Complete:
- [x] Remove the import of `login_required` from `fleet_track/views.py`
- [x] Verify and remove any `@login_required` decorators from views (if present)
- [x] Check `fleet_project/settings.py` for `LOGIN_URL` and `LOGOUT_REDIRECT_URL` and remove if present
- [x] Test that all pages load without authentication by running the server
