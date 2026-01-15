document.addEventListener('DOMContentLoaded', () => {
    // UI Helpers
    const toast = document.getElementById('toast');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalMessage = document.getElementById('modal-message');
    const modalCancel = document.getElementById('modal-cancel');
    const modalConfirm = document.getElementById('modal-confirm');
    let modalResolve = null;

    function showToast(message, duration = 3000) {
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), duration);
    }

    function showModal(message) {
        if (!modalOverlay || !modalMessage) return Promise.resolve(false);
        modalMessage.textContent = message;
        modalOverlay.classList.add('show');
        return new Promise((resolve) => {
            modalResolve = resolve;
        });
    }

    if (modalCancel) {
        modalCancel.addEventListener('click', () => {
            modalOverlay.classList.remove('show');
            if (modalResolve) modalResolve(false);
        });
    }

    if (modalConfirm) {
        modalConfirm.addEventListener('click', () => {
            modalOverlay.classList.remove('show');
            if (modalResolve) modalResolve(true);
        });
    }

    // Custom Select Logic
    function initCustomSelect(id, optionsId, callback) {
        const wrapper = document.getElementById(id);
        const options = document.getElementById(optionsId);
        
        if (!wrapper || !options) return;

        wrapper.addEventListener('click', (e) => {
            e.stopPropagation();
            options.classList.toggle('show');
        });

        options.querySelectorAll('.custom-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const val = option.dataset.value;
                const text = option.textContent;
                wrapper.querySelector('span').textContent = text;
                wrapper.dataset.value = val;
                options.classList.remove('show');
                if (callback) callback(val);
            });
        });

        document.addEventListener('click', () => {
            options.classList.remove('show');
        });
    }

    const customInput = document.getElementById('custom-keywords');
    const customCountryInput = document.getElementById('custom-country');

    initCustomSelect('country-select', 'country-options', (val) => {
        if (customCountryInput) {
            customCountryInput.style.display = val === 'custom' ? 'block' : 'none';
        }
    });

    initCustomSelect('industry-select', 'industry-options', (val) => {
        if (customInput) {
            customInput.style.display = val === 'custom' ? 'block' : 'none';
        }
    });

    // Sidebar Navigation
    const sections = document.querySelectorAll('.section');
    const navItems = document.querySelectorAll('.sidebar nav ul li');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetSectionId = item.dataset.section;
            const targetSection = document.getElementById(targetSectionId);
            
            if (!targetSection) return;

            // Update active nav item
            navItems.forEach(ni => ni.classList.remove('active'));
            item.classList.add('active');

            // Update active section
            sections.forEach(s => s.classList.remove('active'));
            targetSection.classList.add('active');
        });
    });

    // Start Scrape
    const startScrapeBtn = document.getElementById('start-scrape');
    if (startScrapeBtn) {
        startScrapeBtn.addEventListener('click', () => {
            const countrySelect = document.getElementById('country-select');
            const industrySelect = document.getElementById('industry-select');
            
            let country = countrySelect ? countrySelect.dataset.value : 'all';
            let industry = industrySelect ? industrySelect.dataset.value : 'finance';
            
            if (country === 'custom' && customCountryInput) {
                country = customCountryInput.value || 'all';
            }

            if (industry === 'custom' && customInput) {
                industry = customInput.value || 'finance';
            }

            const status = document.getElementById('scrape-status');
            const progress = document.getElementById('progress-bar');
            
            if (status) status.textContent = 'Scrape started...';
            showToast('🚀 Scrape pipeline initiated');
            if (progress) progress.style.width = '0%';

            fetch('/scrape', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    if (status) status.textContent = 'Scrape running in background...';
                    let width = 0;
                    const interval = setInterval(() => {
                        width += Math.random() * 5;
                        if (width >= 100) { 
                            width = 100; 
                            clearInterval(interval); 
                            if (status) status.textContent = 'Scrape queued!'; 
                            showToast('✅ Scrape successfully queued');
                        }
                        if (progress) progress.style.width = width + '%';
                    }, 500);
                })
                .catch(err => {
                    if (status) status.textContent = 'Error starting scrape';
                    showToast('❌ Failed to start scrape');
                    console.error(err);
                });
        });
    }

    // Export Files
    window.exportFile = function(type) {
        const status = document.getElementById('export-status');
        showToast(`📦 Preparing ${type.toUpperCase()} export...`);
        fetch(`/export/${type}`)
            .then(res => {
                if (res.ok) {
                    if (status) status.textContent = `Downloading ${type.toUpperCase()}...`;
                    return res.blob();
                } else { throw 'Export failed'; }
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `domains.${type}`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                if (status) status.textContent = `Downloaded ${type.toUpperCase()}`;
                showToast(`💾 ${type.toUpperCase()} downloaded successfully`);
            })
            .catch(err => {
                if (status) status.textContent = 'Export failed';
                showToast('❌ Export failed');
                console.error(err);
            });
    };

    // Theme Toggle
    const themeToggle = document.getElementById('toggle-theme');
    const mobileThemeToggle = document.getElementById('mobile-toggle-theme');

    const toggleTheme = () => {
        const isLight = document.body.classList.toggle('light');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    };

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    if (mobileThemeToggle) {
        mobileThemeToggle.addEventListener('click', toggleTheme);
    }

    // Action Buttons
    const refreshBtn = document.getElementById('refresh-data');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadStats();
            showToast('🔄 Stats refreshed');
            refreshBtn.style.transform = 'scale(0.95)';
            setTimeout(() => refreshBtn.style.transform = 'scale(1)', 100);
        });
    }

    const deleteBtn = document.getElementById('delete-data');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async () => {
            const confirmed = await showModal('Are you sure you want to delete all stored domains? This action cannot be undone.');
            if (confirmed) {
                fetch('/api/domains', { method: 'DELETE' })
                    .then(res => res.json())
                    .then(data => {
                        loadStats();
                        showToast('🗑️ Database cleared');
                    })
                    .catch(err => {
                        console.error('Failed to delete domains:', err);
                        showToast('❌ Deletion failed');
                    });
            }
        });
    }

    // Load stats
    function loadStats() {
        fetch('/api/stats')
            .then(res => res.json())
            .then(data => {
                const total = document.getElementById('total-domains');
                const ind = document.getElementById('industry-count');
                const count = document.getElementById('country-count');
                if (total) total.textContent = data.total_domains;
                if (ind) ind.textContent = data.industry_count;
                if (count) count.textContent = data.country_count;
            })
            .catch(err => console.error('Failed to load stats:', err));
    }

    loadStats();
    setInterval(loadStats, 30000);
});