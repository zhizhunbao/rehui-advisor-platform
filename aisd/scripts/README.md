# Scripts Directory

This directory contains utility scripts for the AISD project. Most scripts have been migrated to their corresponding skill directories for better organization.

## Migration Status

All scripts have been migrated to skill directories:

### ✅ Migrated to `backend/scripts/data/skills/`

#### dev-pdf_processing/scripts/

- `pdf_to_markdown.py` - PDF to markdown converter with image extraction
- `pdf_to_bilingual.py` - PDF to bilingual document converter
- `pdf_to_images.py` - PDF pages to images converter

#### dev-web_scraping/scripts/

- `scrape_medium.py` - Medium article scraper
- ~~`fetch_links.py`~~ - Batch link scraper (removed, use scrape_medium.py)

#### dev-code_standards/scripts/

- `organize_courses.py` - Course directory standardization tool

## Remaining Structure

```
aisd/scripts/
├── organizers/          # Empty (migrated)
├── scrapers/
│   └── brightspace/     # Brightspace course scraper (complex, kept in place)
└── README.md            # This file
```

## Brightspace Scraper

The Brightspace scraper remains in `scrapers/brightspace/` due to its complexity and dependencies on local configuration files. It includes:

- Session management
- Course content scraping
- File downloads
- Link extraction
- HTML cleanup tools

To use the Brightspace scraper, see `scrapers/brightspace/README.md` (if available) or check the script documentation.

## Using Migrated Scripts

All migrated scripts can now be found in their respective skill directories:

```bash
# PDF processing
cd backend/scripts/data/skills/dev-pdf_processing/scripts/
python pdf_to_markdown.py input.pdf output.md

# Web scraping
cd backend/scripts/data/skills/dev-web_scraping/scripts/
python scrape_medium.py https://medium.com/article-url

# Code standards
cd backend/scripts/data/skills/dev-code_standards/scripts/
python organize_courses.py --course rl --execute
```

## Benefits of Migration

1. **Better Organization**: Scripts are grouped by their functional domain
2. **Skill Integration**: Scripts are now part of the skill system
3. **Documentation**: Each skill has comprehensive documentation
4. **Discoverability**: Easier to find relevant scripts through skills
5. **Reusability**: Scripts can be referenced in skill workflows
