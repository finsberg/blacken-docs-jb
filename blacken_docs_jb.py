from __future__ import annotations

import re

import blacken_docs

# Monkey patching MD_RE in blacken_docs
blacken_docs.MD_RE = re.compile(
    r'(?P<before>^(?P<indent> *)```(\{code-cell\})?\s*python\n)'
    r'(?P<code>.*?)'
    r'(?P<after>^(?P=indent)```\s*$)',
    re.DOTALL | re.MULTILINE,
)


def main() -> int:
    return blacken_docs.main()


if __name__ == '__main__':
    raise SystemExit(main())
