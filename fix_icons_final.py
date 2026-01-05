#!/usr/bin/env python3
"""
Fix icons on all pages
1. Ensure Font Awesome CDN is loaded
2. Add fix-icons.css
"""

import os
from pathlib import Path
import shutil

FONT_AWESOME_CDN = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">'

def fix_page_icons(file_path, base_dir):
    """Fix icons on a single page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Ensure Font Awesome is loaded
        if 'font-awesome' not in content.lower():
            # Add Font Awesome before </head>
            content = content.replace('</head>', f'    {FONT_AWESOME_CDN}\n</head>')
            changed = True

        # 2. Add fix-icons.css if not present
        if 'fix-icons.css' not in content:
            rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))

            # Add after theme-force.css or before </head>
            if 'theme-force.css' in content:
                icon_css = f'    <link rel="stylesheet" href="{rel_path}/fix-icons.css">\n    <link rel="stylesheet" href="{rel_path}/theme-force.css">'
                content = content.replace(f'    <link rel="stylesheet" href="{rel_path}/theme-force.css">', icon_css)
            elif '</head>' in content:
                icon_css = f'    <link rel="stylesheet" href="{rel_path}/fix-icons.css">\n</head>'
                content = content.replace('</head>', icon_css)
            else:
                return 'error'

            changed = True

        if not changed:
            return 'skipped'

        # Backup
        shutil.copy2(file_path, f"{file_path}.icon_backup")

        # Write
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🔧 Fixing Icons on ALL Pages")
    print("=" * 60)
    print("This will:")
    print("  • Ensure Font Awesome CDN is loaded")
    print("  • Add fix-icons.css to make icons visible")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent
    html_files = list(base_dir.rglob('*.html'))

    exclude_dirs = {'node_modules', '.git', 'venv'}
    html_files = [
        f for f in html_files
        if not any(ex in f.parts for ex in exclude_dirs)
        and not str(f.name).endswith('.backup')
        and not str(f.name).endswith('.icon_backup')
    ]

    print(f"🔍 Found {len(html_files)} HTML files")
    print()

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 {rel_file}")

        result = fix_page_icons(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ Icons fixed")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already fixed")
            skipped += 1
        else:
            errors += 1

    print()
    print("=" * 60)
    print("✨ Icon Fix Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:     {updated} files")
    print(f"   ⏭️  Skipped:     {skipped} files")
    print(f"   ⚠️  Errors:      {errors} files")
    print()

    if updated > 0:
        print("🎉 Icons should now be visible on all pages!")
        print()
        print("🧪 TEST:")
        print("   1. Hard refresh browser (Ctrl+Shift+R)")
        print("   2. Check sidebar - all icons should be visible")
        print("   3. Icons should be same size on all pages")
        print()

if __name__ == '__main__':
    main()
