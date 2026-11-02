#!/usr/bin/env python3
import argparse
import itertools
import sys
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(errors="replace")

LEET = str.maketrans({
    "a": "4", "A": "4",
    "b": "8", "B": "8",
    "e": "3", "E": "3",
    "g": "9", "G": "9",
    "i": "1", "I": "1",
    "l": "1", "L": "1",
    "o": "0", "O": "0",
    "s": "5", "S": "5",
    "t": "7", "T": "7",
    "z": "2", "Z": "2",
})

LEET_OPTIONS = {
    "a": ("4", "@"), "A": ("4", "@"),
    "b": ("8",), "B": ("8",),
    "e": ("3",), "E": ("3",),
    "g": ("9",), "G": ("9",),
    "i": ("1", "!"), "I": ("1", "!"),
    "l": ("1",), "L": ("1",),
    "o": ("0",), "O": ("0",),
    "s": ("5", "$"), "S": ("5", "$"),
    "t": ("7",), "T": ("7",),
    "z": ("2",), "Z": ("2",),
}

LEET_DEPTH_DEFAULT = 2
AUTO_LEET_DEPTH = 3

TURKISH_ASCII = str.maketrans({
    "ç": "c", "Ç": "C",
    "ğ": "g", "Ğ": "G",
    "ı": "i", "İ": "I",
    "ö": "o", "Ö": "O",
    "ş": "s", "Ş": "S",
    "ü": "u", "Ü": "U",
})

DEFAULT_SYMBOL_CHARS = "!@#$%^&*._-"
COMMON_SYMBOL_PATTERNS = (
    "!", ".", "_", "*", "+", "-", "..", "$", "?", "__", "...", ")",
    "**", ",", "++", "!!", "#", "]", ":", "--", "&", "/", "+-", "??",
    "***", "___", ">", "!!!", "+++", ";", "[", "(", '"', "'", "^",
    "<", "=", "@", "%",
    "!@#", "!@#$", "!@#$%^&*", "*@#!.$%",
)

DEFAULT_NUMBERS_SPEC = (
    "1,123,123456,123456789,12,12345,1234,01,0123,2,11,3,7,10,"
    "123123,5,4,13,34,21,61,22,9,06,6,23,8,12345678,55,44,35,"
    "99,69,14,08,09,07,15,101,16,18,24,17,1234567,111111,"
    "1234567890,000000"
)

AUTO_YEARS_SPEC = "1980-2026"
MAX_SYMBOL_LENGTH = 5

COMMON_LAYERED_SUFFIXES = (
    "_123", "1!", "_1", ".1", ".123", "123.", "123!", "1.", "_2",
    "_01", "_12", "_34", "_07", "-123", "-1", "_21", "+11", "_35",
    "1234!", "12345!", "123456!", "1_", "123_", "_1234", "_12345",
    "_2024", "_2025", "_2026", "2024!", "2025!", "2026!",
    "_1907", "_1905", "_1903", "1907!", "1905!", "1903!",
)

TURKISH_SEED_PRESET = (
    "galatasaray", "fenerbahce", "besiktas", "trabzonspor",
    "istanbul", "ankara", "izmir", "bursa", "antalya", "trabzon",
    "kayseri", "malatya", "sakarya", "adana", "konya",
    "gaziantep", "diyarbakir", "mersin", "eskisehir", "kartal",
    "samsun", "denizli", "sanliurfa", "erzurum",
    "mustafa", "mehmet", "ahmet", "ali", "huseyin", "hasan",
    "ibrahim", "ismail", "ramazan", "abdullah", "fatih", "emre",
    "burak", "murat", "serkan", "kemal", "zeynep", "yasemin",
    "ozlem", "elif", "merve", "busra", "ayse", "fatma", "emine",
    "hatice", "sevgi", "melis", "sibel", "derya",
)

