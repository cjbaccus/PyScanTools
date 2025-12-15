# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyScanTools is a collection of Python utilities for network scanning and host discovery on subnets. This is a security/network administration tool intended for authorized network reconnaissance.

## Current Tools

### PyHost.py
A production-grade network scanning script that performs reverse DNS lookups on subnet hosts with proper error handling, logging, and rate limiting.

**Usage:**
```bash
./PyHost.py <subnet> [options]

# Basic scan
./PyHost.py 192.168.3.0/24

# Custom timeout and delay
./PyHost.py 192.168.1.0/24 -t 5.0 -d 0.5

# Verbose mode (show all failed lookups)
./PyHost.py 10.0.0.0/24 -v

# Quiet mode (results only, no logging)
./PyHost.py 172.16.0.0/24 -q

# Help
./PyHost.py --help
```

**Command-line Options:**
- `-t, --timeout`: DNS query timeout in seconds (default: 2.0)
- `-d, --delay`: Delay between queries for rate limiting (default: 0.1)
- `-v, --verbose`: Show failed DNS lookups and debug information
- `-q, --quiet`: Suppress logging, show only results

**Implementation Details:**
- **Input Validation**: Uses `argparse` for robust argument parsing with help text
- **Error Handling**: Specific exception handling for `socket.herror`, `socket.gaierror`, and `OSError`
- **Performance**: Single DNS lookup per host (stores result to avoid duplicate queries)
- **Timeout Protection**: Configurable DNS timeout prevents hanging on unresponsive hosts
- **Rate Limiting**: Configurable delay between requests to avoid overwhelming DNS servers or triggering IDS
- **Logging**: Structured logging with timestamps for audit trails and debugging
- **Statistics**: Provides summary of successful lookups vs total hosts scanned
- **Graceful Exit**: Proper handling of `KeyboardInterrupt` (Ctrl+C)
- **Output Format**:
  - IP address -> hostname
  - Associated IP addresses
  - Optional aliases (in verbose mode)
  - 30-character separator line

## Development Notes

### Python Environment
- Standard library only (no external dependencies)
- Requires Python 3.6+ for f-strings and `ipaddress` module
- Uses shebang: `#!/usr/bin/env python3`
- PEP 8 compliant code formatting

### Running Scripts
All scripts are executable and can be run directly:
```bash
./PyHost.py <arguments>
```

Or via Python interpreter:
```bash
python PyHost.py <arguments>
```

### Security Context
This is a network reconnaissance tool. When modifying or extending:
- Ensure code is used only for authorized security testing, network administration, or educational purposes
- **Current security features implemented:**
  - Specific exception handling (no bare `except` clauses)
  - Input validation to prevent injection attacks
  - Configurable timeouts to prevent DoS conditions
  - Rate limiting to avoid triggering IDS/IPS
  - Structured logging for compliance and audit trails
  - Graceful error handling that doesn't leak system information
- All scans should be authorized and documented
- Consider network impact when scanning large subnets
- to memorize