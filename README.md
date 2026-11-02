# wordlist-gen

A Python wordlist generator for CTFs and authorized security testing. It builds candidate lists from seed words using common password patterns, Turkish-specific normalization, partial leetspeak, symbols, numbers, years, and layered endings.

## Features

- Interactive setup when run without seed words
- Case, partial leet, Turkish ASCII, symbol, number, year, and layered suffix mutations
- Common-password seed list and Turkish teams/cities/names preset
- Multi-seed support and optional two-word combinations
- Frequency-oriented ordering, deduplication, length filters, and optional output limits
- `--auto` and `--max` presets for larger lists

## Requirements

Python 3.9 or newer.

## Usage

```powershell
python wordlist_gen.py
```

Starts the interactive wizard.

```powershell
python wordlist_gen.py fatih --auto
```

Generates the recommended preset for `fatih` and writes `wordlist.txt`.

```powershell
python wordlist_gen.py password --max
```

Uses the maximum preset. This can produce very large files.

```powershell
python wordlist_gen.py alice bob --auto --combine
```

Generates single-seed variants plus two-word combinations.

```powershell
python wordlist_gen.py --auto --common
```

Uses the built-in common-password and word list without seed words.

Use `python wordlist_gen.py --help` for all options.

## Notes

- Default output is `wordlist.txt`; use `-o <file>` to change it or `-o -` for stdout.
- Use `--limit <n>` while testing presets that produce large output.
- The tool deduplicates candidates and applies length filters after mutations.
- Higher `--leet-depth`, `--symbol-length`, and `--common` values grow output quickly.

## Data sources

The built-in common seeds include a selected, deduplicated subset of public entries from [SecLists](https://github.com/danielmiessler/SecLists) (MIT licensed), plus Turkish-specific terms informed by [utkusen/turkce-wordlist](https://github.com/utkusen/turkce-wordlist).

## Responsible use

Use this tool only for systems and accounts you own or are explicitly authorized to test.
