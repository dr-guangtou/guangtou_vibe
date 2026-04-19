#!/usr/bin/env python
"""
galfit_cli.py - Thin CLI wrapper around galfit_io and galfit_constraints.

Subcommands:

    summary     <in>            - Print a compact overview of a .galfit file.
    to-yaml     <in> <out>      - Parse and emit YAML.
    from-yaml   <in> <out>      - Load YAML and emit .galfit.
    to-json     <in> <out>      - Parse and emit JSON.
    from-json   <in> <out>      - Load JSON and emit .galfit.
    rewrite     <in> <out>      - Parse and re-emit .galfit (strips output
                                  decorations by default).
    rewrite     <in> <out> --preserve-decorations
                                - Round-trip preserving `[]`, `{}`, `*`, (err).

    constraints-to-yaml   <in> <out>
    constraints-from-yaml <in> <out>

Usage from the shell:

    python galfit_cli.py summary /path/to/galfit.01
    python galfit_cli.py to-yaml in.feedme in.yaml
    python galfit_cli.py from-yaml in.yaml out.feedme
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import galfit_io  # noqa: E402
import galfit_constraints  # noqa: E402


def cmd_summary(args: argparse.Namespace) -> int:
    gf = galfit_io.read_galfit(args.input)
    h = gf.header
    print(f"File: {args.input}")
    print(f"Input image: {h.input_image}")
    print(f"Fit region: {h.fit_region}")
    print(f"Zeropoint: {h.zeropoint}")
    print(f"Plate scale: {h.plate_scale}")
    print(f"Components: {len(gf.components)}")
    for i, c in enumerate(gf.components, start=1):
        cls = type(c).__name__
        if isinstance(c, galfit_io.TruncationComponent):
            print(f"  [{i}] {cls} type={c.trunc_type}")
        else:
            print(f"  [{i}] {cls} profile={c.profile_token}")
        hb = c.hidden
        extras = []
        if hb.c0 is not None:
            extras.append("C0")
        if hb.bending:
            extras.append(f"B{sorted(hb.bending)}")
        if hb.fourier:
            extras.append(f"F{sorted(hb.fourier)}")
        if hb.rotation is not None:
            extras.append(f"R({hb.rotation.mode})")
        if hb.trunc_inner_ref is not None:
            extras.append(f"Ti={hb.trunc_inner_ref}")
        if hb.trunc_outer_ref is not None:
            extras.append(f"To={hb.trunc_outer_ref}")
        if extras:
            print(f"       hidden: {', '.join(extras)}")
    return 0


def cmd_to_yaml(args: argparse.Namespace) -> int:
    gf = galfit_io.read_galfit(args.input)
    Path(args.output).write_text(galfit_io.to_yaml(gf), encoding="utf-8")
    return 0


def cmd_from_yaml(args: argparse.Namespace) -> int:
    gf = galfit_io.from_yaml(Path(args.input).read_text(encoding="utf-8"))
    galfit_io.write_galfit(
        gf, args.output, preserve_decorations=args.preserve_decorations,
    )
    return 0


def cmd_to_json(args: argparse.Namespace) -> int:
    gf = galfit_io.read_galfit(args.input)
    Path(args.output).write_text(galfit_io.to_json(gf), encoding="utf-8")
    return 0


def cmd_from_json(args: argparse.Namespace) -> int:
    gf = galfit_io.from_json(Path(args.input).read_text(encoding="utf-8"))
    galfit_io.write_galfit(
        gf, args.output, preserve_decorations=args.preserve_decorations,
    )
    return 0


def cmd_rewrite(args: argparse.Namespace) -> int:
    gf = galfit_io.read_galfit(args.input)
    galfit_io.write_galfit(
        gf, args.output, preserve_decorations=args.preserve_decorations,
    )
    return 0


def cmd_constraints_to_yaml(args: argparse.Namespace) -> int:
    entries = galfit_constraints.read_constraints(args.input)
    Path(args.output).write_text(
        galfit_constraints.to_yaml_constraints(entries), encoding="utf-8",
    )
    return 0


def cmd_constraints_from_yaml(args: argparse.Namespace) -> int:
    entries = galfit_constraints.from_yaml_constraints(
        Path(args.input).read_text(encoding="utf-8"),
    )
    galfit_constraints.write_constraints(entries, args.output)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("summary")
    p.add_argument("input")
    p.set_defaults(func=cmd_summary)

    for name, fn in [
        ("to-yaml", cmd_to_yaml),
        ("to-json", cmd_to_json),
    ]:
        sp = sub.add_parser(name)
        sp.add_argument("input")
        sp.add_argument("output")
        sp.set_defaults(func=fn)

    for name, fn in [
        ("from-yaml", cmd_from_yaml),
        ("from-json", cmd_from_json),
        ("rewrite",   cmd_rewrite),
    ]:
        sp = sub.add_parser(name)
        sp.add_argument("input")
        sp.add_argument("output")
        sp.add_argument("--preserve-decorations", action="store_true",
                        help="Keep `[]`, `{}`, `*`, (err) tokens on write.")
        sp.set_defaults(func=fn)

    sp = sub.add_parser("constraints-to-yaml")
    sp.add_argument("input")
    sp.add_argument("output")
    sp.set_defaults(func=cmd_constraints_to_yaml)

    sp = sub.add_parser("constraints-from-yaml")
    sp.add_argument("input")
    sp.add_argument("output")
    sp.set_defaults(func=cmd_constraints_from_yaml)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
