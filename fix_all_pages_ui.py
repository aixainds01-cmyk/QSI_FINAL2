#!/usr/bin/env python3
"""
QSI - Fix All Pages to Use Unified UI
Removes inline styles and ensures all pages use the unified CSS theme
"""

import os
import re
from pathlib import Path

def clean_inline_styles(content):
    """Remove inline <style> blocks that override the unified CSS"""

    # Remove entire <style> blocks (but keep the qsi-styles.css link)
    # Keep only essential page-specific styles if needed

    # Pattern to match <style>...</style> blocks
    style_pattern = r'<style>.*?</style>'

    # Remove all inline style blocks
    content = re.sub(style_pattern, '', content, flags=re.DOTALL)

    return content

def ensure_css_link(content, file_path, base_dir):
    """Ensure the unified CSS is properly linked"""

    # Calculate relative path to CSS
    rel_path = os.path.relpath(os.path.join(base_dir, 'js'), os.path.dirname(file_path))
    css_path = f"{rel_path}/qsi-styles.css"

    # Check if CSS is already linked
    if 'qsi-styles.css' in content:
        return content

    # Add CSS link before </head>
    css_link = f'    <link rel="stylesheet" href="{css_path}">\n</head>'
    content = content.replace('</head>', css_link)

    return content

def remove_body_inline_styles(content):
    """Remove inline style attributes from body tag"""

    # Remove style attribute from body tag
    content = re.sub(r'<body[^>]*style="[^"]*"[^>]*>', '<body>', content)

    return content

def fix_tailwind_classes(content):
    """Replace common Tailwind classes with unified CSS classes"""

    replacements = {
        # Background colors - replace with theme-aware classes
        r'class="([^"]*)\bbg-gray-50\b([^"]*)"': r'class="\1bg-secondary\2"',
        r'class="([^"]*)\bbg-gray-100\b([^"]*)"': r'class="\1bg-secondary\2"',
        r'class="([^"]*)\bbg-gray-800\b([^"]*)"': r'class="\1sidebar\2"',
        r'class="([^"]*)\bbg-white\b([^"]*)"': r'class="\1card\2"',

        # Remove background-color from inline styles
        r'style="([^"]*)background-color:\s*[^;]+;([^"]*)"': r'style="\1\2"',
        r'style="([^"]*)background:\s*[^;]+;([^"]*)"': r'style="\1\2"',
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    return content

def update_page(file_path, base_dir):
    """Update a single page to use unified UI"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Remove inline <style> blocks
        content = clean_inline_styles(content)

        # 2. Ensure unified CSS is linked
        content = ensure_css_link(content, file_path, base_dir)

        # 3. Remove inline styles from body
        content = remove_body_inline_styles(content)

        # 4. Fix some common Tailwind classes
        # Note: We keep Tailwind for layout utilities, only fix conflicting ones

        # Only update if content changed
        if content != original_content:
            # Backup
            with open(f"{file_path}.ui_backup", 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return 'updated'

        return 'no_change'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🎨 QSI - Fix All Pages UI")
    print("=" * 60)
    print("This will:")
    print("  • Remove inline <style> blocks")
    print("  • Ensure all pages use qsi-styles.css")
    print("  • Make all pages respond to theme changes")
    print()
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
        and not f.name.endswith('.ui_backup')
    ]

    print(f"🔍 Found {len(html_files)} HTML files")
    print()

    updated = 0
    no_change = 0
    errors = 0

    for file_path in html_files:
        rel_file = file_path.relative_to(base_dir)
        print(f"📝 {rel_file}")

        result = update_page(file_path, base_dir)

        if result == 'updated':
            print(f"   ✅ Fixed - now uses unified UI")
            updated += 1
        elif result == 'no_change':
            print(f"   ⏭️  No changes needed")
            no_change += 1
        else:
            errors += 1

        print()

    print("=" * 60)
    print("✨ UI Fix Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:     {updated} files")
    print(f"   ⏭️  No changes:  {no_change} files")
    print(f"   ⚠️  Errors:      {errors} files")
    print()

    if updated > 0:
        print("🎉 Success!")
        print()
        print("📦 Backups saved as *.ui_backup")
        print()
        print("🧪 Testing:")
        print("   1. Open your app in browser")
        print("   2. Login and go to Settings → Theme")
        print("   3. Try switching between Light and Dark themes")
        print("   4. Navigate to ALL pages - they should all change theme")
        print()
        print("⚠️  Important:")
        print("   Some pages may need manual review for:")
        print("   • Custom components")
        print("   • Special layouts")
        print("   • Page-specific functionality")
        print()

if __name__ == '__main__':
    main()
