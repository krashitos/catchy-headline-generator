document.addEventListener('DOMContentLoaded', () => {
    const topicInput = document.getElementById('topicInput');
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const loader = generateBtn.querySelector('.loader');
    const resultsSection = document.getElementById('resultsSection');
    const headlinesList = document.getElementById('headlinesList');
    const copyAllBtn = document.getElementById('copyAllBtn');

    generateBtn.addEventListener('click', async () => {
        const topic = topicInput.value.trim();
        if (!topic) {
            alert('Please enter a topic!');
            return;
        }

        // UI State: Loading
        generateBtn.disabled = true;
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate headlines');
            }

            const data = await response.json();
            displayResults(data.headlines);

        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong: ' + error.message);
        } finally {
            // UI State: Default
            generateBtn.disabled = false;
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    function displayResults(headlines) {
        headlinesList.innerHTML = '';
        headlines.forEach((headline, index) => {
            const card = document.createElement('div');
            card.className = 'headline-card';
            card.style.animationDelay = `${index * 0.1}s`;
            card.innerHTML = `
                <span>${headline}</span>
                <span class="copy-hint" style="font-size: 0.7rem; color: var(--text-muted);">Click to copy</span>
            `;

            card.addEventListener('click', () => copyToClipboard(headline, card));
            headlinesList.appendChild(card);
        });

        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    async function copyToClipboard(text, element) {
        try {
            await navigator.clipboard.writeText(text);
            const hint = element.querySelector('.copy-hint');
            const originalText = hint.innerText;
            hint.innerText = 'Copied!';
            hint.style.color = 'var(--secondary)';

            setTimeout(() => {
                hint.innerText = originalText;
                hint.style.color = 'var(--text-muted)';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }

    copyAllBtn.addEventListener('click', () => {
        const allHeadlines = Array.from(headlinesList.querySelectorAll('span:first-child'))
            .map(span => span.innerText)
            .join('\n');

        copyToClipboard(allHeadlines, copyAllBtn);
    });

    // Enter key support
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            generateBtn.click();
        }
    });
});
