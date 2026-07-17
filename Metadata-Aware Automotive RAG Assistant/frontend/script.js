/**
 * Drive Wise - Frontend Application Script
 * Handles chat interactions, API calls, animations, and UI state management.
 */

// ═══════════════════════════════════════════════
// Configuration
// ═══════════════════════════════════════════════
const API_BASE = window.location.origin;

// ═══════════════════════════════════════════════
// State Management
// ═══════════════════════════════════════════════
const state = {
    selectedBrand: '',
    selectedModel: '',
    isLoading: false,
    chatHistory: [],
    brands: [],
    models: []
};

// ═══════════════════════════════════════════════
// DOM Elements
// ═══════════════════════════════════════════════
const elements = {
    brandSelect: document.getElementById('brand-select'),
    modelSelect: document.getElementById('model-select'),
    chatInput: document.getElementById('chat-input'),
    sendBtn: document.getElementById('send-btn'),
    messagesArea: document.getElementById('messages-area'),
    charCount: document.getElementById('char-count'),
    headerTitle: document.getElementById('header-title'),
    headerStatus: document.getElementById('header-status'),
    statusDot: document.getElementById('status-dot'),
    uploadBtn: document.getElementById('upload-btn'),
    uploadModal: document.getElementById('upload-modal'),
    modalClose: document.getElementById('modal-close'),
    uploadForm: document.getElementById('upload-form'),
    fileDropZone: document.getElementById('file-drop-zone'),
    fileInput: document.getElementById('file-input'),
    fileName: document.getElementById('file-name'),
    mobileToggle: document.getElementById('mobile-toggle'),
    sidebar: document.getElementById('sidebar'),
    mobileOverlay: document.getElementById('mobile-overlay'),
    statDocs: document.getElementById('stat-docs'),
    statQueries: document.getElementById('stat-queries'),
    statAvgTime: document.getElementById('stat-avg-time'),
    statGemini: document.getElementById('stat-gemini')
};

// ═══════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    try {
        // Fetch available brands
        await fetchBrands();
        
        // Check health status
        await checkHealth();

        console.log('Drive Wise initialized successfully');
    } catch (error) {
        console.error('Initialization error:', error);
        showToast('Failed to connect to server. Ensure the backend is running.', 'error');
    }
}

// ═══════════════════════════════════════════════
// Event Listeners
// ═══════════════════════════════════════════════
function setupEventListeners() {
    // Brand selection
    elements.brandSelect.addEventListener('change', async (e) => {
        state.selectedBrand = e.target.value;
        state.selectedModel = '';
        elements.modelSelect.innerHTML = '<option value="">Select Model</option>';
        
        if (state.selectedBrand) {
            await fetchModels(state.selectedBrand);
        }
        updateHeaderInfo();
    });

    // Model selection
    elements.modelSelect.addEventListener('change', (e) => {
        state.selectedModel = e.target.value;
        updateHeaderInfo();
    });

    // Chat input
    elements.chatInput.addEventListener('input', () => {
        updateCharCount();
        autoResizeInput();
    });

    elements.chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send button
    elements.sendBtn.addEventListener('click', sendMessage);

    // Upload modal
    elements.uploadBtn.addEventListener('click', () => {
        elements.uploadModal.classList.add('active');
    });

    elements.modalClose.addEventListener('click', () => {
        elements.uploadModal.classList.remove('active');
    });

    elements.uploadModal.addEventListener('click', (e) => {
        if (e.target === elements.uploadModal) {
            elements.uploadModal.classList.remove('active');
        }
    });

    // File drop zone
    elements.fileDropZone.addEventListener('click', () => {
        elements.fileInput.click();
    });

    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            elements.fileName.textContent = e.target.files[0].name;
            elements.fileDropZone.classList.add('active');
        }
    });

    elements.fileDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.fileDropZone.classList.add('active');
    });

    elements.fileDropZone.addEventListener('dragleave', () => {
        if (!elements.fileInput.files.length) {
            elements.fileDropZone.classList.remove('active');
        }
    });

    elements.fileDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].name.endsWith('.pdf')) {
            elements.fileInput.files = files;
            elements.fileName.textContent = files[0].name;
            elements.fileDropZone.classList.add('active');
        } else {
            showToast('Please upload a PDF file', 'error');
        }
    });

    // Upload form submission
    elements.uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await uploadBrochure();
    });

    // Mobile sidebar toggle
    elements.mobileToggle.addEventListener('click', () => {
        elements.sidebar.classList.toggle('open');
        elements.mobileOverlay.classList.toggle('active');
    });

    elements.mobileOverlay.addEventListener('click', () => {
        elements.sidebar.classList.remove('open');
        elements.mobileOverlay.classList.remove('active');
    });

    // Suggestion chips
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('suggestion-chip')) {
            elements.chatInput.value = e.target.textContent;
            updateCharCount();
            elements.chatInput.focus();
        }
    });
}

