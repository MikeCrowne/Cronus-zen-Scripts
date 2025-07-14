# GPC Bit Packing Optimization Guide

## Overview

Bit flags in GPC allow you to efficiently store multiple boolean values in a single integer variable. Each bit represents a different flag or attribute, corresponding to powers of 2.

## 32-bit Support

**As of firmware version 2.1.0**, all variables in GPC support both 16-bit and 32-bit signed integers:
- **16-bit signed**: -32,768 to +32,767
- **32-bit signed**: -2,147,483,648 to +2,147,483,647

Zen Studio defaults to 32-bit compilation for enhanced capabilities while maintaining compatibility with older 16-bit scripts.

## Bit Representation

Variables in GPC can use different bit ranges depending on compilation mode:

### 16-bit Mode
- 1st bit: 1 (2^0)
- 2nd bit: 2 (2^1) 
- 3rd bit: 4 (2^2)
- 4th bit: 8 (2^3)
- ...up to 16th bit: -32768 (2^15)

### 32-bit Mode  
- 1st bit: 1 (2^0)
- 2nd bit: 2 (2^1)
- 3rd bit: 4 (2^2)
- 4th bit: 8 (2^3)
- ...up to 32nd bit: -2147483648 (2^31)

## Basic Operations

### Setting Bits (Bitwise OR `|`)
Sets a bit or leaves it set if already set:
```cpp
var = var | 1;  // Sets the first bit
var = var | 2;  // Sets the second bit
var = var | 4;  // Sets the third bit
var = var | 8;  // Sets the fourth bit
```

### Checking Bits (Bitwise AND `&`)
Returns the value of the bit being checked (or 0 if not set):
```cpp
if(var & 1)  // Checks the first bit
if(var & 2)  // Checks the second bit
if(var & 4)  // Checks the third bit
```

### Toggling Bits (Bitwise XOR `^`)
Either sets or unsets the bit:
```cpp
var = var ^ 1;  // Toggles the first bit
var = var ^ 2;  // Toggles the second bit
var = var ^ 4;  // Toggles the third bit
```

## Advanced Operations

### Unsetting Multiple Bits
Using bitwise AND with bitwise NOT:
```cpp
var = var & ~(1 | 2 | 4);  // Unsets bits 1, 2, and 3
```

### Checking Multiple Bits
Returns a mask showing which bits are set:
```cpp
var = var & (1 | 2 | 4);  // Checks bits 1, 2, and 3
```

### Toggling Multiple Bits
```cpp
var = var ^ (1 | 2 | 4);  // Toggles bits 1, 2, and 3
```

## ZenStudio Constants

ZenStudio provides predefined constants instead of manual power-of-2 calculations:
- `BITMASK_1` (1)
- `BITMASK_2` (2) 
- `BITMASK_3` (4)
- ...up to `BITMASK_32` (-2147483648)

### Manual Constant Definition
If constants weren't available, you could define them using bit shifting:
```cpp
define BITMASK_1 = 1 << 0;  // 1
define BITMASK_2 = 1 << 1;  // 2
define BITMASK_3 = 1 << 2;  // 4
define BITMASK_4 = 1 << 3;  // 8
```

## Built-in Bit Functions

GPC provides several built-in functions for bit manipulation:

### Individual Bit Operations
```cpp
set_bit(variable, bit_index);    // Sets one bit
clear_bit(variable, bit_index);  // Clears one bit  
test_bit(variable, bit_index);   // Tests a bit (returns 0 or 1)
```

### Multi-bit Operations
```cpp
set_bits(variable, bit_index, num_bits, value);  // Stores a value into bit range
get_bits(variable, bit_index, num_bits);         // Gets a value from bit range
```

### Legacy opcode Function
```cpp
opcode(variable, bit_index);  // Sets one bit (16-bit mode, index 0-15)
```

