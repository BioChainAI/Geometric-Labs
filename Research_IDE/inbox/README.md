# inbox/

Point your browser's download folder here (or move downloads here) while you work in the IDE. Files in this folder are **not committed** (see `../.gitignore`).

When a paper session is done, file everything into the paper:

```sh
make ingest PAPER=RP-0001
```

Each file is sorted by its IDE export name, hashed into the paper's `manifest.json`, and removed from this inbox. A file that differs from an already filed file of the same name stays here until you re-run with `--replace`. See [WALKTHROUGH.md, Step 11](../WALKTHROUGH.md#step-11-file-the-exports-into-the-paper).
