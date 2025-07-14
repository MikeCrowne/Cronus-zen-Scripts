# GPC (Game Pack Code) Reference Guide

## Overview

GPC is a C-based programming language designed for the Cronus Zen and CronusMAX devices. It enables customization of game controller inputs through scripts that modify gamepad signals before they reach the console.

## Operator Types

### Assignment Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `=`      | Sets left operand to value of right operand | `a = 5;` |
| `+=`     | Adds right to left operand | `a += 5;` (a = a + 5) |
| `-=`     | Subtracts right from left operand | `a -= 5;` (a = a - 5) |
| `*=`     | Multiplies left by right operand | `a *= 5;` (a = a * 5) |
| `/=`     | Divides left by right operand | `a /= 5;` (a = a / 5) |
| `%=`     | Modulus assignment | `a %= 5;` (a = a % 5) |

### Arithmetic Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `+`      | Addition | `a + b` |
| `-`      | Subtraction | `a - b` |
| `*`      | Multiplication | `a * b` |
| `/`      | Division (integer only, fractions dropped) | `a / b` |
| `%`      | Modulus (remainder) | `a % b` |
| `++`     | Increment by 1 | `a++` |
| `--`     | Decrement by 1 | `a--` |

### Logical Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `&&`     | AND - both operands must be TRUE | `a && b` |
| `\|\|`   | OR - either operand can be TRUE | `a \|\| b` |
| `^^`     | XOR - either operand TRUE but not both | `a ^^ b` |
| `!`      | NOT - reverses logical state | `!a` |

### Relational Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `==`     | Equal to | `a == b` |
| `!=`     | Not equal to | `a != b` |
| `>`      | Greater than | `a > b` |
| `<`      | Less than | `a < b` |
| `>=`     | Greater than or equal to | `a >= b` |
| `<=`     | Less than or equal to | `a <= b` |

### Binary Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `&`      | Bitwise AND | `a & b` |
| `\|`     | Bitwise OR | `a \| b` |
| `^`      | Bitwise XOR | `a ^ b` |
| `<<`     | Left shift | `a << 1` |
| `>>`     | Right shift | `a >> 1` |
| `~`      | Bitwise NOT | `~a` |

## Flow Control

### Conditional Statements

#### if Statement
Executes code block if condition is TRUE.
```gpc
if (condition) {
    // code to execute
}
```

#### else Statement
Executes when preceding if condition is FALSE.
```gpc
if (condition) {
    // code if true
} else {
    // code if false
}
```

#### else if Statement
Chain multiple conditions.
```gpc
if (condition1) {
    // code for condition1
} else if (condition2) {
    // code for condition2
} else {
    // default code
}
```

### Loops

#### while Loop
Runs while condition remains TRUE.
```gpc
while (condition) {
    // code to repeat
}
```

#### do while Loop
Executes block at least once, then checks condition.
```gpc
do {
    // code to execute
} while (condition);
```

#### for Loop
Runs for a set number of iterations.
```gpc
for (initializer; condition; increment) {
    // code to repeat
}

// Example:
for (a = 0; a < 10; a++) {
    // runs 10 times
}
```

#### break Statement
Exits a loop early.
```gpc
while (true) {
    if (condition) {
        break; // exit loop
    }
}
```

## OLED Display Functions (Zen Only)

The Cronus Zen includes OLED display capabilities with these functions:

### Drawing Functions
- **`pixel_oled(x, y, color)`** - Draw single pixel
- **`line_oled(x, y, tox, toy, thickness, color)`** - Draw line
- **`rect_oled(x, y, width, height, fill, color)`** - Draw rectangle
- **`circle_oled(x, y, radius, fill, color)`** - Draw circle
- **`cls_oled(color)`** - Clear entire display

### Text Functions
- **`putc_oled(position, ascii)`** - Place character in buffer
- **`puts_oled(x, y, font, length, color)`** - Draw buffered text
- **`printf(x, y, font, color, stringaddr)`** - Draw string from data section

### Color Values
- `0` = Black
- `1` = White

## Variable Types and Constants

### Variables
- **16-bit signed integers**: -32,768 to +32,767
- **32-bit signed integers**: -2,147,483,648 to +2,147,483,647
- Variables are global by default
- Boolean values: `TRUE` = 1, `FALSE` = 0
- No fraction support (values rounded down)

### Common Controller Constants

#### Xbox One Constants
```gpc
XB1_A, XB1_B, XB1_X, XB1_Y          // Face buttons
XB1_LB, XB1_RB                      // Shoulder buttons  
XB1_LT, XB1_RT                      // Triggers (0-100)
XB1_LS, XB1_RS                      // Stick clicks
XB1_LX, XB1_LY, XB1_RX, XB1_RY      // Analog sticks (-100 to 100)
XB1_UP, XB1_DOWN, XB1_LEFT, XB1_RIGHT // D-pad
XB1_MENU, XB1_VIEW                   // Menu buttons
```

#### PlayStation Constants
```gpc
PS4_CROSS, PS4_CIRCLE, PS4_SQUARE, PS4_TRIANGLE  // Face buttons
PS4_L1, PS4_R1                                   // Shoulder buttons
PS4_L2, PS4_R2                                   // Triggers
PS4_L3, PS4_R3                                   // Stick clicks
PS4_LX, PS4_LY, PS4_RX, PS4_RY                   // Analog sticks
PS4_UP, PS4_DOWN, PS4_LEFT, PS4_RIGHT            // D-pad
PS4_OPTIONS, PS4_SHARE                           // Menu buttons
```

## Basic Script Structure

```gpc
// Global variable declarations
int variable1 = 100;
int variable2;

// Init section (runs once when script starts)
init {
    // Initialization code
}

// Main section (runs continuously)
main {
    // Main script logic
    if (get_val(XB1_RT) > 95) {
        combo_run(rapid_fire);
    }
}

// Combo definitions
combo rapid_fire {
    set_val(XB1_RT, 100);
    wait(40);
    set_val(XB1_RT, 0);
    wait(30);
}
```

## Key Programming Notes

1. **Semicolons**: Required at end of statements (except last line of blocks)
2. **Comments**: Use `//` for single line or `/* */` for multi-line
3. **Case Sensitivity**: Variable names are case-sensitive
4. **CPU Load**: Keep below 80% to prevent output delays
5. **Memory Management**: Use variables efficiently for optimal performance
6. **Real-time Execution**: Scripts run in real-time, modifying controller input

## Advanced Features

### 32-bit Support
- Enhanced precision for calculations
- Larger value ranges for complex scripts
- Better memory management capabilities

### Event Handling
- `event_press()` - Detect button press events
- `event_release()` - Detect button release events

### Device Functions
- `get_console()` - Detect connected console
- `set_val()` - Set output values
- `get_val()` - Read input values
- `get_ival()` - Get unmodified input values

This reference covers the core concepts needed for GPC scripting. The language's C-like syntax makes it accessible while providing powerful game controller customization capabilities.