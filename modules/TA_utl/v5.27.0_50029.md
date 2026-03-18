# Changelog

## v5.27.0 (2026-03-18)

### Bug Fixes
- **Accent color not persisting** — manually picking an accent color from the picker didn't disable randomization, so the next page load or tab switch would randomize over the user's choice. Picker now auto-disables randomization and syncs the toggle state
- **Apps silently removed from target.txt** — `cleanup_dead_apps` relied solely on `pm list packages -3` which can be filtered by HideMyAppList or miss apps in other user profiles. Now cross-checks `/data/data/<pkg>` existence and requires 3 consecutive misses before removing, preventing false removals during app updates or when HMA is active
- **WebUI save race with daemon** — `target.txt` was written non-atomically (`echo > file`), allowing the daemon to read a truncated file mid-write. Now uses temp-file-then-rename

---

## v5.26.0 (2026-03-17)

### Bug Fixes
- **Custom ROM version wiped by propclean** — `hexpatch_deleteprop` was destroying all properties matching ROM fingerprint substrings (e.g. `crdroid`), including `ro.crdroid.build.version` which crDroid needs for its About screen and OTA updater. Now auto-detects the running ROM by checking for `ro.<fingerprint>*` properties before wiping — if the device owns those props, they're preserved. Generic fix that works for any ROM in the fingerprint list (LineageOS, EvolutionX, PixelOS, etc.)

---

## v5.25.0 (2026-03-14)

