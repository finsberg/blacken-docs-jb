from __future__ import annotations

import black

import blacken_docs_jb


BLACK_MODE = black.FileMode(line_length=black.DEFAULT_LINE_LENGTH)


def test_format_src_trivial():
    after, _ = blacken_docs_jb.format_str('', BLACK_MODE)
    assert after == ''


def test_format_src_markdown_simple1():
    before = (
        '```python\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_leading_whitespace():
    before = (
        '```   python\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```   python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_trailing_whitespace():
    before = (
        '```python\n'
        'f(1,2,3)\n'
        '```    \n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```    \n'
    )


def test_format_src_indented_markdown():
    before = (
        '- do this pls:\n'
        '  ```python\n'
        '  f(1,2,3)\n'
        '  ```\n'
        '- also this\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '- do this pls:\n'
        '  ```python\n'
        '  f(1, 2, 3)\n'
        '  ```\n'
        '- also this\n'
    )


def test_integration_ok(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert not capsys.readouterr()[1]
    assert f.read() == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_magic1(tmpdir, capsys):
    f = tmpdir.join('f.md')
    before = (
        'Hello hello\n'
        '```{code-cell} python\n'
        '%timeit -n 5 -r 10 some_function()'
        '```\n'
        'world\n'
    )
    f.write(before)
    assert not blacken_docs_jb.main((str(f),))
    assert not capsys.readouterr()[1]
    assert f.read() == before


def test_integration_modifies(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(1,2,3)\n'
        '```\n',
    )
    assert blacken_docs_jb.main((str(f),))
    out, _ = capsys.readouterr()
    assert out == f'{f}: Rewriting...\n'
    assert f.read() == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_integration_line_length(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'foo(very_very_very_very_very_very_very, long_long_long_long_long)\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f), '--line-length=80'))
    assert blacken_docs_jb.main((str(f), '--line-length=50'))
    assert f.read() == (
        '```python\n'
        'foo(\n'
        '    very_very_very_very_very_very_very,\n'
        '    long_long_long_long_long,\n'
        ')\n'
        '```\n'
    )


def test_integration_py36(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert blacken_docs_jb.main((str(f), '--target-version=py36'))
    assert f.read() == (
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long,\n'
        '):\n'
        '    pass\n'
        '```\n'
    )


def test_integration_filename_last(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert blacken_docs_jb.main(('--target-version', 'py36', str(f)))
    assert f.read() == (
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long,\n'
        '):\n'
        '    pass\n'
        '```\n'
    )


def test_integration_multiple_target_version(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert not blacken_docs_jb.main(
        ('--target-version', 'py35', '--target-version', 'py36', str(f)),
    )


def test_integration_skip_string_normalization(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        "f('hi')\n"
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f), '--skip-string-normalization'))
    assert f.read() == (
        '```python\n'
        "f('hi')\n"
        '```\n'
    )


def test_integration_syntax_error(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(\n'
        '```\n',
    )
    assert blacken_docs_jb.main((str(f),))
    out, _ = capsys.readouterr()
    assert out.startswith(f'{f}:1: code block parse error')
    assert f.read() == (
        '```python\n'
        'f(\n'
        '```\n'
    )


def test_integration_ignored_syntax_error(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f( )\n'
        '```\n'
        '\n'
        '```python\n'
        'f(\n'
        '```\n',
    )
    assert blacken_docs_jb.main((str(f), '--skip-errors'))
    out, _ = capsys.readouterr()
    assert f.read() == (
        '```python\n'
        'f()\n'
        '```\n'
        '\n'
        '```python\n'
        'f(\n'
        '```\n'
    )


def test_format_src_markdown_simple_code_cell():
    before = (
        '```{code-cell} python\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell} python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_leading_whitespace_code_cell():
    before = (
        '```{code-cell}   python\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell}   python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_trailing_whitespace_code_cell():
    before = (
        '```{code-cell} python\n'
        'f(1,2,3)\n'
        '```    \n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell} python\n'
        'f(1, 2, 3)\n'
        '```    \n'
    )


def test_format_src_indented_markdown_code_cell():
    before = (
        '- do this pls:\n'
        '  ```{code-cell} python\n'
        '  f(1,2,3)\n'
        '  ```\n'
        '- also this\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '- do this pls:\n'
        '  ```{code-cell} python\n'
        '  f(1, 2, 3)\n'
        '  ```\n'
        '- also this\n'
    )


def test_integration_ok_code_cell(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'f(1, 2, 3)\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert not capsys.readouterr()[1]
    assert f.read() == (
        '```{code-cell} python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_integration_modifies_code_cell(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'f(1,2,3)\n'
        '```\n',
    )
    assert blacken_docs_jb.main((str(f),))
    out, _ = capsys.readouterr()
    assert out == f'{f}: Rewriting...\n'
    assert f.read() == (
        '```{code-cell} python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_integration_line_length_code_cell(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'foo(very_very_very_very_very_very_very, long_long_long_long_long)\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f), '--line-length=80'))
    assert blacken_docs_jb.main((str(f), '--line-length=50'))
    assert f.read() == (
        '```{code-cell} python\n'
        'foo(\n'
        '    very_very_very_very_very_very_very,\n'
        '    long_long_long_long_long,\n'
        ')\n'
        '```\n'
    )


def test_integration_py36_code_cell(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert blacken_docs_jb.main((str(f), '--target-version=py36'))
    assert f.read() == (
        '```{code-cell} python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long,\n'
        '):\n'
        '    pass\n'
        '```\n'
    )


def test_integration_filename_last_code_cell(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert blacken_docs_jb.main(('--target-version', 'py36', str(f)))
    assert f.read() == (
        '```{code-cell} python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long,\n'
        '):\n'
        '    pass\n'
        '```\n'
    )


def test_integration_multiple_target_version_code_cell(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f),))
    assert not blacken_docs_jb.main(
        ('--target-version', 'py35', '--target-version', 'py36', str(f)),
    )


def test_integration_skip_string_normalization_code_cell(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        "f('hi')\n"
        '```\n',
    )
    assert not blacken_docs_jb.main((str(f), '--skip-string-normalization'))
    assert f.read() == (
        '```{code-cell} python\n'
        "f('hi')\n"
        '```\n'
    )


def test_integration_syntax_error_code_cell(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'f(\n'
        '```\n',
    )
    assert blacken_docs_jb.main((str(f),))
    out, _ = capsys.readouterr()
    assert out.startswith(f'{f}:1: code block parse error')
    assert f.read() == (
        '```{code-cell} python\n'
        'f(\n'
        '```\n'
    )


def test_integration_ignored_syntax_error_code_cell(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```{code-cell} python\n'
        'f( )\n'
        '```\n'
        '\n'
        '```{code-cell} python\n'
        'f(\n'
        '```\n',
    )

    assert blacken_docs_jb.main((str(f), '--skip-errors'))
    out, _ = capsys.readouterr()
    assert f.read() == (
        '```{code-cell} python\n'
        'f()\n'
        '```\n'
        '\n'
        '```{code-cell} python\n'
        'f(\n'
        '```\n'
    )


def test_format_src_markdown_simple_code_cell_with_magic():
    before = (
        '```{code-cell} python\n'
        '% matplotlib inline  \n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)

    assert after == (
        '```{code-cell} python\n'
        '% matplotlib inline\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_simple_code_cell_with_magic_and_comment():
    before = (
        '```{code-cell} python\n'
        '% matplotlib inline  \n'
        'f(1,2,3) # This is a comment\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell} python\n'
        '% matplotlib inline\n'
        'f(1, 2, 3)  # This is a comment\n'
        '```\n'
    )


def test_format_src_markdown_simple_code_cell_with_command():
    before = (
        '```{code-cell} python\n'
        '!pip install -m blacken_docs  \n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)

    assert after == (
        '```{code-cell} python\n'
        '!pip install -m blacken_docs\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_markdown_simple_code_cell_with_tag():
    before = (
        '```{code-cell} python\n'
        ':tags: ["hide-input", "another_tag"]\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell} python\n'
        ':tags: ["hide-input", "another_tag"]\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_invalid_tag_raises_TagParserError():
    before = (
        '```{code-cell} python\n'
        ':tags: :tags["hide-input", "another_tag"]\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, errors = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert len(errors) == 1
    assert isinstance(errors[0].exc, blacken_docs_jb.TagParserError)


def test_script_magic():
    before = (
        '```{code-cell} python\n'
        '%%script echo skipping\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, _ = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert after == (
        '```{code-cell} python\n'
        '%%script echo skipping\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_script_invalid_magic():
    before = (
        '```{code-cell} python\n'
        '%%%script echo skipping\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after, errors = blacken_docs_jb.format_str(before, BLACK_MODE)
    assert len(errors) == 1
    assert isinstance(errors[0].exc, blacken_docs_jb.CmdParserError)
