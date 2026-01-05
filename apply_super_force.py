#!/usr/bin/env python3
"""
Apply SUPER FORCE theme CSS to all pages
This ensures ALL pages have EXACTLY the same UI
"""

import os
from pathlib import Path
import shutil

def apply_super_force(file_path, base_dir):
    """Replace theme-overrides.css with theme-force.css"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has theme-force.css
        if 'theme-force.css' in content:
            return 'skipped'

        # Calculate relative path
        rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))

        # Replace theme-overrides.css with theme-force.css
        if 'theme-overrides.css' in content:
            content = content.replace('theme-overrides.css', 'theme-force.css')
        # Or add it if not present
        elif 'theme-manager.js' in content:
            override_css = f'    <link rel="stylesheet" href="{rel_path}/theme-force.css">\n    <script src="{rel_path}/theme-manager.js"></script>'
            content = content.replace(f'    <script src="{rel_path}/theme-manager.js"></script>', override_css)
        elif '</head>' in content:
            override_css = f'    <link rel="stylesheet" href="{rel_path}/theme-force.css">\n</head>'
            content = content.replace('</head>', override_css)
        else:
            return 'error'

        # Backup
        shutil.copy2(file_path, f"{file_path}.force_backup")

        # Write
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🚀 Applying SUPER FORCE Theme to ALL Pages")
    print("=" * 70)
    print("This will make ALL pages have EXACTLY the same UI:")
    print("  • Same background color")
    print("  • Same font family and size")
    print("  • Same sidebar theme and icons")
    print("  • Same buttons, forms, tables")
    print("  • All pages change when theme is changed in Settings")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent
    html_files = list(base_dir.rglob('*.html'))

    exclude_dirs = {'node_modules', '.git', 'venv'}
    html_files = [
        f for f in html_files
        if not any(ex in f.parts for ex in exclude_dirs)
        and not str(f).endswith('.backup')
        and not str(f).endswith('.override_backup')
        and not str(f).endswith('.force_backup')
    ]

    print(f"🔍 Found {len(html_files)} HTML files")
    print()

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 {rel_file}")

        result = apply_super_force(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ Applied SUPER FORCE theme")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already has SUPER FORCE")
            skipped += 1
        else:
            errors += 1

    print()
    print("=" * 70)
    print("✨ SUPER FORCE Applied!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:     {updated} files")
    print(f"   ⏭️  Skipped:     {skipped} files")
    print(f"   ⚠️  Errors:      {errors} files")
    print()

    if updated > 0:
        print("🎉 SUCCESS! All pages now have EXACTLY the same UI!")
        print()
        print("🧪 TEST NOW:")
        print("   1. Open browser (HARD REFRESH: Ctrl+Shift+R)")
        print("   2. Login to your app")
        print("   3. Check ALL pages - they should look IDENTICAL")
        print("   4. Go to Settings → Theme")
        print("   5. Change to Light theme")
        print("   6. Check ALL pages - all should be Light")
        print("   7. Change to Dark theme")
        print("   8. Check ALL pages - all should be Dark")
        print()
        print("✅ Expected Result:")
        print("   • All pages have the SAME background color")
        print("   • All pages have the SAME fonts and sizes")
        print("   • All pages have the SAME sidebar design")
        print("   • All pages CHANGE THEME together")
        print()

if __name__ == '__main__':
    main()
