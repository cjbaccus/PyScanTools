# PyScanTools

A collection of Python utilities for network scanning and host discovery on subnets. These tools are intended for authorized network reconnaissance, security testing, and network administration.

## Scripts

### PyHost.py

A production-grade network scanning script that performs reverse DNS lookups on subnet hosts with proper error handling, logging, and rate limiting.

#### What It Does

PyHost.py scans all hosts in a given subnet and performs reverse DNS lookups to discover hostnames. It provides:
- Reverse DNS resolution for all IP addresses in a subnet
- Configurable timeout and rate limiting
- Detailed logging with timestamps
- Statistics on successful lookups vs total hosts scanned
- Graceful error handling and Ctrl+C support

#### Usage


```bash
./PyHost.py <subnet> [options]
```

**Examples:**

```bash
# Basic scan
./PyHost.py 192.168.3.0/24

# Custom timeout and delay
./PyHost.py 192.168.1.0/24 -t 5.0 -d 0.5

# Verbose mode (show all failed lookups)
./PyHost.py 10.0.0.0/24 -v

# Quiet mode (results only, no logging)
./PyHost.py 172.16.0.0/24 -q

# Export results to markdown table
./PyHost.py 192.168.1.0/24 -e results.md

# Scan with export and custom settings
./PyHost.py 10.0.0.0/24 -t 5.0 -v -e network_scan.md

# Help
./PyHost.py --help
```

#### Command-line Options

- `-t, --timeout`: DNS query timeout in seconds (default: 2.0)
- `-d, --delay`: Delay between queries for rate limiting (default: 0.1)
- `-v, --verbose`: Show failed DNS lookups and debug information
- `-q, --quiet`: Suppress logging, show only results
- `-e, --export FILE`: Export results to markdown table file

#### Features

- **Input Validation**: Robust argument parsing with help text
- **Error Handling**: Specific exception handling for DNS errors
- **Performance**: Single DNS lookup per host with result caching
- **Timeout Protection**: Configurable DNS timeout prevents hanging
- **Rate Limiting**: Configurable delay to avoid overwhelming DNS servers
- **Structured Logging**: Timestamps for audit trails and debugging
- **Statistics**: Summary of successful lookups vs total hosts scanned
- **Export to Markdown**: Generate markdown tables with IP addresses and DNS names
- **Graceful Exit**: Proper Ctrl+C handling

#### Export Format

When using the `-e` option, results are exported to a markdown table file:

```markdown
| IP Address | DNS Name |
|------------|----------|
| 192.168.1.1 | router.local |
| 192.168.1.10 | workstation.local |
| 192.168.1.50 | server.local |
```

This format is easy to view in markdown-compatible applications and can be imported into documentation, reports, or other analysis tools.

#### Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

#### Running the Script

Make executable and run directly:
```bash
chmod +x PyHost.py
./PyHost.py <arguments>
```

Or via Python interpreter:
```bash
python3 PyHost.py <arguments>
```

## Security Context

These tools are for authorized network reconnaissance only. Ensure you have proper authorization before scanning any network. Features include rate limiting to avoid triggering IDS/IPS systems and structured logging for compliance and audit trails.
