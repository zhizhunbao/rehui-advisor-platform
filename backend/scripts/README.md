# Backend Scripts

Internal development and data management scripts for the Rehui Advisor platform.

## Overview

This directory contains scripts for:

- **Resource Discovery**: Finding and evaluating AI tools/frameworks
- **Skill Generation**: Creating and managing Claude skills
- **Data Management**: Domain data, prompts, and initial data
- **Benchmarking**: LLM and RAG performance evaluation

## Directory Structure

```
backend/scripts/
├── base.py                 # Base classes for all scripts
├── discover/               # Resource discovery scripts
│   ├── base.py            # Discovery base classes
│   ├── core/              # Domain-specific discovery
│   ├── sources/           # Data sources (GitHub, HN, Reddit)
│   ├── evaluate/          # LLM/RAG benchmarking
│   └── raw_data/          # Discovery output files
├── generate/               # Skill and prompt generation
│   ├── create_skill.py
│   ├── create_ai_learning_skills.py
│   ├── create_skills_from_domains.py
│   └── extract_prompts.py
├── data/                   # Data files and definitions
│   ├── domain/            # Domain definitions
│   ├── skills/            # Generated skills
│   ├── prompts/           # Prompt templates
│   ├── initial/           # Initial data scripts
│   └── benchmark/         # Benchmark data
└── sync/                   # Data synchronization
```

## Quick Start

### Resource Discovery

Discover AI resources from multiple sources:

```bash
cd backend/scripts

# Discover AI agents
python -m discover.core.discover_ai_agents

# Discover LLM models
python -m discover.core.discover_ai_llm_models

# Discover RAG frameworks
python -m discover.core.discover_ai_rag_frameworks
```

**Output:** `discover/raw_data/raw_<domain>.py`

### Skill Generation

Create new skills programmatically:

```bash
# Create AI learning skills
python -m generate.create_ai_learning_skills

# Create skills from domains
python -m generate.create_skills_from_domains

# Extract prompts from sources
python -m generate.extract_prompts
```

**Output:** `data/skills/<category>-<domain>/`

### Data Management

Initialize or update data:

```bash
# Initialize domain data
python -m data.initial.domain.init_domains

# Sync skills to database
python -m sync.sync_skills
```

## Script Categories

### 1. Discovery Scripts (`discover/`)

Find and evaluate resources from external sources.

**Key Scripts:**

- `discover_ai_agents.py` - AI agent frameworks
- `discover_ai_llm_models.py` - Open-source LLMs
- `discover_ai_llm_providers.py` - LLM API providers
- `discover_ai_rag_frameworks.py` - RAG tools
- `discover_ai_vector_databases.py` - Vector DBs
- `discover_ai_prompts.py` - Prompt libraries
- `discover_ai_skills.py` - Claude skills

**Data Sources:**

- GitHub (stars, activity, language)
- HackerNews (points, comments)
- Reddit (upvotes, discussions)

**Quality Scoring:**

- Source trust (30%)
- Relevance (30%)
- Freshness (20%)
- Activity (20%)

**See:** `data/skills/dev-resource_discovery/scripts/README.md`

### 2. Generation Scripts (`generate/`)

Create skills and prompts programmatically.

**Key Scripts:**

- `create_skill.py` - Create individual skills
- `create_ai_learning_skills.py` - Generate learning assistants
- `create_skills_from_domains.py` - Batch skill creation
- `extract_prompts.py` - Extract prompts from sources

**Output:**

- Skills: `data/skills/<category>-<domain>/`
- Prompts: `data/prompts/<category>-<name>/`

**See:** `data/skills/ai-skills/scripts/README.md`

### 3. Data Scripts (`data/`)

Manage domain definitions, skills, and prompts.

**Subdirectories:**

- `domain/` - Domain, category, tag definitions
- `skills/` - All generated skills (100+ skills)
- `prompts/` - Prompt templates by category
- `initial/` - Database initialization scripts
- `benchmark/` - Benchmark test data

**Key Files:**

- `domain/domains.py` - Domain definitions
- `domain/categories.py` - Category definitions
- `domain/tags.py` - Tag definitions
- `domain/skills.py` - Skill metadata

### 4. Evaluation Scripts (`discover/evaluate/`)

Benchmark LLM providers and RAG frameworks.

**LLM Evaluation:**

```bash
python -m discover.evaluate.llm.run_benchmark
```

**RAG Evaluation:**

```bash
python -m discover.evaluate.rag.run_benchmark
```

**Metrics:**

- Response quality
- Latency
- Cost
- Accuracy

### 5. Sync Scripts (`sync/`)

Synchronize data between files and database.

```bash
python -m sync.sync_skills
python -m sync.sync_prompts
```

## Base Classes

### ScriptBase

Base class for all scripts:

