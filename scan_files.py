r"""
File Structure Scanner
====================

This script generates a text file containing the file structure of a specified folder,
suitable for sharing with LLMs or documentation purposes.

Usage Examples
-------------
1. Basic usage (scan current directory):
    python scan_files.py

2. Scan specific directory:
    Windows: python scan_files.py --dir "C:\Users\username\projects\my_project"
    Unix/Mac: python scan_files.py --dir "/home/username/projects/my_project"
    Relative path: python scan_files.py --dir "../my_project"

3. Specify output file:
    python scan_files.py --output my_structure.txt

4. Ignore specific patterns:
    python scan_files.py --ignore "*.pyc" "*.log" "temp"

5. Use emoji markers instead of text:
    python scan_files.py --emoji

6. Show all ignored patterns:
    python scan_files.py --show-ignored

7. Full examples with all options:
    python scan_files.py --dir "/path/to/project" --output structure.txt --ignore "*.pyc" "build" --emoji
    python scan_files.py --dir "C:\Users\username\project" --output structure.txt --ignore "*.pyc" "build" "*.log" "temp"

Arguments
---------
--dir, -d : Target directory to scan (default: current directory)
    Can be absolute or relative path:
    - Absolute Windows: "C:\Users\username\project"
    - Absolute Unix/Mac: "/home/username/project"
    - Relative: "../project" or "./project" or "project"

--output, -o : Output file path (default: file_structure.txt)
    Can include path: "/path/to/output/structure.txt"

--ignore, -i : Space-separated patterns to ignore (added to default patterns)
    Examples: "*.pyc" ".env" "node_modules"

--emoji, -e : Use emoji markers instead of text markers (📁 and 📄 instead of [DIR] and [FILE])

--show-ignored, -s : Display all patterns being ignored before scanning

Output Format
------------
The output file will look like (with --emoji):
Directory structure for: /path/to/project
==================================================

📁 project_name
    📁 subfolder
        📄 file.txt
    📄 readme.md

Or (without --emoji):
Directory structure for: /path/to/project
==================================================

[DIR] project_name
    [DIR] subfolder
        [FILE] file.txt
    [FILE] readme.md


Notes
-----
- Directory Structure Display:
  * Shows all high-level library and build directories for stack identification
  * Only the directory names are shown, contents are ignored
  * Helps identify technologies used (node_modules, vendor, etc.)
  * Helps identify build tools and frameworks (.next, dist, etc.)

- Config and Environment File Handling:
  * Preserves config files ONLY in:
    - Project root directory
    - Immediate subdirectories (except library/build folders)
  * Root-level environment files (.env*) are always preserved
  * Config files inside library folders are ignored

- Directory Handling:
  * High-Level Directories Shown (but contents ignored):
    - Package Managers: node_modules/, vendor/, bower_components/
    - Build Outputs: dist/, build/, target/, out/
    - Framework Specific: .next/, .nuxt/
    - Language Specific: site-packages/, .pythonlibs/
    - Cache Directories: .parcel-cache/, .webpack/

- Default Ignored Patterns Include:
  * Build Artifacts: *.pyc, *.class, *.o
  * System and IDE: .DS_Store, Thumbs.db, .idea/
  * Temporary Files: *.log, .cache/
  * Source Maps: *.map
  (Use --show-ignored to see the full list)

- Additional Notes:
  * Custom ignore patterns are added to defaults, not replacing them
  * Use quotes around paths with spaces
  * On Windows, both forward slashes (/) and backslashes (\) are supported
  * Emoji option might not display correctly in all terminals

"""


import os
from pathlib import Path
import argparse

