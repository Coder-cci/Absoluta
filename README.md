# Absoluta

A cryptographic system implementing a variation of the one-time pad with an expanded character set and salt insertion mechanism.

## Overview

Absoluta is a symmetric encryption system that achieves perfect secrecy through a combination of large ciphertext alphabet, random salt insertion, and XOR masking. The system provides 13.7 billion possible combinations per source character.

## Core Algorithm

### Key Components

- **Seed**: 32 hexadecimal characters (128 bits of entropy)
- **Salt probability**: 3-digit value (000-999) controlling salt insertion frequency
- **Position weights**: Three digits (0-3) determining salt placement probabilities
- **Cipher alphabet**: 1660 unique Unicode characters loaded from external file

### Encryption Process

For each source character:

1. Convert source character to its index in the source alphabet (0-94 for ASCII)
2. Generate random Y value from cipher alphabet
3. Determine salt presence based on probability parameter
4. If salt is present:
   - Select salt position using cyclic weight algorithm
   - Generate random salt value
   - Construct triplet [salt, X, Y] in determined order
5. If no salt:
   - Construct pair [X, Y]
6. Convert all indices to cipher alphabet symbols

### Salt Position Selection

The system uses a cyclic selection algorithm with configurable weights:

- Weight 0: 0% chance
- Weight 1: 33% chance
- Weight 2: 66% chance
- Weight 3: 99% chance

Positions are checked cyclically (left -> middle -> right -> repeat) until selection occurs.

### XOR Masking

After the main encryption, an XOR mask is applied:

1. Generate mask of same length as intermediate ciphertext using separate RNG seeded with key
2. XOR each ciphertext symbol index with corresponding mask value
3. Convert resulting indices back to cipher alphabet symbols

This ensures avalanche effect: changing one bit in the seed completely alters the final ciphertext.

## Security Properties

### Combinatorial Complexity

- Single character: 3×1660³ + 1660² ≈ 1.37×10¹⁰ combinations
- 10 characters: approximately 10¹⁰¹ combinations
- 100 characters: approximately 10¹⁰¹³ combinations

### Key Space

- Seed: 2¹²⁸ possible values
- Salt probability: 1000 variations
- Position weights: 64 variations
- Total keys: approximately 2¹⁴⁴ ≈ 2.2×10⁴³

### Cryptographic Strength

- Full avalanche effect through XOR masking
- Resistance to frequency analysis due to multiple representations per character
- No deterministic relationship between plaintext and ciphertext
- Mathematical perfect secrecy when key is truly random and used once

## System Requirements

- Python 3.8 and higher interpreter
- At least 1 any cipher alphabet file in alphabets\ directory
- Basically, all you need to do to run the program is place “alphabets\” folder and “absoluta.py” file in the same directory

## Usage

1. Execute "absoluta.py" with any Python 3.8 and higher interpreter
2. Select source alphabet (ASCII, Russian, or Mathematical)
3. Enter text in input field
4. Configure key parameters
5. Execute encryption or decryption
6. Results appear in output field

The system validates all parameters before encryption or decryption and provides clear error messages for invalid inputs.