COMMON_PASSWORD_SEEDS = (
    "123", "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "1234567", "111111", "1234567890", "123123", "000000", "admin",
    "abc123", "1234", "password1", "iloveyou", "welcome", "monkey",
    "login", "princess", "dragon", "football", "baseball", "master",
    "sunshine", "shadow", "superman", "batman", "spiderman", "letmein",
    "apollo", "whatever", "trustno1", "freedom", "hello", "secret",
    "azerty", "linkedin", "computer", "internet", "samsung", "iphone",
    "google", "facebook", "instagram", "twitter", "youtube", "tiktok",
    "lovely", "flower", "summer", "winter", "michael", "jennifer",
    "jordan", "harley", "ranger", "hunter", "killer", "matrix",
    "pokemon", "naruto", "minecraft", "fortnite", "chelsea", "liverpool",
    "arsenal", "barcelona", "realmadrid", "juventus", "messi", "ronaldo",
    "neymar", "galatasaray", "fenerbahce", "besiktas", "trabzonspor",
    "istanbul", "ankara", "izmir", "mustafa", "mehmet", "ahmet",
    "fatih", "zeynep", "yasemin", "sanane", "lovelife", "kartal",
    "qwerty123", "1q2w3e4r", "1qaz2wsx", "zaq12wsx", "123qwe",
    "123abc", "passw0rd", "p@ssw0rd", "admin123", "root", "test",
    "guest", "user", "default", "changeme", "secret123", "eminem",
    "jasmine", "ismail", "ramazan", "abdullah", "malatya", "trabzon",
    "kayseri", "sakarya", "adana", "konya", "gaziantep",
)

SECLISTS_COMMON_SEEDS = (
    'aa123456', 'pass@123', '12345678910', 'aa@123456',
    'admintelecom', 'admin@123', '112233', '102030',
    '654321', 'abcd1234', 'abcd@1234', 'pass@1234',
    '11223344', '87654321', '987654321', '123123123',
    'aa112233', '12341234', 'qwertyuiop', '11111111',
    'password@123', 'asd123', 'aboy1234', '123321',
    'admin1', 'demo@123', '1q2w3e4r5t', 'admin1234',
    '121212', 'asdf1234', '888888', 'guru123456',
    '666666', 'welcome@123', '123456789a', 'kapler123',
    'administrator', '1122334455', 'test@123', 'qwer1234',
    'asdfghjkl', 'global123@', '10203040', '1234qwer',
    'india@123', 'abcd@123', '88888888', '12345678a',
    'aa123123', '12344321', '123456aa@', '123456a',
    'a123456', '202020', '1234abcd', 'admin123456',
    'qwe123', '101010', '222222', '12121212',
    'abc12345', 'abc@1234', 'admin12345', '12345678900',
    '123654', '555555', 'aa123456789', '1111111111',
    '12345678901', 'q1w2e3r4', 'password123', 'heslo1234',
    '22446688', 'vodafone', '999999', 'bismillah',
    'a123456789', 'user1234', '1234567891', '1234512345',
    'adminisp', '1234567899', 'p@$$w0rd', 'aa12345678',
    'zxcvbnm', 'adminadmin', 'qwerty12345', 'gvt12345',
    'pakistan', '10203', 'welcome1', 'theworldinyourhand',
    'aabb1122', 'test123', '54321', '1111111',
    'a1b2c3d4', 'student', 'abc@12345', 'aa102030',
    'pass@12345', '135790', 'cisco', '11111',
    'aa@12345', '111111111', 'lol123456', '147258369',
    '123456aa', 'aa@1234567', 'admin@1234', '1234554321',
    '124578', '12qwaszx', 'abc@123', 'a12345678',
    'qwer4321', 'a1234567', 'qwerty@123', '12345679',
    'ab123456', 'aa@123456789', 'abcd1234@', '123qweasd',
    'pakistan123', 'a123456a', 'qwerty1234', '1234567a',
    'abc123456', 'turktelekom', 'test1234', '999999999',
    '123456788', 'aaa111', '7654321', '1qazxsw2',
    'password@1', 'asdasd', 'aaaaaa', 'qwerty123456',
    '246810', '11112222', 'aaaa1111', 'q1w2e3r4t5',
    '987654', 'azerty123', 'aa1234567', '12345678@',
    'p@55w0rd', 'asd12345', 'zxcvbnm123', '123admin',
    'qwerty1', '00000000', 'target123', 'tinkle',
    'zag12wsx', '1g2w3e4r', 'gwerty123', 'gwerty',
    'qwerty123!', 'qwerty1!', 'q1w2e3r4t5y6', 'fuckyou',
    'qwerty12', '159753', 'dearbook', '1234561',
    'daniel', '111222tianya', '1qaz2wsx3edc', 'qwerty1?',
    '789456123', 'qwerty123?', 'soccer', '7777777',
    '22535', 'testing', 'qazwsx', '1314520',
    'michelle', 'charlie', '7758521', 'woaini',
    'asdfgh', 'starwars', 'jessica', 'unknown',
    '1q2w3e', '789456', 'ashley', 'thomas',
    '159357', 'andrew', 'nicole', 'anthony',
    '147258', 'jonathan', 'basketball', 'cambiami',
    'chocolate', 'zinch', 'asdfasdf', 'justin',
    'purple', 'blink182', 'g_czechout', 'tigger',
    'indya123', 'samantha', 'joshua', 'alexander',
    'hannah', 'qazwsxedc', 'andrea', 'matthew',
    '123456!', 'jordan23', 'qq123456', 'william',
    '123456123', 'buster', 'cookie', 'babygirl',
    'butterfly', 'lol123', 'qwert', 'robert',
    'amanda', '123654789', 'aaaaaaaa', 'benjamin',
    'myspace1', '333333', 'family', 'hello123',
    'maggie', 'cheese',
)


