# EvoApplications 2027 Paper Writing Guide

Live version with tickable checklists: https://claude.ai/artifact/1C9pr183XYzDapi5wddu4i
Dates and submission rules: EvoApplications 2027 Submission Plan, https://claude.ai/artifact/D6ByeoCTMs2HjsN7Wwz5Yj

## Overview

Write the paper locally on Xubuntu with TeX Live and VS Code, in the order below, and run the final checks before uploading to EasyChair on 14 November.

Sections 2, 4, 5, 6, 7 and 8 are drafted and in your voice (files in `paper/sections/`). Write the rest in this order, because the introduction and abstract summarise results you haven't written yet:

1. ~~Section 6, Experimental setup~~ (done 7 Nov)
2. ~~Section 7, Results~~ (done 7 Nov)
3. ~~Section 8, Discussion and threats to validity~~ (done 8 Nov)
4. ~~Cutting pass~~ (done 8 Nov, see page status)
5. Section 3, Related work (next, about 450 words)
6. Section 1, Introduction
7. Section 9, Conclusion
8. Abstract and AI-use statement

Page budget: 14 pages before references. Planned split: 1 + 1 + 1 + 1 + 1.5 + 1.5 + 4 + 1.5 + 0.5 for Sections 1–9.

Page status (8 Nov, after the cutting pass): measured with a local stand-in for `llncs.cls` (LNCS page size, 10 pt, small captions) and dummy text of the planned size in the empty parts (abstract 150 words, Section 1 480, Section 3 450, Section 9 230), the text ends at about 14.7 pages. The real class may differ by up to a page, so check on your machine first.

Cuts done on 8 Nov:

- [x] Merge the three noise points in 4.3 with the noise study in 7.5 (4.3 is now one paragraph; 7.5 has no bullets)
- [x] Shorten the selection bullets in 5.1 (selection and replacement are now short paragraphs)
- [x] Cut 6.5 (Computing) to two sentences (now a paragraph in 6.1)
- [x] Fig. 2 (convergence) removed; the free-game trade-off is now Fig. 2
- [x] Shorten the free-round paragraph in 5.3
- [x] Section 2: paytable table replaced by one sentence with every prize; stats list as a paragraph
- [x] Section 4: targets table as 2 rows; free-game-on-its-own paragraph merged into 4.3
- [x] Section 6: 6.1 and 6.2 merged; settings table removed (its contents are in the text)
- [x] Section 7.4 shortened; Section 8 threats as one paragraph
- [ ] Check the page count with the real `llncs.cls` on your machine (the container used a stand-in)
- [ ] If still over: shorten Section 8 explanations, then 7.2–7.3

## Tool setup on Xubuntu

```bash
sudo apt update
sudo apt install texlive-latex-extra texlive-publishers texlive-science \
  texlive-pictures texlive-fonts-recommended cm-super latexmk \
  git poppler-utils libimage-exiftool-perl
kpsewhich llncs.cls splncs04.bst   # both should print a path
```

| Tool | What it does | Install |
| --- | --- | --- |
| TeX Live + latexmk | Compiles the paper; `texlive-publishers` holds `llncs.cls` and `splncs04.bst` | apt command above |
| cm-super | Vector fonts; without it the PDF uses blurry bitmap fonts | apt command above |
| VS Code + LaTeX Workshop | Editor; compiles on save and shows the PDF beside the source | .deb from code.visualstudio.com, then the extension |
| LTeX+ (VS Code extension) | Offline spelling and grammar check | VS Code extensions panel |
| TeXstudio (alternative) | Simpler all-in-one editor | `sudo apt install texstudio` |
| dblp.org | BibTeX for each reference | Web |
| git | Daily snapshots of the paper | apt command above |
| Overleaf (optional) | Share a link with the outside reader on 13 Nov | Web |

Installing VS Code and the extensions:

```bash
cd ~/Downloads && sudo apt install ./code_*.deb
code --install-extension James-Yu.latex-workshop
code --install-extension ltex-plus.vscode-ltex-plus
```

- On first use LTeX+ downloads its language server (with Java) from GitHub, so stay online once; after that it works offline.
- Set British English in user settings (JSON): `"ltex.language": "en-GB"`. The drafts use British spelling ("optimisation").
- LaTeX Workshop: `Ctrl+Alt+V` shows the PDF, `Ctrl+Alt+B` builds; it also builds on save.

