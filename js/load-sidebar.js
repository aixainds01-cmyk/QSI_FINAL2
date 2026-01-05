/**
 * Load Unified Sidebar on ALL pages
 * This ensures every page has the EXACT same sidebar
 */

(function() {
    'use strict';

    // Function to get the correct path to components based on current page location
    function getComponentPath() {
        const path = window.location.pathname;

        // Determine folder depth
        if (path.includes('/with_login/quotation/') ||
            path.includes('/with_login/invoice/') ||
            path.includes('/with_login/saleorder/') ||
            path.includes('/with_login/parchase/parchase_order/') ||
            path.includes('/with_login/parchase/vendor/')) {
            return '../components/sidebar.html';
        } else if (path.includes('/with_login/parchase/')) {
            return '../components/sidebar.html';
        } else if (path.includes('/with_login/')) {
            return 'components/sidebar.html';
        }

        return 'with_login/components/sidebar.html';
    }

    // Function to fix relative paths in the sidebar based on current page
    function fixSidebarPaths(sidebarHTML) {
        const path = window.location.pathname;
        let prefix = '';

        // Determine path prefix based on folder depth
        if (path.includes('/with_login/quotation/') ||
            path.includes('/with_login/invoice/') ||
            path.includes('/with_login/saleorder/')) {
            prefix = '../';
        } else if (path.includes('/with_login/parchase/parchase_order/') ||
                   path.includes('/with_login/parchase/vendor/') ||
                   path.includes('/with_login/parchase/debit')) {
            prefix = '../../';
        } else if (path.includes('/with_login/parchase/')) {
            prefix = '../';
        }

        // Fix all href paths
        if (prefix) {
            sidebarHTML = sidebarHTML.replace(/href="([^h#][^"]*)"/g, `href="${prefix}$1"`);
        }

        return sidebarHTML;
    }

    // Function to set active link based on current page
    function setActiveLink() {
        const currentPath = window.location.pathname;
        const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1);

        // Remove all active classes first
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.classList.remove('active');
        });

        // Add active class to matching link
        document.querySelectorAll('.sidebar-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href && (href.includes(filename) || currentPath.includes(href))) {
                link.classList.add('active');
            }
        });
    }

    // Load sidebar
    function loadSidebar() {
        const sidebarPlaceholder = document.getElementById('sidebar-placeholder');

        if (!sidebarPlaceholder) {
            console.warn('No sidebar placeholder found. Sidebar already loaded or page structure different.');
            // Sidebar might already be in HTML, just set active link
            setActiveLink();
            return;
        }

        const componentPath = getComponentPath();

        fetch(componentPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                // Fix paths
                html = fixSidebarPaths(html);

                // Insert sidebar
                sidebarPlaceholder.outerHTML = html;

                // Set active link
                setTimeout(setActiveLink, 100);

                console.log('✅ Unified sidebar loaded successfully');
            })
            .catch(error => {
                console.error('Error loading sidebar:', error);
                // Fallback: leave existing sidebar if any
            });
    }

    // Load when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadSidebar);
    } else {
        loadSidebar();
    }

})();
