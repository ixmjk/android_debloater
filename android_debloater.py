import os
import subprocess

from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.uic import loadUi


class App(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        """Initializes the Android Debloater class."""
        super().__init__(*args, **kwargs)
        self.script_location = os.path.dirname(__file__)  # ui file directory
        self.ui_file = "android_debloater.ui"
        self.ui = loadUi(os.path.join(self.script_location, self.ui_file), self)

        self.ui.setWindowTitle("Android Debloater")

        self.ui.table_1.setColumnCount(2)
        self.ui.table_1.setHorizontalHeaderLabels(("", "Package Name"))
        self.ui.table_1.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.ui.table_1.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.table_1.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.table_2.setColumnCount(2)
        self.ui.table_2.setHorizontalHeaderLabels(("", "Package Name"))
        self.ui.table_2.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.ui.table_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.table_2.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.ui.btn_uninstall.clicked.connect(self.uninstall)
        self.ui.btn_reinstall.clicked.connect(self.reinstall)

        self.ui.action_import.triggered.connect(self.import_config)
        self.ui.action_export.triggered.connect(self.export)
        self.ui.action_exit.triggered.connect(QApplication.quit)
        self.ui.action_refresh.triggered.connect(self.refresh)
        self.ui.action_reboot.triggered.connect(self.reboot)
        self.ui.action_help.triggered.connect(self.show_help)
        self.ui.action_about.triggered.connect(self.show_about_dialog)

        self.statusbar_label = QLabel("")
        self.ui.statusbar.addWidget(self.statusbar_label)

    def closeEvent(self, event) -> None:
        """Closes the application's main window when the close event is triggered.

        Args: event (QCloseEvent): The close event that triggered the method.

        Returns: None

        Raises: None

        Description: This method is called when the user tries to close the main window of the application. It prompts a confirmation dialog asking whether the user wants to quit.
        If the UI is not enabled, it means that a process is still running and the close event is ignored.
        Instead, an information dialog is shown to inform the user that they should wait until the current process is finished before closing the application.
        """
        if self.ui.isEnabled():
            respose1 = QMessageBox.question(
                self, "Quit Confirmation", "Are you sure you want to quit?"
            )
            if respose1 == QMessageBox.Yes:
                QApplication.quit()
        else:
            event.ignore()
            QMessageBox.information(
                self,
                "Process is still running",
                "Please wait until the current process is finished.",
            )

    def show(self) -> None:
        """Displays the current state of the object and performs a refresh after a 1-second delay.

        Args: self: The object to be displayed and refreshed.

        Returns: None
        """
        super().show()
        QtTest.QTest.qWait(1000)
        self.refresh()

    def refresh(self) -> None:
        """Updates the UI and refreshes the connected devices.

        This method is responsible for refreshing the UI and updating the connected devices information.
        It disables the UI, performs some operations to retrieve data, and then updates the UI with the new information.
        If there are no connected devices, it displays an error message.

        Parameters:
            None

        Returns:
            None
        """
        try:
            self.ui.setEnabled(False)
            self.update_statusbar("Detecting connected devices...")
            QtTest.QTest.qWait(1000)
            self.fill_table(self.get_installed_packages_list(), self.ui.table_1)
            self.fill_table(self.get_removed_packages_list(), self.ui.table_2)
            self.update_statusbar_with_device_info()
        except:
            self.update_statusbar("No connected devices.")
            QMessageBox.information(self, "Error", "No Connected Devices.")
        finally:
            self.ui.setEnabled(True)

    def update_statusbar(self, message: str) -> None:
        """Updates the status bar label with the given message.

        Args: message (str): The message to display in the status bar.

        Returns: None
        """
        self.statusbar_label.setText(f"   {message} ")

    def get_installed_packages_list(self) -> list:
        """Retrieves the list of installed packages on a device connected via ADB.

        Returns:
            list: A sorted list of installed package names.

        Raises:
            subprocess.CalledProcessError: If the adb shell command fails to execute.
        """
        output = str(
            subprocess.check_output("adb shell pm list packages", shell=True)
        ).split("\\r\\")
        installed_packages_list = [i.split(":")[-1] for i in output if ":" in i]
        return sorted(installed_packages_list)

    def get_removed_packages_list(self) -> list:
        """Returns a list of removed packages from the Android device.

        Uses the ADB command `adb shell pm list packages -u` to retrieve a list of all packages with update flags from the device.
        Compares the extracted package names with the list of installed packages obtained from the get_installed_packages_list method.
        Returns the sorted list of removed packages by finding the difference between all packages and installed packages.

        Returns: list: A sorted list of package names that have been removed from the device.
        """
        output = str(
            subprocess.check_output("adb shell pm list packages -u", shell=True)
        ).split("\\r\\")
        all_packages_set = {i.split(":")[-1] for i in output if ":" in i}
        installed_packages_set = set(self.get_installed_packages_list())
        return sorted(list(all_packages_set - installed_packages_set))

    def fill_table(self, data: list, table: QTableWidget) -> None:
        """Fills a table widget with data.

        Args:
            data (list): A list of strings representing the data to be displayed in the table.
            table (QTableWidget): The table widget to be filled with data.

        Returns:
            None
        """
        row_count = len(data)
        table.setRowCount(row_count)
        for row in range(row_count):
            # first column contains checkboxes
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            table.setItem(row, 0, checkbox_item)
            # second column contains package names
            package_name_item = QTableWidgetItem(data[row])
            table.setItem(row, 1, package_name_item)

    def update_statusbar_with_device_info(self) -> None:
        """Updates the status bar with device information.

        This method retrieves the device model,
        installed packages count, and removed packages count,
        and then calls the update_statusbar method to update the status bar with this information.

        Args:
            None

        Returns:
            None
        """
        device_model = self.get_device_model()
        installed_count = self.ui.table_1.rowCount()
        removed_count = self.ui.table_2.rowCount()
        self.update_statusbar(
            f"Connected Device: {device_model}   |   Installed Packages: {installed_count}    |   Removed Packages: {removed_count}"
        )

    def get_device_model(self) -> str:
        """Returns the model of the connected device.

        This method uses the `adb shell getprop ro.product.model` command to retrieve the device model.
        The output is then decoded and stripped of any leading or trailing white spaces.
        The resulting device model is returned.

        Returns:
            str: The model of the connected device.
        """
        device_model = (
            subprocess.check_output("adb shell getprop ro.product.model")
            .decode()
            .strip()
        )
        return device_model

    def import_config(self) -> None:
        """Imports a configuration file and updates the table accordingly.

        This method prompts the user to select a configuration file in the '*.cfg' format.
        If a file is selected, it reads the file line by line, searches for matches in the
        'table_1' widget, and selects the corresponding checkboxes. After importing the
        configuration, a message box is displayed to inform the user about the import status.

        Returns:
            None
        """
        row_count = self.ui.table_1.rowCount()
        if row_count:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select a file config file:", "", "Config file (*.cfg)"
            )
            if file_path:
                counter = 0
                with open(file_path, "r") as file:
                    for line in file:
                        for row in range(self.ui.table_1.rowCount()):
                            package_item = self.ui.table_1.item(row, 1)
                            checkbox_item = self.ui.table_1.item(row, 0)
                            if package_item.text() == line.strip():
                                checkbox_item.setCheckState(2)
                                counter += 1
                QMessageBox.information(
                    self,
                    "Import Successful",
                    f"Config imported successfully!\n{counter} Packages selected.",
                )
        else:
            QMessageBox.information(self, "Error", "No Connected Devices.")

    def export(self) -> None:
        """Exports selected packages as a config file.

        This method exports the selected packages as a configuration file (.cfg).
        It prompts the user to choose the location and name of the file, and then
        writes the selected packages into the file.

        Returns:
            None

        Raises:
            None
        """
        checked_packages = sorted(self.retrieve_checkbox_values(self.ui.table_1))
        if checked_packages:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export selected packages as a config file:",
                "",
                "Config file (*.cfg)",
            )
            if file_path:
                with open(file_path, "w") as file:
                    for package in checked_packages:
                        file.write(package + "\n")
                QMessageBox.information(
                    self,
                    "Export Successful",
                    "Selected options were exported successfully!",
                )
        else:
            QMessageBox.information(self, "Error", "No packages have been selected.")

    def reboot(self) -> None:
        """Prompts the user to reboot the device and performs the reboot if confirmed.

        This method displays a message box to the user asking if they want to reboot the device. If the user confirms,
        the method executes the "adb shell reboot" command to reboot the device. If there are no connected devices or
        an error occurs during the process, an error message box is shown.

        Raises:
            Exception: If an error occurs during the process.

        Returns:
            None
        """
        try:
            respose1 = QMessageBox.question(
                self, "Rebooting Device", "Reboot the device now?"
            )
            if respose1 == QMessageBox.Yes:
                output = subprocess.check_output("adb shell reboot")
                QMessageBox.information(self, "Error", "No Connected Devices.")
        except:
            QMessageBox.information(self, "Error", "No Connected Devices.")

    def show_help(self) -> None:
        """
        Opens the URL "https://github.com/ixmjk/android_debloater" in the default web browser.

        This method is used to provide help to the user by directing them to the GitHub repository for the Android Debloater tool.

        Parameters:
            self (object): The instance of the class where this method is being called.

        Returns:
            None
        """
        QDesktopServices.openUrl(QUrl("https://github.com/ixmjk/android_debloater"))

    def show_about_dialog(self) -> None:
        """
        Displays an about dialog box with information about the Android Debloater application.

        Returns:
            None

        Raises:
            None
        """
        about_text = (
            "Android Debloater\n"
            "Version: 1.0\n"
            "Author: github.com/ixmjk\n"
            'Description: "Unlock Your Android Phone\'s Potential, Say Goodbye to Bloatware!"'
        )

        QMessageBox.about(self, "About Android Debloater", about_text)

    def uninstall(self) -> None:
        """
        Uninstalls selected packages from the Android device.

        Retrieves the checked packages from the UI table and prompts the user with a confirmation dialog.
        If the user confirms, a warning message is displayed to ensure the user is aware of the risks.
        If the user confirms again, the UI is disabled and each package is uninstalled using the `uninstall_package` method.
        After all selected packages are uninstalled, an information message is displayed and the UI is refreshed.
        If no packages are selected, an error message is displayed.
        If there are no connected devices, an error message is displayed.

        Raises:
            None

        Returns:
            None
        """
        try:
            checked_packages = self.retrieve_checkbox_values(self.ui.table_1)
            if checked_packages:
                package_list_text = "\n".join(checked_packages)
                respose1 = QMessageBox.question(
                    self,
                    "Uninstalling...",
                    f"The following packages have been selected and will be uninstalled:\n\n{package_list_text}\n\nAre you sure you want to continue?",
                )
                if respose1 == QMessageBox.Yes:
                    warning_message = (
                        "Warning:\n"
                        "Uninstalling packages that you are unsure about or that are system packages "
                        "might result in a bootloop.\n"
                        "Are you still sure you want to continue?"
                    )
                    response2 = QMessageBox.question(
                        self, "Important Note!", warning_message
                    )
                    if response2 == QMessageBox.Yes:
                        self.ui.setEnabled(False)
                        for package in checked_packages:
                            self.uninstall_package(package)
                        QMessageBox.information(
                            self,
                            "Uninstall Completed",
                            "All selected packages uninsatlled successfully!",
                        )
                        self.refresh()
            else:
                QMessageBox.information(
                    self, "Error", "No packages have been selected."
                )
        except:
            QMessageBox.information(self, "Error", "No Connected Devices.")
        finally:
            self.ui.setEnabled(True)

    def retrieve_checkbox_values(self, table: QTableWidget) -> list:
        """Retrieves the values of checked checkboxes from a table.

        Args:
            table (QTableWidget): The table widget containing checkboxes.

        Returns:
            list: A list of package names corresponding to the checked checkboxes.
        """
        checked_packages = []
        for row in range(table.rowCount()):
            checkbox_item = table.item(row, 0)
            if checkbox_item.checkState() == Qt.CheckState.Checked:
                checked_packages.append(table.item(row, 1).text())
        return checked_packages

    def uninstall_package(self, package_name: str):
        """Uninstalls a package from the device using adb shell command.

        Args:
            package_name (str): Name of the package to uninstall.

        Returns:
            None: This method doesn't return anything.

        Raises:
            subprocess.CalledProcessError: If the adb shell command fails.

        Note:
            This method updates the status bar with the uninstallation progress and waits for 2 seconds after uninstallation.

        """
        self.update_statusbar(
            f"Do not disconnect the device!   |   [+] Uninstalling {package_name}"
        )
        subprocess.check_output(f"adb shell pm uninstall -k --user 0 {package_name}")
        QtTest.QTest.qWait(2000)

    def reinstall(self) -> None:
        """Reinstalls selected packages.

        This method is responsible for reinstalling the selected packages.
        It retrieves the selected packages from the table, prompts the user for confirmation, and then proceeds with the reinstallation process.
        Finally, it updates the UI and displays relevant messages to the user.

        Args: self: The instance of the class that this method belongs to.

        Returns: None
        """
        try:
            checked_packages = self.retrieve_checkbox_values(self.ui.table_2)
            if checked_packages:
                package_list_text = "\n".join(checked_packages)
                respose1 = QMessageBox.question(
                    self,
                    "Reinstalling...",
                    f"The following packages have been selected and will be reinstalled:\n\n{package_list_text}\n\nAre you sure you want to continue?",
                )
                if respose1 == QMessageBox.Yes:
                    self.ui.setEnabled(False)
                    for package in checked_packages:
                        self.reinstall_package(package)
                    QMessageBox.information(
                        self,
                        "Reinstall Completed",
                        "All selected packages have been reinstalled!",
                    )
                    self.refresh()
            else:
                QMessageBox.information(
                    self, "Error", "No packages have been selected."
                )
        except:
            QMessageBox.information(self, "Error", "No Connected Devices.")
        finally:
            self.ui.setEnabled(True)

    def reinstall_package(self, package_name: str):
        """Reinstalls a package on the device using adb shell command.

        Args:
            package_name (str): The name of the package to be reinstalled.

        Returns:
            None

        Raises:
            subprocess.CalledProcessError: If the adb shell command fails.

        Notes:
            - This method updates the status bar with the current reinstallation process.
            - It uses the adb shell command 'pm install-existing' to reinstall the package.
            - After the reinstallation, it waits for 2 seconds before returning.
        """
        self.update_statusbar(
            f"Do not disconnect the device!  |  [+] Reinstalling {package_name}"
        )
        subprocess.check_output(f"adb shell pm install-existing {package_name}")
        QtTest.QTest.qWait(2000)


def main() -> None:
    """Main function to run the application."""
    app = QApplication([])
    widget = App()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
