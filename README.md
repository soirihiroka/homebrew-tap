# Soiri's Homebrew tap

Install [Shrimply](https://github.com/soirihiroka/shrimply), a video editor with
a native macOS interface:

```sh
brew install --cask soirihiroka/tap/shrimply
```

Requires **Apple Silicon and macOS 15 (Sequoia) or newer**. The cask installs the
upstream `Shrimply.app` into Applications, including its bundled dependencies.
Open Shrimply from Applications after installation.

Shrimply is pre-alpha software. Back up your projects before upgrading. The app
is ad-hoc signed; if macOS blocks its first launch, approve it in **System
Settings > Privacy & Security**, then open it again, as described in the
[upstream release notes](https://github.com/soirihiroka/shrimply/releases).

## Updating and removing

```sh
brew update
brew upgrade --cask soirihiroka/tap/shrimply
brew uninstall --cask soirihiroka/tap/shrimply
```

Uninstalling preserves your settings and caches. To remove those as well:

```sh
brew uninstall --cask --zap soirihiroka/tap/shrimply
```

`--zap` removes `~/Library/Application Support/Shrimply` and
`~/Library/Caches/Shrimply`. Keep backups of any files you put in these directories.

## Maintenance

The Update Shrimply workflow checks upstream daily at **06:17 UTC**, and can also
be run manually from GitHub Actions. It selects the newest timestamped prerelease
that contains an uploaded `shrimply-macos-arm64.zip`, even when a newer release's
macOS build is unfinished. It uses a fixed release URL and verifies the downloaded
archive against GitHub's SHA-256 asset digest before changing the cask.

Cask versions use `YYYYMMDDHHMMSS,commit` from the release tag's UTC timestamp and
short commit hash. A timestamp older than the current cask is never selected.
Future stable releases or a new upstream tag format require an updater change.
Homebrew livecheck is skipped because this workflow manages prerelease updates.

Updates pass the same macOS checks as pushes and pull requests before being
committed directly to `main`. The workflow uses the repository's `GITHUB_TOKEN`
with `contents: write`; repository rules must permit these pushes. A failed check
leaves the published cask unchanged and reports a failed Actions run. Commits
made with `GITHUB_TOKEN` do not trigger another push workflow, so validation
happens before the updater commits.

To inspect or apply an update locally with Python 3.9 or newer:

```sh
python3 scripts/update-shrimply.py --check
python3 scripts/update-shrimply.py
```

`--check` verifies the candidate archive without editing files and exits with
status 1 when an update is available. Set `GITHUB_TOKEN` if GitHub API rate limits
are a concern; the token is sent only to the API. Unchanged scheduled runs avoid
downloading the archive again.

On an Apple Silicon Mac, register this checkout as `soirihiroka/tap` and run:

```sh
brew style Casks/shrimply.rb
brew audit --cask --online soirihiroka/tap/shrimply
brew install --cask soirihiroka/tap/shrimply
```

The workflows also check bundle metadata, the ARM64 executable, its ad-hoc
signature, invalid project arguments, and uninstallation. This third-party tap
explicitly permits Shrimply's GitHub prereleases in its cask audit configuration.

All maintenance commits use
`soirihiroka <133444309+soirihiroka@users.noreply.github.com>` for author and
committer, with both timestamps explicitly set in UTC. For local commits, set
the same repository-local identity and export `TZ=UTC`, `GIT_AUTHOR_DATE`, and
`GIT_COMMITTER_DATE` using `date -u +'%Y-%m-%dT%H:%M:%SZ'`.
