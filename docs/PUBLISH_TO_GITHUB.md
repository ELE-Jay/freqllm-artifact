# Publish to GitHub

This artifact directory is already a local Git repository with an initial commit on branch `main`.

## Create the Remote Repository

Create an empty GitHub repository named `freqllm-ccs26-artifact`.

## Push from This Machine

```bash
cd /root/FHE/EncryptedLLM/freqllm-ccs26-artifact
git remote add origin git@github.com:<your-org-or-user>/freqllm-ccs26-artifact.git
git push -u origin main
```

If you prefer HTTPS:

```bash
cd /root/FHE/EncryptedLLM/freqllm-ccs26-artifact
git remote add origin https://github.com/<your-org-or-user>/freqllm-ccs26-artifact.git
git push -u origin main
```

## After Pushing

1. Open the repository URL in a browser.
2. Confirm that `README.md`, `docs/OPEN_SCIENCE.md`, `figures/`, and `tables/` are visible.
3. Copy the repository URL into the CCS artifact field and the Open Science section of the paper.
