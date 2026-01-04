# ImageOrganiser

ImageOrganiser is a lightweight photo organisation tool developed as part of the **Winter Project 2025** for the **Enigma Club, IIIT Sri City**.

## Problem

Photo galleries become cluttered over time.  
Photos from the same trip, event, or day often get scattered, making it difficult to find specific memories.

Manual organisation is time consuming and impractical at scale.

## Idea

A **moment** is a group of photos taken:
- close in time
- at the same location

Modern photos already store this information in metadata.  
ImageOrganiser uses it to organise photos automatically.

## How It Works

1. **GPS-based sorting**  
   Photos are grouped by location (Country → State → City).

2. **Time-based grouping**  
   Inside each location, photos taken within a fixed time window are grouped into a single **moment**.

Each moment is stored as its own folder.

## Setup & Dependencies

This project uses a **`uv` virtual environment** for dependency management.

## Usage

### Setup

1. Ensure **Python 3.10+** is installed.
2. Install `uv` (if not already installed):
   
   ```bash
   pip install uv
   ```

3. From the project root directory, install all dependencies using the lock file:

   ```bash
   uv sync
   ```

### Running the Project

1. Create an `images/` directory in the **same directory as `main.py`**.
2. Place all photos you want to organise inside the `images/` directory.
3. Run the project using:

   ```bash
   uv run python main.py
   ```

The organised output will be created inside the `images/` directory.
