cask "shrimply" do
  version "20261128140236,e40edd0c5146"
  sha256 "05dc7142c10f84fe2d27a41e72e412db0cb120f8f33e829b534158d8a853da48"

  release_date = version.csv.first[0, 8]
  release_time = version.csv.first[8, 6]
  url "https://github.com/soirihiroka/shrimply/releases/download/prerelease-#{release_date}T#{release_time}Z-#{version.csv.second}/shrimply-macos-arm64.zip"
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