**Example Usage:**
```cpp
int flags;

init {
    set_bit(flags, 0);        // Set bit 0 (equivalent to flags |= 1)
    set_bit(flags, 3);        // Set bit 3 (equivalent to flags |= 8)
    
    if(test_bit(flags, 0)) {  // Check if bit 0 is set
        // Do something
    }
    
    clear_bit(flags, 3);      // Clear bit 3 (equivalent to flags &= ~8)
}
```

## Real-World Example: Person Attributes

```cpp
enum {
    Man         = BITMASK_1,
    Woman       = BITMASK_2,
    Tall        = BITMASK_3,
    Short       = BITMASK_4,
    LeftHanded  = BITMASK_5,
    RightHanded = BITMASK_6,
    Pants       = BITMASK_7,
    Shorts      = BITMASK_8
}

int person;

init {
    // Create a person: man, tall, right-handed, wearing shorts
    person = Man | Tall | RightHanded | Shorts;
}

main {
    // Check if person is tall
    if(person & Tall) {
        // Handle tall person
    }
    
    // Check if person is a left-handed woman
    if(person & (Woman | LeftHanded)) {
        // Handle left-handed woman
    }
    
    // Convert right-handed person to left-handed
    if(person & RightHanded) {
        person = person | LeftHanded & ~RightHanded;
        // Alternative: person = person | LeftHanded ^ RightHanded;
    }
    
    // Change pants to shorts for men
    if(person & (Man | Pants)) {
        person = person | Shorts & ~Pants;
        // Alternative: person = person | Shorts ^ Pants;
    }
    
    // Remove all attributes except height
    person = person & ~(Man | Woman | LeftHanded | RightHanded);
}
```

## Persistent Variables for Bit Packing

### SPVARs (Slot Persistent Variables)
SPVARs allow you to store bit-packed data that persists between script loads. Each memory slot has private variables that other slots cannot access.

**Available SPVARs:**
- **Cronus Zen**: 64 private variables per slot (`SPVAR_1` to `SPVAR_64`)  
- **CronusMAX Plus**: 16 private variables per slot (`SPVAR_1` to `SPVAR_16`)
- **Global Variables**: 16 shared variables (`PVAR_1` to `PVAR_16`)

**Example Usage:**
```cpp
int settings;

init {
    // Load persistent bit-packed settings
    settings = get_pvar(SPVAR_1, 0, 255, 0);  // min=0, max=255, default=0
    
    // Check saved settings
    if(settings & BITMASK_1) {
        // Feature A was enabled
    }
    if(settings & BITMASK_2) {
        // Feature B was enabled  
    }
}

main {
    if(event_press(XB1_A)) {
        // Toggle feature A
        settings = settings ^ BITMASK_1;
        
        // Save to persistent memory
        set_pvar(SPVAR_1, settings);
    }
}
```

**Important Notes:**
- SPVARs are stored in EEPROM (limited read/write cycles)
- Always use `event_press()` or similar one-time triggers when writing
- Never write SPVARs in the main loop continuously
- Use `get_pvar()`/`set_pvar()` functions for access

## Benefits

- **Memory Efficiency**: Store multiple boolean flags in a single integer
- **Performance**: Bitwise operations are very fast
- **Compact Storage**: Up to 32 different flags in just 4 bytes (64 in 32-bit mode)
- **Atomic Operations**: All flags can be modified in single operations
- **Persistence**: SPVARs maintain state across script reloads
- **Isolation**: Each slot's SPVARs are private and secure

## Best Practices

1. Use descriptive enum names for bit flags
2. Use ZenStudio's predefined `BITMASK_X` constants or built-in bit functions
3. Group related flags logically
4. Document which bits represent which attributes
5. Be careful with bit 32 (negative value in signed integers)
6. Use SPVARs for settings that need to persist between sessions
7. Protect EEPROM by avoiding continuous writes to persistent variables
8. Consider using built-in bit functions for cleaner, more readable code