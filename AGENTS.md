# Repository Agent Instructions

## Core Principles
- Keep crates small and composable.
- Prefer stable APIs and explicit errors.
- Keep CI strict and reproducible.

## Validation Loop
- `cargo fmt --all -- --check`
- `cargo check --tests --benches`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo nextest run`

## Workflow Rules
- Protect `main` with required CI checks.
- Never merge code with failing lint or tests.

## Test Design and Evidence
- For a behavior change, name the contract, likely failure modes, and production
  entry points before choosing tests. Assert observable results with an independent
  oracle; do not reproduce the implementation to calculate expected values.
- Keep useful examples and boundary cases. Add property-based tests when a broad
  input space has a meaningful invariant, using `proptest` or the existing project
  framework. Generate valid and invalid classes deliberately; avoid properties
  that mostly discard inputs or only assert that the code did not panic.
- Preserve minimized failures as regression cases and record the seed/replay data.
  A round trip alone can hide a shared encoder/decoder bug; add an independent
  expectation or reference where the contract needs it.
- When strengthening a test suite or changing a critical contract, challenge the
  tests with a plausible defect in an isolated copy of production code. First run
  the unmodified baseline, then the same tests against the defect, restore the
  code, and rerun. Verify that the intended assertion detects the defect.
- Use targeted `cargo-mutants` runs for test audits or critical logic. Keep raw
  outcomes and scope: caught, survived, uncompilable, timeout, crash, and excluded.
  A compilation error, unrelated failure, or process timeout is not evidence that
  the intended assertion works. Investigate survivors; justify equivalent mutants
  individually without silently dropping them or inflating the result.
- Record the source revision, commands, tool versions, selected tests/features,
  actual test count, and remaining limits. Zero tests, missing tools, skipped jobs,
  or a successful build must not be reported as a passing behavioral check.
- Choose the smallest check that resolves a concrete risk. Documentation and other
  low-impact changes do not need artificial tests or a full mutation campaign.

## Rust Tool Selection
- Start with the validation loop above. Add doctests with `cargo test --doc` when
  documenting executable examples; nextest does not run doctests. Check the actual
  supported features and targets, including incompatible feature combinations.
- Parsers, serializers, numeric boundaries, and state transitions: consider
  `proptest`; add `cargo-fuzz` for hostile input or memory-safety risk. Fuzzing needs
  a real production entry point, useful assertions, a time budget, and saved cases.
- Unsafe Rust: use Miri for supported Rust paths. Native/FFI boundaries also need
  tests of the real ABI and appropriate native sanitizers; a Rust-only harness
  cannot establish correctness of the foreign implementation.
- Concurrency: consider Loom only for code using its modeled synchronization
  primitives. State the model, bounds, and excluded production behavior.
- Small critical pure functions: consider Kani when exhaustive bounded reasoning
  is worthwhile. Check assumptions, reachability/non-vacuity, and unwind bounds;
  a bounded harness is not a proof of the entire application.
- Advanced tools are candidates, not installed or enforced by this template.
  Before enabling one, add a reproducible invocation, compatible pinned tooling,
  a meaningful detection control, and an explicit CI policy. Required jobs must
  fail on unavailable tools or missing execution; optional jobs must expose skips.

References: [Proptest](https://proptest-rs.github.io/proptest/intro.html),
[cargo-mutants outcomes](https://mutants.rs/using-results.html),
[Rust Fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html),
[Miri](https://github.com/rust-lang/miri), [Loom](https://github.com/tokio-rs/loom),
[Kani results](https://model-checking.github.io/kani/verification-results.html).