Checklist:

- [ ] Run the apt command and confirm `kpsewhich` prints both paths
- [ ] Install VS Code, LaTeX Workshop and LTeX+
- [ ] Unzip `evoapps2027-paper.zip` into `~/paper`
- [ ] Run `latexmk -pdf main.tex` once and open `main.pdf`
- [ ] Run `git init` in `~/paper` and make a first commit (local or private repo only)
- [ ] Commit at the end of every writing day

## Section-by-section guide

### Sections 2, 4, 5: review the drafts (done)

- [x] Read all three aloud and rewrite any sentence that doesn't sound like you
- [x] Confirm the free-game scoring mode: confirmed, all 30 free seeds in `results.json` used `sessions`
- [x] Confirm the SA temperatures (0.14 to 0.002) were not tuned: set once when the baselines were added (10 Oct commit), never changed
- [x] Remove the red `\chk` note in Section 4

To improve later (optional, about 20 minutes, after Sections 1, 3 and 9 are written):

- [ ] Read aloud the paragraphs merged in the cutting pass: 2 (stats paragraph), 4.3, 5.1 (selection, replacement), 7.5
- [ ] 4.4 operators paragraph: change a few phrases into your own wording
- [ ] 5.3 "Same budget" and "Parameters" paragraphs: reword only, facts are confirmed
- [ ] Final read of the whole paper: same terms everywhere (reel set, stats, Roulette, SUS, steady-state, elitist generational)

### Section 6: Experimental setup (done)

- [x] Paired design (now in 6.1)
- [x] Re-evaluation and fixed-base check, with the reason random search was left out
- [x] Noise floor: SD 0.034 / 0.10 fixed from an earlier measurement, floors 0.0298 / 0.088; final-study maxima 0.030 / 0.093 (random search) and 0.025 / 0.061 (other methods)
- [x] Statistics: Friedman reported but not used as a gate; Wilcoxon + Holm; A12 (your wording)
- [x] Claim rule: Holm significant, A12 at least small, gap above the noise floor
- [x] Computing: 83 run-hours, about 14 h elapsed with 6 parallel seeds (shortened in the cutting pass)
- [x] Settings table removed in the cutting pass
- [ ] Anonymous code link (anonymous.4open.science): create on 12 Nov, replace the `\chk` in 6.1

### Section 7: Results (done)

- [x] 7.1 Tuning works: starting error about 91, most methods reach about 0.1, random search stays at 37.5
- [x] 7.2 Replacement, selection and mutation; m = 1 result flagged as the weakest (p_Holm = 0.044, Friedman p = 0.107)
- [x] 7.3 GA vs local search: draw at best in the base stage, never beats it there
- [x] 7.4 Free game and fixed-base check: higher error comes from conflicting targets, not base reels (1.661 vs 1.649, p = 0.77)
- [x] 7.5 Noise study, ending with why the best methods are reported as tied
- [x] Table 3 (was Table 5): median re-evaluated error per method × m, noise-tied values in bold
- [x] Every claim checked against the stats reports and the noise floor

### Section 8: Discussion and threats to validity (done 8 Nov)

- [x] Why generational fails
- [x] Why selection matters only without elitism (expected picks of the best member: Tournament 3, SUS exactly 2, Roulette 2 but misses it in 11% of generations)
- [x] Why the GA only ties local search in the base stage, and beats hill climbing at m = 3 in the free stage
- [x] Practical advice for a slot designer
- [x] Threats: one game, one budget, μ = 10, untuned SA, best m chosen on the same seeds, weighted-sum error, conflicting free targets, noise floor

### Section 3: Related work (about 450 words, 1 page)

Four short paragraphs, each ending with one sentence on how this paper differs. Find papers on Google Scholar and copy BibTeX from dblp.org.

- [ ] Search-based game balancing and procedural content generation
- [ ] Evolutionary optimisation under noise (resampling, re-evaluation, selection bias)
- [ ] Slot machine mathematics, PAR sheets, RTP design
- [ ] Steady-state vs generational GAs, takeover time
- [ ] 15 to 25 references in total, every entry checked on DBLP

### Section 1: Introduction (1 page)

- [ ] Paragraph 1: designers tune reel strips by hand, one simulation per check
- [ ] Paragraph 2: why it is hard: 10^238 reel sets, noisy and costly evaluations, several targets
- [ ] Paragraph 3: the open question: does a GA earn its extra complexity over local search under equal budget and noise?
- [ ] Paragraph 4: what you did and the headline result, with numbers
- [ ] The three contributions as a short list
- [ ] One sentence on how the paper is organised

