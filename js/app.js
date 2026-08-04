// TOEIC Reading Part 5 Application Logic

document.addEventListener('DOMContentLoaded', () => {
    // Web Audio API Sound Synthesizer
    let audioCtx = null;

    function playSound(type) {
        try {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const now = audioCtx.currentTime;
            
            if (type === 'correct') {
                // Ascending chime (G5 -> C6)
                const osc1 = audioCtx.createOscillator();
                const gain1 = audioCtx.createGain();
                osc1.type = 'sine';
                osc1.frequency.setValueAtTime(783.99, now); // G5
                gain1.gain.setValueAtTime(0.12, now);
                gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc1.connect(gain1);
                gain1.connect(audioCtx.destination);
                osc1.start(now);
                osc1.stop(now + 0.12);
                
                const osc2 = audioCtx.createOscillator();
                const gain2 = audioCtx.createGain();
                osc2.type = 'sine';
                osc2.frequency.setValueAtTime(1046.50, now + 0.08); // C6
                gain2.gain.setValueAtTime(0.12, now + 0.08);
                gain2.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc2.connect(gain2);
                gain2.connect(audioCtx.destination);
                osc2.start(now + 0.08);
                osc2.stop(now + 0.3);
                
            } else if (type === 'incorrect') {
                // Low buzz descending (130Hz -> 90Hz)
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                const filter = audioCtx.createBiquadFilter();
                
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(130, now);
                osc.frequency.linearRampToValueAtTime(90, now + 0.22);
                
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.22);
                
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(300, now);
                
                osc.connect(filter);
                filter.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.start(now);
                osc.stop(now + 0.22);
            }
        } catch (e) {
            console.error("Audio failed to play:", e);
        }
    }
    // Define global Mini-Quiz validation helper
    window.checkMiniQuiz = function(button, selected, correct, explanation) {
        const parent = button.parentElement;
        const buttons = parent.querySelectorAll('.mini-quiz-opt');
        const feedbackBox = parent.nextElementSibling;
        
        buttons.forEach(btn => btn.disabled = true);
        
        if (selected === correct) {
            button.style.borderColor = 'var(--color-success)';
            button.style.background = 'rgba(16, 185, 129, 0.1)';
            button.style.color = 'var(--color-success)';
            
            feedbackBox.style.display = 'block';
            feedbackBox.style.color = 'var(--color-success)';
            feedbackBox.innerHTML = `<i class="fa-solid fa-circle-check"></i> <strong>Chính xác!</strong> ${explanation}`;
            
            playSound('correct');
            if (typeof spawnConfetti === 'function') {
                spawnConfetti(25);
            }
        } else {
            button.style.borderColor = 'var(--color-error)';
            button.style.background = 'rgba(239, 68, 68, 0.1)';
            button.style.color = 'var(--color-error)';
            button.classList.add('shake');
            setTimeout(() => button.classList.remove('shake'), 400);
            
            buttons.forEach(btn => {
                if (btn.textContent.trim() === correct) {
                    btn.style.borderColor = 'var(--color-success)';
                    btn.style.color = 'var(--color-success)';
                }
            });
            
            playSound('incorrect');
            feedbackBox.style.display = 'block';
            feedbackBox.style.color = 'var(--color-error)';
            feedbackBox.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> <strong>Chưa chính xác!</strong> ${explanation}`;
        }
    }

    // Global Event Delegation for Mini-Challenge Quizzes
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.mini-quiz-opt');
        if (btn) {
            const opt = btn.getAttribute('data-opt');
            const correct = btn.getAttribute('data-correct');
            const explanation = btn.getAttribute('data-explanation');
            if (opt && correct && explanation) {
                e.preventDefault();
                window.checkMiniQuiz(btn, opt, correct, explanation);
            }
        }
    });;

    // State Variables
    let currentChapter = null; // null represents Home view, 0-7 represents chapters
    let currentTestIndex = null;
    let currentSlideIndex = 0;
    let currentQuestionIndex = 0;
    let quizScore = 0;
    let quizActive = false;
    let selectedOption = null;
    let quizMode = 'practice'; // 'practice' or 'homework'

    // Confetti Canvas Particle System
    const canvas = document.getElementById('confettiCanvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationFrameId = null;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class ConfettiParticle {
        constructor(x, y, isGoldOnly = false) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 8 + 4;
            this.speedX = Math.random() * 10 - 5;
            this.speedY = Math.random() * -12 - 4;
            this.rotation = Math.random() * 360;
            this.rotationSpeed = Math.random() * 4 - 2;
            this.gravity = 0.25;
            
            if (isGoldOnly) {
                const goldTones = ['#ffd700', '#f59e0b', '#fbbf24', '#fef08a'];
                this.color = goldTones[Math.floor(Math.random() * goldTones.length)];
            } else {
                const colors = ['#00f2fe', '#a855f7', '#ec4899', '#3b82f6', '#10b981'];
                this.color = colors[Math.floor(Math.random() * colors.length)];
            }
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.speedY += this.gravity;
            this.rotation += this.rotationSpeed;
        }
        
        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation * Math.PI / 180);
            ctx.fillStyle = this.color;
            ctx.fillRect(-this.size / 2, -this.size / 2, this.size, this.size);
            ctx.restore();
        }
    }

    function spawnConfetti(count = 50, isGoldOnly = false) {
        for (let i = 0; i < count; i++) {
            particles.push(new ConfettiParticle(
                canvas.width * (0.25 + Math.random() * 0.5),
                canvas.height * 0.85,
                isGoldOnly
            ));
        }
        
        if (!animationFrameId) {
            animateConfetti();
        }
    }

    function animateConfetti() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.update();
            p.draw();
            
            // Remove offscreen
            if (p.y > canvas.height || p.x < 0 || p.x > canvas.width) {
                particles.splice(i, 1);
            }
        }
        
        if (particles.length > 0) {
            animationFrameId = requestAnimationFrame(animateConfetti);
        } else {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    // DOM Elements
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarBtn = document.getElementById('toggleSidebarBtn');
    const toggleIcon = document.getElementById('toggleIcon');
    const menuToggleBtn = document.getElementById('menuToggleBtn');
    
    const navHomeBtn = document.getElementById('navHomeBtn');
    const welcomeView = document.getElementById('homeView');
    const chapterView = document.getElementById('chapterView');
    const submenuItems = document.querySelectorAll('.submenu-item');
    
    const startStudyingBtn = document.getElementById('startStudyingBtn');
    
    // Tab Elements
    const tabLessonBtn = document.getElementById('tabLessonBtn');
    const tabPracticeBtn = document.getElementById('tabPracticeBtn');
    const tabHomeworkBtn = document.getElementById('tabHomeworkBtn');
    const lessonContent = document.getElementById('lessonContent');
    const practiceContent = document.getElementById('practiceContent');
    
    // Slide Player Elements
    const slideCanvas = document.getElementById('slideCanvas');
    const slideContentArea = document.getElementById('slideContentArea');
    const prevSlideBtn = document.getElementById('prevSlideBtn');
    const nextSlideBtn = document.getElementById('nextSlideBtn');
    const slideProgressBarFill = document.getElementById('slideProgressBarFill');
    const slideProgressText = document.getElementById('slideProgressText');
    
    // Quiz Elements
    const quizActiveArea = document.getElementById('quizActiveArea');
    const quizSummaryArea = document.getElementById('quizSummaryArea');
    const questionText = document.getElementById('questionText');
    const optionsList = document.getElementById('optionsList');
    const explanationPanel = document.getElementById('explanationPanel');
    const explanationText = document.getElementById('explanationText');
    const nextQuestionBtn = document.getElementById('nextQuestionBtn');
    const quizProgressText = document.getElementById('quizProgressText');
    const quizScoreText = document.getElementById('quizScoreText');
    
    const summaryScore = document.getElementById('summaryScore');
    const summaryTotal = document.getElementById('summaryTotal');
    const summaryComment = document.getElementById('summaryComment');
    const retryQuizBtn = document.getElementById('retryQuizBtn');
    const backToLessonBtn = document.getElementById('backToLessonBtn');
    
    const chapterSub = document.getElementById('chapterSub');
    const chapterTitle = document.getElementById('chapterTitle');

    // Theme Toggle Hook & Logic
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    // Quiz Placeholder Elements
    const quizPlaceholderArea = document.getElementById('quizPlaceholderArea');
    const backToLessonFromPlaceholderBtn = document.getElementById('backToLessonFromPlaceholderBtn');

    // Initialize Theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        themeIcon.className = 'fa-solid fa-lightbulb';
        themeText.textContent = 'TẮT ĐÈN';
    } else {
        document.body.classList.remove('light-theme');
        themeIcon.className = 'fa-solid fa-moon';
        themeText.textContent = 'BẬT ĐÈN';
    }

    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        if (isLight) {
            localStorage.setItem('theme', 'light');
            themeIcon.className = 'fa-solid fa-lightbulb';
            themeText.textContent = 'TẮT ĐÈN';
        } else {
            localStorage.setItem('theme', 'dark');
            themeIcon.className = 'fa-solid fa-moon';
            themeText.textContent = 'BẬT ĐÈN';
        }
    });

    // --- 1. Sidebar Toggling Logic ---
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        if (sidebar.classList.contains('collapsed')) {
            toggleIcon.className = 'fa-solid fa-angles-right';
        } else {
            toggleIcon.className = 'fa-solid fa-angles-left';
        }
    });

    menuToggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Close mobile sidebar when clicking outside on mobile view
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 992) {
            if (!sidebar.contains(e.target) && !menuToggleBtn.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // --- 2. Navigation Control ---
    function showHomeView() {
        currentChapter = null;
        currentTestIndex = null;
        welcomeView.classList.add('active');
        chapterView.classList.remove('active');
        
        // Update sidebar active highlights
        navHomeBtn.classList.add('active');
        submenuItems.forEach(item => item.classList.remove('active'));
        document.querySelectorAll('.test-item').forEach(item => item.classList.remove('active'));
        
        // Close sidebar if on mobile
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('open');
        }
    }

    let pendingChapterId = null;
    let pendingTestId = null;

    function updateLockStatusInSidebar() {
        submenuItems.forEach(item => {
            const chId = parseInt(item.getAttribute('data-id'));
            if (chId > 2) {
                const isUnlocked = localStorage.getItem(`chapter_${chId}_unlocked`) === 'true';
                const lockIcon = item.querySelector('.lock-badge');
                if (lockIcon) lockIcon.remove();
                
                // Get the raw text ignoring icon if present
                const textNode = Array.from(item.childNodes).find(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim().length > 0);
                const titleText = textNode ? textNode.textContent.trim() : item.textContent.trim();
                
                if (!isUnlocked) {
                    item.innerHTML = `${titleText} <span class="lock-badge" style="color: var(--color-gold); margin-left: auto; font-size: 0.85rem; padding-left: 8px;"><i class="fa-solid fa-lock"></i></span>`;
                    item.style.display = 'flex';
                    item.style.alignItems = 'center';
                    item.style.justifyContent = 'space-between';
                } else {
                    item.innerHTML = `${titleText} <span class="lock-badge" style="color: var(--color-success); margin-left: auto; font-size: 0.85rem; padding-left: 8px;"><i class="fa-solid fa-lock-open"></i></span>`;
                    item.style.display = 'flex';
                    item.style.alignItems = 'center';
                    item.style.justifyContent = 'space-between';
                }
            }
        });

        document.querySelectorAll('.test-item').forEach(item => {
            const testId = parseInt(item.getAttribute('data-test-id'));
            const isUnlocked = localStorage.getItem(`test_${testId}_unlocked`) === 'true';
            const lockIcon = item.querySelector('.lock-badge');
            if (lockIcon) lockIcon.remove();
            
            // Re-render based on structure: icon + text + (optional) lock
            const textNode = Array.from(item.childNodes).find(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim().length > 0);
            const titleText = textNode ? textNode.textContent.trim() : item.textContent.trim();
            const prefixIcon = testId <= 4 ? '<i class="fa-solid fa-square-poll-horizontal"></i>' : '<i class="fa-solid fa-file-signature"></i>';
            
            if (!isUnlocked) {
                item.innerHTML = `<span style="display: flex; align-items: center; gap: 8px;">${prefixIcon} ${titleText}</span> <span class="lock-badge" style="color: var(--color-gold); margin-left: auto; font-size: 0.85rem; padding-left: 8px;"><i class="fa-solid fa-lock"></i></span>`;
                item.style.display = 'flex';
                item.style.alignItems = 'center';
                item.style.justifyContent = 'space-between';
            } else {
                item.innerHTML = `<span style="display: flex; align-items: center; gap: 8px;">${prefixIcon} ${titleText}</span> <span class="lock-badge" style="color: var(--color-success); margin-left: auto; font-size: 0.85rem; padding-left: 8px;"><i class="fa-solid fa-lock-open"></i></span>`;
                item.style.display = 'flex';
                item.style.alignItems = 'center';
                item.style.justifyContent = 'space-between';
            }
        });
    }

    function showTestView(testId) {
        const isUnlocked = localStorage.getItem(`test_${testId}_unlocked`) === 'true';
        if (!isUnlocked) {
            pendingTestId = testId;
            const testName = testId <= 4 ? `BÀI ÔN TẬP 0${testId}` : `ETS 2026 - TEST 0${testId - 4}`;
            showPasswordModal("ĐỀ THI BỊ KHÓA", `${testName} yêu cầu mật khẩu truy cập từ Miss Nguyệt.`);
            return;
        }
        currentChapter = null;
        currentTestIndex = testId - 1; // 0-indexed
        
        welcomeView.classList.remove('active');
        chapterView.classList.add('active');
        
        navHomeBtn.classList.remove('active');
        submenuItems.forEach(item => item.classList.remove('active'));
        
        // Highlight active test in sidebar
        document.querySelectorAll('.test-item').forEach(item => {
            if (parseInt(item.getAttribute('data-test-id')) === testId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Initialize Test Contents
        const testData = toeicTestsData[currentTestIndex];
        if (testId <= 4) {
            chapterSub.textContent = "PHẦN 02: ÔN TẬP";
        } else {
            chapterSub.textContent = "PHẦN 03: LUYỆN ĐỀ";
        }
        chapterTitle.textContent = testData.title;
        
        // Hide theory/homework tabs since it's a test
        document.querySelector('.tab-switcher').style.display = 'none';
        
        lessonContent.style.display = 'none';
        practiceContent.style.display = 'block';
        
        quizMode = 'test';
        initQuiz();
        
        // Close sidebar if on mobile
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('open');
        }
    }

    function showChapterView(chapterId) {
        if (chapterId > 2) {
            const isUnlocked = localStorage.getItem(`chapter_${chapterId}_unlocked`) === 'true';
            if (!isUnlocked) {
                pendingChapterId = chapterId;
                const chName = `Chủ điểm ${chapterId < 10 ? '0' + chapterId : chapterId}`;
                showPasswordModal("CHỦ ĐIỂM BỊ KHÓA", `${chName} yêu cầu mật khẩu truy cập từ Miss Nguyệt.`);
                return;
            }
        }
        currentChapter = chapterId - 1; // 0-indexed
        currentTestIndex = null;
        welcomeView.classList.remove('active');
        chapterView.classList.add('active');
        
        navHomeBtn.classList.remove('active');
        submenuItems.forEach(item => {
            if (parseInt(item.getAttribute('data-id')) === chapterId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        document.querySelectorAll('.test-item').forEach(item => item.classList.remove('active'));

        // Initialize Chapter Contents
        const chapterData = toeicReadingData[currentChapter];
        chapterSub.textContent = `PHẦN 01: TRỌNG TÂM KIẾN THỨC - Chủ điểm ${chapterId < 10 ? '0' + chapterId : chapterId}`;
        chapterTitle.textContent = chapterData.title;
        
        // Restore tab switcher and default to Lesson tab
        document.querySelector('.tab-switcher').style.display = 'flex';
        switchTab('lesson');
        currentSlideIndex = 0;
        renderSlide();
        
        // Close sidebar if on mobile
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('open');
        }
    }

    navHomeBtn.addEventListener('click', showHomeView);
    startStudyingBtn.addEventListener('click', () => showChapterView(1));

    submenuItems.forEach(item => {
        item.addEventListener('click', () => {
            const chId = parseInt(item.getAttribute('data-id'));
            if (!isNaN(chId)) {
                showChapterView(chId);
            }
        });
    });

    document.querySelectorAll('.test-item').forEach(item => {
        item.addEventListener('click', () => {
            const testId = parseInt(item.getAttribute('data-test-id'));
            showTestView(testId);
        });
    });

    // --- 3. Tabs Swapping ---
    // --- 3. Tabs Swapping ---
    function switchTab(tabType) {
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        if (tabType === 'lesson') {
            tabLessonBtn.classList.add('active');
            tabPracticeBtn.classList.remove('active');
            tabHomeworkBtn.classList.remove('active');
            lessonContent.style.display = 'block';
            practiceContent.style.display = 'none';
        } else if (tabType === 'practice') {
            tabLessonBtn.classList.remove('active');
            tabPracticeBtn.classList.add('active');
            tabHomeworkBtn.classList.remove('active');
            lessonContent.style.display = 'none';
            practiceContent.style.display = 'block';
            quizMode = 'practice';
            initQuiz();
        } else if (tabType === 'homework') {
            tabLessonBtn.classList.remove('active');
            tabPracticeBtn.classList.remove('active');
            tabHomeworkBtn.classList.add('active');
            lessonContent.style.display = 'none';
            practiceContent.style.display = 'block';
            quizMode = 'homework';
            initQuiz();
        }
    }

    // Enhance rendered slide with pill highlight synchronization
    function enhanceRenderedSlide() {
        // Setup dynamic Pill Tag highlighting synchronization

        // Setup dynamic Pill Tag highlighting synchronization
        const pillItems = slideContentArea.querySelectorAll('.pill-item');
        pillItems.forEach(pill => {
            pill.addEventListener('click', () => {
                const strongEl = pill.querySelector('strong');
                let targetWord = strongEl ? strongEl.textContent.trim().toLowerCase() : '';
                if (!targetWord) {
                    targetWord = pill.textContent.split('(')[0].trim().toLowerCase();
                }
                
                if (!targetWord) return;

                const vocabs = slideContentArea.querySelectorAll('.hl-vocab');
                vocabs.forEach(vocab => {
                    const vocabText = vocab.textContent.trim().toLowerCase();
                    let isMatch = vocabText === targetWord || vocabText.includes(targetWord);
                    if (targetWord.includes('...')) {
                        const parts = targetWord.split('...').map(p => p.trim()).filter(Boolean);
                        isMatch = parts.some(p => vocabText.includes(p) || p.includes(vocabText));
                    }

                    if (isMatch) {
                        if (pill.classList.contains('active')) {
                            vocab.classList.add('glow-pulse');
                        } else {
                            vocab.classList.remove('glow-pulse');
                        }
                    }
                });
            });
        });
    }

    tabLessonBtn.addEventListener('click', () => switchTab('lesson'));
    tabPracticeBtn.addEventListener('click', () => switchTab('practice'));
    tabHomeworkBtn.addEventListener('click', () => switchTab('homework'));

    // --- 4. Slideshow Player Logic ---
    function formatSlideText(text) {
        const lines = text.split('\n');
        let html = '';
        let inList = false;
        
        lines.forEach(line => {
            const trimmed = line.trim();
            if (!trimmed) return;
            
            // Check list formatting
            if (trimmed.startsWith('-') || trimmed.startsWith('✦') || trimmed.startsWith('*') || /^\d+\./.test(trimmed)) {
                if (!inList) {
                    html += '<ul style="margin-left: 20px; margin-bottom: 16px;">';
                    inList = true;
                }
                const cleanLine = trimmed.replace(/^[-✦*\d\.]+\s*/, '');
                html += `<li style="margin-bottom: 8px; font-size: 1.05rem; color: var(--text-primary); line-height: 1.6;">${cleanLine}</li>`;
            } else {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                
                // Highlight structures or examples
                if (trimmed.startsWith('EXAMPLE:') || trimmed.startsWith('EX:') || trimmed.startsWith('EXAMPLE')) {
                    const content = trimmed.replace(/^EXAMPLE:?\s*|^EX:?\s*/i, '');
                    html += `
                    <div style="background: rgba(0, 242, 254, 0.03); border-left: 3px solid var(--color-cyan); padding: 16px 20px; margin: 16px 0; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        <strong style="color: var(--color-cyan); font-family: var(--font-heading); font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 6px;"><i class="fa-solid fa-lightbulb"></i> VÍ DỤ:</strong>
                        <span style="font-style: italic; font-size: 1.1rem; line-height: 1.6; color: var(--text-primary);">${content}</span>
                    </div>`;
                } else if (trimmed.startsWith('Cấu trúc:') || trimmed.startsWith('Cấu trúc chung:')) {
                    html += `
                    <div style="background: rgba(168, 85, 247, 0.05); border: 1px dashed rgba(168, 85, 247, 0.3); padding: 14px 18px; margin: 16px 0; border-radius: 10px; font-family: var(--font-heading); font-weight: 700; font-size: 1.1rem; color: var(--color-purple); display: inline-block;">
                        <i class="fa-solid fa-gears"></i> ${trimmed}
                    </div>`;
                } else if (trimmed.includes('to Vo') || trimmed.includes('Ving') || trimmed.includes('to V-ing') || trimmed.includes(' Vo ')) {
                    html += `<div style="font-family: var(--font-heading); font-weight: 700; font-size: 1.15rem; color: var(--color-cyan); background: rgba(0,0,0,0.25); padding: 8px 16px; border-radius: 10px; display: inline-block; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);">${trimmed}</div><br>`;
                } else {
                    html += `<p style="margin-bottom: 16px; font-size: 1.1rem; color: var(--text-primary); line-height: 1.7; font-weight: 500;">${trimmed}</p>`;
                }
            }
        });
        
        if (inList) {
            html += '</ul>';
        }
        
        return html;
    }

    function renderSlide() {
        const chapter = toeicReadingData[currentChapter];
        if (!chapter || !chapter.slides || chapter.slides.length === 0) {
            slideContentArea.innerHTML = '<p style="color: var(--text-secondary)">Chủ điểm này không có slide lý thuyết.</p>';
            return;
        }

        const slide = chapter.slides[currentSlideIndex];
        
        if (slide.is_example) {
            if (slide.is_multi) {
                // Render multi-question example slide
                slideContentArea.innerHTML = `
                    <div class="slide-header">${slide.title}</div>
                    <div class="slide-body interactive-example-container" style="display: flex; flex-direction: column; gap: 24px; padding-bottom: 10px;">
                        ${slide.questions.map((q, idx) => `
                            <div class="sub-question-card" style="background: rgba(255,255,255,0.015); border: 1px solid var(--border-color); padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: border-color 0.2s;">
                                <div class="example-question-text" style="font-size: 1.15rem; margin-bottom: 16px; line-height: 1.6; font-weight: 600; color: var(--text-primary);">
                                    ${q.question_html}
                                </div>
                                
                                <div class="options-list q-options-${idx}" style="margin-top: 12px; gap: 14px; margin-bottom: 0;">
                                    <button class="option-item" data-opt="A" style="padding: 12px 18px; font-size: 1.05rem; border-radius: 14px;">
                                        <span class="option-badge" style="width: 26px; height: 26px; font-size: 0.9rem;">A</span>
                                        <span class="option-text">${q.options.A || ''}</span>
                                    </button>
                                    <button class="option-item" data-opt="B" style="padding: 12px 18px; font-size: 1.05rem; border-radius: 14px;">
                                        <span class="option-badge" style="width: 26px; height: 26px; font-size: 0.9rem;">B</span>
                                        <span class="option-text">${q.options.B || ''}</span>
                                    </button>
                                    <button class="option-item" data-opt="C" style="padding: 12px 18px; font-size: 1.05rem; border-radius: 14px;">
                                        <span class="option-badge" style="width: 26px; height: 26px; font-size: 0.9rem;">C</span>
                                        <span class="option-text">${q.options.C || ''}</span>
                                    </button>
                                    <button class="option-item" data-opt="D" style="padding: 12px 18px; font-size: 1.05rem; border-radius: 14px;">
                                        <span class="option-badge" style="width: 26px; height: 26px; font-size: 0.9rem;">D</span>
                                        <span class="option-text">${q.options.D || ''}</span>
                                    </button>
                                </div>
                                
                                <div class="explanation-panel q-explanation-${idx}" style="display: none; margin-top: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 3.5px solid var(--color-success); border-radius: 10px; padding: 12px 18px; background: rgba(16, 185, 129, 0.03);">
                                    <div class="explanation-title" style="color: var(--color-success); font-family: var(--font-heading); font-size: 1rem; font-weight: 700; margin-bottom: 4px;">
                                        <i class="fa-solid fa-circle-check"></i> ĐÁP ÁN ĐÚNG: ${q.correct_answer}. ${q.options[q.correct_answer]}
                                    </div>
                                    <div class="explanation-text" style="font-size: 0.95rem; line-height: 1.5; color: var(--text-secondary);">
                                        ${q.explanation_html}
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;

                // Attach handlers for each multi question
                slide.questions.forEach((q, idx) => {
                    const optButtons = slideContentArea.querySelectorAll(`.q-options-${idx} .option-item`);
                    const explanationBox = slideContentArea.querySelector(`.q-explanation-${idx}`);
                    
                    optButtons.forEach(btn => {
                        btn.addEventListener('click', () => {
                            const selectedLetter = btn.getAttribute('data-opt');
                            if (selectedLetter === q.correct_answer) {
                                btn.classList.add('correct');
                                btn.querySelector('.option-badge').innerHTML = '<i class="fa-solid fa-check"></i>';
                                
                                // Disable siblings
                                optButtons.forEach(b => b.disabled = true);
                                
                                playSound('correct');
                                spawnConfetti(30);
                                explanationBox.style.display = 'block';
                            } else {
                                btn.classList.add('incorrect');
                                btn.classList.add('shake');
                                btn.querySelector('.option-badge').innerHTML = '<i class="fa-solid fa-xmark"></i>';
                                
                                playSound('incorrect');
                                setTimeout(() => {
                                    btn.classList.remove('shake');
                                }, 400);
                            }
                        });
                    });
                });
            } else {
                // Render single-question example slide
                slideContentArea.innerHTML = `
                    <div class="slide-header">${slide.title}</div>
                    <div class="slide-body interactive-example-container">
                        <div class="example-question-text" style="font-size: 1.2rem; margin-bottom: 20px; line-height: 1.6; color: var(--text-primary);">
                            ${slide.question_html}
                        </div>
                        
                        <div class="options-list interactive-example-options" style="margin-top: 16px; margin-bottom: 20px;">
                            <button class="option-item" data-opt="A">
                                <span class="option-badge">A</span>
                                <span class="option-text">${slide.options.A || ''}</span>
                            </button>
                            <button class="option-item" data-opt="B">
                                <span class="option-badge">B</span>
                                <span class="option-text">${slide.options.B || ''}</span>
                            </button>
                            <button class="option-item" data-opt="C">
                                <span class="option-badge">C</span>
                                <span class="option-text">${slide.options.C || ''}</span>
                            </button>
                            <button class="option-item" data-opt="D">
                                <span class="option-badge">D</span>
                                <span class="option-text">${slide.options.D || ''}</span>
                            </button>
                        </div>
                        
                        <div class="explanation-panel example-explanation" style="display: none; margin-top: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 3.5px solid var(--color-success); border-radius: 12px; padding: 14px 20px; background: rgba(16, 185, 129, 0.03);">
                            <div class="explanation-title" style="color: var(--color-success); font-family: var(--font-heading); font-size: 1.05rem; font-weight: 700; margin-bottom: 6px;">
                                <i class="fa-solid fa-circle-check"></i> ĐÁP ÁN ĐÚNG: ${slide.correct_answer}. ${slide.options[slide.correct_answer]}
                            </div>
                            <div class="explanation-text" style="font-size: 1rem; line-height: 1.6; color: var(--text-secondary);">
                                ${slide.explanation_html}
                            </div>
                        </div>
                    </div>
                `;

                const optButtons = slideContentArea.querySelectorAll('.interactive-example-options .option-item');
                const explanationBox = slideContentArea.querySelector('.example-explanation');
                
                optButtons.forEach(btn => {
                    btn.addEventListener('click', () => {
                        const selectedLetter = btn.getAttribute('data-opt');
                        if (selectedLetter === slide.correct_answer) {
                            btn.classList.add('correct');
                            btn.querySelector('.option-badge').innerHTML = '<i class="fa-solid fa-check"></i>';
                            
                            // Disable siblings
                            optButtons.forEach(b => b.disabled = true);
                            
                            playSound('correct');
                            spawnConfetti(45);
                            explanationBox.style.display = 'block';
                        } else {
                            btn.classList.add('incorrect');
                            btn.classList.add('shake');
                            btn.querySelector('.option-badge').innerHTML = '<i class="fa-solid fa-xmark"></i>';
                            
                            playSound('incorrect');
                            setTimeout(() => {
                                btn.classList.remove('shake');
                            }, 400);
                        }
                    });
                });
            }
        } else {
            // Render regular theory slide
            slideContentArea.innerHTML = `
                <div class="slide-header">${slide.title}</div>
                <div class="slide-body">${slide.html_content || ''}</div>
            `;
            
            // Execute scripts inside the slide body so that interactive elements work
            const scripts = slideContentArea.querySelectorAll('script');
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }

        // Update progress bar
        const totalSlides = chapter.slides.length;
        const progressPercent = ((currentSlideIndex + 1) / totalSlides) * 100;
        slideProgressBarFill.style.width = `${progressPercent}%`;
        slideProgressText.textContent = `Trang ${currentSlideIndex + 1} / ${totalSlides}`;

        // Disable buttons accordingly
        prevSlideBtn.disabled = currentSlideIndex === 0;
        nextSlideBtn.disabled = currentSlideIndex === totalSlides - 1;

        // Enhance slide with audio pronunciation and dynamic highlight syncing
        enhanceRenderedSlide();
    }

    prevSlideBtn.addEventListener('click', () => {
        if (currentSlideIndex > 0) {
            currentSlideIndex--;
            renderSlide();
        }
    });

    nextSlideBtn.addEventListener('click', () => {
        const chapter = toeicReadingData[currentChapter];
        if (currentSlideIndex < chapter.slides.length - 1) {
            currentSlideIndex++;
            renderSlide();
        }
    });

    // --- 5. Practice Quiz Logic ---
    function initQuiz() {
        let db = [];
        if (quizMode === 'test') {
            const test = toeicTestsData[currentTestIndex];
            db = test ? (test.questions || []) : [];
        } else {
            const chapter = toeicReadingData[currentChapter];
            db = quizMode === 'homework' ? (chapter.homework || []) : (chapter.questions || []);
        }
        currentQuestionIndex = 0;
        quizScore = 0;
        
        if (db.length === 0) {
            quizActiveArea.style.display = 'none';
            quizSummaryArea.style.display = 'none';
            quizPlaceholderArea.style.display = 'block';
            
            const pTitle = quizPlaceholderArea.querySelector('.welcome-title');
            const pText = quizPlaceholderArea.querySelector('.summary-text');
            if (quizMode === 'homework') {
                pTitle.textContent = "Bài tập về nhà";
                pText.textContent = "Bài tập về nhà cho chủ điểm này đang được biên soạn bởi Miss Nguyệt và sẽ được cập nhật trong thời gian sớm nhất! Vui lòng ôn tập kỹ lý thuyết trong phần Bài học.";
            } else {
                pTitle.textContent = "Bài tập ôn luyện";
                pText.textContent = "Hệ thống bài tập tự luyện cho chủ điểm này đang được biên soạn bởi Miss Nguyệt và sẽ được cập nhật trong thời gian sớm nhất! Vui lòng ôn tập kỹ lý thuyết trong phần Bài học.";
            }
            return;
        }

        quizActiveArea.style.display = 'block';
        quizSummaryArea.style.display = 'none';
        quizPlaceholderArea.style.display = 'none';
        
        renderQuestion();
    }

    // Return to lesson slideshow from placeholder page
    backToLessonFromPlaceholderBtn.addEventListener('click', () => {
        switchTab('lesson');
    });

    function renderQuestion() {
        let db = [];
        if (quizMode === 'test') {
            const test = toeicTestsData[currentTestIndex];
            db = test ? (test.questions || []) : [];
        } else {
            const chapter = toeicReadingData[currentChapter];
            db = quizMode === 'homework' ? (chapter.homework || []) : (chapter.questions || []);
        }
        const question = db[currentQuestionIndex];
        selectedOption = null;
        
        // Reset panels
        explanationPanel.classList.remove('active');
        nextQuestionBtn.style.display = 'none';

        // Update Progress
        const displayNum = quizMode === 'test' ? (101 + currentQuestionIndex) : (currentQuestionIndex + 1);
        quizProgressText.textContent = quizMode === 'test' ? `Câu ${displayNum} (Tổng: ${db.length} câu)` : `Câu hỏi ${currentQuestionIndex + 1} / ${db.length}`;
        quizScoreText.textContent = `${quizScore} / ${currentQuestionIndex}`;

        // Format Question sentence to style '____'
        let formattedQ = question.question;
        formattedQ = formattedQ.replace(/_{4,}/g, '<span class="blank-space">&nbsp;&nbsp;&nbsp;&nbsp;</span>');

        questionText.innerHTML = formattedQ;

        // Render Options
        optionsList.innerHTML = '';
        Object.keys(question.options).forEach(key => {
            const val = question.options[key];
            const optBtn = document.createElement('button');
            optBtn.className = 'option-item';
            optBtn.innerHTML = `
                <div class="option-badge">${key}</div>
                <div class="option-text-val">${val}</div>
            `;
            optBtn.addEventListener('click', () => selectOption(key, optBtn));
            optionsList.appendChild(optBtn);
        });
    }

    function selectOption(choice, element) {
        if (selectedOption !== null) return; // Prevent multiple clicks
        
        selectedOption = choice;
        let db = [];
        if (quizMode === 'test') {
            const test = toeicTestsData[currentTestIndex];
            db = test ? (test.questions || []) : [];
        } else {
            const chapter = toeicReadingData[currentChapter];
            db = quizMode === 'homework' ? (chapter.homework || []) : (chapter.questions || []);
        }
        const question = db[currentQuestionIndex];
        const isCorrect = choice === question.answer;
        const quizCard = document.querySelector('.quiz-card');

        // Visual feedback
        if (isCorrect) {
            quizScore++;
            element.classList.add('correct');
            // Spawn celebration confetti
            playSound('correct');
            spawnConfetti(35);
        } else {
            element.classList.add('incorrect');
            // Shake the quiz card to draw attention
            quizCard.classList.add('shake');
            setTimeout(() => quizCard.classList.remove('shake'), 450);
            
            playSound('incorrect');
            // Highlight correct choice
            const optionBtns = optionsList.querySelectorAll('.option-item');
            optionBtns.forEach(btn => {
                const badgeText = btn.querySelector('.option-badge').textContent;
                if (badgeText === question.answer) {
                    btn.classList.add('correct');
                }
            });
        }

        // Disable options
        const optionBtns = optionsList.querySelectorAll('.option-item');
        optionBtns.forEach(btn => btn.classList.add('disabled'));

        // Update Score counters
        quizScoreText.textContent = `${quizScore} / ${currentQuestionIndex + 1}`;

        // Reveal grammar explanation
        explanationText.innerHTML = question.explanation;
        explanationPanel.classList.add('active');

        // Show Next / Finish button
        nextQuestionBtn.style.display = 'inline-flex';
        if (currentQuestionIndex === db.length - 1) {
            nextQuestionBtn.innerHTML = 'Xem kết quả <i class="fa-solid fa-circle-check"></i>';
        } else {
            nextQuestionBtn.innerHTML = 'Câu tiếp theo <i class="fa-solid fa-arrow-right"></i>';
        }
    }

    nextQuestionBtn.addEventListener('click', () => {
        let db = [];
        if (quizMode === 'test') {
            const test = toeicTestsData[currentTestIndex];
            db = test ? (test.questions || []) : [];
        } else {
            const chapter = toeicReadingData[currentChapter];
            db = quizMode === 'homework' ? (chapter.homework || []) : (chapter.questions || []);
        }
        if (currentQuestionIndex < db.length - 1) {
            currentQuestionIndex++;
            renderQuestion();
        } else {
            showQuizSummary();
        }
    });

    function showQuizSummary() {
        let db = [];
        let titleLabel = "";
        if (quizMode === 'test') {
            const test = toeicTestsData[currentTestIndex];
            db = test ? (test.questions || []) : [];
            titleLabel = test ? test.title : "ETS 2026 Test";
        } else {
            const chapter = toeicReadingData[currentChapter];
            db = quizMode === 'homework' ? (chapter.homework || []) : (chapter.questions || []);
            titleLabel = chapter ? chapter.title : "Chủ điểm";
        }
        quizActiveArea.style.display = 'none';
        quizSummaryArea.style.display = 'block';

        summaryScore.textContent = quizScore;
        summaryTotal.textContent = db.length;

        // Auto-report quiz score to Google Form in the background
        const studentName = localStorage.getItem('studentName') || 'Ẩn danh';
        const quizTypeLabel = quizMode === 'test' ? 'Đề thi thử Part 5' : (quizMode === 'homework' ? 'Bài tập về nhà' : 'Luyện tập');
        submitToGoogleForm(studentName, titleLabel, quizTypeLabel, quizScore, db.length);

        // Populate report fields for screenshots
        const reportStudentName = document.getElementById('reportStudentName');
        const reportChapterTitle = document.getElementById('reportChapterTitle');
        const reportQuizType = document.getElementById('reportQuizType');
        const reportTimestamp = document.getElementById('reportTimestamp');
        
        if (reportStudentName) reportStudentName.textContent = studentName;
        if (reportChapterTitle) reportChapterTitle.textContent = titleLabel;
        if (reportQuizType) {
            reportQuizType.textContent = quizTypeLabel;
            if (quizMode === 'test') {
                reportQuizType.style.color = 'var(--color-cyan)';
            } else if (quizMode === 'homework') {
                reportQuizType.style.color = 'var(--color-purple)';
            } else {
                reportQuizType.style.color = 'var(--color-gold)';
            }
        }
        if (reportTimestamp) {
            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0];
            const dateStr = now.toLocaleDateString('vi-VN');
            reportTimestamp.textContent = `${timeStr} - ${dateStr}`;
        }

        // Custom commentary based on performance
        const pct = (quizScore / db.length) * 100;
        
        // Custom message based on mode
        const summaryTitleEl = quizSummaryArea.querySelector('.welcome-title');
        if (quizMode === 'test') {
            summaryTitleEl.textContent = "Hoàn thành Đề thi thử!";
            let levelBadge = "";
            let evaluationText = "";
            
            if (pct === 100) {
                levelBadge = `<span style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Năng lực: XUẤT SẮC (30/30)</span>`;
                evaluationText = `Quá đỉnh! Bạn đã làm đúng tuyệt đối toàn bộ 30 câu Part 5 của đề thi này. Phản xạ ngữ pháp và từ vựng của bạn đã đạt mức chuyên nghiệp 990 TOEIC!`;
            } else if (pct >= 80) {
                levelBadge = `<span style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Năng lực: MỤC TIÊU 750+ (${quizScore}/30)</span>`;
                evaluationText = `Chúc mừng bạn! Kết quả này cho thấy bạn có nền tảng cực kỳ vững chắc và phản xạ nhạy bén. Hãy rà soát lại các câu sai để tối ưu thời gian làm bài nhé!`;
            } else if (pct >= 60) {
                levelBadge = `<span style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Năng lực: MỤC TIÊU 600+ (${quizScore}/30)</span>`;
                evaluationText = `Khá tốt! Bạn đã đạt trên trung bình. Để nâng lên mức 750+, hãy tập trung củng cố thêm vốn từ vựng thương mại và các collocations nâng cao.`;
            } else {
                levelBadge = `<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Năng lực: CẦN CỐ GẮNG (${quizScore}/30)</span>`;
                evaluationText = `Bạn cần ôn tập kỹ lại các chủ điểm ngữ pháp ở phần dưới để cải thiện điểm số. Đừng nản chí, hãy kiên trì ôn luyện nhé!`;
            }
            
            summaryComment.innerHTML = `
                <div style="margin-top: 15px;">
                    ${levelBadge}
                    <div style="font-size: 1.05rem; line-height: 1.6; color: var(--text-secondary); max-width: 550px; margin: 0 auto; text-align: center;">
                        <strong>Đánh giá năng lực:</strong> ${evaluationText}
                    </div>
                </div>
            `;
        } else if (quizMode === 'homework') {
            summaryTitleEl.textContent = "Hoàn thành Bài tập về nhà!";
            let encouragementText = "";
            let emoji = "";
            
            if (pct === 100) {
                emoji = "🌟";
                encouragementText = `Ôi tuyệt vời quá! Bạn làm đúng hết sạch rồi! Trí thông minh và sự nỗ lực của bạn thực sự khiến Miss Nguyệt rất tự hào. Hãy giữ vững phong độ đỉnh cao này cho các chủ điểm tiếp theo nhé!`;
            } else if (pct >= 80) {
                emoji = "🎉";
                encouragementText = `Kết quả rất đáng nể nha! Bạn chỉ suýt soát đạt điểm tối đa thôi đó. Miss Nguyệt tin chắc rằng nếu xem lại kỹ các câu làm sai và rút kinh nghiệm, lần sau bạn sẽ đạt điểm số tuyệt đối 20/20 một cách dễ dàng. Tiếp tục cố gắng nhé!`;
            } else if (pct >= 50) {
                emoji = "🌻";
                encouragementText = `Làm được thế này là tiến bộ nhiều rồi nè! Đừng lo lắng về các lỗi sai nhé, vì mỗi lần làm sai là một lần mình nhớ sâu và lâu hơn. Đọc kỹ lại lời giải chi tiết của cô Nguyệt và tiếp tục vững bước nha!`;
            } else {
                emoji = "💖";
                encouragementText = `Không sao cả đâu bạn ơi! Chặng đường chinh phục TOEIC luôn cần sự bền bỉ. Mới đầu có thể hơi khó khăn, nhưng Miss Nguyệt tin chỉ cần bạn kiên trì đọc lại bài học và thử sức lại lần nữa, điểm số sẽ tăng lên rõ rệt. Cố gắng lên nào!`;
            }
            
            summaryComment.innerHTML = `
                <div style="margin-top: 15px; padding: 15px 20px; background: rgba(255,255,255,0.02); border: 1px dashed var(--border-color); border-radius: 16px; max-width: 550px; margin: 15px auto 0 auto;">
                    <div style="font-size: 2.2rem; margin-bottom: 10px;">${emoji}</div>
                    <div style="font-size: 1.05rem; line-height: 1.6; color: var(--text-secondary); text-align: center;">
                        <strong style="color: var(--color-purple);">Lời khích lệ từ Miss Nguyệt:</strong><br>
                        <span style="font-style: italic;">"${encouragementText}"</span>
                    </div>
                </div>
            `;
        } else {
            summaryTitleEl.textContent = "Hoàn thành Luyện tập!";
            let levelBadge = "";
            let evaluationText = "";
            
            if (pct === 100) {
                levelBadge = `<span style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Mức độ: XUẤT SẮC (100%)</span>`;
                evaluationText = `Bạn đã hoàn thành xuất sắc! Khả năng nhận diện dấu hiệu ngữ pháp và áp dụng quy tắc phân tích câu đạt độ chính xác tuyệt đối. Bạn đã hoàn toàn sẵn sàng chinh phục các chủ điểm nâng cao tiếp theo.`;
            } else if (pct >= 80) {
                levelBadge = `<span style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Mức độ: GIỎI (${Math.round(pct)}%)</span>`;
                evaluationText = `Khả năng vận dụng kiến thức rất tốt! Bạn phản xạ nhanh với các dạng câu hỏi, chỉ cần lưu ý kỹ một vài lỗi nhỏ (bẫy từ vựng hoặc các trường hợp đặc biệt) để đạt điểm số tối đa.`;
            } else if (pct >= 50) {
                levelBadge = `<span style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Mức độ: KHÁ (${Math.round(pct)}%)</span>`;
                evaluationText = `Bạn đã nắm được nền tảng ngữ pháp cơ bản của chủ điểm. Tuy nhiên, mức độ vận dụng chưa thực sự ổn định khi gặp các câu có cấu trúc phức tạp. Hãy dành chút thời gian xem lại chi tiết phần giải thích câu ở các lỗi sai.`;
            } else {
                levelBadge = `<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); font-size: 0.95rem; padding: 6px 14px; border-radius: 99px; font-weight: 700; display: inline-block; margin-bottom: 12px;">Mức độ: TRUNG BÌNH (${Math.round(pct)}%)</span>`;
                evaluationText = `Mức độ vận dụng kiến thức còn hạn chế. Bạn dễ bị nhầm lẫn giữa các loại từ hoặc chia sai các cấu trúc cốt lõi. Hãy xem lại phần Lý thuyết và kiên trì làm lại bài tập để củng cố nhé!`;
            }
            
            summaryComment.innerHTML = `
                <div style="margin-top: 15px;">
                    ${levelBadge}
                    <div style="font-size: 1.05rem; line-height: 1.6; color: var(--text-secondary); max-width: 550px; margin: 0 auto; text-align: center;">
                        <strong>Đánh giá năng lực:</strong> ${evaluationText}
                    </div>
                </div>
            `;
        }

        if (pct === 100) {
            // Continuous celebrations!
            let count = 0;
            const interval = setInterval(() => {
                spawnConfetti(40, true); // Gold only
                count++;
                if (count > 6) clearInterval(interval);
            }, 450);
        } else if (pct >= 80) {
            spawnConfetti(60);
        } else if (pct >= 50) {
            spawnConfetti(35);
        }
    }

    retryQuizBtn.addEventListener('click', initQuiz);
    backToLessonBtn.addEventListener('click', () => switchTab('lesson'));

    // --- Google Form Auto-reporting Submitter ---
    function submitToGoogleForm(studentName, chapterTitle, quizType, score, total) {
        const formUrl = "https://docs.google.com/forms/d/e/1FAIpQLSfDHLX7j91RApmGiu7OT83fJ7r5outpA6-pDtrdDO_Us7x7WA/formResponse";
        const entryId = "entry.388968236";
        const reportValue = `${studentName} - ${chapterTitle} - ${quizType} - ${score}/${total}`;
        
        const iframe = document.createElement('iframe');
        iframe.name = 'hidden_iframe';
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        
        const form = document.createElement('form');
        form.action = formUrl;
        form.method = 'POST';
        form.target = 'hidden_iframe';
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = entryId;
        input.value = reportValue;
        
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
        
        setTimeout(() => {
            document.body.removeChild(form);
            document.body.removeChild(iframe);
        }, 1000);
    }

    // --- Name Entry Overlay Handling ---
    const nameEntryOverlay = document.getElementById('nameEntryOverlay');
    const studentNameInput = document.getElementById('studentNameInput');
    const nameInputError = document.getElementById('nameInputError');
    const startLearningBtn = document.getElementById('startLearningBtn');
    const sidebarProfileBox = document.getElementById('sidebarProfileBox');
    const sidebarStudentName = document.getElementById('sidebarStudentName');
    const profileAvatar = document.getElementById('profileAvatar');
    const changeNameBtn = document.getElementById('changeNameBtn');

    function checkStudentName() {
        const name = localStorage.getItem('studentName');
        if (!name) {
            nameEntryOverlay.style.display = 'flex';
            nameEntryOverlay.style.opacity = '1';
            sidebarProfileBox.style.display = 'none';
        } else {
            nameEntryOverlay.style.display = 'none';
            sidebarProfileBox.style.display = 'flex';
            sidebarStudentName.textContent = name;
            profileAvatar.textContent = name.trim().charAt(0).toUpperCase();
        }
    }

    startLearningBtn.addEventListener('click', () => {
        const name = studentNameInput.value.trim();
        if (!name) {
            nameInputError.style.display = 'block';
            studentNameInput.classList.add('shake');
            setTimeout(() => {
                studentNameInput.classList.remove('shake');
            }, 400);
        } else {
            localStorage.setItem('studentName', name);
            nameInputError.style.display = 'none';
            nameEntryOverlay.style.opacity = '0';
            setTimeout(() => {
                nameEntryOverlay.style.display = 'none';
            }, 500);
            
            sidebarProfileBox.style.display = 'flex';
            sidebarStudentName.textContent = name;
            profileAvatar.textContent = name.charAt(0).toUpperCase();
        }
    });

    studentNameInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            startLearningBtn.click();
        }
    });

    changeNameBtn.addEventListener('click', () => {
        const currentName = localStorage.getItem('studentName') || '';
        studentNameInput.value = currentName;
        nameInputError.style.display = 'none';
        nameEntryOverlay.style.display = 'flex';
        setTimeout(() => {
            nameEntryOverlay.style.opacity = '1';
        }, 10);
        studentNameInput.focus();
    });

    // --- Password Unlock Modal for Chapters 11, 12 and Tests ---
    const passwordModal = document.getElementById('passwordModal');
    const chapterPasswordInput = document.getElementById('chapterPasswordInput');
    const passwordError = document.getElementById('passwordError');
    const cancelUnlockBtn = document.getElementById('cancelUnlockBtn');
    const confirmUnlockBtn = document.getElementById('confirmUnlockBtn');
    
    const modalTitleEl = passwordModal.querySelector('h3');
    const modalMsgEl = passwordModal.querySelector('p');

    function showPasswordModal(title = "CHỦ ĐIỂM BỊ KHÓA", message = "Yêu cầu mật khẩu truy cập từ Miss Nguyệt để vào học.") {
        if (modalTitleEl) modalTitleEl.textContent = title;
        if (modalMsgEl) modalMsgEl.textContent = message;
        
        passwordModal.style.display = 'flex';
        setTimeout(() => {
            passwordModal.style.opacity = '1';
        }, 10);
        chapterPasswordInput.value = '';
        chapterPasswordInput.focus();
        passwordError.style.display = 'none';
    }

    function hidePasswordModal() {
        passwordModal.style.opacity = '0';
        setTimeout(() => {
            passwordModal.style.display = 'none';
        }, 300);
    }

    confirmUnlockBtn.addEventListener('click', () => {
        const pass = chapterPasswordInput.value.trim();
        if (pass === 'missnguyet2026') {
            if (pendingChapterId) {
                localStorage.setItem(`chapter_${pendingChapterId}_unlocked`, 'true');
                hidePasswordModal();
                showChapterView(pendingChapterId);
                pendingChapterId = null;
            } else if (pendingTestId) {
                localStorage.setItem(`test_${pendingTestId}_unlocked`, 'true');
                hidePasswordModal();
                showTestView(pendingTestId);
                pendingTestId = null;
            }
            updateLockStatusInSidebar();
        } else {
            passwordError.style.display = 'block';
            chapterPasswordInput.classList.add('shake');
            setTimeout(() => {
                chapterPasswordInput.classList.remove('shake');
            }, 400);
        }
    });

    chapterPasswordInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            confirmUnlockBtn.click();
        }
    });

    cancelUnlockBtn.addEventListener('click', () => {
        hidePasswordModal();
        pendingChapterId = null;
        pendingTestId = null;
    });

    // Clear student name on reload to force re-entry (F5)
    localStorage.removeItem('studentName');

    // Run name checking and sidebar locks on initialize
    checkStudentName();
    updateLockStatusInSidebar();
});
