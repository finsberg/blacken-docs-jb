# blacken-docs-jb

Extension of [blacken-docs](https://github.com/asottile/blacken-docs) which also supports the [executable code blocks](https://jupyterbook.org/en/stable/reference/cheatsheet.html#executable-code) from [JupyterBook](https://jupyterbook.org) e.g

````
```{code-cell} python
x = 1 + 2
```
````

## Install

```bash
pip install blacken-docs-jb
```

## Usage with pre-commit

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/finsberg/blacken-docs-jb
    rev: v0.6.2
    hooks:
      - id: blacken-docs-jb
        additional_dependencies: [black==22.3.0]
        exclude: slides
```

## License
This project is licensed under [MIT](LICENSE). The license file from blacken-docs is found in [LICENSE_blacken_docs](LICENSE_blacken_docs).
