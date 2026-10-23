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

Updates use Homebrew livecheck and `brew bump-cask-pr` daily at 06:17 UTC,
selecting the newest prerelease with a completed macOS build.
