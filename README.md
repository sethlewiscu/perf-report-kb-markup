# Performance Report KB Article

This repository contains the cleaned-up HTML source for the **"Investigating + Creating the Report"** knowledge base article. The document is an SOP for Technical Support, covering how to identify, troubleshoot, and create performance reports.

The HTML was originally exported from ClickUp and has been stripped of proprietary markup, leaving clean semantic HTML that can be edited and maintained by hand.

## Repository contents

| File | Purpose |
|---|---|
| `Investigating + Creating the Report.html` | The KB article (semantic HTML) |
| `cleanup.py` | Script used to strip ClickUp/Quill markup |
| `wrap_sections.py` | Script used to wrap content in section divs |
| `fix_img_li.py` | Script used to fix image/list formatting |
| `CLAUDE.md` | Cleanup rules reference for AI-assisted editing |

## How to clone, edit, and update

### 1. Clone the repository

```bash
git clone https://github.com/sethlewiscu/perf-report-kb-markup.git
cd perf-report-kb-markup
```

### 2. Create a branch for your changes

```bash
git checkout -b your-branch-name
```

### 3. Edit the HTML file

Open `Investigating + Creating the Report.html` in any text editor or IDE. The file is plain semantic HTML — no build step or framework is needed.

You can preview your changes by opening the file directly in a browser.

### 4. Stage and commit your changes

```bash
git add "Investigating + Creating the Report.html"
git commit -m "Brief description of what you changed"
```

### 5. Push your branch and open a pull request

```bash
git push -u origin your-branch-name
```

Then open a pull request on GitHub from your branch into `main`.

### 6. After your PR is merged

Switch back to `main` and pull the latest changes:

```bash
git checkout main
git pull
```
