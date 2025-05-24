echo "Running mypy..."
poetry run mypy .

echo
echo "Running ruff checker..."
poetry run ruff check

echo
echo "Running ruff formatter..."
poetry run ruff format
