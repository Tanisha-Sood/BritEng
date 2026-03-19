import argparse
import csv
import json
import os
import time
from datetime import datetime

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from assistant import process_input


def load_benchmark_data(file_path="data/benchmark.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_invoke_process(input_text: str, mode: str):
    """
    Call user's existing process_input() and capture exceptions.
    Returns (model_output, error_msg). If successful, error_msg is None.
    """
    try:
        output = process_input(input_text, mode=mode)
        return output if output is not None else "", None
    except Exception as e:
        return "", str(e)


def compute_bleu(reference: str, hypothesis: str):
    """
    Compute sentence BLEU with smoothing. Returns float between 0 and 1.
    """
    smoothie = SmoothingFunction().method4
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    # If hypothesis is empty, BLEU will be 0.
    if len(hyp_tokens) == 0:
        return 0.0
    try:
        score = sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)
        return float(score)
    except Exception:
        return 0.0


def evaluate_and_save(
    benchmark_path="data/benchmark.json",
    mode="grammar and spelling correction",
    out_dir="evaluation_results",
):
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(out_dir, f"results_{timestamp}.csv")
    summary_path = os.path.join(out_dir, f"summary_{timestamp}.json")

    data = load_benchmark_data(benchmark_path)
    total = len(data)
    bleu_scores = []
    exact_matches = 0
    rows = []

    for idx, sample in enumerate(data, start=1):
        input_text = sample.get("input", "")
        expected = sample.get("expected", "")

        model_output, err = safe_invoke_process(input_text, mode=mode)

        bleu = compute_bleu(expected, model_output)
        bleu_scores.append(bleu)

        exact_match = (
            1
            if model_output.strip().lower() == expected.strip().lower() and err is None
            else 0
        )
        exact_matches += exact_match

        row = {
            "id": idx,
            "input": input_text,
            "expected": expected,
            "model_output": model_output,
            "bleu": round(bleu, 6),
            "exact_match": exact_match,
            "error": err if err is not None else "",
        }
        rows.append(row)

        # Print progress 
        print(
            f"[{idx}/{total}] BLEU={row['bleu']:.4f} ExactMatch={row['exact_match']} Error={bool(err)}"
        )

    avg_bleu = sum(bleu_scores) / total if total > 0 else 0.0
    accuracy = (exact_matches / total) * 100 if total > 0 else 0.0

    # Save CSV
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = [
            "id",
            "input",
            "expected",
            "model_output",
            "bleu",
            "exact_match",
            "error",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # Save summary
    summary = {
        "timestamp": timestamp,
        "benchmark_path": os.path.abspath(benchmark_path),
        "mode": mode,
        "total_samples": total,
        "exact_matches": exact_matches,
        "accuracy_percent": round(accuracy, 4),
        "average_bleu": round(avg_bleu, 6),
        "csv_path": os.path.abspath(csv_path),
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Final print
    print("\n--- Evaluation Summary ---")
    print(f"Samples evaluated : {total}")
    print(f"Exact matches     : {exact_matches}")
    print(f"Accuracy (%)      : {summary['accuracy_percent']}")
    print(f"Average BLEU      : {summary['average_bleu']}")
    print(f"Results CSV       : {summary['csv_path']}")
    print(f"Summary JSON      : {os.path.abspath(summary_path)}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate UK-Eng corrector and save CSV summary.")
    parser.add_argument(
        "--benchmark",
        type=str,
        default="data/benchmark.json",
        help="Path to benchmark JSON file (list of {input, expected}).",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="grammar and spelling correction",
        help="Mode to pass to process_input (e.g. 'grammar and spelling correction' or 'rephrase').",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="evaluation_results",
        help="Output folder for CSV and summary JSON.",
    )
    args = parser.parse_args()

    # small delay to ensure timestamp uniqueness if run quickly in succession
    time.sleep(0.1)
    evaluate_and_save(benchmark_path=args.benchmark, mode=args.mode, out_dir=args.out)
