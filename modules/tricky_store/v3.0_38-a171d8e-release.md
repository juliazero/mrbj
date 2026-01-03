TEESimulator 3.0 is a significant update focused on powerful new configuration options, major improvements to stealth, and enhanced stability.

#### ✨ **Highlights & New Features**

*   **🎯 Per-App Security Patch Configuration**: Gain ultimate control by setting security patch levels on a per-package basis. Define a global default in `security_patch.txt` and override it for specific apps like `[com.google.android.gms]`. Moreover, your configuration is now alive! Use the `today` keyword to always report the current date, or create rolling dates with templates like `YYYY-MM-05`. Be sure to check README for more details.
*   **🕰️ Full Software Emulation on Android 11**: We've implemented a complete, software-based key generation and attestation flow for the legacy `IKeystoreService` API, bringing full emulation capabilities to older devices.

#### 🛡️ **Stealth & Evasion Upgrades**

*   **⛓️ Consistent Certificate Signatures**: Say goodbye to a major detection vector in `icu.nullptr.nativetest`. Patched certificates are now cached, ensuring that every request for a key returns a byte-for-byte identical certificate, just like a real TEE.
*   **🔑 Authentic Device Properties**: To appear more genuine, the simulator now sources and uses your device's real `verifiedBootHash` and `moduleHash`, moving away from placeholder values.
*   **📜 Structurally Sound Certificates**: The patching logic has been rewritten to be less intrusive. It now modifies the attestation extension in-place, preserving the original order of other extensions and preventing duplicates to avoid suspicion.

#### 🐛 **Bug Fixes & Reliability**

*   ✅ **Robust Crypto Engine**: Fixed critical crashes related to cryptographic provider conflicts. The signing logic is now more explicit and the KeyBox parser is more resilient against malformed files.
*   ➡️ **Improved Compatibility**: Resolved a native crash on Android 11 devices.

#### 🚀 **The Road Ahead**

Our work to fix detection vectors and provide full support for TEE-broken devices and Android 10/11 is ongoing. We welcome your feedback! Please **report any issues** or **contribute a pull request** on our GitHub.
