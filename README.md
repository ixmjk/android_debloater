# Android Debloater

**Android Debloater** is a program written in Python that offers a user-friendly interface to streamline the process of managing installed packages on Android devices. Android Debloater operates without requiring root access, making it a convenient and safe option for optimizing your device. By utilizing the power of [ADB (Android Debug Bridge)](https://developer.android.com/tools/adb) and [PyQt5](https://pypi.org/project/PyQt5/), this tool allows users to easily remove bloatware, enhance device performance, and create/share debloat configs with others.

![python_FOKz2rIzqH](https://github.com/ixmjk/android_debloater/assets/66163456/3f43c8ff-9a8e-4965-8606-c8eb97ab4238)

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [ADB Installation](#adb-installation)
  - [Dependencies](#dependencies)
  - [Running the Program](#running-the-program)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites
- Python 3.9 or later
- ADB (Android Debug Bridge) installed on your computer

### ADB Installation
#### Windows
1. Download the [Minimal ADB and Fastboot Installer](https://forum.xda-developers.com/t/tool-minimal-adb-and-fastboot-2-9-18.2317790/).
2. Run the installer and follow the on-screen instructions.
3. Add the ADB installation directory to your system's PATH.

#### Linux
1. Open a terminal.
2. Install ADB using your package manager:
```
sudo apt update && sudo apt install adb
```

### Dependencies
PyQt5: Install it using pip:
```
pip install pyqt5
```

### Running the Program
1. Clone this repository to your local machine:
```
git clone https://github.com/ixmjk/android_debloater
```
2. Navigate to the project directory:
```
cd android_debloater
```
3. Run the program:
```
python android_debloater.py
```

## Usage

**Note: Android Debloater _does not_ require root access.**

1. **Enable USB Debugging on Your Android Phone:**
   Before using Android Debloater, make sure USB debugging is enabled on your Android phone. To enable it:
   - Navigate to your phone's **Settings**.
   - Go to **About Phone** > **Software Information**.
   - Tap on the **Build Number** multiple times until you see a message indicating developer mode is enabled.
   - Go back to the main **Settings** screen and enter the newly enabled **Developer Options**.
   - Enable **USB Debugging**.

2. **Connect Your Phone to Your PC:**
   - Connect your Android phone to your PC using a USB cable.

3. **Run Android Debloater:**
   - Open a terminal or command prompt.
   - Navigate to the directory where you have the Android Debloater files.
   - Run the command: `python android_debloater.py`

4. **Allow USB Debugging:**
   - After running the program, you might see a pop-up on your Android phone that says "Allow USB debugging."
   - Select "**Always allow from this computer**" and then tap "**Allow**."

5. **Refresh Device List (If Needed):**
   - If you encounter the error message "No Connected Devices," click **OK**.
   - In the program's menu, go to **View** > **Refresh**, or you can use the shortcut `Ctrl + R` to refresh.

6. **View and Manage Packages:**
   - Once your device is connected, you will see a list of installed and removed packages.
   - The **Installed Packages** tab displays the packages that arecurrently installed on your device, while the **Removed Packages** tab lists previously removed packages.

7. **Uninstall Packages:**
   - In the **Installed Packages** tab, select the packages you wish to remove or uninstall from your Android device.
   - Click on the "**Uninstall Selected**" button to initiate the removal process.

8. **Reinstall Packages (If Needed):**
   - In the **Removed Packages** tab, you can select previously removed packages that you want to reinstall.
   - Click on the "**Reinstall Selected**" button to restore the selected packages.

9. **Create and Import Debloat Config:**
   - A debloat config is a configuration file that contains a list of package names, which are considered safe to remove from an Android device. Here is a [sample debloat config](https://github.com/ixmjk/android_debloater/blob/main/sample_config.cfg).
   - Android Debloater offers a convenient way to debloat your phone by creating or importing a debloat configuration.
   - To create a debloat config, select packages you consider safe to remove in the **Installed Packages** tab, then click  **File** > **Export Selected...**, or you can use the shortcut `Ctrl + E` to export.

   - To import a debloat config, click **File** > **Import Config...**, or you can use the shortcut `Ctrl + I` to import.


## Disclaimer
Android Debloater is a tool designed to help users manage their Android device's packages. While efforts have been made to ensure the safety and functionality of this tool, it's important to note the following:

- **Use at Your Own Risk:** The use of Android Debloater is at your own risk. The author of this tool is not responsible for any damage, data loss, or other negative outcomes that may result from using this tool on your Android device.

- **Selecting Safe Packages:** When using Android Debloater to remove packages, it's crucial to exercise caution and only select packages that you are confident are safe to remove. Removing critical system packages could potentially lead to device instability or unintended consequences.

- **Backup Your Data:** Before making any significant changes to your Android device, it's recommended to back up your data and create a system backup. This can help you restore your device to a working state if any issues arise.

- **Debloat Configs:** When creating or importing debloat configs, ensure that you understand the packages included in the configuration. Packages listed in a debloat config are intended to be safe for removal, but mistakes or unforeseen issues can still occur.

- **Read Documentation:** Familiarize yourself with the documentation provided by the tool to understand its features, limitations, and best practices for usage.

By using Android Debloater, you acknowledge and accept these disclaimers. If you have any concerns or questions about using the tool, please seek assistance from knowledgeable sources or post an issue on the project's GitHub repository before proceeding.

## Contributing
Contributions are welcome! If you'd like to contribute to Android Debloater, please follow the standard GitHub fork and pull request workflow.

## License
This project is licensed under the [MIT License](LICENSE).

---

By using Android Debloater, you can easily enhance the performance of your Android device by removing unnecessary packages and bloatware. Enjoy a cleaner and faster smartphone experience! If you encounter any issues or have suggestions for improvement, please feel free to open an issue on the GitHub repository.
