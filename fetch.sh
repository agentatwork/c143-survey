#!/bin/bash
# Fetch public metadata for every repo linked from a claim on poidh Arb #143.
# Read-only: repo metadata, README text, commit list. Nothing is cloned, installed or run.
TOKEN=$(cat /home/agent/work/gh_token)
gh_api(){ curl -sS -m 30 -H "Authorization: Bearer $TOKEN" -H "Accept: ${2:-application/vnd.github+json}" "https://api.github.com/$1"; }
while read -r r; do
  slug=${r//\//_}
  gh_api "repos/$r" > meta_$slug.json
  gh_api "repos/$r/readme" "application/vnd.github.raw" > readme_$slug.md
  gh_api "repos/$r/commits?per_page=100" > commits_$slug.json
done < repos.txt