# Common patterns to ignore across different types of projects
DEFAULT_IGNORE_PATTERNS = [
    # Version Control
    '.git', '.svn', '.hg', '.bzr',
    
    # Python
    '__pycache__', '.pytest_cache', 'htmlcov',
    '.tox', '.venv', 'venv', 'env',  # Virtual environments only, not .env files
    'dist', 'build', '*.egg-info', 'eggs',
    '.pythonlibs', 'site-packages', '.local/lib/python*',
    'pip-wheel-metadata', 'poetry.lock',
    
    # Node.js/JavaScript/React Build and Cache
    'node_modules', 'bower_components', '.npm',
    '.cache', '.parcel-cache',
    '.webpack/build/',    # Only webpack build directory
    '.rollup-cache/',
    '.vite/build/',      # Only vite build directory
    '.next/cache/',      # Only next.js cache
    '.nuxt/cache/',      # Only nuxt cache
    '.output/cache/',
    '.yarn', '.pnp.*',
    
    # Java/Kotlin/Android Build
    'target/', 'bin/', '.gradle/cache/',
    '.m2/repository/',   # Maven repository only
    'classes/', 'out/', 'build/',
    'META-INF/', 'MANIFEST.MF',
    '*.iml', '*.iws', '*.ipr',
    
    # IDE and Editors
    '.idea', '.vscode', '.vs',
    '.settings', '.project', '.classpath',
    '*.swp', '*.swo', '*~',
    '.history/', '.sourcemaps/',
    
    # OS Specific
    '.DS_Store', '.AppleDouble', '.LSOverride',
    'Thumbs.db', 'desktop.ini', '$RECYCLE.BIN/',
    'System Volume Information',
    '.Spotlight-V100', '.Trashes',
    
    # Build and Dependency Directories
    'vendor/', 'bower_components', 'jspm_packages',
    'packages/', '.serverless/cache/',
    
    # Common Build Tools and Test Coverage
    'coverage/', '.nyc_output/',
    '.sass-cache/', 
    '*.css.map', '*.js.map',  # Source maps
    
    # Logs and Temporary Files
    '*.log', 'logs/', 'log/', 
    '.temp/', '.tmp/', 'tmp/',
    '*.bak', '*.retry',
    
    # Compiled Files
    '*.pyc', '*.pyo', '*.pyd',
    '*.so', '*.dll', '*.dylib',
    '*.class', '*.o', '*.ko',
    '*.obj', '*.exe', '*.pid',
    
    # Package Lock Files (often very large)
    'yarn.lock', 'package-lock.json',
    'pnpm-lock.yaml', 'bun.lockb',
    
    # Documentation Build
    'docs/_build/', 'site/build/', '.docusaurus/build/',
    
    # Docker
    '.docker/cache/',
    
    # CI/CD (but keep workflow definitions)
    '.github/actions/', '.gitlab/runners/', '.circleci/cache/',
    
    # Testing and Coverage
    'coverage/', '.coverage', 
    'coverage.xml', 'nosetests.xml',
    '.hypothesis/cache/', 
    
    # Development Tools
    '.conda/pkgs/', 
    '.jupyter/cache/',
]

