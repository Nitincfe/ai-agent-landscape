# AI agent landscape

What kinds of AI agents are developers building? To find out, I took the project list in the README of [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects), pulled it into a CSV with Python, and sorted 112 entries into 12 categories.

## What I found

- About half of the entries, 54 of 112, are productivity/automation or software engineering tools.
- Healthcare, finance, retail and customer support have only 2 to 5 entries each.
- 28 of the 33 productivity entries are AutoGen or LangGraph examples. Part of that lead comes from framework tutorials, not independent projects.
- All healthcare and industrial entries are standalone projects, not framework examples.

![Projects per category](https://github.com/Nitincfe/ai-agent-landscape/blob/main/Images/readme_final.png)

![Framework split per category](https://github.com/Nitincfe/ai-agent-landscape/blob/main/Images/framework_final.png)

| Category | Projects |
|---|---|
| Productivity & Automation | 33 |
| Software Engineering & AI | 21 |
| Media & Entertainment | 14 |
| Business & Legal Services | 10 |
| Education & Research | 6 |
| Finance | 5 |
| Travel & Hospitality | 5 |
| Retail & Supply Chain | 5 |
| Industrial & Core | 4 |
| Healthcare | 4 |
| Sales & Marketing | 3 |
| Customer Support | 2 |

## Data

`projects.csv` has 112 entries extracted from the README tables of the source repo on October 11, 2026.

| Column | Meaning |
|---|---|
| name | Project name as listed |
| section | README section it came from |
| framework | Standalone, AutoGen, CrewAI, LangGraph or Agno |
| industry | Original industry label from the README (free text) |
| description | Short description from the README |
| url | Link to the project |

The 12 categories above are my own grouping of the original industry labels. The grouping is applied in `agents_deployment.py`.

## Files

| File | What it does |
|---|---|
| `agent_dataset.py` | Reads the source README and writes `projects.csv`. Also has an optional `enrich` step (see below). |
| `agents_deployment.py` | Reads `projects.csv`, groups industries into categories, and draws the charts. |
| `projects.csv` | The extracted data. |
| `Images/` | The charts used in my posts. |

## How to run

```
pip install requests pandas matplotlib
python agent_dataset.py extract
python agents_deployment.py
```

Optional: `python agent_dataset.py enrich` adds GitHub stars, forks and dates for each linked repo using the GitHub API. Set a `GITHUB_TOKEN` environment variable first to avoid rate limits. This step is untested against the live API, and most framework examples link to a folder inside a bigger repo, so they would all show the parent repo's stars.

## Limitations

- The source repo is titled "500+ AI Agent Projects", but its README tables list 112 entries, so that is what I analyzed. The 21 runnable agents in its `agents/` folder are not included.
- It is one person's curated list. It shows what is in this collection, not everything developers build.
- Counts are listed entries. They do not show adoption, quality or popularity.
- The categories are my own grouping, and categories with 2 to 5 entries are too small to rank against each other.
- I have not checked the license of each linked project.
- This is a snapshot from one date. The source repo changes over time.

## Credits and license

- Source data: [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) (MIT License).
- Code and category grouping: MIT License, Nitin. See `LICENSE`.
