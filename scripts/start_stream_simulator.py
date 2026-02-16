"""
Simulate a live stream of security events.

Reads data/sample_logs.csv and gradually appends rows to data/live_stream.csv.
Run this in a separate terminal:

    python scripts/start_stream_simulator.py --delay 0.5 --chunk-size 10
"""

import argparse
import time
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delay", type=float, default=0.5,
        help="Seconds between batches (default: 0.5)",
    )
    parser.add_argument(
        "--chunk-size", type=int, default=10,
        help="Number of events to append per batch (default: 10)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    sample_path = root / "data" / "sample_logs.csv"
    live_path = root / "data" / "live_stream.csv"

    if not sample_path.exists():
        raise FileNotFoundError(
            f"{sample_path} not found. Run 'python scripts/generate_dataset.py' first."
        )

    print(f"Loading full dataset from: {sample_path}")
    df = pd.read_csv(sample_path)

    # Sort by timestamp if possible
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp")
    else:
        df = df.sort_index()

    # Reset live stream file
    if live_path.exists():
        live_path.unlink()
    print(f"Starting new live stream file at: {live_path}")

    header_written = False

    total = len(df)
    print(f"Total events to stream: {total}")
    print(f"Chunk size: {args.chunk_size}, delay: {args.delay}s\n")

    start_idx = 0
    while start_idx < total:
        end_idx = min(start_idx + args.chunk_size, total)
        batch = df.iloc[start_idx:end_idx]

        mode = "a"
        header = not header_written
        batch.to_csv(live_path, mode=mode, header=header, index=False)
        header_written = True

        print(f"Appended rows {start_idx}–{end_idx - 1} "
              f"({end_idx}/{total} total)")
        start_idx = end_idx

        time.sleep(args.delay)

    print("\n✅ Streaming complete. All events have been written to live_stream.csv")


if __name__ == "__main__":
    main()
