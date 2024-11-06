# File Structure Scanner

A Python script that generates a clean, readable text representation of your project's file structure. This tool is especially useful when you need to share your project layout with Large Language Models (LLMs) to provide better context about your codebase.

## Why Use This Tool?

- **Clear Project Structure**: Get a clean view of your project without build artifacts, caches, and dependencies cluttering the output
- **LLM Integration**: Share your project structure with AI assistants to get more contextual help
- **Documentation**: Quickly generate project structure documentation for READMEs or wikis
- **Code Review**: Understand the layout of unfamiliar codebases
- **Project Analysis**: Review project organization and identify structural issues

## Features

- **Clean Output**: Automatically excludes common build artifacts, cache directories, and dependencies
- **Config Preservation**: Keeps all configuration files (like vite.config.js, webpack.config.js)
- **Environment Files**: Preserves all environment files (.env, .env.local, etc.)
- **Format Options**: Choose between text ([DIR]/[FILE]) or emoji (📁/📄) markers
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Dependencies**: Uses only Python standard library

## Requirements

- Python 3.6 or higher
  ```bash
  # Check your Python version
  python --version
  ```
  
If Python is not found:
1. Download from [Python's official website](https://www.python.org/downloads/)
2. During Windows installation, check "Add Python to PATH"
3. Restart your terminal after installation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/file-structure-scanner.git
cd file-structure-scanner
```

2. Ready to use! No additional installation needed.

## Usage

### Basic Commands

Scan current directory:
```bash
python scan_files.py
```

Scan specific directory:
```bash
# Windows
python scan_files.py --dir "C:\Users\username\projects\my_project"

# Mac/Linux
python scan_files.py --dir "/home/username/projects/my_project"
```

### Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|----------|
| --dir | -d | Directory to scan | --dir "/path/to/project" |
| --output | -o | Output file name | --output structure.txt |
| --ignore | -i | Additional patterns to ignore | --ignore "*.tmp" "backup" |
| --emoji | -e | Use emoji markers | --emoji |
| --show-ignored | -s | List all ignored patterns | --show-ignored |

### Example Output

Text format (default):
```
File structure for: /path/to/project
==================================================

[DIR] my_project
    [DIR] src
        [FILE] index.js
        [FILE] App.js
    [FILE] package.json
    [FILE] vite.config.js
    [FILE] .env
```

Emoji format (with --emoji):
```
File structure for: /path/to/project
==================================================

📁 my_project
    📁 src
        📄 index.js
        📄 App.js
    📄 package.json
    📄 vite.config.js
    📄 .env
```

## Output Structure

The scanner provides a comprehensive view of your project while managing complexity:

### Directory Visibility
- **High-Level Directories**: Shows all important directories even if their contents are ignored:
  ```
  [DIR] my_project
      [DIR] src
      [DIR] node_modules     # Shown, but contents ignored
      [DIR] vendor          # Shown, but contents ignored
      [DIR] dist           # Shown, but contents ignored
      [FILE] package.json
  ```
  This helps identify:
  - Technology stack (node_modules, vendor, etc.)
  - Build tools (dist, build folders)
  - Frameworks (.next, .nuxt folders)
  - Programming languages (site-packages, vendor)

### What's Included
- All source code files and directories
- Root directory config files
- Important subdirectory config files
- High-level library and build directories (names only)
- Root level environment files
- Project definition files
- Documentation files

### What's Excluded
- Contents of library directories
- Contents of build directories
- Cache files and directories
- Compiled files
- Logs and temporary files
- System files

This approach provides:
- Clear project structure visualization
- Technology stack identification
- Build and deployment setup understanding
- Clean, uncluttered output while preserving important structural information

Use `--show-ignored` to see the complete list of patterns affecting directory contents.

## Best Practices

1. Run from your project root directory
2. Use quotes around paths with spaces
3. Check ignored patterns first with --show-ignored
4. Specify custom output location if needed

## Troubleshooting

1. **Python Not Found Error**
   - Ensure Python is installed and in PATH
   - Try using `python3` instead of `python`
   - Restart your terminal after installation

2. **Path Not Found**
   - Verify the path exists
   - Use quotes around paths with spaces
   - Check for correct slashes (/ or \\)

3. **Missing Files in Output**
   - Check --show-ignored
   - Add custom ignore patterns if needed
   - Verify file/directory permissions

## Contributing

Contributions are welcome! Areas for improvement:
- Additional ignore patterns for other frameworks
- New output format options
- Performance improvements
- Documentation enhancements

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
