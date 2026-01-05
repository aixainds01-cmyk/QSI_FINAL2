#!/usr/bin/env python3
"""
QSI Theme Manager - Update All Pages
Adds theme manager to all HTML pages in the project
"""

import os
import re
import shutil
from pathlib import Path

def get_relative_path(file_path, base_dir):
    """Calculate relative path from file to js folder"""
    rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))
    return rel_path

def update_html_file(file_path, base_dir):
    """Update a single HTML file with theme manager"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has theme manager
        if 'theme-manager.js' in content:
            return 'skipped'

        # Backup original file
        shutil.copy2(file_path, f"{file_path}.backup")

        # Get relative path to js folder
        rel_path = get_relative_path(file_path, base_dir)

        # Add theme manager script before </head>
        theme_script = f'    <!-- Global Theme Manager -->\n    <script src="{rel_path}/theme-manager.js"></script>\n</head>'

        if '</head>' not in content:
            print(f"   ⚠️  Warning: No </head> tag found in {file_path}")
            return 'error'

        content = content.replace('</head>', theme_script)

        # Remove hardcoded theme classes from body
        content = re.sub(r'<body class="theme-dark">', '<body>', content)
        content = re.sub(r'<body class="theme-light">', '<body>', content)
        content = re.sub(r'<body class="theme-dark ', '<body class="', content)
        content = re.sub(r'<body class="theme-light ', '<body class="', content)

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error updating {file_path}: {e}")
        return 'error'

def main():
    print("🎨 QSI Theme Manager - Update All Pages")
    print("=" * 50)
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
    ]

    print(f"🔍 Found {len(html_files)} HTML files")
    print()

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 Processing: {rel_file}")

        result = update_html_file(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ Updated successfully!")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already has theme manager")
            skipped += 1
        else:
            errors += 1

        print()

    print("=" * 50)
    print("✨ Update Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:        {updated} files")
    print(f"   ⏭️  Already Updated: {skipped} files")
    print(f"   ⚠️  Errors:         {errors} files")
    print()

    if updated > 0:
        print(f"🎉 Success! {updated} pages have been updated.")
        print()
        print("💡 Next Steps:")
        print("   1. Open your browser and navigate to your app")
        print("   2. Go to Settings → Theme tab")
        print("   3. Select 'Light' theme")
        print("   4. Navigate to different pages (Dashboard, Invoices, etc.)")
        print("   5. Verify all pages are now in Light theme")
        print("   6. Try 'Dark' theme and verify again")
        print()
        print("📦 Backups:")
        print("   • All original files saved as *.backup")
        print("   • If everything works, you can delete backups:")
        print("     python3 -c \"import pathlib; [f.unlink() for f in pathlib.Path('.').rglob('*.backup')]\"")
        print()
        print("🔄 To restore backups (if something went wrong):")
        print("   python3 -c \"import pathlib; [f.replace(str(f)[:-7]) for f in pathlib.Path('.').rglob('*.backup')]\"")
    else:
        print("ℹ️  All files were already updated!")

    print()
    print("📖 Documentation:")
    print("   • README_THEME_SETUP.md - Quick start guide")
    print("   • THEME_SYSTEM_GUIDE.md - Complete technical docs")
    print()

if __name__ == '__main__':
    main()
