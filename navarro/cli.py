"""
Navarro CLI - Command line interface for the OSINT username checker.

Usage:
    navarro <username>
    navarro -l usernames.txt
    navarro <username> --platforms github,reddit,telegram
    navarro <username> -q -e results.json
"""
import argparse
import json
import sys
import time
import random
from datetime import datetime
from typing import Optional

from navarro import (
    __version__,
    CheckResult,
    RateLimiter,
    SessionManager,
    validate_username,
    get_all_checkers,
    list_platforms,
    PLATFORM_REGISTRY,
)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def display_results(username: str, results: dict, quiet: bool = False) -> dict:
    """Display check results and return stats."""
    stats = {
        CheckResult.FOUND: 0,
        CheckResult.NOT_FOUND: 0,
        CheckResult.NETWORK_ERROR: 0,
        CheckResult.RATE_LIMITED: 0,
        CheckResult.TIMEOUT: 0,
        CheckResult.UNKNOWN_ERROR: 0,
    }
    
    found_profiles = {}
    
    for platform, result in results.items():
        stats[result] += 1
        if result == CheckResult.FOUND:
            checker = PLATFORM_REGISTRY.get(platform)
            if checker:
                found_profiles[platform] = checker.get_profile_url(username)
    
    if RICH_AVAILABLE and not quiet:
        console = Console()
        table = Table(title=f"Results for @{username}")
        table.add_column("Platform", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Profile URL", style="blue")
        
        for platform, result in sorted(results.items()):
            if result == CheckResult.FOUND:
                url = found_profiles.get(platform, "")
                table.add_row(platform, "✅ FOUND", url)
            elif not quiet:
                status_map = {
                    CheckResult.NOT_FOUND: ("❌ Not Found", "dim"),
                    CheckResult.NETWORK_ERROR: ("⚠️ Network Error", "yellow"),
                    CheckResult.RATE_LIMITED: ("🚫 Rate Limited", "red"),
                    CheckResult.TIMEOUT: ("⏱️ Timeout", "yellow"),
                    CheckResult.UNKNOWN_ERROR: ("❓ Unknown", "dim"),
                }
                status, style = status_map.get(result, ("?", "dim"))
                if not quiet:
                    table.add_row(f"[{style}]{platform}[/{style}]", f"[{style}]{status}[/{style}]", "")
        
        console.print(table)
        console.print(f"\n📊 Summary: {stats[CheckResult.FOUND]} found, {stats[CheckResult.NOT_FOUND]} not found")
    elif quiet:
        # Quiet mode: only show found profiles
        for platform, url in found_profiles.items():
            print(f"{platform}: {url}")
    else:
        # No rich, standard output
        print(f"\n{'='*50}")
        print(f"Results for @{username}")
        print(f"{'='*50}")
        for platform, result in sorted(results.items()):
            if result == CheckResult.FOUND:
                url = found_profiles.get(platform, "")
                print(f"[+] {platform:12} : FOUND - {url}")
            else:
                print(f"[-] {platform:12} : {result.value}")
        print(f"\nSummary: {stats[CheckResult.FOUND]} found, {stats[CheckResult.NOT_FOUND]} not found")
    
    return {
        "stats": stats,
        "found_profiles": found_profiles,
    }


def check_username(
    username: str,
    platforms: Optional[list] = None,
    timeout: int = 8,
    quiet: bool = False,
) -> dict:
    """Check a username across platforms."""
    rate_limiter = RateLimiter()
    session_manager = SessionManager()
    
    checkers = get_all_checkers(rate_limiter, session_manager)
    
    # Filter platforms if specified
    if platforms:
        platforms_lower = [p.lower() for p in platforms]
        checkers = {k: v for k, v in checkers.items() if k.lower() in platforms_lower}
    
    results = {}
    
    if RICH_AVAILABLE and not quiet:
        console = Console()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Checking {len(checkers)} platforms...", total=len(checkers))
            
            for platform, checker in checkers.items():
                progress.update(task, description=f"Checking {platform}...")
                try:
                    results[platform] = checker.check(username)
                except Exception:
                    results[platform] = CheckResult.UNKNOWN_ERROR
                progress.advance(task)
    else:
        for platform, checker in checkers.items():
            if not quiet:
                print(f"Checking {platform}...", end="\r")
            try:
                results[platform] = checker.check(username)
            except Exception:
                results[platform] = CheckResult.UNKNOWN_ERROR
    
    return results


def export_json(data: dict, filepath: str) -> None:
    """Export results to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"📁 Results exported to {filepath}")


def export_csv(data: dict, filepath: str) -> None:
    """Export results to CSV file."""
    import csv
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Username', 'Platform', 'Status', 'Profile URL'])
        
        for username, user_data in data.items():
            results = user_data.get('results', {})
            found_profiles = user_data.get('found_profiles', {})
            
            for platform, status in results.items():
                url = found_profiles.get(platform, '')
                writer.writerow([username, platform, status, url])
    
    print(f"📁 Results exported to {filepath}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="🔍 Navarro - OSINT username checker for 26+ platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  navarro johndoe                          Check single username
  navarro -l users.txt                     Check list from file
  navarro johndoe --platforms github,reddit Filter platforms
  navarro johndoe -q -e results.json       Quiet mode + JSON export
  navarro --list-platforms                 Show available platforms
        """
    )
    
    parser.add_argument(
        "username",
        nargs="?",
        help="Username to search"
    )
    parser.add_argument(
        "--list", "-l",
        dest="list_file",
        help="File containing list of usernames (one per line)"
    )
    parser.add_argument(
        "--export", "-e",
        help="Export results to JSON file"
    )
    parser.add_argument(
        "--csv",
        help="Export results to CSV file"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode: only show found profiles"
    )
    parser.add_argument(
        "--platforms", "-p",
        help="Comma-separated list of platforms to check (e.g., github,reddit,telegram)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=8,
        help="Request timeout in seconds (default: 8)"
    )
    parser.add_argument(
        "--list-platforms",
        action="store_true",
        help="List available platforms and exit"
    )
    parser.add_argument(
        "--version", "-V",
        action="version",
        version=f"Navarro {__version__}"
    )
    
    args = parser.parse_args()
    
    # Handle --list-platforms
    if args.list_platforms:
        platforms = list_platforms()
        print(f"📋 Available platforms ({len(platforms)}):")
        for name in sorted(platforms):
            print(f"  • {name}")
        sys.exit(0)
    
    # Validate input
    if not args.username and not args.list_file:
        parser.print_help()
        sys.exit(1)
    
    # Parse platforms filter
    platforms_filter = None
    if args.platforms:
        platforms_filter = [p.strip() for p in args.platforms.split(',')]
        available = [p.lower() for p in list_platforms()]
        invalid = [p for p in platforms_filter if p.lower() not in available]
        if invalid:
            print(f"⚠️ Unknown platforms: {', '.join(invalid)}")
            print(f"   Use --list-platforms to see available options")
            sys.exit(1)
    
    if not args.quiet:
        print(f"\n🔍 Navarro v{__version__} - OSINT Username Checker")
    
    all_results = {}
    
    # Get list of usernames to check
    usernames = []
    if args.list_file:
        try:
            with open(args.list_file, 'r') as f:
                usernames = [line.strip().lstrip("@") for line in f if line.strip()]
            if not args.quiet:
                print(f"📋 Loaded {len(usernames)} usernames from {args.list_file}")
        except FileNotFoundError:
            print(f"❌ Error: File '{args.list_file}' not found")
            sys.exit(1)
    else:
        usernames = [args.username.strip().lstrip("@")]
    
    # Validate usernames
    for username in usernames:
        is_valid, error = validate_username(username)
        if not is_valid:
            print(f"❌ Invalid username '{username}': {error}")
            sys.exit(1)
    
    # Check each username
    for idx, username in enumerate(usernames):
        if len(usernames) > 1 and not args.quiet:
            print(f"\n{'='*50}")
            print(f"Checking username: {username}")
            # Add delay between usernames
            if idx > 0:
                delay = random.uniform(2, 5)
                print(f"⏳ Waiting {delay:.1f}s before next username...")
                time.sleep(delay)
        
        results = check_username(
            username,
            platforms=platforms_filter,
            timeout=args.timeout,
            quiet=args.quiet,
        )
        
        display_data = display_results(username, results, quiet=args.quiet)
        
        all_results[username] = {
            "timestamp": datetime.now().isoformat(),
            "results": {k: v.value for k, v in results.items()},
            "found_profiles": display_data["found_profiles"],
        }
    
    # Export if requested
    if args.export:
        export_json(all_results, args.export)
    
    if args.csv:
        export_csv(all_results, args.csv)


if __name__ == "__main__":
    main()
