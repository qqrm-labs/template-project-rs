# Rust Project Template

Template repository for general-purpose Rust projects.

## Included
- CI workflow with fmt/check/clippy/nextest and dependency checks (`.github/workflows/ci.yml`)
- GitHub Actions security workflow with actionlint and Zizmor (`.github/workflows/workflow-security.yml`)
- Release workflow for version tags (`.github/workflows/release.yml`)
- Weekly cross-ecosystem dependency batches and event-driven native auto-merge

## Usage
1. Create a repository from this template.
2. Replace crate name in `Cargo.toml`.
3. Implement project code in `src/`.
4. Push a tag like `v0.1.0` to trigger release workflow.

## Maintenance policy

Dependabot collects Cargo and GitHub Actions updates into one `maintenance` PR
on Mondays at 12:00 Europe/Moscow. Ordinary releases have a seven-day cooldown.
Security updates are grouped separately for Cargo and do not wait for the weekly
version-update schedule or cooldown. Dependabot fixes dependencies, not arbitrary
code or CI findings; those still need a separate maintenance PR passing CI.

Native auto-merge is enabled when the current Dependabot commit passes both
`ci-gate` and `workflow-security-gate`. Missing, skipped, cancelled, or failed
checks block these gates. There is no scheduled merge sweep or human approval
requirement, including for major versions, Rust 0.x changes, and Actions updates.
The read-only provenance check requires every commit to be signed by Dependabot
and the batch head to match the checked event. A provenance failure blocks the
batch; human approval cannot override it. Compatibility is established by the
project's automated checks, so derived projects must test their actual behavior.
The privileged merge workflow consumes only GitHub metadata, never PR code or
artifacts; it uses the repository token without a PAT or production secrets.

Repository settings are not copied with this template. For each derived repo:

1. Protect `main`, including administrators: require an up-to-date PR and the
   `ci-gate` and `workflow-security-gate` checks from GitHub Actions (app ID 15368).
2. Disable required pull request reviews, including code-owner and last-push
   approvals. Require conversation resolution; disallow force pushes and deletions.
   No maintainer or bot needs an exception to the required checks.
3. Enable native auto-merge. Keep the default workflow token read-only and automatic
   PR approval disabled; only the metadata-only merge job receives write access.

Releases remain tag-triggered. Merging a maintenance batch does not create a
version tag or publish a release. GitHub-token mutations may not trigger follow-on
workflows, so a downstream publisher must be invoked explicitly and validated
before enabling automatic releases in a derived project.

## Local Commands
- `cargo fmt --all -- --check`
- `cargo check --tests --benches`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo nextest run`
- `cargo audit`
- `cargo deny check advisories bans sources`
- `cargo machete`

Before publishing a derived project, choose and declare its license. License
enforcement is intentionally not enabled by the template's `cargo-deny` policy.