```python
from scripts.base import ScriptBase, ScriptResult

class MyScript(ScriptBase):
    NAME = "my_script"
    DESCRIPTION = "Script description"

    def run(self) -> ScriptResult:
        # Implementation
        return ScriptResult(
            success=True,
            message="Completed",
            created=5,
            updated=2
        )
```

### DomainDiscoverScript

Base class for discovery scripts:

```python
from scripts.discover.base import DomainDiscoverScript

class DiscoverMyDomain(DomainDiscoverScript):
    NAME = "discover_my_domain"
    DOMAIN_CODE = "my_domain"
    MIN_QUALITY_SCORE = 60.0

    @property
    def KEYWORDS(self) -> list[str]:
        return ["keyword1", "keyword2"]

    def _init_sources(self) -> None:
        self.SOURCES = [GitHubSource(min_stars=300)]
```

## Configuration

### Environment Variables

```bash
# GitHub API (for discovery)
GITHUB_TOKEN=your_token_here

# Database (for sync)
DATABASE_URL=postgresql://...
```

### Script Settings

Edit script constants:

```python
# Discovery
MIN_QUALITY_SCORE = 60.0  # Quality threshold
MIN_STARS = 300           # GitHub stars filter

# Generation
SKILLS_DATA_DIR = Path("data/skills")
PROMPTS_DATA_DIR = Path("data/prompts")
```

## Common Tasks

### Add a New Domain

1. Add to `data/domain/domains.py`:

```python
{
    "code": "my_domain",
    "name": "My Domain",
    "name_en": "My Domain",
    "category_code": "category",
    "description": "Description"
}
```

2. Add tags to `data/domain/tags.py`
3. Create discovery script in `discover/core/`
4. Run discovery and generation

### Create a New Skill

```python
from scripts.generate.create_skill import CreateSkillScript

script = CreateSkillScript(verbose=True)
result = script.create(
    name="category-domain",
    description="Description with use cases",
    instructions="Detailed instructions",
    keywords=["keyword1", "keyword2"]
)
```

### Update Skill Documentation

Skills are documented in:

- `data/skills/<skill-name>/SKILL.md` - Main definition
- `data/skills/<skill-name>/references/` - Detailed guides
- `data/skills/<skill-name>/scripts/` - Utility scripts

### Run Benchmarks

```bash
# LLM providers
python -m discover.evaluate.llm.run_benchmark

# RAG frameworks
python -m discover.evaluate.rag.run_benchmark

# View results
cat discover/evaluate/results/benchmark_results.json
```

## Development Workflow

1. **Discover Resources**

   ```bash
   python -m discover.core.discover_<domain>
   ```

2. **Review Output**

   ```bash
   cat discover/raw_data/raw_<domain>.py
   ```

3. **Generate Skills**

   ```bash
   python -m generate.create_skills_from_domains
   ```

4. **Validate Skills**

   ```bash
   # Check SKILL.md format
   # Verify metadata.json
   # Test with skills-manager
   ```

5. **Sync to Database**
   ```bash
   python -m sync.sync_skills
   ```

## Testing

```bash
# Run all tests
pytest backend/scripts/tests/

# Test specific script
pytest backend/scripts/tests/test_discover.py

# Test with verbose output
pytest -v backend/scripts/tests/
```

## Troubleshooting

### Discovery Issues

**No results found:**

- Lower `MIN_QUALITY_SCORE`
- Add more keywords
- Check data source availability

**Rate limiting:**

- Add GitHub token
- Reduce `max_results`
- Add delays between requests

### Generation Issues

**Skill not created:**

- Check domain exists in `domains.py`
- Verify category_code is valid
- Ensure name follows format: `category-domain`

**Invalid SKILL.md:**

- Check front matter format
- Verify description includes use cases
- Ensure instructions are clear

### Sync Issues

**Database connection failed:**

- Check DATABASE_URL
- Verify database is running
- Check network connectivity

**Data conflicts:**

- Review existing data
- Use `--force` flag to overwrite
- Check for duplicate names

## Dependencies

```bash
# Core dependencies
uv add requests beautifulsoup4 python-dateutil pyyaml

# Database (for sync)
uv add psycopg2-binary sqlalchemy

# Testing
uv add --dev pytest pytest-asyncio
```

## Related Documentation

- **Resource Discovery**: `data/skills/dev-resource_discovery/scripts/README.md`
- **Skill Generation**: `data/skills/ai-skills/scripts/README.md`
- **Code Standards**: `data/skills/dev-code_standards/SKILL.md`
- **API Documentation**: `docs/backend-templates.md`

## Contributing

When adding new scripts:

1. Inherit from `ScriptBase` or `DomainDiscoverScript`
2. Add clear NAME and DESCRIPTION
3. Implement `run()` method
4. Return `ScriptResult`
5. Add tests in `tests/`
6. Update this README

## License

Internal use only - Part of Rehui Advisor platform.
