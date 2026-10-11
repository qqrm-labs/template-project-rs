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
code or CI findings; those still need a reviewed maintenance PR.

Native auto-merge is enabled when the current Dependabot commit passes both
`ci-gate` and `workflow-security-gate`. Missing, skipped, cancelled, or failed
checks block these gates. There is no scheduled merge sweep. Breaking updates,
including Rust 0.x compatibility changes, incomplete metadata, and commits not
signed by Dependabot require a maintainer's approval of the current head commit.
Submitting or dismissing a review reruns the read-only security/policy checks.
Changes to workflows, automation, or security policy also require CODEOWNER review.
The privileged merge workflow consumes only GitHub metadata, never PR code or
artifacts; it uses the repository token without a PAT or production secrets.

Repository settings are not copied with this template. For each derived repo:

1. Replace `@qqrm` in `.github/CODEOWNERS` with the responsible maintainer/team.
2. Protect `main`, including administrators: require an up-to-date PR and the
   `ci-gate` and `workflow-security-gate` checks from GitHub Actions (app ID 15368).
3. Require code-owner review, dismiss stale approvals, and resolve conversations.
   Zero blanket approvals permits compatible dependency-only batches to merge.
   Do not allow force pushes or deletions. The sole maintainer may bypass the
   review requirement for their own PRs; required checks still apply to them.
   Never grant the Actions or Dependabot bots a review bypass.
4. Enable native auto-merge. Keep the default workflow token read-only and automatic
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
