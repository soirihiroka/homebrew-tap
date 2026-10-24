cask "shrimply" do
  version "20261024013529,72d9eb17bd7d"
  sha256 "bad4b00b75b48fffd759e591141974aa8ffdfe577bb820de74a4b79c34a66659"

  url "https://github.com/soirihiroka/shrimply/releases/download/prerelease-#{version.csv.first[0, 8]}T#{version.csv.first[8, 6]}Z-#{version.csv.second}/shrimply-macos-arm64.zip"
  name "Shrimply"
  desc "Video editor"
  homepage "https://github.com/soirihiroka/shrimply"

  livecheck do
    url :url
    regex(/^prerelease-(\d{8})T(\d{6})Z-([0-9a-f]{12})$/i)
    strategy :github_releases do |json, regex|
      json.filter_map do |release|
        next if release["draft"]
        next unless release["assets"].any? do |asset|
          asset["name"] == "shrimply-macos-arm64.zip" && asset["state"] == "uploaded"
        end

        match = release["tag_name"].match(regex)
        "#{match[1]}#{match[2]},#{match[3]}" if match
      end
    end
  end

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Shrimply.app"

  postflight_steps do
    run "/usr/bin/xattr", args: ["-dr", "com.apple.quarantine", "{{appdir}}/Shrimply.app"]
  end

  zap trash: [
    "~/Library/Application Support/Shrimply",
    "~/Library/Caches/Shrimply",
  ]
end
