#!/usr/bin/env python3

import socket
import sys
import argparse
import logging
from ipaddress import IPv4Network, AddressValueError
from time import sleep

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def scan_subnet(subnet, timeout=2.0, delay=0.1, verbose=False):
    """Perform reverse DNS lookup on all hosts in subnet.

    Args:
        subnet (str): Subnet in CIDR notation (e.g., '192.168.1.0/24')
        timeout (float): DNS query timeout in seconds
        delay (float): Delay between queries in seconds (rate limiting)
        verbose (bool): Enable verbose output for debugging

    Returns:
        None: Prints results to stdout
    """
    socket.setdefaulttimeout(timeout)

    try:
        net = IPv4Network(subnet)
    except (AddressValueError, ValueError) as e:
        logging.error(f"Invalid subnet format: {e}")
        sys.exit(1)

    logging.info(f"Scanning {subnet} ({net.num_addresses} addresses)")
    logging.info(f"Timeout: {timeout}s, Delay: {delay}s")

    found_count = 0
    total_count = 0

    for addr in net:
        total_count += 1
        try:
            # Single DNS lookup - store result to avoid duplicate queries
            hostname, aliases, ip_list = socket.gethostbyaddr(str(addr))

            print(f"{addr} -> {hostname}")
            print(f"IPs: {', '.join(ip_list)}")
            if aliases and verbose:
                print(f"Aliases: {', '.join(aliases)}")
            print("*" * 30)

            logging.info(f"Found: {addr} -> {hostname}")
            found_count += 1

        except socket.herror as e:
            # Host not found - expected for most IPs
            if verbose:
                logging.debug(f"{addr}: No reverse DNS entry (herror: {e})")
        except socket.gaierror as e:
            # Address-related error
            if verbose:
                logging.debug(f"{addr}: DNS resolution failed (gaierror: {e})")
        except OSError as e:
            # Network/system errors
            logging.error(f"{addr}: OS error - {e}")
        except Exception as e:
            # Unexpected errors - log for debugging
            logging.error(f"{addr}: Unexpected error - {type(e).__name__}: {e}")

        # Rate limiting to avoid overwhelming DNS servers or triggering IDS
        if delay > 0:
            sleep(delay)

    # Summary statistics
    logging.info(f"Scan complete: {found_count}/{total_count} hosts with reverse DNS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan subnet for hostnames via reverse DNS lookup",
        epilog="Example: %(prog)s 192.168.1.0/24"
    )
    parser.add_argument(
        "subnet",
        help="Subnet in CIDR notation (e.g., 192.168.1.0/24)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=2.0,
        help="DNS timeout in seconds (default: 2.0)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0.1,
        help="Delay between requests in seconds (default: 0.1)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (show failed lookups)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode (suppress logging, show only results)"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        scan_subnet(args.subnet, args.timeout, args.delay, args.verbose)
    except KeyboardInterrupt:
        logging.warning("\nScan interrupted by user")
        sys.exit(130)
    except Exception as e:
        logging.critical(f"Fatal error: {type(e).__name__}: {e}")
        sys.exit(1)
