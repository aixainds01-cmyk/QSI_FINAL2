# QSI Unified CSS Implementation Guide

## Overview
The QSI project now has a **unified CSS design system** located at `/js/qsi-styles.css`. This single CSS file provides consistent styling across ALL pages in your project.

---

## ✅ What Has Been Done

### 1. Enhanced the Existing CSS File
- **Location**: `/js/qsi-styles.css`
- **Added**: 400+ lines of additional unified styles
- **Includes**:
  - CSS Variables for theming
  - Base styles
  - Three theme classes (`theme-dark`, `theme-light`, `theme-auth`)
  - Typography
  - Form elements
  - Buttons (10+ variants)
  - Cards
  - Tables
  - Modals
  - Alerts
  - Loading states
  - Badges
  - Progress bars
  - Sidebar navigation
  - Dashboard components
  - Utility classes

---

## 🎨 Unified Design System

### Color Palette
```css
Primary: #4f46e5 (Indigo-600)
Success: #10b981 (Green-500)
Warning: #f59e0b (Orange-500)
Danger: #ef4444 (Red-500)
Info: #3b82f6 (Blue-500)

Dark Theme Background: #1a1a2e
Light Theme Background: #f9fafb
```

### Typography
- **Font Family**: Inter (sans-serif)
- **Font Sizes**: xs (0.75rem) to 4xl (2.25rem)
- **Line Height**: 1.5 (body), 1.3 (headings)

---

## 📋 How to Use in Your HTML Pages

### Step 1: Add the CSS Link
Add this to the `<head>` section of **every HTML page**:

```html
<link rel="stylesheet" href="../js/qsi-styles.css">
<!-- OR -->
<link rel="stylesheet" href="js/qsi-styles.css"> <!-- if in root -->
```

### Step 2: Add Theme Class to Body
Choose the appropriate theme for your page:

```html
<!-- For dashboard and main app pages -->
<body class="theme-dark">

<!-- For light theme pages -->
<body class="theme-light">

<!-- For login/signup pages with gradient background -->
<body class="theme-auth">
```

### Step 3: Use the Unified Classes
Replace inline styles and Tailwind classes with the unified CSS classes:

#### Before (Inconsistent):
```html
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
```

#### After (Unified):
```html
<div class="card">
```

---

## 🔧 Common Component Examples

### Buttons
```html
<!-- Primary Button -->
<button class="btn btn-primary">Save Changes</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Cancel</button>

<!-- Success Button -->
<button class="btn btn-success">Approve</button>

<!-- Danger Button -->
<button class="btn btn-danger">Delete</button>

<!-- Outline Button -->
<button class="btn btn-outline">More Options</button>

<!-- Ghost Button -->
<button class="btn btn-ghost">Close</button>
```

### Form Elements
```html
<!-- Input Field -->
<div class="form-group">
  <label class="form-label">Email</label>
  <input type="email" class="input-field" placeholder="you@example.com">
</div>

<!-- Select Field -->
<div class="form-group">
  <label class="form-label">Status</label>
  <select class="select-field">
    <option>Select Status</option>
    <option>Active</option>
    <option>Inactive</option>
  </select>
</div>

<!-- Textarea -->
<div class="form-group">
  <label class="form-label">Description</label>
  <textarea class="textarea-field"></textarea>
</div>
```

### Cards
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
    <span class="card-badge">New</span>
  </div>
  <p>Card content goes here...</p>
</div>
```

### Dashboard Components
```html
<!-- Dashboard Card -->
<div class="dashboard-card">
  <h2 class="text-lg font-semibold">Total Sales</h2>
  <p class="stat-value">₹45,000</p>
  <p class="stat-label">This month</p>
</div>

<!-- Progress Bar -->
<div class="progress-bar-bg">
  <div class="progress-bar-fill progress-green" style="width: 75%"></div>
</div>
```

### Tables
```html
<div class="table-container">
  <table class="data-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>John Doe</td>
        <td>john@example.com</td>
        <td><span class="badge badge-success">Active</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

### Status Badges
```html
<span class="badge badge-success">Approved</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-danger">Rejected</span>
<span class="badge badge-info">In Progress</span>
```

### Alerts
```html
<div class="alert alert-success">
  <i class="fas fa-check-circle"></i>
  Your changes have been saved successfully!
</div>

<div class="alert alert-warning">
  <i class="fas fa-exclamation-triangle"></i>
  Please review your information before submitting.
</div>

<div class="alert alert-danger">
  <i class="fas fa-times-circle"></i>
  An error occurred. Please try again.
</div>
```

### Modals
```html
<div class="modal-backdrop active">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">Modal Title</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <p>Modal content goes here...</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Save</button>
    </div>
  </div>
</div>
```

### Loading States
```html
<div class="loading-overlay">
  <div class="spinner"></div>
  <p class="loading-text">Loading...</p>
</div>
```

---

## 🎯 Utility Classes

