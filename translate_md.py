import glob
import sys

md_files = glob.glob("freqtrade/docs/**/*.md", recursive=True)
print(f"{len(md_files)}個の.mdファイルが見つかりました")
for f in md_files[:10]:
    print(f"  - {f}")
print("...")