// ═══════════════════════════════════════════════
// API Calls
// ═══════════════════════════════════════════════
async function fetchBrands() {
    try {
        const response = await fetch(`${API_BASE}/api/brands`);
        const data = await response.json();
        state.brands = data.brands;

        elements.brandSelect.innerHTML = '<option value="">Select Brand</option>';
        data.brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand;
            option.textContent = brand;
            elements.brandSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to fetch brands:', error);
    }
}

async function fetchModels(brand) {
    try {
        const response = await fetch(`${API_BASE}/api/models/${encodeURIComponent(brand)}`);
        const data = await response.json();
        state.models = data.models;

        elements.modelSelect.innerHTML = '<option value="">Select Model</option>';
        data.models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            elements.modelSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to fetch models:', error);
    }
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();

        elements.statDocs.textContent = data.documents_loaded;
        elements.statGemini.textContent = data.gemini_available ? 'Active' : 'Fallback';
        elements.statGemini.className = `stat-value ${data.gemini_available ? 'success' : 'accent'}`;

        if (data.gemini_available) {
            elements.statusDot.classList.remove('offline');
        }
    } catch (error) {
        elements.statusDot.classList.add('offline');
        elements.headerStatus.querySelector('span').textContent = 'Offline';
    }
}

async function sendMessage() {
    const query = elements.chatInput.value.trim();

    if (!query || state.isLoading) return;

    if (!state.selectedBrand || !state.selectedModel) {
        showToast('Please select a brand and model first', 'info');
        return;
    }

    // Clear input
    elements.chatInput.value = '';
    updateCharCount();
    autoResizeInput();

    // Remove welcome message
    const welcome = elements.messagesArea.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    // Add user message
    addMessage('user', query);

    // Show typing indicator
    state.isLoading = true;
    elements.sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                brand: state.selectedBrand,
                model: state.selectedModel
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add assistant message with sources
        addAssistantMessage(data);

        // Update stats
        updateStats();

    } catch (error) {
        removeTypingIndicator();
        addMessage('assistant', `Sorry, I encountered an error: ${error.message}. Please try again.`);
        console.error('Chat error:', error);
    } finally {
        state.isLoading = false;
        elements.sendBtn.disabled = false;
    }
}

async function uploadBrochure() {
    const formData = new FormData();
    const fileInput = elements.fileInput;
    const brand = document.getElementById('upload-brand').value;
    const model = document.getElementById('upload-model').value;
    const version = document.getElementById('upload-version').value || '2024';

    if (!fileInput.files.length || !brand || !model) {
        showToast('Please fill in all fields and select a PDF file', 'error');
        return;
    }

    formData.append('file', fileInput.files[0]);
    formData.append('brand', brand);
    formData.append('model', model);
    formData.append('document_version', version);

    // Show progress
    const progressBar = document.querySelector('.upload-progress');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    const submitBtn = document.querySelector('.modal-submit');

    progressBar.classList.add('active');
    submitBtn.disabled = true;
    progressFill.style.width = '30%';
    progressText.textContent = 'Uploading brochure...';

    try {
        progressFill.style.width = '60%';
        progressText.textContent = 'Processing and chunking...';

        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }

        const data = await response.json();

        progressFill.style.width = '100%';
        progressText.textContent = `✅ ${data.message}`;

        showToast(`Successfully uploaded ${data.brand} ${data.model} brochure (${data.chunks_created} chunks)`, 'success');

        // Refresh brands/models
        await fetchBrands();
        await checkHealth();

        // Close modal after delay
        setTimeout(() => {
            elements.uploadModal.classList.remove('active');
            progressBar.classList.remove('active');
            progressFill.style.width = '0%';
            submitBtn.disabled = false;
            elements.uploadForm.reset();
            elements.fileName.textContent = '';
            elements.fileDropZone.classList.remove('active');
        }, 2000);

    } catch (error) {
        progressFill.style.width = '0%';
        progressText.textContent = `❌ ${error.message}`;
        submitBtn.disabled = false;
        showToast(`Upload failed: ${error.message}`, 'error');
    }
}

async function updateStats() {
    try {
        const response = await fetch(`${API_BASE}/api/logs?limit=1`);
        const data = await response.json();

        elements.statQueries.textContent = data.total_queries;
        elements.statAvgTime.textContent = `${data.avg_response_time_ms.toFixed(0)}ms`;
    } catch (error) {
        console.error('Failed to update stats:', error);
    }
}

