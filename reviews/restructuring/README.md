# Historical restructuring archive

These files record the completed, gated restructuring begun from commit
`65469bbd4e7aa811db0f0511ae10a4386299308f`. They are preserved unchanged as
evidence, not maintained as today's build or validation pipeline.

- [CHANGES.md](CHANGES.md): the phase-by-phase restructuring log, distinct from
  the current [release changelog](../../CHANGELOG.md).
- [NEEDS-DECISION.md](NEEDS-DECISION.md): historical G0/G4 approvals, not pending
  decisions for the current edition.
- [recon.md](recon.md) and [phase4-proposal.md](phase4-proposal.md): reconnaissance
  and the judged-substitution proposal.
- [baseline.json](baseline.json), `phase1-audit.json` through `phase6-audit.json`,
  and [final-audit.json](final-audit.json): point-in-time structural snapshots.
- `audit.py`, `restructure.py`, `verify.py`: the original phase-specific scripts.

## Do not run these as current maintenance

The scripts retain their original root-relative assumptions, hard-coded phase
commits and snapshot expectations. They are deliberately not adapted to the
current book or this archive location. In particular, `restructure.py` is a
historical mutating migration, and `audit.py` defaults to writing a baseline
report. Their old commands are not current contributor instructions.

For historical reproduction, use the corresponding historical commit in a
separate checkout, where the original directory layout and source snapshot are
available. For the live edition, use [the maintained tooling](../../tools/README.md).
