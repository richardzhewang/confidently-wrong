"""Shared helpers: directory layout, prompt, answer parsing, grading, report writer."""

import os
import pathlib
import re

# ---- study layout (single source of truth; scripts import these) ----
STUDY = pathlib.Path(__file__).resolve().parent.parent
DATA = STUDY / "data"          # measured artifacts: generations, selfcons(+meta), baselines
CACHE = STUDY / "cache"        # big regenerable npz (activations, per-token)
SCORES = STUDY / "scores"      # per-example score CSVs (one per model x dataset)
RESULTS_DIR = STUDY / "results"  # generated tables
PILOT = DATA / "pilot"         # 800-question Qwen3-8B FinQA pilot (placebo + grader audit)

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen3-8B")


def score_csv_path(condition: str) -> pathlib.Path:
    """scores/{condition}.csv, e.g. scores/qwen_full_finqa.csv."""
    SCORES.mkdir(parents=True, exist_ok=True)
    return SCORES / f"{condition}.csv"


def results_path(stem: str) -> pathlib.Path:
    """results/{stem}.md"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / f"{stem}.md"


def rel(path) -> str:
    """Path relative to the repository root, for provenance headers in result files."""
    try:
        return str(pathlib.Path(path).resolve().relative_to(STUDY.parent))
    except ValueError:
        return str(path)


def generations_path(condition: str) -> pathlib.Path:
    """Map a scores condition (e.g. 'qwen_full_finqa') to its generations jsonl.

    FinQA is the default dataset (no suffix); TAT-QA carries a '_tatqa' suffix:
        qwen_full_finqa -> generations_qwen_full.jsonl
        qwen_full_tatqa -> generations_qwen_full_tatqa.jsonl
    """
    if condition.endswith("_tatqa"):
        stem, suffix = condition[:-len("_tatqa")], "_tatqa"
    elif condition.endswith("_finqa"):
        stem, suffix = condition[:-len("_finqa")], ""
    else:
        stem, suffix = condition, ""
    core = f"_{stem}" if stem else ""
    return DATA / f"generations{core}{suffix}.jsonl"


def build_messages(system: str, user: str):
    """Gemma templates reject a system role -> fold it into the user turn."""
    if "gemma" in MODEL_NAME.lower():
        return [{"role": "user", "content": f"{system}\n\n{user}"}]
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def ensure_pad(tok):
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


class Reporter:
    """Tee analysis output to stdout AND a provenance-stamped markdown file.

    Usage:
        rep = Reporter("12_two_by_two_llama", meta={"model": "...", "folds": "..."})
        rep.log("some line")
        rep.save()          # -> study/results/12_two_by_two_llama.md

    Results files are machine-generated: rerunning the script overwrites them,
    so they can never go stale relative to the code/labels that produced them.
    """

    def __init__(self, name, meta=None):
        import pathlib

        self.name = name
        self.meta = meta or {}
        self.lines = []

    def log(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def save(self):
        from datetime import datetime

        hdr = [
            f"# {self.name}",
            "",
            f"- generated: {datetime.now().isoformat(timespec='seconds')}",
            "- grader: v2 (x1000 scales, strict sign, 2% tol)",
        ]
        hdr += [f"- {k}: {v}" for k, v in self.meta.items()]
        body = "\n".join(["```"] + self.lines + ["```"])
        path = results_path(self.name)
        path.write_text("\n".join(hdr) + "\n\n" + body + "\n")
        print(f"\n[saved {path}]", flush=True)


def pick_probe_feat(npz_keys, pooling="ans_mean"):
    """Default probe feature = the layer closest to 2/3 depth."""
    layers = sorted({int(k.split("_")[0][1:]) for k in npz_keys if k.startswith("L")})
    target = max(layers) * 2 / 3
    best = min(layers, key=lambda l: abs(l - target))
    return f"L{best}_{pooling}"

SYSTEM_PROMPT = (
    "You are a financial analyst. Answer the question using the provided filing "
    "excerpt. Think briefly step by step, then give the final numeric answer on "
    "its own last line in the exact format: ANSWER: <number>"
)

_NUM_RE = re.compile(r"-?\$?\(?\d[\d,]*\.?\d*\)?%?")
_PURE_NUM_RE = re.compile(r"^-?\$?\s?\(?\d[\d,]*\.?\d*\)?\s?(%|percent|million|billion|thousand)?$")


def is_pure_number(s: str) -> bool:
    """True if the gold answer is just a number (not a text span containing digits)."""
    return bool(_PURE_NUM_RE.match(s.strip()))


def parse_number(s: str):
    """Parse a numeric string like '-4.9%', '$(1,234.5)', '94' -> float, is_pct."""
    s = s.strip()
    m = _NUM_RE.search(s)
    if not m:
        return None, False
    tok = m.group(0)
    is_pct = tok.endswith("%")
    neg = "(" in tok
    tok = tok.strip("%").replace("$", "").replace("(", "").replace(")", "").replace(",", "")
    try:
        val = float(tok)
    except ValueError:
        return None, False
    if neg:
        val = -val
    return val, is_pct


# Explicit "the filing doesn't contain it" refusal phrasing. Canonical definition of an
# abstention, shared by the grader-side analysis and 17_abstention_robustness.py.
_ABSTAIN_RE = re.compile(
    r"cannot|can't|not provided|not include|does not|doesn't|unable|"
    r"insufficient|no information|not enough|not available|not given|not specified",
    re.IGNORECASE,
)


def is_abstention(output: str) -> bool:
    """True if the model declined rather than committing to a number: either it emitted
    no `ANSWER:` line, or the response contains explicit "not in the filing" refusal
    phrasing. Used to show the confident-stratum probe advantage is not refusal-reading."""
    if not output or not re.search(r"ANSWER:", output, flags=re.IGNORECASE):
        return True
    return bool(_ABSTAIN_RE.search(output))


def extract_final_answer(text: str):
    """Pull the model's final answer after the last 'ANSWER:' marker."""
    matches = re.findall(r"ANSWER:\s*(.+)", text, flags=re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    # fallback: last number in the last non-empty line
    lines = [l for l in text.strip().splitlines() if l.strip()]
    return lines[-1].strip() if lines else ""


def grade(pred_str: str, gold_str: str, rel_tol: float = 0.02) -> bool:
    """Numeric match with relative tolerance, forgiving scale-convention mismatches
    (percent vs decimal ×100, thousands/millions ×1000) but NOT sign flips.

    v2 after LLM-judge audit (2026-07-08): added ×1000 scales, dropped sign
    forgiveness (it excused genuinely wrong answers), tol 1% -> 2% (rounding)."""
    pred, _ = parse_number(pred_str)
    gold, _ = parse_number(gold_str)
    if pred is None or gold is None:
        return False

    def close(a, b):
        if b == 0:
            return abs(a) < 1e-6
        return abs(a - b) / max(abs(b), 1e-12) <= rel_tol

    return any(close(pred * s, gold) for s in (1.0, 100.0, 0.01, 1000.0, 0.001))
