# BIOT 6900 coursework
# BIOT 6900 coursework

Mohammed Sharukh — Module 1 Lab Guide

Completed Parts A, B, and C (all four database queries). Part D skipped per instructor's announcement (Sept 15) — will be covered in Week 2 class.

Notes on what didn't work: ran into a Git merge conflict on README.md early in setup, caused by PowerShell's `echo` command writing the file in UTF-16 encoding, which Git treated as binary instead of text. Resolved by rewriting the file with `Set-Content -Encoding utf8` and re-merging.