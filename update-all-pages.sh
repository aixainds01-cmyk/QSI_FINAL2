#!/bin/bash

##############################################
# QSI Theme Manager - Bulk Update Script
# This script adds theme manager to all HTML pages
##############################################

echo "🎨 QSI Theme Manager - Bulk Update Script"
echo "=========================================="
echo ""

# Counter for updated files
updated=0
skipped=0

# Function to update a single file
update_file() {
    local file="$1"
    local relative_path="$2"

    # Skip if file doesn't exist
    if [ ! -f "$file" ]; then
        return
    fi

    # Check if theme-manager.js is already included
    if grep -q "theme-manager.js" "$file"; then
        echo "⏭️  Skipped (already has theme manager): $file"
        ((skipped++))
        return
    fi

    # Backup original file
    cp "$file" "$file.backup"

    # Add theme manager script before </head>
    sed -i '' "s|</head>|    <!-- Global Theme Manager -->\n    <script src=\"$relative_path/js/theme-manager.js\"></script>\n</head>|" "$file"

    # Remove theme-dark class from body
    sed -i '' 's/<body class="theme-dark">/<body>/g' "$file"

    # Remove theme-light class from body (but keep theme-auth)
    sed -i '' 's/<body class="theme-light">/<body>/g' "$file"

    echo "✅ Updated: $file"
    ((updated++))
}

echo "Updating pages in /with_login..."
echo ""

# Update root level with_login pages
for file in with_login/*.html; do
    [ -f "$file" ] && update_file "$file" ".."
done

# Update invoice pages
for file in with_login/invoice/*.html; do
    [ -f "$file" ] && update_file "$file" "../.."
done

# Update sales order pages
for file in with_login/saleorder/*.html; do
    [ -f "$file" ] && update_file "$file" "../.."
done

# Update quotation pages
for file in with_login/quotation/*.html; do
    [ -f "$file" ] && update_file "$file" "../.."
done

# Update purchase order pages
for file in with_login/parchase/parchase_order/*.html; do
    [ -f "$file" ] && update_file "$file" "../../.."
done

# Update vendor pages
for file in with_login/parchase/vendor/*.html; do
    [ -f "$file" ] && update_file "$file" "../../.."
done

# Update debit notes pages
for file in with_login/parchase/debit\ notes/*.html; do
    [ -f "$file" ] && update_file "$file" "../../.."
done

# Update other purchase pages
for file in with_login/parchase/*.html; do
    [ -f "$file" ] && update_file "$file" "../.."
done

echo ""
echo "Updating pages in /without_login..."
echo ""

# Update without_login pages
for file in without_login/*.html; do
    [ -f "$file" ] && update_file "$file" ".."
done

echo ""
echo "Updating signup pages..."
echo ""

# Update signup pages
for file in signup/*.html; do
    [ -f "$file" ] && update_file "$file" ".."
done

echo ""
echo "=========================================="
echo "✨ Update Complete!"
echo ""
echo "📊 Statistics:"
echo "   ✅ Updated: $updated files"
echo "   ⏭️  Skipped: $skipped files"
echo ""
echo "💡 Next Steps:"
echo "   1. Test a few pages to verify theme switching works"
echo "   2. If everything looks good, delete .backup files:"
echo "      find . -name '*.backup' -delete"
echo "   3. If something went wrong, restore backups:"
echo "      for f in **/*.backup; do mv \"\$f\" \"\${f%.backup}\"; done"
echo ""
echo "📖 For more information, see THEME_SYSTEM_GUIDE.md"
echo ""
