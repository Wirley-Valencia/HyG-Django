#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Definir las credenciales del superusuario
USERNAME="adminHyG"
EMAIL="hygvalencia10@gmail.com"
PASSWORD="hygdb1052"

# Verificar si el superusuario ya existe antes de crearlo
if ! python -c "import sys; from django.contrib.auth import get_user_model; \
                User = get_user_model(); \
                sys.exit(0 if User.objects.filter(username='$USERNAME').exists() else 1)"; then
    echo "El superusuario '$USERNAME' ya existe."
else
    # Crear un superusuario automáticamente
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
          User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')" \
          | python manage.py shell
fi