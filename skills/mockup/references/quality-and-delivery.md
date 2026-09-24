# Quality and delivery

Inspect every image before delivery:

- correct logo and spelling;
- preserved proportions and recognizable colors;
- placement stays inside the intended surface;
- perspective matches the photographed plane;
- folds, texture, highlights, and occlusion remain believable;
- no accidental background rectangle, clipping, or edge halo;
- no unrelated generated text or marks.

The output directory must contain:

```text
brand-analysis.md
images/01-surface.png ...
contact-sheet.jpg
manifest.json
```

The contact sheet must show every selected image with a readable label and no accidental cropping. `manifest.json` is the source of truth for inputs, selected templates, render mode, dimensions, prompts, and file paths.

In the final response, report the output directory and link the contact sheet, analysis, manifest, and individual image folder.
