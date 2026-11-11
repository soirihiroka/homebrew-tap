# Soiri's Homebrew tap

[Shrimply](https://github.com/soirihiroka/shrimply) for Apple Silicon and macOS 15+.

```sh
brew install --cask soirihiroka/tap/shrimply
```

```sh
brew update
brew upgrade --cask soirihiroka/tap/shrimply
```

The cask removes quarantine automatically on every install and upgrade because
Shrimply is ad-hoc signed. This bypasses the Gatekeeper quarantine check.
For an existing installation, apply the hook once with:

```sh
brew update
brew reinstall --cask soirihiroka/tap/shrimply
```

The Shrimply macOS CI calls this tap's reusable updater after successfully
publishing a prerelease. A deploy key scoped to this tap authorizes the update.
The daily check at 06:17 UTC remains as a fallback. Both paths use Homebrew
livecheck and `brew bump-cask-pr`, selecting the newest prerelease with a
completed macOS build. Automated commits use UTC author and committer dates.
