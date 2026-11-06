#!/bin/sh
# Fija la contraseña del rol authenticator desde el entorno (no se versiona ningún valor).
# psql solo interpola :'pw' en la entrada estándar, no con -c.
set -eu
echo "ALTER ROLE authenticator PASSWORD :'pw';" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" -v pw="$AUTHENTICATOR_PASSWORD"
