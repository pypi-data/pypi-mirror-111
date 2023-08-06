# finstar

🚧 WIP 🚧

## Installation

```
poetry install
poetry run pre-commit install
```

### Serving documentation

```
poetry run mkdocs serve
```

## Development

### Testing

```
poetry run pytest
```

### Bumping version

```
poetry run bump2version minor # major or minor or patch
git-push --tags
```

### Publication to PyPI

```
poetry build
poetry publish
```

### tox

```
 poetry run tox
 ```
