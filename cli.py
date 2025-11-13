import argparse
import sys
from sports_agent import SportsAgent


def main():
    parser = argparse.ArgumentParser(prog="sports-agent", add_help=True)
    parser.add_argument("-q", "--query", type=str, help="Sports query text")
    parser.add_argument("-p", "--provider", type=str, choices=["rule", "openai"], default="rule")
    parser.add_argument("-m", "--model", type=str, default=None)
    args = parser.parse_args()

    agent = SportsAgent(provider=args.provider, model=args.model)

    if args.query:
        prompt = args.query
    else:
        print("Enter your sports query, then press Ctrl+D (Unix) or Ctrl+Z Enter (Windows):", file=sys.stderr)
        prompt = sys.stdin.read()

    prompt = prompt.strip()
    if not prompt:
        print("No query provided.")
        sys.exit(1)

    out = agent.respond(prompt)
    print(out)


if __name__ == "__main__":
    main()
