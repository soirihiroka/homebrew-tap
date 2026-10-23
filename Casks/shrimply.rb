cask "shrimply" do
  version "20261023150907,1b4d50a2a42a"
  sha256 "7cde98771c10424635519229974a7dd0f967a455cbeb15cf722515c28635d093"

  url "https://github.com/soirihiroka/shrimply/releases/download/prerelease-#{version.csv.first[0, 8]}T#{version.csv.first[8, 6]}Z-#{version.csv.second}/shrimply-macos-arm64.zip"
  name "Shrimply"
  desc "Video editor"
  homepage "https://github.com/soirihiroka/shrimply"

  livecheck do
    skip "Updated by this tap's scheduled prerelease updater"
  end

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Shrimply.app"

  zap trash: [
    "~/Library/Application Support/Shrimply",
    "~/Library/Caches/Shrimply",
  ]

  caveats <<~EOS
    Shrimply is pre-alpha software. Back up projects before upgrading.
    The app is ad-hoc signed. If macOS blocks its first launch, approve it
    in System Settings > Privacy & Security, then open it again.
  EOS
end