### Text Utilities
```html
<p class="text-xs">Extra small text</p>
<p class="text-sm">Small text</p>
<p class="text-base">Base text</p>
<p class="text-lg">Large text</p>
<p class="text-xl">Extra large text</p>

<p class="text-center">Centered text</p>
<p class="text-right">Right-aligned text</p>

<p class="font-normal">Normal weight</p>
<p class="font-medium">Medium weight</p>
<p class="font-semibold">Semibold weight</p>
<p class="font-bold">Bold weight</p>

<p class="text-primary">Primary color</p>
<p class="text-success">Success color</p>
<p class="text-warning">Warning color</p>
<p class="text-danger">Danger color</p>
<p class="text-muted">Muted color</p>
```

### Spacing Utilities
```html
<div class="mt-4">Margin top</div>
<div class="mb-6">Margin bottom</div>
<div class="p-4">Padding all sides</div>
<div class="px-4">Padding horizontal</div>
<div class="py-2">Padding vertical</div>
```

### Layout Utilities
```html
<div class="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Display Utilities
```html
<div class="hidden">Hidden element</div>
<div class="block">Block element</div>
<div class="flex">Flex container</div>
<div class="inline-flex">Inline flex</div>
```

### Border & Shadow Utilities
```html
<div class="rounded">Rounded corners</div>
<div class="rounded-lg">Large rounded corners</div>
<div class="rounded-full">Fully rounded</div>

<div class="shadow-sm">Small shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
```

---

## 📱 Responsive Design

The CSS includes mobile-first responsive breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1023px
- **Desktop**: ≥ 1024px

Example responsive grid:
```html
<div class="grid grid-cols-1 md-grid-cols-2 lg-grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

---

## 🔄 Migration Steps for Existing Pages

### 1. Replace Inline Styles
**Before:**
```html
<div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb;">
```

**After:**
```html
<div class="card">
```

### 2. Replace Tailwind Classes with Unified Classes
**Before:**
```html
<button class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
```

**After:**
```html
<button class="btn btn-primary">
```

### 3. Update Theme Classes
**Before:**
```html
<body style="background-color: #f9fafb;">
```

**After:**
```html
<body class="theme-light">
```

---

## 📝 Pages That Need Updates

All pages currently reference the CSS file, but some still have inline styles and Tailwind classes. Here's a prioritized list:

### High Priority (Most Inconsistencies):
1. ✅ `index.html` - Already uses unified CSS
2. `with_login/dashboard_with_login.html` - Mix of unified CSS and Tailwind
3. `with_login/settings.html` - Custom inline styles
4. `with_login/saleorder/home_sales_order.html` - Tailwind + inline styles
5. `without_login/dashboard_without_login.html` - Custom inline styles
6. `signup/sign_up.html` - Custom inline styles

### Medium Priority:
- All invoice pages (`with_login/invoice/*.html`)
- All quotation pages (`with_login/quotation/*.html`)
- All purchase pages (`with_login/parchase/**/*.html`)

### Low Priority:
- Vendor management pages
- Client management pages
- Settings-related pages

---

## 🎨 Theme Switcher Implementation

The CSS includes a theme system. To implement a theme switcher:

```javascript
// Save theme preference
localStorage.setItem('qsi-theme', 'dark'); // or 'light' or 'system'

// Apply theme
function applyTheme(theme) {
  if (theme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    theme = prefersDark ? 'dark' : 'light';
  }

  document.body.classList.remove('theme-light', 'theme-dark');
  document.body.classList.add(`theme-${theme}`);
}

// Load saved theme
const savedTheme = localStorage.getItem('qsi-theme') || 'light';
applyTheme(savedTheme);
```

---

## ⚡ Benefits of Using the Unified CSS

1. **Consistency**: All pages look and feel the same
2. **Maintainability**: Change styles in one place, affects all pages
3. **Performance**: Single CSS file, cached by browser
4. **Theme Support**: Easy dark/light mode switching
5. **Responsive**: Mobile-first design built-in
6. **Accessibility**: Proper focus states and color contrast
7. **Developer Experience**: Predictable class names, easy to remember

---

## 🔍 CSS File Structure

```
qsi-styles.css
├── CSS Variables (Colors, Typography, Spacing)
├── Base Styles (Reset, HTML, Body)
├── Theme Styles
│   ├── theme-dark
│   ├── theme-light
│   └── theme-auth
├── Typography (h1-h6, paragraphs)
├── Auth Components (Login/Signup)
├── Form Elements
│   ├── Input fields
│   ├── Select fields
│   ├── Textareas
│   └── Labels
├── Buttons (10+ variants)
├── Cards
├── Sidebar Navigation
├── Tables
├── Modals
├── Alerts
├── Badges
├── Progress Bars
├── Loading States
├── Empty States
├── Quick Actions
├── Dashboard Stats
├── Utility Classes
├── Responsive Helpers
└── Print Styles
```

---

## 📞 Support & Questions

If you encounter any styling issues:
1. Check if the CSS file is properly linked
2. Verify the theme class is applied to `<body>`
3. Ensure you're using the correct class names (refer to this guide)
4. Clear browser cache if styles don't update

---

## 🚀 Next Steps

1. **Keep using the unified CSS file** - It's already referenced in most pages
2. **Remove inline styles gradually** - Replace with unified classes
3. **Replace Tailwind classes** - Use unified classes for consistency
4. **Test on different devices** - Ensure responsive design works
5. **Implement theme switcher** - Give users dark/light mode options

---

**Last Updated**: January 2026
**Version**: 2.0.0
**File Location**: `/js/qsi-styles.css`