### Bug Fixes
- **`marketname` false positive in ROM fingerprint detection** — stock Xiaomi `marketname` props were being scrubbed as custom ROM indicators, breaking Xiaomi Share device naming and iOS Interconnectivity (#16, #17)
- **ReSukiSU excluded from target list** — added `com.resukisu.resukisu` to the manager exclusion list alongside existing SukiSU Ultra entry (#18)

---

## v5.24.0 (2026-03-11)

### Features
- **x86_64 and x86 ABI support** — module now ships binaries for all four Android ABIs (arm64-v8a, armeabi-v7a, x86_64, x86), enabling Waydroid and emulator installs

### Bug Fixes
- **Bootloader detection by TrustAttestor** — `check_reset_prop` was creating props on devices where they don't naturally exist (e.g. Realme/OnePlus-specific props on Xiaomi), giving attestor apps a clear tampering signal. Now skips non-existent props instead of blindly injecting them, matching stock behavior
- **AVB version mismatch** — `ro.boot.vbmeta.avb_version` was set to `1.3` (non-standard) instead of `1.0`, creating a detectable inconsistency with the actual AVB stack
- **Extra props in Rust backend** — removed `ro.bootimage.build.tags`, `ro.boot.verifiedbooterror`, and `ro.boot.veritymode.managed` from the Rust prop list since they don't exist on most devices and would be created unnecessarily
- **Unconditional prop injection** — `ro.oem_unlock_supported` and `ro.secureboot.devicelock` were set outside the ZeroMount guard, now properly gated
- **Stale description on uninstall** — WebUI uninstall now immediately restores the original TrickyStore/TEESimulator description instead of relying on daemon timing; also fixed path mismatch between Rust (`description.bak`) and shell (`.original_description`) backup files

---

## v5.23.0 (2026-03-11)

### Features
- **`ro.boot.product.hardware.sku` support** — fourth region prop added across the full stack (config, install snapshot, boot enforcement, WebUI)
- **Collapsible region UI** — `ro.boot.hwc` always visible, remaining 3 fields behind a chevron expand to reduce clutter
- **GitHub Actions CI** — build workflow cross-compiles both ABIs and uploads the module ZIP as artifact on every push

### Improvements
- **Region i18n** — all 3 region strings translated across 22 locales (was English-only fallback)
- **Dynamic README badges** — version badge pulls from GitHub releases, build status badge from CI

---

## v5.22.0 (2026-03-10)

### Features
- **Config-driven MIUI region props** — snapshots `ro.boot.hwc`, `ro.boot.hwcountry`, `ro.product.mod_device` at install time instead of blind CN→GLOBAL spoofing. Supports Global/CN/India variants without breaking Xiaomi.eu or stock Indian ROMs
- **Region WebUI controls** — toggle and text fields inside Keybox Automation settings for per-device override of region props
- **Boot hash priority chain** — prefers TEESimulator's persisted `boot_hash.bin` when present (cert-chain consistent), falls back to our install-time capture. No gap if TEESimulator is absent or uses upstream without persistence

### Improvements
- **Uninstall completeness** — cleans up `.verbose`, `devconfig.toml`, `TA_enhanced` module dir, `banner.png` symlink, and banner line from TrickyStore's `module.prop`

---

## v5.8.0 (2026-03-09)

### Features
- **Inotify-based app detection** — daemon watches `/data/app/` for installs and uninstalls via inotify, gated on `automation.use_inotify` config. Two-stage scan at 3s and 8s after directory event handles the PM registration race where the package manager hasn't finished registering the app when the directory first appears
- **On-demand automation trigger** — scheduler exposes `run_automation_now()` so inotify events bypass the regular 10s polling interval

### Bug Fixes
- **Module version not shown in WebUI** — `service.sh` deletes `module.prop` to hide from manager UI, but `webui_init.rs` couldn't read it. Now preserves a copy to `/data/adb/tricky_store/ta-enhanced/module.prop` before deletion, added as first lookup path
- **Version fallback missing `v` prefix** — `CARGO_PKG_VERSION` fallback now formats as `v5.8.0` instead of `5.8.0`

### Performance
- **WebUI init unblocked** — `webui-init` no longer waits for binary path resolution (`kc()`); path is resolved inline within the shell call, saving one sequential round trip on page load

---

## v5.7.0 (2026-03-08)

### Bug Fixes
- **KSU theme colors** — use KSU native theme system for Material surface colors instead of hardcoded values

---

## v5.6.0 (2026-03-07)

### Bug Fixes
- **Security patch not applied on reinstall** — `security-patch set` wrote device ROM dates (e.g. 2025-xx) and `update` silently skipped when `auto_update` was previously disabled; install now uses `--force` flag to always fetch latest bulletin date regardless of config, with built-in fallback table for offline installs
- **VBMeta hash not refreshed on reinstall** — installer skipped capture when `boot_hash` already existed; now compares live `ro.boot.vbmeta.digest` against stored value and updates if changed

### Enhancements
- **Keybox interval badge** — Automation settings now shows the current fetch interval as a badge next to the section header, updated in real-time when changed via chips or custom input

---

## v5.5.0 (2026-03-07)

### Bug Fixes
- **Security patch dialog empty on open** — dialog always showed blank fields because auto-mode config (default true) short-circuited file reading; now always reads and displays current values from `security_patch.txt`
- **Get patch date failing** — fetching latest Pixel bulletin date failed due to exec buffer limits with full HTML response; now pipes through `sed` on shell side (matching upstream), with `busybox wget` fallback
- **Boot script overwriting bulletin dates** — `service.sh` ran `security-patch set` on boot which overwrote daemon-fetched dates with stale device props; removed in favor of daemon's `SecurityPatchTask`
- **Security patch validator rejecting valid dates** — save dialog rejected `YYYY-MM-DD` format written by Rust; validator now accepts both `YYYYMM` and `YYYY-MM-DD`
- **Auto-set not detected in dialog** — dialog checked for legacy flag file instead of Rust config value
- **Security patch toggle resetting** — `hydrateUI()` used camelCase config keys but Rust serializes snake_case
- **Custom interval input not discoverable** — added pulse animation so users notice the editable field
- **VBMeta hash stale after reboot** — `extract()` returned the persisted file without checking the live `ro.boot.vbmeta.digest` property; now always reads the property first and updates the file if the digest has changed

### Install
- **Legacy module auto-removal** — `TA_utl` and `.TA_utl` are now detected and tagged for removal during install before conflict checks run
- **Version gate removal** — removed minimum APatch/KSU version checks from `customize.sh`

---

## v5.3.0 (2026-03-06)

### Ground-Up Rust Rewrite

The entire backend has been rewritten from scratch in Rust. Shell scripts were too fragile — hundreds of thousands of wakeups per day, fork-per-config-read, race conditions, and cascading failures. All eliminated.

| Metric | Shell (v4.x) | Rust (v5.x) |
|---|---|---|
| Wakeups/day | 884,449 | ~100 |
| JVM spawns/day | 20,170 | ~200 |
| Processes | 6 | 1 |
| Background CPU | ~28 min/day | <1 min/day |
| Config reads | 43,200 forks/day | 0 (in-memory) |
| App detection | 10s–minutes | Instant (inotify) |

### Native Daemon
- Single `ta-enhanced` binary (4.0MB arm64, 2.7MB armv7) replaces 16 shell scripts
- Unified scheduler — keybox, security patch, health, status, automation in one process
- inotify app detection — new installs targeted instantly
- In-memory TOML config — zero fork overhead
- Proper signal handling, graceful shutdown

### CLI
- `ta-enhanced config get/set` — type-safe config with validation and clamping
- `ta-enhanced keybox fetch/validate/generate/backup` — full keybox pipeline
- `ta-enhanced security-patch set/get-latest` — engine-aware patch management
- `ta-enhanced webui-init` — batched JSON endpoint (replaces ~14 shell calls)
- `ta-enhanced conflict check` — structured conflict detection
- `ta-enhanced applist` — package enumeration with labels

### Device Keybox Generation
- ECDSA P-256 + RSA-2048 via `ring` — valid AOSP-level keybox without remote sources

### WebUI
- Batched init — single shell call, <300ms cold start
- Cache-first hydration from localStorage
- Font subset 287KB → 5KB (28 icons)
- Non-blocking external CSS via media swap
- Keybox automation panel — 6 source cards, interval chips (1h–7d), custom input with min/hr/day toggle
- About dialog rebranded — Enginex0 author, SuperPowers Telegram, full credits
- Debounced health refresh (30s throttle)
- SukiSU theme caching

### Shell Elimination
- 16 scripts deleted, `service.sh` reduced to daemon launcher
- Config migrated from `enhanced.conf` to `config.toml` (auto-migration on first boot)
- Module ID: `TA_utl` → `TA_enhanced`

### Bug Fixes
- Daemon double-init panic after daemonize fork (tracing subscriber inherited by child)
- All 16 audit bugs from v4.9 eliminated by architectural change

---

## v4.9-auto (2026-02-13)

### Features
- **Volume key install-time selection** — press Vol- during flash to disable automatic target.txt population. Manual mode seeds only GMS/GSF/Vending so attestation works out of the box; Vol+ or 10s timeout defaults to full automation. Respects `automation_target_enabled` in config (`2661584`)
- **Build script** — `package.sh` auto-bumps versionCode and builds the release ZIP in one command (`8648fa7`)

### Fixes
- **78-bug codebase audit** — supervisor kill chain (PID tracking, SIGTERM cascade via process group, exponential backoff 1-60s), property race elimination (prop.sh sole VBMeta authority), keybox pipeline hardening (staged decode, 6-point validation, TOCTOU fix, rotating backup, 60s minimum interval), health monitor circuit breaker (10 max restarts, resets on recovery), atomic PID files, TLS enforced on wget, POSIX bashism cleanup (`8a8ada9`)
- **Keybox preserved on failed fetch** — no-network boot was falling through to bundled AOSP keybox, overwriting a valid device-specific one. Guard now preserves existing keybox; bundled fallback only fires on fresh install (`3089524`)
- **WebUI CLI sourcing** — manual keybox fetch was hanging because keybox_manager.sh lost logging.sh/utils.sh sourcing, causing `read_config` undefined. Restored sourcing for all CLI entry points (`3089524`)
- **MODPATH collision** — get_extra.sh manager scripts inherited `common/` subdirectory path instead of module root, causing `common/common/` sourcing failures on `--fetch-keybox-now`, `--set-security-patch-now`, `--check-conflicts` (`3089524`)
- **WebUI uninstall** — module.prop was restored to `MODPATH` (common/) instead of `MODDIR` (module root), so ksud/apd couldn't find the module to remove (`4367b7b`)
- **Bounded post-fs-data wait** — KernelSU kills post-fs-data after 10s; unbounded while loop on slow /data mounts capped at 8 iterations (`ae03ca4`)
- **Strict manager detection** — loose `[ "$APATCH" ]` matched any non-empty string; aligned to `[ "$APATCH" = "true" ]` (`ae03ca4`)
- **WebUI input validation** — innerHTML replaced with textContent for app names, hex validation on boot_hash input, shell metacharacter stripping on security patch values, config key/value whitelisting against sed injection (`08a004a`, `8a8ada9`)

### Performance
- **Cache-first app list** — localStorage renders instantly on subsequent opens with stale-while-revalidate background refresh. `fetchAppList`/`loadTranslations`/`getBasePath` fire in parallel instead of waterfall. Generation counter prevents stale writes (`3e9063c`)

### Refactoring
- **Consolidated read_config()** — was defined in 5 files with subtly different behavior; unified in utils.sh with `cut -f2-` (handles values containing `=`), trim, and file existence check. Removed duplicates from keybox_manager.sh, security_patch_manager.sh, status_monitor.sh, health_check.sh (`4a00a14`)

## v4.8-auto (2026-02-07)

### Fixes
- **VBHash extraction broken on some devices** — APK-based attestation extraction fails silently on certain OEM/Android combos (reported on OnePlus 12 / ColorOS 16 / Android 16). VBHash now captured directly from `ro.boot.vbmeta.digest` at install time — instant, zero dependencies, works on all AVB-enabled devices. APK method retained as last-resort fallback (#2) (`3ed7269`)
- **VBHash hex validation** — all extraction paths regex-validate the hash as exactly 64 lowercase hex characters, rejecting malformed or empty values before persisting

### Improvements
- **Discoverable log directory** — logs moved from hidden `/data/adb/tricky_store/.automation/` to `/data/adb/Tricky-addon-enhanced/logs/`
- **Separated concerns** — log files and automation state (exclude patterns, known packages, daemon PID) no longer share the same directory

### Internals
- VBHash extraction refactored into three composable functions: `extract_from_property()`, `extract_from_apk()`, `persist_and_apply_hash()`
- `LOG_BASE_DIR` updated across 8 files
- Uninstall cleanup covers both old and new directory paths

## v4.7-supervisor (2026-02-07)

### Features
- **Native process supervisor** — single compiled binary (5.6KB ARM64, 3.9KB ARM32) manages all 5 background processes via fork/wait/restart, based on TEESimulator's supervisor.cpp pattern (`022ee63`)
- **Full self-healing** — daemon, health monitor, status monitor, keybox loop, and security patch loop all restart within 1s of silent death
- **PR_SET_PDEATHSIG** — child processes auto-killed if supervisor dies, preventing orphaned processes
- **Root manager cache refresh** — force-stops KSU/Magisk/APatch manager after new app is added to target.txt, ensuring WebUI shows fresh package list immediately
- **Uninstall-aware exit** — supervised scripts exit with code 42 on module removal; supervisor stops cleanly without restart loops

### Internals
- Replaced shell supervisor (supervisor.sh) with native ARM64/ARM32 binary
- Extracted shared utility functions to `common/utils.sh`
- service.sh reduced from 257 to 141 lines
- Uninstall signal touches both `/data/adb/modules/TA_utl/remove` and `.TA_utl/remove` paths

## v4.6-auto (2026-02-06)

### Features
- **4-source keybox failover** — Yurikey → Upstream → IntegrityBox → bundled backup, with XML validation and custom keybox protection
- **Aggressive boot-time fetch** — keybox and security patch retry up to 10 times with 3s backoff after network ready
- **Install-time patch upgrade** — security patch dates fetched from Google during module flash, not just at boot
- **Automatic security patch updates** — detects attestation engine variant (James, Standard, Legacy) and sets system/boot/vendor dates at configurable intervals
- **VBHash spoofing** — one-time extraction via camouflaged APK, persists to `/data/adb/boot_hash`, 15 properties spoofed as locked bootloader
- **TEESimulator health monitor** — polls attestation engine every 10s with 5s grace period, auto-restarts on crash
- **Live status monitor** — module description updates every 30s with real-time app count, keybox source, patch level, VBHash state
- **Live target watcher** — WebUI polls target.txt every 3s and hot-inserts app cards without full reload
- **Dynamic engine detection** — auto-detects TEESimulator vs TrickyStore from daemon `--nice-name` parameter
- **Module conflict detection** — 19 conflicting modules detected at install and boot
- **Unified logging** — centralized 1MB rotation across 13 scripts

### Fixes
- **Status monitor app count** — whitespace/CR normalization; count now matches WebUI (`8c5dbf5`)
- **Monitor cleanup on uninstall** — status monitor and health check detect the `remove` flag within 30s, restore original description, exit cleanly (`8c5dbf5`)
- **TEESimulator variant misdetection** — versionCode-based detection now correctly identifies standard variant (`f14b5b4`)
- **Security patch fallback regression** — auto-update no longer overwrites valid dates with stale ROM values when Google fetch fails
- **Config preservation** — keybox and `enhanced.conf` survive reinstalls and engine switches (`0f6a581`)

### WebUI
- Modern glass morphism design with AMOLED-friendly dark gradients
- Health status banner with live attestation engine state
- Redesigned Save FAB and Uninstall button with glass morphism
- Scroll indicator in settings panel
- Automation settings bottom sheet
- 6 accent color presets with random selection
- 23 languages with RTL support

## v4.5-auto (2026-02-03)

### Features
- **Live status monitor** — module.prop description updates every 30s with active app count, keybox source, and patch level (`999e8a8`)
- **Live target watcher** — WebUI watches target.txt changes with event delegation and exec timeout (`54b50ab`)
- **Dynamic engine detection** — health monitor auto-detects TEESimulator vs TrickyStore at runtime (`ab23edd`)
- **Config preservation** — keybox and enhanced.conf preserved across reinstalls and engine switches (`0f6a581`)
- **Playwright test suite** — dynamic mock environment for WebUI testing (`db790de`)

### Fixes
- **TEESimulator misdetected as legacy** in security patch pipeline (`f14b5b4`)

## v4.4-auto (2026-02-02)

### Features
- **VBHash one-time persistence** — extracted hash persisted to `/data/adb/boot_hash`, APK camouflaged as `com.ceco.gravitybox.unlocker` (`e934494`, `6ca7ab7`)
- **TEESimulator health monitor** — background supervisor polls attestation engine, auto-restarts on crash (`a465142`)
- **WebUI automation integration** — automation.js backend integration, elite toast notifications with glass morphism (`92dc9cd`)
- **VBHash extraction** — extracts `verifiedBootHash` from KeyStore attestation extension (OID `1.3.6.1.4.1.11129.2.1.17`) via temp APK (`92dc9cd`)

### Fixes
- **Boot hash display** — sed filter was inverted, showing PEM comments instead of hash (`ed9aa68`)
- **GPU performance** — removed 12 backdrop-filter blur() calls and 3 infinite CSS animations (`ed9aa68`)

### WebUI
- Modern glass morphism overhaul with AMOLED dark gradients (`c3b5ab6`)
- 29 bug fixes including bounds checks, null guards, race conditions (`97d2b97`)
- 6 accent color presets with randomization toggle
- Signature rotating rainbow ring logo
- Light/dark mode, RTL, accessibility (focus states, ARIA)

## v4.3-auto (2026-01-20)

### Initial Release
- **Dual-source keybox** with 4-source failover (Yurikey → Upstream → IntegrityBox → Bundled)
- **Auto security patch updates** — system/boot/vendor dates from Google
- **Module conflict detection** — 16 regular + 1 aggressive + 2 app conflicts
- **WebUI** with automation settings
- **POSIX sh / BusyBox ash** compatible — no bashisms, properly quoted, injection-safe
- Supports Magisk, KernelSU (32234+), APatch (11159+)

---
