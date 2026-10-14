# Alembic migration notes

No migration is hard-coded here because `down_revision` must match the actual repository migration history.

After importing every model into `Base.metadata`, generate a migration:
`alembic -c backend/alembic.ini revision --autogenerate -m "add career profile tables"`

Review the generated migration, make sure it doesn't recreate existing auth/user tables, and only then run:
`alembic -c backend/alembic.ini upgrade head`

If the database already has tables but Alembic is not tracking them, stop and reconcile the schema/revision state before applying a migration.
