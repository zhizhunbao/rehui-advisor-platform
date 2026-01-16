---
inclusion: fileMatch
fileMatchPattern: "**/scripts/discover/**"
---

# Resource Discovery & Evaluation

## Core Classes

- `DomainDiscoverScript` - Base class for domain discovery scripts
- `DataSource` - Abstract base for data sources (GitHub, HackerNews, Reddit)
- `QualityEvaluator` - Scores URLs by source trust, relevance, freshness, activity

## Creating a Discover Script

```python
from scripts.discover.base import DomainDiscoverScript
from scripts.discover.sources.github import GitHubSource

class DiscoverMyDomainScript(DomainDiscoverScript):
    NAME = "discover_my_domain"
    DOMAIN_CODE = "my_domain"  # Must match tags.py domain_code
    MIN_QUALITY_SCORE = 60.0

    @property
    def KEYWORDS(self) -> list[str]:
        return ["keyword1", "keyword2"]

    def _init_sources(self) -> None:
        self.SOURCES = [GitHubSource(verbose=self.verbose, min_stars=300)]
```

Run: `uv run python -m scripts.discover.core.discover_my_domain`

## Key Files

| Path                  | Purpose                            |
| --------------------- | ---------------------------------- |
| `discover/base.py`    | Base classes and quality evaluator |
| `discover/core/`      | Domain-specific discover scripts   |
| `discover/sources/`   | Data source implementations        |
| `discover/raw_data/`  | Output files (`raw_*.py`)          |
| `discover/evaluate/`  | LLM and RAG benchmark code         |
| `data/domain/tags.py` | Domain codes and keywords          |

## Workflow

1. Check `tags.py` for existing domain_code
2. Add tags if needed
3. Create/update discover script with KEYWORDS
4. Run discovery, review `raw_data/raw_*.py` output
5. Adjust MIN_QUALITY_SCORE or keywords as needed

## Quality Scoring

Weights: source (30%), relevance (30%), freshness (20%), activity (20%)

- GitHub: stars boost score (100+ → +10, 500+ → +15, 1000+ → +20)
- HackerNews: points boost similarly
- Items without matching tags are filtered out

## Evaluation (LLM/RAG)

For benchmarking providers or frameworks, see `discover/evaluate/`:

- Inherit `LLMProvider` or `RAGFramework`
- Implement required methods
- Run: `uv run python -m scripts.discover.evaluate.llm.run_benchmark`

**For detailed guide:** See `backend/scripts/data/skills/dev-resource_discovery/SKILL.md`
