import argparse
import sys
import json
import readline  # For better input handling
from typing import Optional, Dict, Any
from datetime import datetime
from sports_agent import SportsAgent

# ANSI color codes for better CLI output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_response(response: str, output_format: str = 'text') -> str:
    """Format the response based on the output format"""
    if output_format == 'json':
        try:
            # If response is already JSON, parse and pretty print
            json_response = json.loads(response)
            return json.dumps(json_response, indent=2)
        except json.JSONDecodeError:
            # If not JSON, wrap in a JSON object
            return json.dumps({"response": response}, indent=2)
    return response

def interactive_mode(agent: SportsAgent, output_format: str = 'text') -> None:
    """Run the CLI in interactive mode"""
    print(f"{Colors.HEADER}Sports Agent CLI (Interactive Mode){Colors.ENDC}")
    print(f"Type {Colors.CYAN}exit{Colors.ENDC} or press {Colors.CYAN}Ctrl+C{Colors.ENDC} to quit\n")
    
    while True:
        try:
            query = input(f"{Colors.BLUE}❯ {Colors.ENDC}")
            
            if query.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
                
            if not query.strip():
                continue
                
            response = agent.respond(query)
            print(f"\n{format_response(response, output_format)}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        prog="sports-agent",
        description="Sports Agent CLI - Get sports information and analysis",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main arguments
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Sports query text (leave empty for interactive mode)",
        default=None
    )
    
    # Optional arguments
    parser.add_argument(
        "-p", "--provider",
        type=str,
        choices=["rule", "openai", "gemini"],
        default="rule",
        help="AI provider to use"
    )
    
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=None,
        help="Model to use (provider-specific)"
    )
    
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        agent = SportsAgent(provider=args.provider, model=args.model)
        
        # Interactive mode if no query provided
        if not args.query:
            interactive_mode(agent, args.format)
            return
            
        # Single query mode
        response = agent.respond(args.query.strip())
        print(format_response(response, args.format))
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
