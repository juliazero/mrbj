## 🚀 Release: TEESimulator v3.2 (Hotfix)

TEESimulator v3.2 is rolling out today as an hotfix. This release was pushed ahead of schedule because our recent GitHub build artifacts were expiring, and a severe Google Play Services (GMS) log flooding bug was significantly degrading device performance for many users. 📱⚡

⚠️ **Important Development Update:**
*   **Detections:** Due to time constraints, we haven't patched *all* the new detections currently in the wild. However, this hotfix does successfully address a few critical detection points. 🛡️
*   **LSPosed ➡️ Vector:** I (JingMatrix) am currently dedicating my efforts to refactoring LSPosed into **Vector**. Consequently, TEESimulator's development pace will temporarily slow down. Please stay tuned and monitor the commit history to follow along with our progress! 🛠️👀

Here is the changelog for this release:

🔧 **Stability & Performance**
*   **🛑 GMS Log Flooding:** Mitigated massive log spam and battery drain (especially noticeable on WearOS or Nearby Share) by safely bypassing `list` hooks for GMS.
*   **💥 Binder Leak Resolved:** Squashed a critical strong reference memory leak during binder transaction interception that caused random crashes.

🛡️ **Anti-Detection & Emulation**
*   **🔑 Pre-Existing Key Override:** TEESimulator now detects and replaces hardware keys that apps managed to request *before* the module was installed, ensuring all future operations remain under control.
*   **🧩 Accurate `module_hash`:** Completely aligned the APEX module hashing logic with the official Android `keystore2` implementation (including direct `/apex` filesystem scanning and exact ASN.1 DER sorting).
*   **📜 Certificate `KeyUsage` Fix:** Dynamically sets X.509 `KeyUsage` bits based on the actual key purpose to properly adhere to Android HAL specifications *(the first contribution of @Enginex0!)*.
*   **⚙️ Core Improvements:** Enhanced KeyMint logging (parsing `ORIGIN`, `OS_VERSION`, etc.) and fixed Parcel position resets for cleaner internal error handling.
