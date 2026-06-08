import os
from pathlib import Path
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("compcleaner")

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

def scan_downloads(cutoff_days: int):
    """Scan the user's Downloads folder for files older than n amount of days.
    
    Args:
        cutoff_days: The number of days to use as a cutoff for old files.
    """

    downloads_path = Path.home() / "Downloads"
    now = datetime.now() 
    cutoff_time = now - timedelta(days=cutoff_days)

    for file in downloads_path.iterdir():
        if file.is_file():
            last_modified_time = datetime.fromtimestamp(file.stat().st_mtime)
            if last_modified_time < cutoff_time:
                print(f"Old file found: {file} (Last modified: {last_modified_time})")
