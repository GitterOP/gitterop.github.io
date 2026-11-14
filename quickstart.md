# Updating the website

## Profile and CV

Edit [_data/profile.yml](./_data/profile.yml) to update the name, alumni affiliation, interests, education, honors, experience, or links. The public affiliation describes an alumnus of Universidad del Pacífico; it does not imply a current university position.

Replace [the public CV](./files/cv/juan-david-cardenas-cv.pdf) to update the downloadable document. Its original full name is preserved within the PDF.

## Publications

Edit [_data/publications.yml](./_data/publications.yml). Every entry has a stable identifier, original title, ordered authors, venue, year, DOI, public PDF path, personal contribution, and BibTeX. The two featured entries additionally contain research summaries and figure references.

Place published article PDFs in [files/papers/](./files/papers/). Label an accepted author version explicitly. Check that each PDF matches its article before replacing a file. Figures belong in [assets/images/research/](./assets/images/research/) and need an alternative description, caption, and source.

Only report a result that can be traced to the published paper, and retain the conditions under which it was obtained. Contributions should continue to distinguish collaboration, supervision, and implementation.

## Projects in progress

[_data/current_projects.yml](./_data/current_projects.yml) deliberately contains only identifiers, titles, categories, status, and short summaries. The three approved projects are thesis unmixing, wetland segmentation, and SLBot as a hobby. Their results, figures, manuscripts, code links, and implementation details are excluded from this version.

## Build and check

```bash
ruby scripts/site.rb build
python3 tests/check_site.py
```

The checker covers local links and anchors, PDF access, publication counts, and the publishing boundaries of work in progress. Also review the layout on mobile and desktop, keyboard focus, and the six article downloads.

## GitHub Pages

The intended destination is the personal repository `GitterOP/gitterop.github.io`, with URL `https://gitterop.github.io/`. No remote was created or published during initial local implementation.

Once publication is authorized, verify the repository identity, push only the reviewed public source files, and select **GitHub Actions** under **Settings → Pages**. The [workflow](./.github/workflows/pages.yml) builds and checks pull requests; pushes to `main` also deploy the site. The committed lockfile fixes Ruby dependencies.

If using a project site instead, update `url` and `baseurl` in [_config.yml](./_config.yml). All local navigation and asset links use Jekyll URL filters. Rebuild, rerun checks for that deployment path, and verify the resulting site before sharing its URL.

## Source boundary

Local agent settings, the original CV source copy, SDD working documents, build output, and installed dependencies are ignored by Git. The complete contributions database and research repositories are never copied into the website. Review the staged paths before pushing to a public repository.

## Portrait and color themes

The profile photograph is [the provided portrait](./assets/images/juan-david-cardenas.png), referenced in the profile data with alternative text. The original image is preserved.

The site starts in dark mode. The header button switches between dark and light and remembers the choice across pages and reloads. The [theme script](./assets/js/theme.js) handles unavailable browser storage; the [stylesheet](./assets/css/main.css) defines both palettes. Without JavaScript, content remains available in the default dark palette.
