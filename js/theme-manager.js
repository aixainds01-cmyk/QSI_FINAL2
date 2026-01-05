/**
 * QSI Global Theme Manager
 * Manages theme preferences across all pages
 * Version: 1.0.0
 */

(function() {
  'use strict';

  const THEME_STORAGE_KEY = 'qsi-theme';
  const THEME_CLASSES = ['theme-light', 'theme-dark', 'theme-auth'];

  /**
   * Get the current theme preference
   * @returns {string} 'light', 'dark', or 'system'
   */
  function getThemePreference() {
    return localStorage.getItem(THEME_STORAGE_KEY) || 'light';
  }

  /**
   * Set theme preference
   * @param {string} theme - 'light', 'dark', or 'system'
   */
  function setThemePreference(theme) {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
    applyTheme(theme);

    // Dispatch custom event so other parts of the app can react
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
  }

  /**
   * Apply theme to the current page
   * @param {string} theme - 'light', 'dark', or 'system'
   */
  function applyTheme(theme) {
    let actualTheme = theme;

    // Handle system preference
    if (theme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      actualTheme = prefersDark ? 'dark' : 'light';
    }

    // Remove all theme classes
    document.body.classList.remove(...THEME_CLASSES);

    // Don't apply theme to auth pages (login, signup) - they use theme-auth
    const isAuthPage = window.location.pathname.includes('index.html') ||
                       window.location.pathname.includes('sign_up.html') ||
                       window.location.pathname.includes('businessDetails.html') ||
                       window.location.pathname.includes('bank_detail.html');

    if (isAuthPage) {
      document.body.classList.add('theme-auth');
    } else {
      // Apply the selected theme
      document.body.classList.add(`theme-${actualTheme}`);
    }

    // Update any theme-dependent elements
    updateThemeDependentElements(actualTheme);
  }

  /**
   * Update elements that depend on theme (like sticky headers, etc.)
   */
  function updateThemeDependentElements(theme) {
    // Update sticky headers if they exist
    const stickyHeader = document.querySelector('.sticky-header');
    if (stickyHeader) {
      const bgColor = theme === 'dark' ? 'var(--dark-bg-primary)' : 'var(--light-bg-secondary)';
      stickyHeader.style.backgroundColor = bgColor;
    }

    // Update any other theme-dependent elements here
    const mainContent = document.getElementById('main-content');
    if (mainContent && theme === 'dark') {
      mainContent.style.backgroundColor = 'var(--dark-bg-primary)';
    } else if (mainContent && theme === 'light') {
      mainContent.style.backgroundColor = 'var(--light-bg-secondary)';
    }
  }

  /**
   * Initialize theme on page load
   */
  function initTheme() {
    const savedTheme = getThemePreference();
    applyTheme(savedTheme);

    // Listen for system theme changes
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeMediaQuery.addEventListener('change', (e) => {
      const currentTheme = getThemePreference();
      if (currentTheme === 'system') {
        applyTheme('system');
      }
    });

    // Listen for storage changes (theme changed in another tab)
    window.addEventListener('storage', (e) => {
      if (e.key === THEME_STORAGE_KEY && e.newValue) {
        applyTheme(e.newValue);
      }
    });
  }

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }

  // Expose public API
  window.QSITheme = {
    get: getThemePreference,
    set: setThemePreference,
    apply: applyTheme,
    THEMES: {
      LIGHT: 'light',
      DARK: 'dark',
      SYSTEM: 'system'
    }
  };

})();
