#!/bin/bash

##############################################
# QSI Theme Manager - Complete Update Script
# Updates ALL HTML pages in the project
##############################################

echo "🎨 QSI Theme Manager - Complete Update Script"
echo "=============================================="
echo ""

# Counter for updated files
updated=0
skipped=0
errors=0

# Function to calculate relative path to js folder
get_relative_path() {
    local file_path="$1"
    local depth=$(echo "$file_path" | grep -o "/" | wc -l)

    if [ $depth -eq 0 ]; then
        echo "js"
    elif [ $depth -eq 1 ]; then
        echo "../js"
    elif [ $depth -eq 2 ]; then
        echo "../../js"
    elif [ $depth -eq 3 ]; then
        echo "../../../js"
    else
        echo "../../../../js"
    fi
}

# Function to update a single file
update_file() {
    local file="$1"

    # Skip if file doesn't exist
    if [ ! -f "$file" ]; then
        return
    fi

    # Skip backup files
    if [[ "$file" == *.backup ]]; then
        return
    fi

    # Check if theme-manager.js is already included
    if grep -q "theme-manager.js" "$file"; then
        echo "⏭️  Already has theme manager: $file"
        ((skipped++))
        return
    fi

    # Calculate relative path
    local rel_path=$(get_relative_path "$file")

    echo "📝 Processing: $file"
    echo "   Path to JS: $rel_path"

    # Backup original file
    cp "$file" "$file.backup"

    # Add theme manager script before </head>
    if grep -q "</head>" "$file"; then
        sed -i '' "s|</head>|    <!-- Global Theme Manager -->\n    <script src=\"$rel_path/theme-manager.js\"></script>\n</head>|" "$file"
    else
        echo "   ⚠️  Warning: No </head> tag found in $file"
        ((errors++))
        return
    fi

    # Remove theme-dark class from body (but keep theme-auth)
    sed -i '' 's/<body class="theme-dark">/<body>/g' "$file"
    sed -i '' 's/<body class="theme-dark /<body class="/g' "$file"

    # Remove theme-light class from body (but keep theme-auth)
    sed -i '' 's/<body class="theme-light">/<body>/g' "$file"
    sed -i '' 's/<body class="theme-light /<body class="/g' "$file"

    echo "   ✅ Updated successfully!"
    ((updated++))
}

echo "🔍 Finding all HTML files..."
echo ""

# Find and update ALL HTML files recursively
while IFS= read -r file; do
    update_file "$file"
done < <(find . -type f -name "*.html" ! -path "*/node_modules/*" ! -path "*/.git/*")

echo ""
echo "=============================================="
echo "✨ Update Complete!"
echo ""
echo "📊 Statistics:"
echo "   ✅ Updated:        $updated files"
echo "   ⏭️  Already Updated: $skipped files"
echo "   ⚠️  Errors:         $errors files"
echo ""

if [ $updated -gt 0 ]; then
    echo "🎉 Success! $updated pages have been updated."
    echo ""
    echo "💡 Next Steps:"
    echo "   1. Test the theme switching in your browser"
    echo "   2. Go to Settings → Theme and change themes"
    echo "   3. Navigate to different pages to verify theme applies"
    echo ""
    echo "📦 Backups:"
    echo "   • All original files saved as *.backup"
    echo "   • To delete backups after testing:"
    echo "     find . -name '*.backup' -delete"
    echo ""
    echo "🔄 To restore backups (if needed):"
    echo "   for f in \$(find . -name '*.backup'); do mv \"\$f\" \"\${f%.backup}\"; done"
else
    echo "ℹ️  All files were already updated or no HTML files found."
fi

echo ""
echo "📖 For more info, see:"
echo "   • README_THEME_SETUP.md - Quick start"
echo "   • THEME_SYSTEM_GUIDE.md - Complete guide"
echo ""
