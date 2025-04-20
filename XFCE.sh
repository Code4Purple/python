#!/bin/bash

# Script to install XFCE and LightDM on Arch Linux
echo "Starting the installation of XFCE desktop environment..."

# Update the system
echo "Updating the system..."
sudo pacman -Syu --noconfirm

# Install XFCE and XFCE goodies
echo "Installing XFCE desktop environment..."
sudo pacman -S --noconfirm xfce4 xfce4-goodies

# Install LightDM (Display Manager) and its greeter
echo "Installing LightDM display manager..."
sudo pacman -S --noconfirm lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings

# Enable LightDM to start on boot
echo "Enabling LightDM service..."
sudo systemctl enable lightdm

# Start LightDM right now
echo "Starting LightDM service..."
sudo systemctl start lightdm

echo "XFCE desktop environment and LightDM have been successfully installed and configured!"