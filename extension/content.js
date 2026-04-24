// content.js — Injected into Gmail pages
// Reads the currently open email body from Gmail's DOM

function getGmailEmailBody() {
    // Gmail renders email body in these selectors (in order of priority)
    const selectors = [
        'div.a3s.aiL',           // Primary: full email body
        'div[data-message-id] .a3s',  // Thread view
        'div.ii.gt div',         // Older Gmail layout
        'div.Am.Al.editable',    // Compose/reply area fallback
    ];

    for (const selector of selectors) {
        const el = document.querySelector(selector);
        if (el && el.innerText && el.innerText.trim().length > 20) {
            return el.innerText.trim();
        }
    }

    return null;
}

function getEmailSubject() {
    const subjectEl = document.querySelector('h2.hP');
    return subjectEl ? subjectEl.innerText.trim() : '';
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getGmailEmail') {
        const body    = getGmailEmailBody();
        const subject = getEmailSubject();

        if (body) {
            sendResponse({
                success: true,
                text: subject ? `Subject: ${subject}\n\n${body}` : body,
                subject: subject
            });
        } else {
            sendResponse({
                success: false,
                error: 'No email open. Please open an email in Gmail first.'
            });
        }
    }
    return true; // Keep channel open for async response
});
