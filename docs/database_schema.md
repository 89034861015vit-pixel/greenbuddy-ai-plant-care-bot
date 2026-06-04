# Database Schema

GreenBuddy uses SQLite for lightweight local storage.

## plants

Stores plant names created by users.

Fields:

- `id`
- `user_id`
- `name`
- `created_at`

## plant_logs

Stores AI analysis history.

Fields:

- `id`
- `user_id`
- `plant_name`
- `health_score`
- `diagnosis`
- `action`
- `created_at`

## user_state

Stores the current plant selected by the user.

Fields:

- `user_id`
- `plant_name`
- `updated_at`

The real `.db` file must not be committed to GitHub.