def scan_directory(start_path, output_file, ignore_patterns=None, use_emoji=False):
    """
    Scan a directory and write its file structure to a text file.
    
    Args:
        start_path (str): The root directory to scan
        output_file (str): Path to the output text file
        ignore_patterns (list): List of patterns to ignore
        use_emoji (bool): Whether to use emoji markers instead of text markers
    """
    if ignore_patterns is None:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS
    
    def should_ignore(path):
        """
        Determine if a path should be ignored.
        
        Args:
            path (Path): Path object to check
        Returns:
            bool: True if path should be ignored, False otherwise
        """
        path_str = str(path)
        path_name_lower = path.name.lower()
        
        # Get path depth relative to start_path
        try:
            depth = len(path.relative_to(Path(start_path)).parts)
        except ValueError:
            return True

        # Common library and build folder names that should be shown but contents ignored
        library_folders = {
            # Package managers and dependencies
            'node_modules', 'vendor', 'bower_components', 'packages',
            'site-packages', '.pythonlibs', 'jspm_packages',
            
            # Version control
            '.git',
            
            # Build and output
            'dist', 'build', 'target', 'out', 'bin',
            
            # Framework specific
            '.next', '.nuxt', '.output',
            
            # Python specific
            '__pycache__', '.venv', 'venv', 'env',
            
            # Caches
            '.parcel-cache', '.webpack', '.rollup-cache'
        }

        # Show the directory itself but ignore its contents
        if path_name_lower in library_folders:
            return depth > 1

        # If we're inside a library folder, ignore everything
        current = path
        while current != Path(start_path):
            if current.name.lower() in library_folders:
                return True
            current = current.parent

        # List of config files to preserve in root and immediate non-library subdirectories
        important_config_files = {
            # Build configs
            'vite.config.js', 'vite.config.ts',
            'webpack.config.js', 'webpack.config.ts',
            'rollup.config.js', 'rollup.config.ts',
            'next.config.js', 'next.config.ts',
            'svelte.config.js', 'svelte.config.ts',
            'nuxt.config.js', 'nuxt.config.ts',
            # Package managers
            'package.json', 'composer.json',
            'cargo.toml', 'go.mod',
            # Environment files
            '.env', '.env.local', '.env.development',
            '.env.test', '.env.production',
            # Other common configs
            'tsconfig.json', 'babel.config.js',
            'jest.config.js', 'postcss.config.js'
        }

        # Preserve config files in root directory
        if depth == 1 and path_name_lower in important_config_files:
            return False

        # For immediate subdirectories, check they're not library folders before preserving configs
        if (depth == 2 and 
            path.parent.name.lower() not in library_folders and
            path_name_lower in important_config_files):
            return False

        # For root directory, also preserve any config.* and .env* files
        if depth == 1 and (
            path_name_lower.startswith('config.') or 
            path_name_lower.endswith('.config.js') or 
            path_name_lower.endswith('.config.ts') or
            path_name_lower.startswith('.env')):
            return False

        # Check against ignore patterns
        return any(
            pattern in path_str or 
            path_str.endswith(pattern.rstrip('/')) or
            (pattern.startswith('*.') and path_str.endswith(pattern[1:]))
            for pattern in ignore_patterns
        )

    # Define markers based on user preference
    if use_emoji:
        dir_marker = "📁 "
        file_marker = "📄 "
    else:
        dir_marker = "[DIR] "
        file_marker = "[FILE] "
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"File structure for: {start_path}\n")
        f.write("=" * 50 + "\n\n")
        
        for path in sorted(Path(start_path).rglob('*')):
            if should_ignore(path):
                continue
                
            # Get relative path
            rel_path = path.relative_to(start_path)
            
            # Calculate the depth for indentation
            depth = len(rel_path.parts) - 1
            indent = "    " * depth
            
            # Use appropriate marker based on type and user preference
            marker = dir_marker if path.is_dir() else file_marker
            
            f.write(f"{indent}{marker}{rel_path.name}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a text file containing file structure.')
    parser.add_argument('--dir', '-d', 
                      default=".",
                      help='Target directory to scan (default: current directory)')
    parser.add_argument('--output', '-o',
                      default="file_structure.txt",
                      help='Output file path (default: file_structure.txt)')
    parser.add_argument('--ignore', '-i',
                      nargs='+',
                      help='Additional patterns to ignore (space-separated)')
    parser.add_argument('--emoji', '-e',
                      action='store_true',
                      help='Use emoji markers instead of text markers')
    parser.add_argument('--show-ignored', '-s',
                      action='store_true',
                      help='Show list of ignored patterns before scanning')
    
    args = parser.parse_args()
    
    # Combine default ignore patterns with user-provided ones
    ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    if args.ignore:
        ignore_patterns.extend(args.ignore)
    
    # Show ignored patterns if requested
    if args.show_ignored:
        print("\nIgnored patterns:")
        for pattern in sorted(ignore_patterns):
            print(f"  - {pattern}")
        print()
    
    scan_directory(args.dir, args.output, ignore_patterns, args.emoji)
    print(f"File structure has been written to {args.output}")