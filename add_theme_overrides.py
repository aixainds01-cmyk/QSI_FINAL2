#!/usr/bin/env python3
"""
Add theme override CSS to all HTML pages
This ensures all pages use the unified theme
"""

import os
import re
from pathlib import Path
import shutil

def add_override_css(file_path, base_dir):
    """Add theme override CSS to a page"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if override CSS is already added
        if 'theme-overrides.css' in content:
            return 'skipped'

        # Calculate relative path
        rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))

        # Add override CSS AFTER qsi-styles.css and BEFORE theme-manager.js
        # This ensures it loads in the correct order

        # Find where to insert
        if '<!-- Global Theme Manager -->' in content:
            # Insert before theme manager
            override_css = f'    <link rel="stylesheet" href="{rel_path}/theme-overrides.css">\n    <!-- Global Theme Manager -->'
            content = content.replace('    <!-- Global Theme Manager -->', override_css)
        elif 'theme-manager.js' in content:
            # Insert before theme manager script
            override_css = f'    <link rel="stylesheet" href="{rel_path}/theme-overrides.css">\n    <script src="{rel_path}/theme-manager.js"></script>'
            content = content.replace(f'    <script src="{rel_path}/theme-manager.js"></script>', override_css)
        elif '</head>' in content:
            # Just add before </head>
            override_css = f'    <link rel="stylesheet" href="{rel_path}/theme-overrides.css">\n</head>'
            content = content.replace('</head>', override_css)
        else:
            return 'error'

        # Backup original
        shutil.copy2(file_path, f"{file_path}.override_backup")

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🎨 Adding Theme Override CSS to All Pages")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent

    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))

    # Exclude certain directories
    exclude_dirs = {'node_modules', '.git', 'venv', 'env'}
    html_files = [
        f for f in html_files
        if not any(excluded in f.parts for excluded in exclude_dirs)
        and not f.name.endswith('.backup')
        and not f.name.endswith('.override_backup')
    ]

    print(f"🔍 Found {len(html_files)} HTML files")
    print()

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 {rel_file}")

        result = add_override_css(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ Added theme override CSS")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already has override CSS")
            skipped += 1
        else:
            errors += 1

        print()

    print("=" * 60)
    print("✨ Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:     {updated} files")
    print(f"   ⏭️  Skipped:     {skipped} files")
    print(f"   ⚠️  Errors:      {errors} files")
    print()

    if updated > 0:
        print("🎉 Success! Theme override CSS added to all pages.")
        print()
        print("🧪 Next Steps:")
        print("   1. Open your browser")
        print("   2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)")
        print("   3. Go to Settings → Theme")
        print("   4. Switch between Light and Dark themes")
        print("   5. Navigate to ALL pages and verify theme changes")
        print()
        print("✨ All pages should now have:")
        print("   • Unified UI design")
        print("   • Consistent colors")
        print("   • Theme switching working everywhere")
        print()

if __name__ == '__main__':
    main()
