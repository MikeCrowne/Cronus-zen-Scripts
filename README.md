# GPC Aim Assist Script Collection

This repository contains two GPC (GamePack Code) scripts for advanced aim assist functionality with multiple movement patterns.

## Files Included

1. **`aim_assist_script.gpc`** - Full-featured version with advanced patterns and customization
2. **`simple_aim_assist.gpc`** - Simplified version for easier understanding and modification

## Features

### Movement Patterns
- **Circle**: Smooth circular movement around the current aim point
- **Triangle**: Sharp triangular movement pattern with three distinct sides
- **Spiral**: Expanding spiral movement that grows outward
- **Helix**: 3D helix pattern projected to 2D for complex tracking
- **Scared**: Erratic, jittery movement with random spikes for unpredictable aim

### Activation
- **LT (Left Trigger)** or **RT (Right Trigger)** - Hold to activate aim assist
- Release trigger to deactivate

### Pattern Selection
- **D-Pad UP**: Circle pattern
- **D-Pad RIGHT**: Triangle pattern
- **D-Pad DOWN**: Spiral pattern
- **D-Pad LEFT**: Helix pattern
- **Y Button**: Scared pattern

## Setup Instructions

### For Cronus Devices
1. Open Cronus PRO software
2. Load one of the `.gpc` files
3. Compile and upload to your device
4. Connect your controller and target device

### For Titan Devices
1. Open Titan One/Two software
2. Import the `.gpc` file
3. Compile and flash to device
4. Configure your controller setup

## Usage

1. **Activate**: Hold LT or RT to enable aim assist
2. **Select Pattern**: Use D-pad or Y button to choose your preferred pattern
3. **Aim**: The script will apply the selected movement pattern to your right stick
4. **Deactivate**: Release LT/RT to turn off aim assist

## Customization

### Advanced Script (`aim_assist_script.gpc`)
Modify these constants at the top of the file:

```c
#define SENSITIVITY 30      // Overall sensitivity (1-100)
#define PATTERN_SPEED 8     // Speed of pattern execution (1-20)
#define PATTERN_SIZE 25     // Size of movement patterns (1-50)
```

### Simple Script (`simple_aim_assist.gpc`)
Modify these constants:

```c
#define SPEED 10    // Pattern execution speed (1-20)
#define SIZE 20     // Movement pattern size (1-50)
```

## Pattern Descriptions

### Circle Pattern
Creates smooth circular movement around your current aim point. Ideal for tracking moving targets or area control.

### Triangle Pattern
Creates a triangular movement pattern with three distinct sides. Good for covering corners or systematic area scanning.

### Spiral Pattern
Starts small and expands outward in a spiral. Useful for gradually expanding your search area or tracking erratic targets.

### Helix Pattern
A 3D helix pattern projected to 2D, creating complex vertical and horizontal movement. Advanced pattern for sophisticated tracking.

### Scared Pattern
Erratic, jittery movement with random spikes. Creates unpredictable aim movement that can be useful for avoiding counter-aim or creating chaos.

## Troubleshooting

### Script Not Working
- Ensure your device firmware is up to date
- Check that the controller is properly connected
- Verify the script compiled without errors

### Movement Too Fast/Slow
- Adjust the `SPEED` or `PATTERN_SPEED` values
- Lower values = faster movement
- Higher values = slower movement

### Movement Too Large/Small
- Adjust the `SIZE` or `PATTERN_SIZE` values
- Higher values = larger movements
- Lower values = smaller movements

### Patterns Not Smooth
- Ensure consistent frame rate on your target device
- Try adjusting the speed settings
- Check for interference with other scripts

## Legal Notice

This script is provided for educational and research purposes only. Users are responsible for compliance with:
- Game terms of service
- Platform/console terms of use
- Local laws and regulations
- Competitive gaming rules

Use responsibly and ethically.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your device compatibility
3. Ensure proper script compilation
4. Test with different games/applications

## Version History

- v1.0 - Initial release with all 5 patterns
- Advanced and simple versions included
- Full documentation and customization options