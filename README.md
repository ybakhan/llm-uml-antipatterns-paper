# LLM-Based Antipattern Detection in UML Use Case Models

ACM SIGCONF paper submitted to MODELS 2026 NIER track.

## Dependencies

- **TeX Live** (BasicTeX is sufficient): `brew install --cask basictex`
- **pandoc** (for `.md`/`.docx` exports): `brew install pandoc`

After installing BasicTeX, install the required LaTeX packages:

```sh
sudo tlmgr update --self
sudo tlmgr install hyperxmp ncctools enumitem inconsolata newtx libertine \
                   txfonts fontaxes mweights kastrup preprint lastpage
```

## Rendering

| Command | Output |
|---|---|
| `make` | PDF, Markdown, and Word (.docx) |
| `make llm-uml-antipatterns.pdf` | PDF only |
| `make clean` | Remove build artefacts (keeps PDF) |
| `make cleanall` | Remove build artefacts and PDF |

The PDF is the authoritative formatted version (two-column ACM SIGCONF layout). The `.docx` and `.md` are single-column exports for sharing and editing.

## Review mode

The document is currently compiled with `review` and `anonymous` options, which add red line numbers and suppress author names for double-blind review. Remove these from the `\documentclass` line before submitting the camera-ready version:

```latex
% review submission
\documentclass[sigconf,review,anonymous]{acmart}

% camera-ready
\documentclass[sigconf]{acmart}
```
