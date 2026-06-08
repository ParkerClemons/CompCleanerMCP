import os
from pathlib import Path
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("compcleaner")

# scan_downloads will analyze all files within the downloads folder and look for files
# that haven't been modified in selected amount of days.
@mcp.tool()
def scan_downloads(cutoff_days: int, top_n: int):
    """
    Scans the user's Downloads folder for files that haven't been modified in X amount of days.
    
    Args:
        cutoff_days: The number of days to use as a cutoff for old files.
        top_n: The max number of results to return (default: 10)
    """

    # grabs the downloads path, today's date, and cutoff modified date for old files
    downloads_path = Path.home() / "Downloads"
    now = datetime.now() 
    cutoff_time = now - timedelta(days=cutoff_days)

    oldFiles = []

    # loop through download folder and checks each file's last modified date.
    # If the files last modified date is past the cutoff date, the files stats are put into a sorted List.
    # Issues I ran into : 
    # 1. at first considered using a dataclass to hold the stats of old files 
    # but changed it to dicts so data sizer will be smaller
    # 2. Limited how many of the old files returned by the tool to a selected amount to keep data smaller.
    for file in downloads_path.rglob("*"):
        # only looks into actual files
        if file.is_file():
            last_modified_time = datetime.fromtimestamp(file.stat().st_mtime)

            # if file has an old last modified date, the size in mb is calculated and the info appended to oldFiles list
            if last_modified_time < cutoff_time:
                size_mb = file.stat().st_size / (1024 * 1024)
                oldFiles.append({
                    "path": str(file.relative_to(downloads_path)),
                    "size_mb": round(size_mb, 2),
                    "modified_date": last_modified_time.strftime("%Y-%m-%d")
                })

    # sorts oldFiles by their modified date
    oldFiles.sort(key=lambda f: f["modified_date"])
    return oldFiles[:top_n]        

# main has to be below the function so the scan_download tool can actually run when mcp.run is called
def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()