class LimitReached(Exception):
    pass


def parse_suffixes(spec):
    values = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            step = 1 if end >= start else -1
            values.extend(str(number) for number in range(start, end + step, step))
        else:
            values.append(part)
    return values


def build_exhaustive_symbol_patterns(chars, max_length):
    if max_length < 1:
        return []
    patterns = []
    unique_chars = "".join(dict.fromkeys(chars))
    for length in range(1, max_length + 1):
        for combo in itertools.product(unique_chars, repeat=length):
            patterns.append("".join(combo))
    return patterns


def ask_text(prompt, default=""):
    shown = f" [{default}]" if default else ""
    value = input(f"{prompt}{shown}: ").strip()
    return value or default


def ask_yes_no(prompt, default):
    hint = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} [{hint}]: ").strip().lower()
        if not value:
            return default
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Please enter yes or no.")


def ask_int(prompt, default, minimum=0):
    while True:
        value = ask_text(prompt, str(default))
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if number < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        return number


def ask_range(prompt, default, display_default=None):
    while True:
        if display_default is not None:
            shown_default = display_default
        else:
            shown_default = default if default else "none"
        value = input(f"{prompt} [{shown_default}]: ").strip()
        if not value:
            return default
        if value.lower() in ("none", "off"):
            return None
        try:
            parse_suffixes(value)
        except ValueError:
            print("Use comma-separated numbers or ranges, e.g. 0-9 or 1,2,42.")
            continue
        return value


