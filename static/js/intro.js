(function() {
    const overlay = document.createElement('div');
    overlay.id = 'intro-overlay';
    overlay.innerHTML = `
        <div class="intro-content">
            <div class="intro-icon">⌂</div>
            <div class="intro-text">
                <span class="intro-letters"></span>
                <span class="intro-cursor">|</span>
            </div>
            <div class="intro-tagline">California Housing Market</div>
        </div>
    `;

    const style = document.createElement('style');
    style.textContent = `
        #intro-overlay {
            position: fixed;
            inset: 0;
            background: #0c0f0a;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }

        .intro-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }

        .intro-icon {
            font-size: 3rem;
            color: #c9a84c;
            opacity: 0;
            transform: translateY(10px);
            animation: iconReveal 0.6s ease 0.3s forwards;
            filter: drop-shadow(0 0 20px rgba(201,168,76,0.6));
        }

        @keyframes iconReveal {
            to { opacity: 1; transform: translateY(0); }
        }

        .intro-text {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 300;
            color: #f0ede6;
            letter-spacing: 0.08em;
            display: flex;
            align-items: center;
            gap: 2px;
            min-height: 80px;
        }

        .intro-cursor {
            color: #c9a84c;
            font-weight: 300;
            animation: blink 0.7s step-end infinite;
            margin-left: 2px;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        .intro-tagline {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: rgba(138,136,128,0.7);
            opacity: 0;
            animation: tagReveal 0.6s ease 2.4s forwards;
        }

        @keyframes tagReveal {
            to { opacity: 1; }
        }

        #intro-overlay.exit .intro-icon,
        #intro-overlay.exit .intro-cursor {
            animation: none;
        }

        #intro-overlay.exit {
            animation: overlayExit 0.9s cubic-bezier(0.76, 0, 0.24, 1) forwards;
        }

        #intro-overlay.exit .intro-text {
            animation: textExit 0.9s cubic-bezier(0.76, 0, 0.24, 1) forwards;
        }

        #intro-overlay.exit .intro-icon {
            animation: iconExit 0.9s cubic-bezier(0.76, 0, 0.24, 1) forwards;
        }

        #intro-overlay.exit .intro-tagline {
            animation: tagExit 0.6s ease forwards;
        }

        @keyframes overlayExit {
            0%   { opacity: 1; clip-path: inset(0 0 0 0); }
            100% { opacity: 0; clip-path: inset(0 0 100% 0); }
        }

        @keyframes textExit {
            0%   { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-40px) scale(0.95); }
        }

        @keyframes iconExit {
            0%   { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-30px); }
        }

        @keyframes tagExit {
            0%   { opacity: 1; }
            100% { opacity: 0; }
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(overlay);

    const letters        = document.querySelector('.intro-letters');
    const fullText       = 'E-state IQ';
    const typeDelay      = 100;
    const startDelay     = 1000;
    const holdAfterType  = 1000;
    const exitDelay      = 400;

    function typeWriter(text, el, delay, start, done) {
        let i = 0;
        setTimeout(() => {
            const interval = setInterval(() => {
                el.textContent += text[i];
                i++;
                if (i >= text.length) {
                    clearInterval(interval);
                    if (done) done();
                }
            }, delay);
        }, start);
    }

    typeWriter(fullText, letters, typeDelay, startDelay, () => {
        setTimeout(() => {
            overlay.classList.add('exit');
            overlay.addEventListener('animationend', () => {
                overlay.remove();
            }, { once: true });
        }, holdAfterType + exitDelay);
    });
})();