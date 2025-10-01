// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Active navigation highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}` || 
                (current === '' && link.getAttribute('href') === '#home')) {
                link.classList.add('active');
            }
        });
    });
});

// Prediction form functionality
const predictionForm = document.getElementById('predictionForm');
const resultContainer = document.getElementById('resultContainer');

if (predictionForm) {
    predictionForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        showLoadingState();
        
        // Collect form data
        const formData = new FormData(predictionForm);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showPredictionResult(result);
            } else {
                showError(result.error);
            }
        } catch (error) {
            showError('Network error. Please try again.');
        }
    });
}

function showLoadingState() {
    const resultContainer = document.getElementById('resultContainer');
    const resultIcon = document.getElementById('resultIcon');
    const predictionStatus = document.getElementById('predictionStatus');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidencePercentage = document.getElementById('confidencePercentage');
    
    resultContainer.style.display = 'block';
    resultIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    predictionStatus.innerHTML = '<span class="status-text">Analyzing...</span>';
    confidenceFill.style.width = '0%';
    confidencePercentage.textContent = '0%';
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

function showPredictionResult(result) {
    const resultIcon = document.getElementById('resultIcon');
    const predictionStatus = document.getElementById('predictionStatus');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidencePercentage = document.getElementById('confidencePercentage');
    const resultDetails = document.getElementById('resultDetails');
    
    // Update icon and status
    if (result.prediction === 'Crisis') {
        resultIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        resultIcon.className = 'result-icon crisis';
        predictionStatus.innerHTML = '<span class="status-text crisis">CRISIS DETECTED</span>';
    } else {
        resultIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        resultIcon.className = 'result-icon no-crisis';
        predictionStatus.innerHTML = '<span class="status-text no-crisis">NO CRISIS</span>';
    }
    
    // Animate confidence bar
    setTimeout(() => {
        confidenceFill.style.width = result.probability + '%';
        confidencePercentage.textContent = result.probability + '%';
    }, 500);
    
    // Add result details
    resultDetails.innerHTML = `
        <div class="result-info">
            <p><strong>Prediction:</strong> ${result.prediction}</p>
            <p><strong>Confidence:</strong> ${result.probability}%</p>
            <p><strong>Model:</strong> Random Forest Classifier</p>
        </div>
    `;
}

function showError(error) {
    const resultIcon = document.getElementById('resultIcon');
    const predictionStatus = document.getElementById('predictionStatus');
    const resultDetails = document.getElementById('resultDetails');
    
    resultIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
    resultIcon.className = 'result-icon';
    resultIcon.style.color = '#e74c3c';
    
    predictionStatus.innerHTML = '<span class="status-text" style="background: #e74c3c; color: white;">Error</span>';
    
    resultDetails.innerHTML = `
        <div class="result-info">
            <p style="color: #e74c3c;"><strong>Error:</strong> ${error}</p>
        </div>
    `;
}

function resetForm() {
    predictionForm.reset();
    resultContainer.style.display = 'none';
    
    // Scroll back to form
    document.getElementById('predict').scrollIntoView({ behavior: 'smooth' });
}

// Charts functionality
let crisisChart, countryChart, timelineChart;

async function loadCharts() {
    try {
        const response = await fetch('/data');
        const data = await response.json();
        
        createCrisisChart(data.crisis_distribution);
        createCountryChart(data.country_crisis);
        createTimelineChart(data.year_crisis);
    } catch (error) {
        console.error('Error loading chart data:', error);
    }
}

function createCrisisChart(crisisData) {
    const ctx = document.getElementById('crisisChart');
    if (!ctx) return;
    
    crisisChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(crisisData).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
            datasets: [{
                data: Object.values(crisisData),
                backgroundColor: [
                    '#e74c3c',
                    '#27ae60'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createCountryChart(countryData) {
    const ctx = document.getElementById('countryChart');
    if (!ctx) return;
    
    const labels = Object.keys(countryData);
    const data = Object.values(countryData);
    
    countryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Crisis Count',
                data: data,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createTimelineChart(yearData) {
    const ctx = document.getElementById('timelineChart');
    if (!ctx) return;
    
    const labels = Object.keys(yearData).sort((a, b) => parseInt(a) - parseInt(b));
    const data = labels.map(year => yearData[year]);
    
    timelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Crisis Count',
                data: data,
                borderColor: 'rgba(231, 76, 60, 1)',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Initialize charts when analytics section is visible
const analyticsSection = document.getElementById('analytics');
if (analyticsSection) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadCharts();
                observer.unobserve(entry.target);
            }
        });
    });
    
    observer.observe(analyticsSection);
}

// Form validation and enhancement
function enhanceForm() {
    const inputs = document.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        // Add real-time validation
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            
            if (this.value !== '' && (value < min || value > max)) {
                this.style.borderColor = '#e74c3c';
                this.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.1)';
            } else {
                this.style.borderColor = '#667eea';
                this.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
            }
        });
        
        // Add helpful tooltips
        input.addEventListener('focus', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = `Enter a value between ${this.min} and ${this.max}`;
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
                top: -30px;
                left: 0;
            `;
            
            this.parentNode.style.position = 'relative';
            this.parentNode.appendChild(tooltip);
        });
        
        input.addEventListener('blur', function() {
            const tooltip = this.parentNode.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Initialize form enhancements
if (predictionForm) {
    enhanceForm();
}

// Add some interactive animations
function addAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.about-card, .chart-card, .form-container, .result-container').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Initialize animations
addAnimations(); 