"""Reapply the round-three review faults one at a time in a disk scratch copy."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = "five_fund_snapshot"
CORRUPT = "guards_reject_corrupt"
INVALID = "rejects_invalid_denominator"
PROBES = {
    "kill_test": (
        ("issuer floor only", "max(fund.supply_floor_usd, custody + contracts + other_exclusions)",
         "fund.supply_floor_usd", SNAPSHOT),
        ("OUSG exclusions at high NAV", 'ousg_exclusion_nav = model["direct_exclusion_nav_usd"]',
         'ousg_exclusion_nav = model["high_nav_usd"]', SNAPSHOT),
        ("negative shortfall", "max(ZERO, THRESHOLD * ceiling - verified)",
         "(THRESHOLD * ceiling - verified)", SNAPSHOT),
        ("BENJI exclusions at par", "benji_nav,\n    }", "D(1),\n    }", SNAPSHOT),
        ("trust Curve coin result", 'or result("ethereum", label)[-40:].lower() != coin["address"][2:].lower()',
         'or False', CORRUPT),
        ("trust wrong Frax destination", "value = pinned_read(chains[chain], label, method, *args)",
         'if label == "frax_buidl":\n'
         '            args = [chains[chain]["reads"][label]["params"][0]]\n'
         '        value = pinned_read(chains[chain], label, method, *args)', CORRUPT),
        ("ignore RPC cutoff", ' or rpc["cutoff"] != CUTOFF', '', CORRUPT),
        ("accept zero or negative USYC NAV", "not 0 < answer < 2**255 or ", "", CORRUPT),
        ("ignore Franklin period", 'filing["report_period"] != DATE or ', '', CORRUPT),
        ("ignore Franklin share class", 'or filing["class"] != "C000215714"', 'or False', CORRUPT),
        ("ignore Franklin share count", 'or D(filing["item_b5_shares"]) != D(facts["franklin_benji_shares"])',
         'or False', CORRUPT),
        ("ignore OUSG adjacent window", 'or sorted(row["timestamp"] for row in adjacent) != [',
         'or False and sorted(row["timestamp"] for row in adjacent) != [', CORRUPT),
        ("accept wrong collateral underlying", ' or result[-40:] != report["token"][2:]', '', CORRUPT),
        ("accept duplicate fund", 'if len(funds_by_ticker) != len(funds):', 'if False:', INVALID),
        ("accept floor above cap", 'not ZERO < row.supply_floor_usd <= row.supply_ceiling_usd',
         'not ZERO < row.supply_floor_usd', INVALID),
        ("accept nonpositive position", ' or row.usd <= ZERO', '', INVALID),
        ("accept unknown classification", 'if row.kind not in {"wrapper_contract", "reserve_custody", "verified_non_wrapper"}:',
         'if False:', INVALID),
        ("remove STBL net deposits cap", 'min(stbl["native"], usst["net_deposits_ousg"],',
         'min(stbl["native"],', 'stbl_credit_is_capped'),
    ),
    "holder_audit": (
        ("ignore pinned read block", 'row["params"] != [*args, capture["block"]["number"]]',
         'row["params"][:-1] != list(args)', CORRUPT),
        ("accept nonconsecutive successor", 'or int(successor["number"], 16) != int(block["number"], 16) + 1',
         'or False', CORRUPT),
        ("accept future block", 'not int(block["timestamp"], 16) <= CUTOFF < int(successor["timestamp"], 16)',
         'not CUTOFF < int(successor["timestamp"], 16)', CORRUPT),
    ),
    "check_post_card": (
        ("accept malformed PNG magic", ' or png[:16] != b"\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR"',
         '', 'malformed_png'),
        ("accept wrong PNG dimensions", 'if list(struct.unpack(">II", png[16:24])) != receipt["size_px"]:',
         'if False:', 'malformed_png'),
        ("accept two draft claims", 'if len(claims) != 1:', 'if not claims:', 'requires_one_claim'),
    ),
    "replay_evidence": (
        ("accept extra logs", 'if len(actual) != len(expected):', 'if False:', 'exact_log_cardinality'),
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True, help="existing task-owned disk directory")
    args = parser.parse_args()
    survivors = []
    with TemporaryDirectory(dir=args.scratch) as directory:
        copy = Path(directory)
        for folder in ("scripts", "tests", "evidence", "docs", "posts"):
            shutil.copytree(ROOT / folder, copy / folder, ignore=shutil.ignore_patterns("__pycache__"))
        for module, probes in PROBES.items():
            path = copy / "scripts" / f"{module}.py"
            original = path.read_text()
            for label, before, after, test in probes:
                if original.count(before) != 1:
                    raise ValueError(f"unexpected mutation anchor for {label}")
                path.write_text(original.replace(before, after, 1))
                try:
                    run = subprocess.run(
                        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-q", "-k", test],
                        cwd=copy, capture_output=True, text=True,
                    )
                finally:
                    path.write_text(original)
                if run.returncode == 1 and "FAIL:" in run.stderr and "ERROR:" not in run.stderr:
                    print(f"killed: {label}")
                else:
                    survivors.append(label)
                    print(f"unconfirmed: {label}\n{run.stderr}")
    total = sum(map(len, PROBES.values()))
    print(f"{total - len(survivors)}/{total} probes killed by behavioral assertions")
    return bool(survivors)


if __name__ == "__main__":
    raise SystemExit(main())