### Section 9: Conclusion (half a page)

- [ ] One paragraph restating the main claim with its key number
- [ ] Future work: multi-objective tuning of the free game, more games, tuned baselines, a GA without crossover and a diversity measure

### Abstract and AI-use statement

- [ ] Abstract of about 150 words: context, problem, method, two or three key numbers, takeaway
- [ ] Abstract matches the core claim in the submission plan
- [ ] AI-use statement: AI tools helped with the code, the analysis scripts and the writing

## Writing style

Write the first draft of every paragraph yourself, then edit.

- [ ] One idea per paragraph, with the point in its first sentence
- [ ] Use "we" and the active voice
- [ ] Use numbers instead of adjectives ("30 of 30 seeds", not "consistently")
- [ ] Split any sentence you can't read aloud in one breath
- [ ] One name per concept throughout: reel set, evaluation, run, seed, mutation strength m
- [ ] Same method names as Table 2 (Steady-state, Elitist generational, Generational, Tournament, Roulette, SUS)
- [ ] Avoid filler words such as "crucial", "notably", "leverage", "delve", "robust", "comprehensive"
- [ ] Run LTeX+ on every section before marking it done

## Figures and tables

Two figures and three tables after the cutting pass.

| Exhibit | Section | Source file |
| --- | --- | --- |
| Reel strip and window diagram (Fig. 1) | 2 | Drafted in TikZ |
| Free-game trade-off (Fig. 2) | 7.4 | `paper/figures/free_tradeoff.pdf` from `paper/make_figures.py` |
| Targets and weights (Table 1) | 4.2 | written in `04_problem.tex` |
| The twelve methods (Table 2) | 5 | written in `05_methods.tex` |
| Main table: median re-evaluated error (Table 3) | 7 | written in `07_results.tex` |

The convergence figure was removed on 8 Nov to save space; `make_figures.py` now only draws the trade-off figure (at 0.5 × text width high). Regenerate it with `python paper/make_figures.py Results/results.json Results/results_fixedbase.json paper/figures` (the PDF is binary, so it is not stored in this project).

- [x] Re-export each chart as PDF, not PNG
- [x] Size charts for the LNCS text width (about 12 cm) with fonts of at least 8 pt
- [x] Check each figure in greyscale; tell series apart by marker or line style, not colour alone
- [x] Replace the code spelling "Elistism" with "Elitist" in every label, legend and table
- [x] Remove file paths, usernames, machine names and titles from the figures
- [ ] Give every figure and table a caption that says what to look for
- [ ] Refer to every figure and table in the text before it appears

## Final checks before upload

Run these on 12–14 November on the final PDF.

```bash
cd ~/paper
grep -rniE "travi|thapa|gamemano|ravi" .   # should print nothing
latexmk -pdf main.tex
pdfinfo main.pdf          # page count; Author field must be empty
pdffonts main.pdf         # every font should show "emb yes"
exiftool -all= main.pdf   # clears hidden PDF metadata
```

Anonymity

- [ ] The grep above prints nothing
- [ ] No name, email, affiliation, GitHub username or company in the text, figures, file names or acknowledgements
- [ ] Code link is anonymous, and the anonymised repo also contains no names
- [ ] PDF metadata cleared and checked with `pdfinfo`

Format

- [ ] Unmodified LNCS template, margins and fonts
- [ ] At most 14 pages before the references
- [ ] All fonts embedded (`pdffonts`)
- [ ] No compile warnings about undefined references or citations

Content

- [ ] Abstract states the core claim with numbers
- [ ] Contributions listed at the end of the introduction
- [ ] Equal evaluation budget stated explicitly (Section 5)
- [ ] How the baselines were set up explained (Section 5)
- [ ] Every results claim matches `stats_report.md`
- [x] Threats to validity present (Section 8)
- [ ] AI-use statement included
- [ ] Every `\chk` note removed

Outside read and upload

- [ ] 13 Nov: PDF sent to one professor or researcher; top 3 issues fixed
- [ ] 14 Nov: uploaded to EasyChair (evostar2027); title, abstract and keywords match the PDF
- [ ] Downloaded the PDF EasyChair stored and checked it opens correctly