def split_list(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def interactive_setup(args):
    print("Wordlist Generator - interactive setup")
    print("Press Enter to accept a default in [brackets].\n")

    existing_words = ", ".join(args.words)
    while True:
        words = split_list(ask_text("Seed words (comma-separated)", existing_words))
        if words:
            break
        print("Enter at least one seed word.")

    existing_files = ", ".join(args.words_file)
    while True:
        files_text = ask_text(
            "Seed word file (comma-separated, blank for none)",
            existing_files,
        )
        words_files = split_list(files_text)
        missing = [path for path in words_files if not Path(path).is_file()]
        if not missing:
            break
        print(f"File not found: {', '.join(missing)}")
        existing_files = ""

    output = ask_text("Output file (- for stdout)", args.output)
    while output != "-" and Path(output).exists():
        if ask_yes_no(f"{output} already exists. Overwrite?", False):
            break
        output = ask_text("Output file", "wordlist.txt")

    use_turkish_seeds = ask_yes_no(
        "Add built-in Turkish seed preset (teams/cities/names)?",
        args.turkish_seeds,
    )
    use_common = ask_yes_no(
        "Add built-in common password/word list?",
        args.common,
    )
    case = ask_yes_no("Add case variations?", args.case)
    leet = ask_yes_no("Add leet substitutions (a->4, e->3, etc.)?", args.leet)
    leet_depth = args.leet_depth
    if leet:
        leet_depth = ask_int(
            "Maximum simultaneous leet substitutions",
            args.leet_depth,
            0,
        )
    turkish = ask_yes_no(
        "Normalize Turkish characters to ASCII?",
        args.turkish,
    )

    use_symbols = ask_yes_no("Add symbol patterns?", args.symbols is not None)
    symbol_chars = args.symbols if use_symbols else None
    symbol_length = args.symbol_length
    if use_symbols:
        symbol_chars = ask_text("Symbol characters", args.symbols or DEFAULT_SYMBOL_CHARS)
        symbol_length = ask_int(
            "Maximum symbol pattern length (0 = common patterns only)",
            args.symbol_length,
            0,
        )

    numbers = ask_range(
        "Numeric suffixes (e.g. 0-9, or none)",
        args.numbers,
        "common" if args.numbers == DEFAULT_NUMBERS_SPEC else None,
    )
    years = ask_range("Year suffixes (e.g. 1980-2026, or none)", args.years)

    prefixes = split_list(ask_text(
        "Prefixes (comma-separated, blank for none)",
        ", ".join(args.prefix),
    ))
    suffixes = split_list(ask_text(
        "Suffixes (comma-separated, blank for none)",
        ", ".join(args.suffix),
    ))
    layered = ask_yes_no(
        "Add layered number+symbol endings (e.g. 123!, _123)?",
        args.layered,
    )

    combine = ask_yes_no("Combine every pair of seed words?", args.combine)
    separators = args.separator
    if combine:
        default_separator = ",".join(args.separator) if args.separator is not None else ""
        separator_text = ask_text(
            "Pair separators (comma-separated, blank for none)",
            default_separator,
        )
        separators = split_list(separator_text) if separator_text else [""]
    else:
        separators = None

    min_length = ask_int("Minimum candidate length (0 for no limit)", args.min_length)
    max_length = ask_int("Maximum candidate length (0 for no limit)", args.max_length)
    while max_length and min_length > max_length:
        print("Maximum length must be 0 or at least the minimum length.")
        max_length = ask_int(
            "Maximum candidate length (0 for no limit)",
            args.max_length,
        )
    limit = ask_int("Maximum entries to write (0 for unlimited)", args.limit)

    print("\nSetup:")
    print(f"  Seed words: {', '.join(words)}")
    if words_files:
        print(f"  Seed files: {', '.join(words_files)}")
    if use_turkish_seeds:
        print("  Turkish seed preset: on")
    if use_common:
        print("  Common password/word seeds: on")
    print(f"  Output: {output}")
    print(f"  Case: {'on' if case else 'off'}")
    if leet:
        print(f"  Leet: on (depth {leet_depth})")
    else:
        print("  Leet: off")
    print(f"  Turkish normalization: {'on' if turkish else 'off'}")
    if use_symbols:
        print(f"  Symbols: {symbol_chars} (exhaustive length: {symbol_length})")
    else:
        print("  Symbols: off")
    number_display = (
        "common" if numbers == DEFAULT_NUMBERS_SPEC else (numbers or "off")
    )
    print(f"  Numbers: {number_display}")
    print(f"  Years: {years or 'off'}")
    print(f"  Prefixes: {', '.join(prefixes) or 'none'}")
    print(f"  Suffixes: {', '.join(suffixes) or 'none'}")
    print(f"  Layered endings: {'on' if layered else 'off'}")
    print(f"  Word pairs: {'on' if combine else 'off'}")
    if combine:
        print(f"  Separators: {', '.join(repr(value) for value in separators)}")
    print(f"  Length: {min_length or 'none'} to {max_length or 'none'}")
    print(f"  Limit: {limit or 'unlimited'}")

    if not ask_yes_no("\nGenerate this wordlist?", True):
        print("Cancelled.")
        return False

    args.words = words
    args.words_file = words_files
    args.turkish_seeds = use_turkish_seeds
    args.common = use_common
    args.output = output
    args.case = case
    args.leet = leet
    args.leet_depth = leet_depth
    args.turkish = turkish
    args.symbols = symbol_chars
    args.symbol_length = symbol_length
    args.numbers = numbers
    args.years = years
    args.prefix = prefixes
    args.suffix = suffixes
    args.layered = layered
    args.combine = combine
    args.separator = separators
    args.min_length = min_length
    args.max_length = max_length
    args.limit = limit
    return True


def load_words(files, inline_words):
    words = []
    for filename in files:
        path = Path(filename)
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                word = line.strip()
                if word and not word.startswith("#"):
                    words.append(word)
    words.extend(w.strip() for w in inline_words if w.strip())
    return list(dict.fromkeys(words))


def build_leet_variants(value, max_depth):
    positions = [index for index, char in enumerate(value) if char in LEET_OPTIONS]
    if not positions or max_depth < 1:
        return []
    variants = []
    limit = min(max_depth, len(positions))
    for depth in range(1, limit + 1):
        for indexes in itertools.combinations(positions, depth):
            option_sets = [LEET_OPTIONS[value[index]] for index in indexes]
            for replacements in itertools.product(*option_sets):
                chars = list(value)
                for index, char in zip(indexes, replacements):
                    chars[index] = char
                variant = "".join(chars)
                if variant != value:
                    variants.append(variant)
    return variants


def mutate(word, use_case, use_leet, use_turkish, leet_depth):
    values = []
    seen = set()

    def add(value):
        if value not in seen:
            seen.add(value)
            values.append(value)

    if use_case:
        add(word.lower())
    add(word)
    if use_case:
        add(word.capitalize())
        add(word.upper())
        add(word.title())
        add(word.swapcase())
    if use_turkish:
        for value in list(values):
            add(value.translate(TURKISH_ASCII))
    if use_leet:
        for value in list(values):
            for variant in build_leet_variants(value, leet_depth):
                add(variant)
            add(value.translate(LEET))
    return values


def build_bases(
    words,
    use_case,
    use_leet,
    use_turkish,
    leet_depth,
    use_combine,
    separators,
):
    variants = {
        word: mutate(word, use_case, use_leet, use_turkish, leet_depth)
        for word in words
    }

    for word in words:
        for variant in variants[word]:
            yield variant

    if not use_combine:
        return

    for first, second in itertools.permutations(words, 2):
        for left in variants[first]:
            for right in variants[second]:
                for separator in separators:
                    yield left + separator + right


def generate(words, prefixes, suffixes, args):
    for base in build_bases(
        words,
        args.case,
        args.leet,
        args.turkish,
        args.leet_depth,
        args.combine,
        args.separator,
    ):
        for prefix in prefixes:
            for suffix in suffixes:
                candidate = prefix + base + suffix
                if args.min_length and len(candidate) < args.min_length:
                    continue
                if args.max_length and len(candidate) > args.max_length:
                    continue
                yield candidate


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a wordlist from seed words with common mutations. "
            "Run without seed words for an interactive setup. "
            "Defaults: case, partial leet, Turkish normalization, common "
            "symbols and numbers, layered endings, output to wordlist.txt. "
            "--auto adds years and 3-character symbol combinations; "
            "--max expands symbols up to length 5. "
            "--common adds standalone common passwords and words."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python wordlist_gen.py\n"
            "  python wordlist_gen.py fatih --auto\n"
            "  python wordlist_gen.py fatih --max\n"
            "  python wordlist_gen.py --auto --common\n"
            "  python wordlist_gen.py fatih --auto --common\n"
            "  python wordlist_gen.py --auto --common-file 10k-most-common.txt\n"
            "  python wordlist_gen.py fatih --no-leet --numbers 0-99\n"
            "  python wordlist_gen.py alice bob --combine -o custom.txt\n"
            "  python wordlist_gen.py --turkish-seeds -o turkish.txt\n"
        ),
    )
    parser.add_argument("words", nargs="*", help="seed words")
    parser.add_argument(
        "-w", "--words-file", action="append", default=[], metavar="FILE",
        help="file containing one seed word per line (repeatable)",
    )
    parser.add_argument(
        "--turkish-seeds", action="store_true",
        help="add a built-in Turkish preset of teams, cities, and names",
    )
    parser.add_argument(
        "--common", "--common-words", dest="common", action="store_true",
        help=(
            "add built-in common passwords and words as extra seeds, "
            "including recent SecLists entries "
            "(for example 123456, password, apollo)"
        ),
    )
    parser.add_argument(
        "--common-file", action="append", default=[], metavar="FILE",
        help=(
            "load extra common seed words from a file, such as a SecLists "
            "password list (repeatable)"
        ),
    )
    parser.add_argument(
        "-o", "--output", default="wordlist.txt", metavar="FILE",
        help="output file (default: wordlist.txt; use - for stdout)",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true",
        help=(
            "ask for every setting interactively "
            "(automatic when no seed words are given)"
        ),
    )
    parser.add_argument(
        "--auto", action="store_true",
        help=(
            "apply the complete preset, including years, 3-character symbol "
            "combinations, and leet depth 3; if no seeds are supplied, the common "
            "password/word preset is used; override with --symbol-length "
            "or use --combine separately for word pairs"
        ),
    )
    parser.add_argument(
        "--max", "--max-symbol", dest="max_mode", action="store_true",
        help=(
            "maximum preset: implies --auto and expands symbol combinations "
            f"to length {MAX_SYMBOL_LENGTH} unless --symbol-length is given"
        ),
    )
    parser.add_argument(
        "--case", action="store_true", default=True, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-case", dest="case", action="store_false",
        help="disable case variations (enabled by default)",
    )
    parser.add_argument(
        "--leet", action="store_true", default=True, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-leet", dest="leet", action="store_false",
        help="disable leetspeak variations (enabled by default)",
    )
    parser.add_argument(
        "--leet-depth", type=int, default=LEET_DEPTH_DEFAULT, metavar="N",
        help=(
            "maximum simultaneous leet substitutions per word; "
            "0 keeps only full substitutions (default: 2; --auto uses 3)"
        ),
    )
    parser.add_argument(
        "--turkish", action="store_true", default=True, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-turkish", dest="turkish", action="store_false",
        help="disable Turkish character normalization (enabled by default)",
    )
    parser.add_argument(
        "--combine", action="store_true",
        help="generate two-word combinations in both orders",
    )
    parser.add_argument(
        "--separator", action="append", default=None, metavar="TEXT",
        help="separator for combined words (repeatable; default: empty string)",
    )
    parser.add_argument("--prefix", action="append", default=[], metavar="TEXT",
                        help="prefix to add (repeatable)")
    parser.add_argument("--suffix", action="append", default=[], metavar="TEXT",
                        help="suffix to add (repeatable)")
    parser.add_argument(
        "--symbols", nargs="?", const=DEFAULT_SYMBOL_CHARS,
        default=DEFAULT_SYMBOL_CHARS, metavar="CHARS",
        help=(
            "include common symbol suffixes; optional CHARS is the charset "
            "used by --symbol-length"
        ),
    )
    parser.add_argument(
        "--no-symbols", dest="symbols", action="store_const", const=None,
        help="disable symbol suffixes",
    )
    parser.add_argument(
        "--symbol-length", type=int, default=0, metavar="N",
        help=(
            "also generate every symbol combination up to length N; "
            "0 uses only common patterns (default: 0)"
        ),
    )
    parser.add_argument(
        "--no-layered", dest="layered", action="store_false",
        help="disable layered number+symbol endings (enabled by default)",
    )
    parser.add_argument(
        "--numbers", default=DEFAULT_NUMBERS_SPEC, metavar="RANGE",
        help="numeric suffixes (default: common observed suffixes)",
    )
    parser.add_argument(
        "--no-numbers", dest="numbers", action="store_const", const=None,
        help="disable numeric suffixes",
    )
    parser.add_argument("--years", metavar="RANGE",
                        help="year suffixes, e.g. 1980-2026")
    parser.add_argument(
        "--no-years", dest="years", action="store_const", const=None,
        help="disable year suffixes, including the years added by --auto",
    )
    parser.add_argument("--min-length", type=int, default=0, metavar="N")
    parser.add_argument("--max-length", type=int, default=0, metavar="N")
    parser.add_argument(
        "--limit", type=int, default=0, metavar="N",
        help="optional maximum entries to write; 0 means unlimited (default)",
    )
    args = parser.parse_args()

    if args.symbol_length < 0:
        parser.error("--symbol-length cannot be negative")
    if args.leet_depth < 0:
        parser.error("--leet-depth cannot be negative")

    if args.max_mode:
        args.auto = True

    if args.auto:
        if (
            not args.words
            and not args.words_file
            and             not args.turkish_seeds
            and not args.common
            and not args.common_file
        ):
            args.common = True
        if args.years is None and "--no-years" not in sys.argv:
            args.years = AUTO_YEARS_SPEC
        if "--no-layered" not in sys.argv:
            args.layered = True
        leet_depth_given = any(
            arg == "--leet-depth" or arg.startswith("--leet-depth=")
            for arg in sys.argv[1:]
        )
        if args.leet and not leet_depth_given:
            args.leet_depth = AUTO_LEET_DEPTH
        symbol_length_given = any(
            arg == "--symbol-length" or arg.startswith("--symbol-length=")
            for arg in sys.argv[1:]
        )
        if args.symbols is not None and not symbol_length_given:
            if args.max_mode:
                args.symbol_length = MAX_SYMBOL_LENGTH
            else:
                args.symbol_length = 3

    if args.interactive or (
        not args.auto
        and not args.turkish_seeds
        and not args.common
        and not args.common_file
        and not args.words
        and not args.words_file
    ):
        try:
            if not interactive_setup(args):
                return
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.", file=sys.stderr)
            return

    words = load_words(args.words_file, args.words)
    if args.common:
        common_words = list(COMMON_PASSWORD_SEEDS)
        common_words.extend(SECLISTS_COMMON_SEEDS)
        words = list(dict.fromkeys(words + common_words))
    if args.common_file:
        words = list(dict.fromkeys(words + load_words(args.common_file, [])))
    if args.turkish_seeds:
        words = list(dict.fromkeys(words + list(TURKISH_SEED_PRESET)))
    if not words:
        parser.error("provide seed words as arguments or with --words-file")

    prefixes = list(dict.fromkeys([""] + args.prefix))
    suffixes = [""] + list(args.suffix)
    try:
        if args.numbers:
            suffixes.extend(parse_suffixes(args.numbers))
        if args.years:
            suffixes.extend(parse_suffixes(args.years))
    except ValueError:
        parser.error("invalid number or year range")
    if args.symbols is not None:
        suffixes.extend(COMMON_SYMBOL_PATTERNS)
    if args.layered:
        suffixes.extend(COMMON_LAYERED_SUFFIXES)
    if args.symbols is not None and args.symbol_length > 0:
        suffixes.extend(
            build_exhaustive_symbol_patterns(args.symbols, args.symbol_length)
        )
    suffixes = list(dict.fromkeys(suffixes))

    separators = [""] if args.separator is None else list(dict.fromkeys(args.separator))

    output = sys.stdout
    if args.output != "-":
        output = Path(args.output).open("w", encoding="utf-8", newline="\n")

    seen = set()
    count = 0

    try:
        for candidate in generate(words, prefixes, suffixes, args):
            if candidate in seen:
                continue
            seen.add(candidate)
            output.write(candidate + "\n")
            count += 1
            if args.limit and count >= args.limit:
                raise LimitReached
    except LimitReached:
        pass
    except BrokenPipeError:
        pass
    finally:
        if output is not sys.stdout:
            output.close()

    destination = "stdout" if args.output == "-" else args.output
    print(f"Generated {count:,} entries to {destination}", file=sys.stderr)
    if args.limit and count >= args.limit:
        print(f"Stopped at the {args.limit:,} entry limit", file=sys.stderr)


if __name__ == "__main__":
    main()
