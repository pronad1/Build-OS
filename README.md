# ShopnilOS: A Lightweight Custom Linux Distribution & System Management Suite

## 1. Introduction
This project demonstrates the practical application of Operating System principles through the development of a custom, lightweight Linux distribution named ShopnilOS, alongside a suite of system administration and process monitoring tools. ShopnilOS is built by customizing the ArchLinux ISO [3] to create a bare-minimum live environment populated only with essential modern applications. It utilizes archinstall for a streamlined, script-free base installation, ensuring a lightweight footprint. The environment is graphical-ready, customized with the Hyprland Wayland compositor, SDDM, Waybar, Rofi, and Waypaper.

To bridge the gap between low-level system configuration and user-space process management, complementary tools were developed: Archmate for comprehensive system administration, a Chaotic AUR installer script, and Tree_tasker, a Python and PySide6-based graphical task manager with web integration for advanced process hierarchy visualization. For automated setups, dotfiles can be integrated, as well as third party providers like, END4 [1], ML4W [2] scripts.

## 2. Objectives
1. To understand Linux system architecture by customizing and building a bootable Arch-based ISO [3], a rolling based distributions.
2. To customize a window manager with lua scripts and custom shell scripts.
3. To automate core OS maintenance tasks including package, user, repository, and configuration management.
4. To visualize and monitor system resource allocation (CPU, RAM, Disk, Network) per application in real-time.
5. To map and interactively explore parent-child process relationships (PIDs) within the operating system.
6. To allow users to use remote connections over ssh using terminal or vscode to remotely edit the operating system without any GUI.

## 3. Problem Statement
Modern operating systems often come pre-packaged with heavy, unnecessary background services (bloatware) that consume valuable hardware resources. Furthermore, traditional command-line process monitors (like top or ps) provide dense tabular data that makes it difficult for users to intuitively understand parent-child process relationships and exact resource distribution. There is a need for a streamlined, customizable OS base paired with an intuitive, visual process manager that clearly maps process hierarchies and resource bottlenecks.

## 4. Related Work
1. General-purpose Linux distributions (e.g., Ubuntu [4], Linux Mint [5]) provide functional environments but lack the minimalism required for strict resource control.
2. ArcoLinux provides minimal functionality but the project is dead now [6].
3. ArchLinux [3] doesn’t provide with any way to automate through shell scripts except for installation archinstall script.
4. On the monitoring side, tools like htop, gnome-system-monitor, or Windows Task Manager offer system overviews but often lack strict tree-based PID mapping.
5. Popular distributions delay to release applications [7], which can be crucial for development. So our approach is to make it more bleeding edge as possible.

## 5. Scope
The scope of this project is currently limited to x86_64 system architectures. The distribution, ShopnilOS, is tailored specifically for Arch-based package management (pacman, AUR). The Tree_tasker application is designed to fetch and visualize process data strictly for the local host machine, though its web interface lays the groundwork for future remote monitoring capabilities.

## 6. Methodology

### OS Building
1. **Kernel:** Linux-7.0.12 (amd64)
2. **Userspace:** GNU
3. **Package Management:** Pacman, AUR
4. **Init System (initfs):** Systemd

### System Tools
1. **OS Customization:** Archiso builder, archinstall
2. **Login Manager:** SDDM
3. **Window Management / UI:** Hyprland (Wayland)
4. **UI:** Waybar, Rofi, Waypaper
5. **Scripting & Administration:** Bash scripting (Archmate, Chaotic AUR Installer)
6. **Application Development:** Python, PySide6 (Tree_tasker), Flask (web – Tree_tasker)

## 7. Design Principles
1. The design principle is to keep the core OS live ISO as small as possible, relying on native tools like archinstall rather than custom, hard-to-maintain installation scripts like calamere.
2. To separate system administration (Archmate) from real-time process monitoring (Tree_tasker) to ensure system stability. Users can also write their own scripts for administration.
3. Use tree structures and pie charts to translate raw OS process data into easily digestible visual information.

## 8. Limitations
1. Currently this project is built only for x86_64 (64 bit processors). 32 bit or ARM CPU won’t work on it.
2. Wayland may not work properly on NVIDIA GPU with some window managers [8].

## 9. Future Plans
For Tree_tasker, plans include adding the capability to terminate or pause specific processes directly from the interactive web interface, and expanding the data polling to support distributed containerized environments (like Docker metrics).

## 10. Conclusion
So we can conclude that our project results in a fully functional operating system, installable via custom user scripts or archinstall from official Arch repository. The administration scripts (Archmate and Chaotic AUR Installer) successfully automate tedious system updates, cleanups, and user management. Finally, the Tree_tasker application accurately polls kernel data to display real-time parent-child process trees and accurately renders CPU, RAM, Disk, and Network usage into interactive pie charts across both desktop and web interfaces.

## 11. References
[1] https://github.com/end-4/dots-hyprland
[2] https://www.ml4w.com/
[3] https://archlinux.org/
[4] https://ubuntu.com/
[5] https://www.linuxmint.com/
[6] https://itsfoss.com/news/arcolinux-discontinued/
[7] https://ubuntu.com/project/docs/release-team/release-cycle/
[8] https://arewewaylandyet.com/
