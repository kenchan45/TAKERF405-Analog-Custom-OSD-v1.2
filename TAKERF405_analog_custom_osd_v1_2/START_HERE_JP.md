# まずここから

このZIP自体はFCへ直接フラッシュするファイルではありません。
GitHub Actionsで「実際に使うHEXとMCM」を自動生成するためのプロジェクトです。

## 一番簡単な使い方

1. GitHubで空のリポジトリを1つ作る（PrivateでOK）。
2. このZIPを展開し、`TAKERF405_analog_custom_osd_v1_2` フォルダの**中身全部**を、そのリポジトリのルートへアップロードする。
   - `.github` フォルダも必須。
3. GitHubの `Actions` タブを開く。
4. 左側の `Build TAKERF405 Custom OSD` を選ぶ。
5. `Run workflow` → 緑の `Run workflow`。
6. 数分〜十数分待ち、緑のチェックになったら、その実行結果を開く。
7. ページ下部の `Artifacts` → `TAKERF405-custom-osd-ready` をダウンロード。

Artifactには以下が入ります。
- TAKERF405用 `.hex` : BetaflightへフラッシュするCustom FW
- `betaflight_kiss_stick.mcm` : MAX7456へ書き込むCustom font
- `enable_kiss_overlay_pal.cli` : KISS風Stick Overlayを有効化
- `restore_stock_overlay.cli` : 純正Stick Overlayへ戻す
- `FLASHING_GUIDE_JP.txt` : 実機への導入手順

## GitHub Actionsが表示されない場合
リポジトリへ `.github/workflows/build.yml` が正しくアップロードされているか確認する。
初回はActionsを有効化する確認画面が出る場合がある。
