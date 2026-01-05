#!/usr/bin/env python3
"""
Apply Professional Unified Sidebar to All Pages
Updates all HTML pages with the new sidebar structure
"""

import os
import re
from pathlib import Path
import shutil

def calculate_relative_path(from_file, to_dir):
    """Calculate relative path from file to directory"""
    return os.path.relpath(to_dir, os.path.dirname(from_file))

def read_sidebar_template(template_path):
    """Read the sidebar template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def update_page_with_sidebar(file_path, sidebar_html, base_dir):
    """Update a single page with new sidebar"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if page has proper structure
        if '<body' not in content or '</body>' not in content:
            return 'malformed'

        # Calculate relative paths
        rel_js_path = calculate_relative_path(file_path, os.path.join(base_dir, 'js'))
        rel_components_path = calculate_relative_path(file_path, os.path.join(base_dir, 'with_login'))

        # Adjust sidebar HTML paths based on file location
        adjusted_sidebar = sidebar_html.replace('href="../', f'href="{rel_components_path}/')
        adjusted_sidebar = adjusted_sidebar.replace('href="../', f'href="{rel_components_path}/')

        # Add professional-sidebar.css if not present
        changed = False
        if 'professional-sidebar.css' not in content:
            # Find theme-force.css and add after it
            if 'theme-force.css' in content:
                pattern = r'(<link[^>]*theme-force\.css[^>]*>)'
                match = re.search(pattern, content)
                if match:
                    old_line = match.group(1)
                    new_lines = f'{old_line}\n    <link rel="stylesheet" href="{rel_js_path}/professional-sidebar.css">'
                    content = content.replace(old_line, new_lines, 1)
                    changed = True
            else:
                # Add before </head>
                content = content.replace('</head>', f'    <link rel="stylesheet" href="{rel_js_path}/professional-sidebar.css">\n</head>', 1)
                changed = True

        # Remove old sidebar (look for common patterns)
        # Pattern 1: <aside>...</aside>
        old_sidebar_pattern = r'<aside[^>]*>.*?</aside>'
        if re.search(old_sidebar_pattern, content, re.DOTALL):
            content = re.sub(old_sidebar_pattern, '<!-- SIDEBAR_PLACEHOLDER -->', content, flags=re.DOTALL, count=1)
            changed = True
        # Pattern 2: <div class="sidebar">...</div>
        elif re.search(r'<div[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</div>', content, re.DOTALL):
            pattern = r'<div[^>]*class="[^"]*sidebar[^"]*"[^>]*>.*?</div>'
            # This is tricky - we need to find the matching closing div
            # For safety, let's look for a specific pattern
            if 'id="sidebar"' in content or 'class="sidebar"' in content:
                # Insert placeholder after <body> tag
                body_match = re.search(r'(<body[^>]*>)', content)
                if body_match:
                    body_tag = body_match.group(1)
                    content = content.replace(body_tag, f'{body_tag}\n    <!-- SIDEBAR_PLACEHOLDER -->\n', 1)
                    changed = True

        # If no old sidebar found, add placeholder after <body>
        if '<!-- SIDEBAR_PLACEHOLDER -->' not in content:
            body_match = re.search(r'(<body[^>]*>)', content)
            if body_match:
                body_tag = body_match.group(1)
                content = content.replace(body_tag, f'{body_tag}\n    <!-- SIDEBAR_PLACEHOLDER -->\n', 1)
                changed = True

        # Replace placeholder with new sidebar
        if '<!-- SIDEBAR_PLACEHOLDER -->' in content:
            content = content.replace('<!-- SIDEBAR_PLACEHOLDER -->', adjusted_sidebar)
            changed = True

        if not changed:
            return 'skipped'

        # Backup original
        backup_path = f"{file_path}.sidebar_backup"
        if not os.path.exists(backup_path):
            shutil.copy2(file_path, backup_path)

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'updated'

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 'error'

def main():
    print("🎨 Applying Professional Unified Sidebar")
    print("=" * 70)
    print("This will:")
    print("  • Add professional-sidebar.css to all pages")
    print("  • Replace old sidebars with new unified sidebar")
    print("  • Update menu structure with correct items")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent
    sidebar_template = base_dir / 'with_login' / 'components' / 'unified_sidebar.html'

    # Read sidebar template
    if not sidebar_template.exists():
        print(f"❌ Error: Sidebar template not found at {sidebar_template}")
        return

    sidebar_html = read_sidebar_template(sidebar_template)
    print(f"✅ Loaded sidebar template ({len(sidebar_html)} characters)")
    print()

    # Find all HTML files in with_login directory
    with_login_dir = base_dir / 'with_login'
    html_files = []

    for root, dirs, files in os.walk(with_login_dir):
        # Skip components directory
        if 'components' in root:
            continue

        for file in files:
            if file.endswith('.html') and not file.endswith('.backup') and not file.endswith('.sidebar_backup'):
                html_files.append(Path(root) / file)

    print(f"🔍 Found {len(html_files)} HTML files to update")
    print()

    updated = 0
    skipped = 0
    errors = 0
    malformed = 0

    for file_path in sorted(html_files):
        rel_path = file_path.relative_to(base_dir)
        print(f"📝 {rel_path}")

        result = update_page_with_sidebar(file_path, sidebar_html, base_dir)

        if result == 'updated':
            print(f"   ✅ Sidebar updated")
            updated += 1
        elif result == 'skipped':
            print(f"   ⏭️  Already has new sidebar")
            skipped += 1
        elif result == 'malformed':
            print(f"   ⚠️  Malformed HTML (skipped)")
            malformed += 1
        else:
            errors += 1

        print()

    print("=" * 70)
    print("✨ Sidebar Update Complete!")
    print()
    print("📊 Statistics:")
    print(f"   ✅ Updated:      {updated} files")
    print(f"   ⏭️  Skipped:      {skipped} files")
    print(f"   ⚠️  Malformed:    {malformed} files")
    print(f"   ❌ Errors:       {errors} files")
    print()

    if updated > 0:
        print("🎉 Professional sidebar applied to all pages!")
        print()
        print("📋 New Sidebar Structure:")
        print("   1. Dashboard")
        print("   2. Sales Documents (Quotations, Sales Orders, Invoices, Credit Notes)")
        print("   3. Purchase Documents (Vendors, Purchase Orders, Bills, Debit Notes)")
        print("   4. Management (Payouts, Clients, Items, Settings)")
        print()
        print("🧪 NEXT STEPS:")
        print("   1. Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)")
        print("   2. Test any page - sidebar should be professional and unified")
        print("   3. Verify all menu items are present")
        print("   4. Test mobile responsive design")
        print("   5. Check theme switching (Settings page)")
        print()

if __name__ == '__main__':
    main()
