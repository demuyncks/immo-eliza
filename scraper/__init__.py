"""
Scraping Module for Immo-Eliza.

This package contains the core intelligence units for data collection:
- crawler: Responsible for discovery of property URLs across Belgian regions.
- scraper: Handles multi-threaded extraction of property features and financial data.

Usage:
    from scraping.crawler import generate_pages_urls
    from scraping.scraper import run_optimized_scraping
"""
