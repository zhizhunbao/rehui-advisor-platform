#!/usr/bin/env python
# 统一入口脚本
import asyncio
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <scraper> [options]")
        print("Scrapers: brightspace (bs)")
        return
    
    scraper = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    
    if scraper in ("brightspace", "bs"):
        from scrapers.brightspace.scraper import main as bs_main
        asyncio.run(bs_main())
    else:
        print(f"Unknown scraper: {scraper}")
        print("Available: brightspace (bs)")


if __name__ == "__main__":
    main()
