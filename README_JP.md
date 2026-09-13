# TAKERF405 Analog Custom OSD v1.2

## あなたの実機から確定したこと
- MCU: STM32F405 / target family S405
- manufacturer_id: GEPR
- board_name: TAKERF405
- Betaflight: 2025.12.0-beta / MSP API 1.47
- Firmware build optionsに `USE_OSD_SD` と `USE_OSD_HD` の両方あり
- 現在 `osd_displayport_device = AUTO`
- 現在 `vcd_video_system = PAL`
- 現在 `osd_framerate_hz = 60`
- Motor 1/2/3/4 pins: PE9 / PE11 / PC8 / PC9 と整合

つまり、アナログOSDを使うための基本設定はすでに揃っている。AUTOのままでMAX7456が検出されればアナログOSDが選ばれる。

## Custom Stick Overlay
Type 1はBetaflight純正のまま。
Type 2 + MAX7456だけ、4x6サブセルglyphを使う。

- 純正: 横7 x 縦15位置
- Custom: 横28 x 縦30位置
- OSD task: 60Hz（現在すでに60Hz）

現在のStick Overlay位置は:
- Left: pos 2407 = x7, y11, Type 1
- Right: pos 2415 = x15, y11, Type 1

Custom firmwareを焼いた後、`enable_kiss_overlay_pal.cli` をCLIへ貼ると、位置を変えずType 2へ切り替わる。

## なぜ専用target configを同梱しているか
TAKER F405 AIOの公式Betaflight configは2025-12-05にupstreamへ追加されたが、あなたのGEPRC firmwareは2025-09-15 buildなので、それ以前のメーカー独自targetを使っている。

さらにupstreamの初期targetはMotor3/4がPE13/PE14だったが、2026-01-27にPC8/PC9へ修正された。あなたの `diff all` のDMA/pin情報はPC8系なので、v1.2ではPC8/PC9版を採用している。

## ソースbase
Betaflight sourceは、build日時より前の同日最新commitとして
`11910a0912b9462e15e700be091a40a04181d190`
を候補baseに固定している。

`norevision` firmwareなので、GEPRCが実際に使ったcommitを100%証明することはできない。飛行制御部分を不用意に変更しないため、まずこの2025.12 beta世代で進める。

## フォント
`make_kiss_stick_font.py` は通常のBetaflight MAX7456 `.mcm` を入力にして、0xA0-0xB7へ24個のサブセルcursor glyphを書き込む。

例:
`python3 make_kiss_stick_font.py betaflight.mcm betaflight_kiss_stick.mcm`

生成したfontをConfiguratorのFont ManagerからMAX7456へ書き込む。
0xA0-0xB7のBetaflight logo glyphは置き換わる。

## 重要
Custom firmwareだけ焼いてfontを書き込まない状態でType 2にすると、cursorはロゴ等の文字化けに見える。先にcustom fontを書き込むか、Type 1のままにすること。

ConfiguratorでStick Overlayを動かした後はType情報が戻る可能性があるので、最後に `enable_kiss_overlay_pal.cli` をもう一度貼る。


## v1.2追加
GitHub Actionsがfirmwareだけでなく公式Betaflight analog fontを取得し、`betaflight_kiss_stick.mcm`も自動生成する。ユーザー側でPythonを実行する必要はない。まず `START_HERE_JP.md` を参照。
