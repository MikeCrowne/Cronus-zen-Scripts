# GPC Bit Packing Optimization Guide

## Overview

Bit flags in GPC allow you to efficiently store multiple boolean values in a single 32-bit signed integer variable. Each bit represents a different flag or attribute, corresponding to powers of 2.

## Bit Representation

Variables in GPC are 32-bit signed integers with each bit representing:
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

## Benefits

- **Memory Efficiency**: Store multiple boolean flags in a single integer
- **Performance**: Bitwise operations are very fast
- **Compact Storage**: 32 different flags in just 4 bytes
- **Atomic Operations**: All flags can be modified in single operations

## Best Practices

1. Use descriptive enum names for bit flags
2. Use ZenStudio's predefined `BITMASK_X` constants
3. Group related flags logically
4. Document which bits represent which attributes
5. Be careful with bit 32 (negative value in signed integers)