// ═══════════════════════════════════════════════
// Message Rendering
// ═══════════════════════════════════════════════
function addMessage(role, content) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const avatarEmoji = role === 'user' ? '👤' : '🚗';

    messageEl.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div class="message-content">
            <div class="message-bubble">${formatMarkdown(content)}</div>
            <div class="message-meta">
                <span class="message-time">${timeStr}</span>
            </div>
        </div>
    `;

    elements.messagesArea.appendChild(messageEl);
    scrollToBottom();
}

function addAssistantMessage(data) {
    const messageEl = document.createElement('div');
    messageEl.className = 'message assistant';

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Build sources HTML
    let sourcesHtml = '';
    if (data.sources && data.sources.length > 0) {
        const sourceCards = data.sources.map((source, i) => `
            <div class="source-card">
                <div class="source-header">
                    <span class="source-section">📄 ${source.section}</span>
                    <span class="source-page">Page ${source.page_number}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span class="source-relevance">Relevance: ${(source.relevance_score * 100).toFixed(0)}%</span>
                </div>
                <div class="source-text">${escapeHtml(source.chunk_text)}</div>
            </div>
        `).join('');

        sourcesHtml = `
            <div class="sources-container">
                <button class="sources-toggle" onclick="toggleSources(this)">
                    <span>📋 ${data.sources.length} Sources</span>
                    <span class="arrow">▼</span>
                </button>
                <div class="sources-list">
                    ${sourceCards}
                </div>
            </div>
        `;
    }

    // Build evaluation metrics HTML
    let evalHtml = '';
    if (data.evaluation) {
        const metrics = [
            { label: 'Relevance', value: data.evaluation.context_relevance },
            { label: 'Grounded', value: data.evaluation.answer_groundedness },
            { label: 'Complete', value: data.evaluation.answer_completeness }
        ];

        const metricCards = metrics.map(m => {
            const pct = (m.value * 100).toFixed(0);
            const level = m.value >= 0.7 ? 'high' : m.value >= 0.4 ? 'medium' : 'low';
            return `
                <div class="eval-metric">
                    <span class="eval-metric-label">${m.label}</span>
                    <div class="eval-metric-bar">
                        <div class="eval-metric-fill ${level}" style="width: ${pct}%"></div>
                    </div>
                    <span class="eval-metric-value">${pct}%</span>
                </div>
            `;
        }).join('');

        evalHtml = `<div class="eval-metrics">${metricCards}</div>`;
    }

    messageEl.innerHTML = `
        <div class="message-avatar">🚗</div>
        <div class="message-content">
            <div class="message-bubble">${formatMarkdown(data.answer)}</div>
            ${sourcesHtml}
            ${evalHtml}
            <div class="message-meta">
                <span class="message-time">${timeStr}</span>
                <span class="response-time-badge">⚡ ${data.response_time_ms.toFixed(0)}ms</span>
            </div>
        </div>
    `;

    elements.messagesArea.appendChild(messageEl);
    scrollToBottom();

    // Store in chat history
    state.chatHistory.push({
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: now.toISOString()
    });
}

// ═══════════════════════════════════════════════
// UI Helpers
// ═══════════════════════════════════════════════
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
        <div class="message-avatar" style="background: var(--accent-gradient); box-shadow: 0 2px 10px rgba(99, 102, 241, 0.2);">🚗</div>
        <div class="typing-bubble">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    elements.messagesArea.appendChild(indicator);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

function toggleSources(btn) {
    btn.classList.toggle('expanded');
    const sourcesList = btn.nextElementSibling;
    sourcesList.classList.toggle('expanded');
}

function updateHeaderInfo() {
    if (state.selectedBrand && state.selectedModel) {
        elements.headerTitle.textContent = `${state.selectedBrand} ${state.selectedModel}`;
        elements.headerStatus.querySelector('span').textContent = 'Ready to answer';
        elements.statusDot.classList.remove('offline');
    } else if (state.selectedBrand) {
        elements.headerTitle.textContent = `${state.selectedBrand} — Select a model`;
        elements.headerStatus.querySelector('span').textContent = 'Select a model to start';
    } else {
        elements.headerTitle.textContent = 'Drive Wise Assistant';
        elements.headerStatus.querySelector('span').textContent = 'Select a vehicle to start';
    }
}

function updateCharCount() {
    const length = elements.chatInput.value.length;
    elements.charCount.textContent = length > 0 ? `${length}` : '';
}

function autoResizeInput() {
    const input = elements.chatInput;
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
}

function scrollToBottom() {
    setTimeout(() => {
        elements.messagesArea.scrollTop = elements.messagesArea.scrollHeight;
    }, 50);
}

function formatMarkdown(text) {
    if (!text) return '';

    // Escape HTML first
    let html = escapeHtml(text);

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic: *text*
    html = html.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

    // Bullet lists: lines starting with - or •
    html = html.replace(/^[\s]*[-•]\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Numbered lists: lines starting with numbers
    html = html.replace(/^[\s]*\d+\.\s+(.+)$/gm, '<li>$1</li>');

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headers
    html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');

    // Line breaks (double newline = paragraph break)
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');

    // Wrap in paragraph if not already wrapped
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }

    return html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ═══════════════════════════════════════════════
// Toast Notifications
// ═══════════════════════════════════════════════
function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;

    container.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        toast.style.transition = 'all 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ═══════════════════════════════════════════════
// Global Functions (called from HTML onclick)
// ═══════════════════════════════════════════════
window.toggleSources = toggleSources;
