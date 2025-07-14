# Cronus Zen GPC Scripts Collection

This repository contains advanced GPC (Game Programming Code) scripts for the Cronus Zen device, featuring sophisticated aim assist patterns and a comprehensive OLED menu navigation system.

## 📁 Files Overview

### 1. `aim_assist_shapes.gpc`
Standalone aim assist script with multiple movement patterns for enhanced gaming experience.

### 2. `oled_menu_system.gpc`
Comprehensive OLED menu navigation system with multiple menu levels and settings management.

### 3. `complete_zen_system.gpc`
**⭐ RECOMMENDED** - Complete integrated system combining aim assist and OLED menu functionality.

## 🎯 Features

### Aim Assist System
- **5 Different Movement Patterns:**
  - **Circle**: Smooth circular movement around target
  - **Triangle**: Sharp triangular scanning pattern
  - **Spiral**: Expanding/contracting spiral motion
  - **Helix**: 3D helix pattern projected to 2D
  - **Scared**: Erratic, unpredictable movement pattern

### OLED Menu System
- **Multi-level Navigation**: Main menu with sub-menus
- **Real-time Settings**: Adjust values on-the-fly
- **Visual Feedback**: Blinking cursor and status indicators
- **Auto-hide Feature**: Menu automatically hides after timeout
- **Scrolling Support**: Handle menus with more items than screen space

### Advanced Features
- **Pattern Switching**: Cycle through shapes with D-pad
- **Intensity Control**: Adjust movement strength (10-100%)
- **Speed Control**: Modify pattern execution speed (1-10x)
- **Visual Status**: OLED display shows current settings
- **Activity Indicator**: Shows when aim assist is active

## 🎮 Controls

### Basic Controls
- **LT/RT**: Activate aim assist
- **Menu Button**: Toggle OLED menu on/off
- **View Button**: Quick access to settings menu

### Menu Navigation
- **D-Pad Up/Down**: Navigate menu items
- **D-Pad Left/Right**: Adjust values or navigate sub-menus
- **A/Cross**: Select/Confirm
- **B/Circle**: Back/Cancel

### Quick Controls (when menu is hidden)
- **D-Pad Up/Down**: Change aim assist shape
- **D-Pad Left/Right**: Adjust intensity
- **LT/RT**: Activate aim assist with current settings

## 🚀 Installation

1. **Download Zen Studio** from the official Cronus website
2. **Connect your Cronus Zen** via USB (PROG port)
3. **Open Zen Studio** and create a new GPC script
4. **Copy and paste** the complete script code
5. **Compile** the script (F7 or Compiler → Compile)
6. **Upload** to your Cronus Zen (F5 or Compiler → Build and Run)

## ⚙️ Configuration

### Default Settings
```
Aim Assist: Enabled
Shape: Circle
Intensity: 30%
Speed: 2x
Controller Sensitivity: 100%
Menu Timeout: 5 seconds
Auto-hide Menu: Enabled
```

### Customization
All settings can be adjusted through the OLED menu system:

**Main Menu:**
- Aim Assist → Configure aim assist settings
- Settings → General configuration
- Controller → Controller-specific settings
- Display → OLED display settings
- About → Script information

**Aim Assist Menu:**
- Enable/Disable: Toggle aim assist on/off
- Shape: Select movement pattern
- Intensity: Adjust movement strength (10-100%)
- Speed: Modify pattern speed (1-10x)

**Settings Menu:**
- Sensitivity: Controller sensitivity (50-150%)
- Auto Hide Menu: Enable/disable auto-hide
- Menu Timeout: Set timeout duration (2-10 seconds)
- Reset Settings: Restore default values

## 🔧 Technical Details

### Performance
- **Update Rate**: 50Hz (20ms intervals)
- **Memory Efficient**: Optimized for Cronus Zen's limited resources
- **CPU Load**: Designed to stay under 80% to prevent output delays

### Mathematical Functions
- **Custom Trigonometry**: Sine/cosine lookup tables for smooth patterns
- **Linear Congruential Generator**: Pseudo-random number generation
- **Clamping Functions**: Ensure values stay within safe ranges

### Pattern Details
- **Circle**: Uses sine/cosine for smooth circular motion
- **Triangle**: Three-sided scanning with linear interpolation
- **Spiral**: Expanding radius with circular motion
- **Helix**: Dual-frequency sine waves for 3D effect
- **Scared**: Random offsets with base circular motion

## 🎯 Usage Tips

### For Best Results
1. **Start with Circle pattern** - Most universally effective
2. **Adjust intensity** based on game sensitivity
3. **Lower speed** for long-range engagements
4. **Higher speed** for close-quarters combat
5. **Use Scared pattern** for unpredictable movement

### Game-Specific Recommendations
- **FPS Games**: Circle or Helix patterns, medium intensity
- **Battle Royale**: Spiral or Triangle for scanning, low intensity
- **Close Combat**: Scared pattern, high intensity
- **Sniping**: Circle pattern, very low intensity and speed

### Troubleshooting
- **Too much movement**: Reduce intensity or speed
- **Not enough effect**: Increase intensity or check LT/RT activation
- **Menu not showing**: Press Menu button, check OLED connection
- **Compilation errors**: Ensure all code is copied correctly

## 📊 Menu Structure

```
Main Menu
├── Aim Assist
│   ├── Enable/Disable
│   ├── Shape (Circle/Triangle/Spiral/Helix/Scared)
│   ├── Intensity (10-100%)
│   ├── Speed (1-10x)
│   └── Back
├── Settings
│   ├── Sensitivity (50-150%)
│   ├── Auto Hide Menu (ON/OFF)
│   ├── Menu Timeout (2-10s)
│   ├── Reset Settings
│   └── Back
├── Controller
│   ├── Deadzone
│   ├── Response Curve
│   ├── Calibrate
│   └── Back
├── Display
│   ├── Brightness (20-100%)
│   ├── Contrast (30-100%)
│   ├── Screen Saver
│   └── Back
├── About
└── Exit
```

## 🔄 Updates & Versions

### Version 1.0 (Current)
- Initial release with 5 aim assist patterns
- Complete OLED menu system
- Real-time settings adjustment
- Visual feedback and status display

### Planned Features
- Pattern intensity curves
- Game-specific profiles
- Advanced deadzone settings
- Custom pattern creation
- Profile save/load system

## ⚠️ Important Notes

### Legal Considerations
- **Check game rules** before using in online multiplayer
- **Use responsibly** - these scripts provide assistance, not automation
- **Competitive play** - Many games prohibit modification devices
- **Practice mode** - Test settings in practice ranges first

### Technical Limitations
- **Cronus Zen memory**: Scripts are optimized for available memory
- **Update rate**: 50Hz maximum for smooth operation
- **OLED display**: 128x64 pixel monochrome display
- **Controller compatibility**: Designed for Xbox One controller constants

## 📝 License

This project is provided as-is for educational and personal use. Use responsibly and in accordance with game terms of service.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your Cronus Zen firmware is up to date
3. Ensure proper script compilation
4. Test with different games and settings

---

**Remember**: Practice makes perfect! Take time to find the optimal settings for your playstyle and games.