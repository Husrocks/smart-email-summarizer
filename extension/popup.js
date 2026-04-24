document.addEventListener('DOMContentLoaded', async () => {
    const inputText     = document.getElementById('inputText');
    const lengthSlider  = document.getElementById('lengthSlider');
    const btnParagraph  = document.getElementById('btnParagraph');
    const btnBullets    = document.getElementById('btnBullets');
    const summarizeBtn  = document.getElementById('summarizeBtn');
    const loading       = document.getElementById('loading');
    const outputSection = document.getElementById('outputSection');
    const summaryResult = document.getElementById('summaryResult');
    const copyBtn       = document.getElementById('copyBtn');
    const backendStatus = document.getElementById('backendStatus');
    const errorArea     = document.getElementById('errorArea');
    const errorText     = document.getElementById('errorText');
    const retryBtn      = document.getElementById('retryBtn');

    let currentFormat = 'paragraph';
    const API_URL = 'http://127.0.0.1:8000';

    // ── Backend health check ─────────────────────────────────────────
    async function checkBackend() {
        try {
            const response = await fetch(`${API_URL}/health`);
            if (response.ok) {
                backendStatus.textContent = 'Online ✅';
                backendStatus.className = 'online';
                summarizeBtn.disabled = false;
            } else throw new Error();
        } catch {
            backendStatus.textContent = 'Offline ❌ (Run python main.py)';
            backendStatus.className = 'offline';
            summarizeBtn.disabled = true;
        }
    }

    await checkBackend();

    // ── Gmail Auto-Extract ────────────────────────────────────────────
    async function tryAutoLoadGmail() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab || !tab.url || !tab.url.includes('mail.google.com')) return;

            inputText.placeholder = '⏳ Reading email from Gmail...';

            // Step 1: Try messaging existing content script
            chrome.tabs.sendMessage(tab.id, { action: 'getGmailEmail' }, async (response) => {

                // If content script not loaded yet (tab was open before extension reload),
                // inject it on-the-fly using scripting API
                if (chrome.runtime.lastError || !response) {
                    try {
                        await chrome.scripting.executeScript({
                            target: { tabId: tab.id },
                            files: ['content.js']
                        });
                        // Retry after injecting
                        setTimeout(() => {
                            chrome.tabs.sendMessage(tab.id, { action: 'getGmailEmail' }, handleGmailResponse);
                        }, 300);
                    } catch (err) {
                        inputText.placeholder = '⚠️ Refresh your Gmail tab and try again.';
                    }
                    return;
                }

                handleGmailResponse(response);
            });
        } catch (e) {
            // Not on Gmail or permission denied — silent fail
        }
    }

    function handleGmailResponse(response) {
        if (response && response.success && response.text) {
            inputText.value = response.text;
            inputText.placeholder = '✅ Email loaded from Gmail!';
            // Auto-trigger summarization
            generateSummary();
        } else {
            inputText.placeholder = response?.error ||
                '📭 Open an email in Gmail, then click the extension.';
        }
    }

    // ── Priority: selected text > Gmail auto-extract ──────────────────
    const hasStorage = typeof chrome !== 'undefined'
        && typeof chrome.storage !== 'undefined'
        && typeof chrome.storage.local !== 'undefined';

    if (hasStorage) {
        chrome.storage.local.get(['selectedText'], (result) => {
            if (result && result.selectedText) {
                inputText.value = result.selectedText;
                chrome.storage.local.remove(['selectedText']);
            } else {
                tryAutoLoadGmail();
            }
        });
    } else {
        tryAutoLoadGmail();
    }

    // ── Format toggles ────────────────────────────────────────────────
    btnParagraph.addEventListener('click', () => {
        currentFormat = 'paragraph';
        btnParagraph.classList.add('active');
        btnBullets.classList.remove('active');
    });

    btnBullets.addEventListener('click', () => {
        currentFormat = 'bullets';
        btnBullets.classList.add('active');
        btnParagraph.classList.remove('active');
    });

    // ── Length slider ─────────────────────────────────────────────────
    const getLengthSetting = (value) => ({ '0': 'short', '1': 'medium', '2': 'long' }[value] || 'medium');

    // ── Summarize ─────────────────────────────────────────────────────
    const generateSummary = async () => {
        const text = inputText.value.trim();
        if (!text) return;

        loading.classList.remove('hidden');
        outputSection.classList.add('hidden');
        errorArea.classList.add('hidden');
        summarizeBtn.disabled = true;

        try {
            const response = await fetch(`${API_URL}/summarize`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text,
                    length_setting: getLengthSetting(lengthSlider.value),
                    format: currentFormat
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Summarization failed');
            }

            const data = await response.json();
            summaryResult.textContent = data.summary;
            outputSection.classList.remove('hidden');
            summaryResult.classList.remove('hidden');
            errorArea.classList.add('hidden');

        } catch (error) {
            errorText.textContent = `Error: ${error.message}`;
            errorArea.classList.remove('hidden');
            summaryResult.classList.add('hidden');
            outputSection.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
            summarizeBtn.disabled = false;
        }
    };

    summarizeBtn.addEventListener('click', generateSummary);
    retryBtn.addEventListener('click', generateSummary);

    // ── Copy ──────────────────────────────────────────────────────────
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(summaryResult.textContent).then(() => {
            const orig = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            setTimeout(() => { copyBtn.innerHTML = orig; }, 2000);
        });
    });
});
