import argparse
import datetime
from pathlib import Path

from stats import calculate_top


parser = argparse.ArgumentParser(description="Calculate stats")
parser.add_argument("--tsv-file-path", type=Path, required=True)
parser.add_argument("--top-size", type=int, required=True)
parser.add_argument("--start-date", type=datetime.date.fromisoformat, required=True)
parser.add_argument("--end-date", type=datetime.date.fromisoformat, required=True)
parser.add_argument(
    "--stats-by", type=str, required=True, choices=["clicks", "shows"],
)


def main():
    arguments = parser.parse_args()
    top = calculate_top(
        arguments.tsv_file_path,
        arguments.start_date,
        arguments.end_date,
        arguments.stats_by,
        arguments.top_size,
    )
    for x in top:
        print(f"{x.company}\t{x.value}")


if __name__ == "__main__":
    main()
