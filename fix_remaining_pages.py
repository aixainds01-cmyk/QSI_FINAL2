#!/usr/bin/env python3
"""
Fix remaining pages that are missing theme-force.css
Adds fix-icons.css and theme-force.css to pages that don't have them
"""

import os
from pathlib import Path
import shutil

def fix_page(file_path, base_dir):
    """Fix a single page by adding missing CSS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Calculate relative path to /js directory
        rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))

        # Check if page has </head> tag
        if '</head>' not in content:
            print(f"   ⚠️  SKIPPED - No </head> tag (malformed HTML)")
            return 'malformed'

        # Add fix-icons.css if missing
        if 'fix-icons.css' not in content:
            # Find qsi-styles.css and add after it
            if 'qsi-styles.css' in content:
                # Add after qsi-styles.css
                import re
                qsi_pattern = r'(<link[^>]*qsi-styles\.css[^>]*>)'
                match = re.search(qsi_pattern, content)
                if match:
                    old_line = match.group(1)
                    new_lines = f'{old_line}\n  <link rel="stylesheet" href="{rel_path}/fix-icons.css">'
                    content = content.replace(old_line, new_lines)
                    changed = True
            else:
                # Add before </head>
                content = content.replace('</head>', f'  <link rel="stylesheet" href="{rel_path}/fix-icons.css">\n</head>')
                changed = True

        # Add theme-force.css if missing
        if 'theme-force.css' not in content:
            # Find fix-icons.css and add after it, or add before </head>
            if 'fix-icons.css' in content:
                import re
                icon_pattern = r'(<link[^>]*fix-icons\.css[^>]*>)'
                match = re.search(icon_pattern, content)
                if match:
                    old_line = match.group(1)
                    new_lines = f'{old_line}\n  <link rel="stylesheet" href="{rel_path}/theme-force.css">'
                    content = content.replace(old_line, new_lines)
                    changed = True
            else:
                content = content.replace('</head>', f'  <link rel="stylesheet" href="{rel_path}/theme-force.css">\n</head>')
                changed = True

        if not changed:
            return 'skipped'

        # Backup
        shutil.copy2(file_path, f"{file_path}.css_fix_backup")

        # Write
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🔧 Fixing Remaining Pages")
    print("=" * 60)
    print("Adding fix-icons.css and theme-force.css to pages")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent

    # Files to check
    files_to_check = [
        base_dir / 'with_login' / 'settings.html',
        base_dir / 'with_login' / 'parchase' / 'parchase_order' / 'view_purchase_order.html',
    ]

    # Also search for any other HTML files that might be missing
    all_html = list(base_dir.rglob('*.html'))
    exclude_dirs = {'node_modules', '.git', 'venv', 'components'}
    all_html = [
        f for f in all_html
        if not any(ex in f.parts for ex in exclude_dirs)
        and not str(f.name).endswith('.backup')
        and not str(f.name).endswith('.css_fix_backup')
    ]

    # Find files missing theme-force.css
    missing_files = []
    for file_path in all_html:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'theme-force.css' not in content and '</head>' in content:
                    missing_files.append(file_path)
        except:
            pass

    print(f"🔍 Found {len(missing_files)} pages missing theme-force.css")
    print()

    updated = 0
    skipped = 0
    errors = 0
    malformed = 0

    for file_path in missing_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 {rel_file}")

        result = fix_page(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ CSS files added")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already has CSS")
            skipped += 1
        elif result == 'malformed':
            malformed += 1
        else:
            errors += 1

    print()
    print("=" * 60)
    print("✨ Fix Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:      {updated} files")
    print(f"   ⏭️  Skipped:      {skipped} files")
    print(f"   ⚠️  Malformed:    {malformed} files")
    print(f"   ❌ Errors:       {errors} files")
    print()

    if updated > 0:
        print("🎉 CSS files added to remaining pages!")
        print()
        print("🧪 NEXT STEPS:")
        print("   1. Hard refresh browser (Ctrl+Shift+R)")
        print("   2. Test the pages that were updated")
        print("   3. Verify theme switching works")
        print()

    if malformed > 0:
        print(f"⚠️  WARNING: {malformed} file(s) have malformed HTML (missing </head> tag)")
        print("   These files need to be fixed manually")
        print()

if __name__ == '__main__':
    main()
