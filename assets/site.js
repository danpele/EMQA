// ============================================================
// EMQA course website (shell shared with the SFM, TSA and BA sites) - rendering + quiz engine
// Reads window.EMQA_DATA (course-data.js), window.EMQA_CONFIG (config.js)
// and quiz banks registered in EMQA_DATA.quizzes by lecture id (assets/quizzes/<id>.js).
// Lectures are referenced by their stable `id`; `num` is only the display order.
// Language is set by the page shell: window.EMQA_LANG = 'en' | 'ro'.
// ============================================================
(function () {
    'use strict';

    const LANG = window.EMQA_LANG === 'ro' ? 'ro' : 'en';
    const D = window.EMQA_DATA;
    const T = D.ui[LANG];
    const CFG = window.EMQA_CONFIG || {};
    const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

    const isConfigured = v => typeof v === 'string' && v.length > 0 && !v.startsWith('YOUR_');
    const $ = id => document.getElementById(id);
    const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

    // values still to be supplied by the instructor start with 'TODO' in course-data.js;
    // on the page they read "To be announced"
    const tbd = s => (typeof s === 'string' && /^TODO/.test(s)) ? `<span class="tbd">${T.tbd}</span>` : s;

    function typeset(el) {
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise(el ? [el] : undefined).catch(() => {});
        }
    }

    // ------------------------------------------------------------
    // STATIC TEXT (header, nav, section titles)
    // ------------------------------------------------------------
    function renderStatic() {
        document.title = T.pageTitle;
        document.documentElement.lang = LANG;
        document.querySelectorAll('[data-t]').forEach(el => {
            const path = el.getAttribute('data-t').split('.');
            let v = T;
            for (const p of path) v = v && v[p];
            if (typeof v === 'string') el.innerHTML = v;
        });
    }

    const cards = list => list.map(c =>
        `<div class="info-card"><h3>${c.h}</h3>${c.p.map(p => `<p>${tbd(p)}</p>`).join('')}</div>`
    ).join('');

    // ------------------------------------------------------------
    // OVERVIEW, OBJECTIVES
    // ------------------------------------------------------------
    function renderOverview() {
        $('overview-cards').innerHTML = cards(D.overview[LANG]);
        $('objectives-list').innerHTML = D.objectives[LANG].map(o => `<li>${o}</li>`).join('');
    }

    // ------------------------------------------------------------
    // LECTURE CARDS
    // Each lecture lists its files (lecture PDF, notebook, code folder). A file is linked when
    // the lecture number is in READY or when the file is found on the server (HEAD request),
    // so a card switches from "in preparation" to links as soon as the PDF is published.
    // ------------------------------------------------------------
    const READY = [];   // e.g. [1] once lecture 1 is final; lectures not listed here are probed
    const LINK_ROWS = [['course', ['slides']], ['code', ['notebook', 'code']]];
    const LINK_CLASS = { slides: 'btn-primary', notebook: 'btn-outline', code: 'btn-outline' };
    const avail = {};   // avail[id] = { slides, notebook, code }

    function linkButton(type, l, ok) {
        const label = T.links[type];
        if (!ok) return `<span class="btn disabled" aria-disabled="true" title="${T.comingSoon}">${label} · ${T.comingSoonShort}</span>`;
        if (type === 'slides') return `<a href="${(LANG === 'ro' && l.files.pdf_ro) || l.files.pdf}" class="btn ${LINK_CLASS[type]}" target="_blank" rel="noopener">${label}</a>`;
        if (type === 'notebook') {
            const nb = (LANG === 'ro' && l.files.notebook_ro) || l.files.notebook;
            return `<span class="link-group"><a href="${D.repo}/blob/main/${nb}" class="btn btn-outline" target="_blank" rel="noopener">${label}</a>` +
                `<a href="${D.colab}${nb}" class="btn btn-colab" target="_blank" rel="noopener" title="${T.links.colab}">Colab</a></span>`;
        }
        return `<a href="${D.repo}/tree/main/${l.files.code}" class="btn btn-outline" target="_blank" rel="noopener">${label}</a>`;
    }

    function lectureCard(l) {
        const a = avail[l.id] || {};
        const ready = !!a.slides;
        const badge = ready ? '' : `<span class="badge badge-soon">${l.status === 'prep' ? T.comingSoon : T.coming}</span>`;
        const anyFile = a.slides || a.notebook || a.code;
        const links = (l.status === 'prep' || anyFile)
            ? LINK_ROWS.map(([row, types]) =>
                `<div class="link-row"><span class="link-row-h">${T.rows[row]}</span><div class="link-row-b">${types.map(t => linkButton(t, l, a[t])).join('')}</div></div>`).join('')
            : `<p class="chapter-soon">${T.chapterSoon}</p>`;
        const cases = (l.cases || []).length
            ? `<p class="lecture-cases"><strong>${T.casesShort}:</strong> ${l.cases.map(id => {
                const c = D.cases.find(x => x.id === id);
                return c ? `<a href="#case-${id}">${c[LANG].h}</a>` : '';
            }).join(', ')}</p>` : '';
        const further = (l.further || []).length
            ? `<div class="quantinar-box"><h4>${T.further}</h4><ul>` +
              l.further.map(f => `<li><a href="${f.url}" target="_blank" rel="noopener">${f[LANG]}</a></li>`).join('') + '</ul></div>'
            : '';
        return `<div class="chapter-card${ready ? '' : ' soon'}" id="lecture-${l.id}">
            <div class="chapter-header"><h3>${T.chapter} ${l.num}: ${l.title[LANG]}</h3><div class="badges">${badge}</div></div>
            <div class="chapter-body">
                <ul>${l.topics[LANG].map(t => `<li>${t}</li>`).join('')}</ul>
                ${cases}
                <div class="chapter-links">${links}</div>
                ${further}
            </div>
        </div>`;
    }

    function renderLectures() {
        $('chapters-grid').innerHTML = D.lectures.map(lectureCard).join('');
    }

    const exists = path => fetch(path, { method: 'HEAD', cache: 'no-store' }).then(r => r.ok).catch(() => false);

    function probeLectures() {
        D.lectures.forEach(l => {
            if (READY.includes(l.num)) { avail[l.id] = { slides: true, notebook: true, code: true }; return; }
            const f = l.files || {};
            // one request per lecture until its PDF exists; the notebook and the code are linked together with the PDF
            (f.pdf ? exists(f.pdf) : Promise.resolve(false)).then(s => {
                if (!s) return;
                return Promise.all([f.notebook ? exists(f.notebook) : false, f.codeProbe ? exists(f.codeProbe) : false]).then(([n, c]) => {
                    avail[l.id] = { slides: true, notebook: n, code: c };
                    const old = $('lecture-' + l.id);
                    if (old) old.outerHTML = lectureCard(l);
                });
            });
        });
    }

    // ------------------------------------------------------------
    // CASE STUDIES, DATA
    // ------------------------------------------------------------
    function renderCases() {
        $('cases-grid').innerHTML = D.cases.map(c =>
            `<div class="info-card case-card" id="case-${c.id}"><h3>${c[LANG].h}</h3>${c[LANG].p.map(p => `<p>${p}</p>`).join('')}</div>`
        ).join('');
    }

    const loc = v => (v && typeof v === 'object') ? v[LANG] : v;

    function renderData() {
        const d = D.data;
        $('data-intro').innerHTML = d.intro[LANG];
        const head = T.dataCols.map(h => `<th>${h}</th>`).join('');
        $('data-table').innerHTML = `<table class="sessions data-table"><thead><tr>${head}</tr></thead><tbody>` +
            d.series.map(s => `<tr><td>${s.name[LANG]}<br><code>${esc(s.file)}</code></td><td>${s.freq[LANG]}</td>` +
                `<td class="c">${loc(s.coverage)}</td><td>${loc(s.units)}</td>` +
                `<td><a href="${s.href}" target="_blank" rel="noopener">${s.source}</a>${s.note ? `<br><span class="muted-note">${s.note[LANG]}</span>` : ''}</td></tr>`).join('') +
            '</tbody></table>';
        $('data-missing').innerHTML = d.missing.map(m => `<li><strong>${m.name}</strong> - ${m[LANG]}</li>`).join('');
        $('data-licence').innerHTML = d.licence[LANG];
    }

    // ------------------------------------------------------------
    // RESOURCES, CONTACT, FOOTER
    // ------------------------------------------------------------
    function renderResources() {
        $('resources-list').innerHTML = D.resources.map(r =>
            `<a href="${r.href}" class="resource-item" target="_blank" rel="noopener">
                ${r.img ? `<img class="resource-logo" src="${r.img}" alt="">` : `<div class="resource-icon">${r.icon}</div>`}
                <div><strong>${r[LANG][0]}</strong><p>${r[LANG][1]}</p></div>
            </a>`
        ).join('');
        $('bibliography').innerHTML = D.bibliography.map(b => `<li>${b}</li>`).join('');
        $('abbreviations').innerHTML = D.abbreviations.map(([a, en, ro]) =>
            `<div class="abbr-row"><dt>${a}</dt><dd>${LANG === 'ro' && ro ? ro : en}</dd></div>`).join('');
    }

    function renderContact() {
        const c = D.contact;
        $('contact-cards').innerHTML =
            `<div class="info-card"><h3>${T.instructor}</h3><p><strong>${c.name}</strong></p>` +
            c[LANG].map(p => `<p>${p}</p>`).join('') +
            `<p style="margin-top:0.6rem"><a href="mailto:${c.email}">${c.email}</a></p>` +
            `<p style="margin-top:0.8rem"><a class="btn btn-primary" href="https://danpele.github.io/${LANG === 'ro' ? 'index_ro.html' : ''}" target="_blank" rel="noopener">${LANG === 'ro' ? 'Site-ul personal' : 'Personal website'}</a></p></div>` +
            `<div class="info-card"><h3>${T.office}</h3><p>${tbd(c.office[LANG])}</p></div>`;
        $('footer-logos').innerHTML = D.footerLogos.map(([href, src, alt]) =>
            `<a href="${href}" target="_blank" rel="noopener"><img src="${src}" alt="${alt}"></a>`
        ).join('');
        $('footer-text').innerHTML = `&copy; 2026 ${T.footer}`;
        document.querySelector('.hero-inner').insertAdjacentHTML('afterbegin', `<figure class="motto"><blockquote lang="it">“Tristo è quel discepolo che non avanza il suo maestro.”</blockquote>` +
            `<p>${LANG === 'ro' ? 'Trist este discipolul care nu își depășește maestrul.' : 'Poor is the pupil who does not surpass his master.'}</p><figcaption>— Leonardo da Vinci</figcaption></figure>`);
    }

    // ------------------------------------------------------------
    // GOOGLE SIGN-IN (ASE accounts) - used by the quizzes only when configured in config.js
    // ------------------------------------------------------------
    const ALLOWED = ['ase.ro', 'stud.ase.ro'];
    const session = {
        get(k) { try { return sessionStorage.getItem('emqa-' + k); } catch (e) { return null; } },
        set(k, v) { try { sessionStorage.setItem('emqa-' + k, v); } catch (e) { /* ignore */ } },
        del(k) { try { sessionStorage.removeItem('emqa-' + k); } catch (e) { /* ignore */ } }
    };

    function decodeJwt(t) {
        try {
            const b = t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
            return JSON.parse(decodeURIComponent(atob(b).split('').map(c =>
                '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')));
        } catch (e) { return null; }
    }

    function getUser() {
        const cred = session.get('google-credential');
        const u = cred && decodeJwt(cred);
        if (!u || u.exp * 1000 < Date.now()) return null;
        return { name: u.name || u.email, email: u.email, credential: cred };
    }

    const loginEnabled = () => isConfigured(CFG.GOOGLE_CLIENT_ID);

    function onGoogleCredential(resp) {
        const u = decodeJwt(resp.credential);
        const domain = u && String(u.email).split('@')[1];
        if (!u || !ALLOWED.includes(domain)) {
            $('login-msg').textContent = T.loginWrongDomain;
            return;
        }
        session.set('google-credential', resp.credential);
        renderLogin();
        if (activeLecture) showQuiz(activeLecture);
    }

    function gisInit() {
        if (gisInit.done || !(window.google && google.accounts && google.accounts.id)) return !!gisInit.done;
        gisInit.done = true;
        google.accounts.id.initialize({ client_id: CFG.GOOGLE_CLIENT_ID, auto_select: true, callback: onGoogleCredential });
        return true;
    }

    function renderLogin() {
        const box = $('quiz-login');
        if (!loginEnabled()) { box.style.display = 'none'; return; }
        if (!document.querySelector('script[src*="accounts.google.com/gsi"]')) {
            const s = document.createElement('script');
            s.src = 'https://accounts.google.com/gsi/client'; s.async = true; s.onload = () => renderLogin();
            document.head.appendChild(s);
        }
        box.style.display = '';
        const user = getUser();
        if (user) {
            box.innerHTML = `<p>${T.loggedAs} <strong>${esc(user.name)}</strong> (${esc(user.email)})
                <button class="btn btn-outline" id="g-logout" style="margin-left:0.5rem;padding:0.2rem 0.6rem">${T.logout}</button></p>`;
            $('g-logout').onclick = () => {
                session.del('google-credential');
                if (window.google && google.accounts) google.accounts.id.disableAutoSelect();
                renderLogin();
                if (activeLecture) showQuiz(activeLecture);
            };
            return;
        }
        box.innerHTML = `<p>${T.loginPrompt}</p><div id="g-button"></div><p class="login-msg" id="login-msg" aria-live="polite"></p>`;
        const el = $('g-button');
        if (el && gisInit()) {
            google.accounts.id.renderButton(el, { theme: 'outline', size: 'large', text: 'signin_with', locale: LANG, width: 280 });
        }
    }

    function sendResults(l, score, total) {
        const user = getUser();
        const out = $('quiz-save-status');
        if (!isConfigured(CFG.QUIZ_SCORES_URL) || !user) return;
        out.textContent = T.saving;
        // text/plain avoids a CORS preflight; the backend parses the JSON body
        fetch(CFG.QUIZ_SCORES_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify({ credential: user.credential, chapter: l.id, score, total, lang: LANG })
        }).then(r => r.json()).then(j => {
            out.textContent = j.ok ? T.saved : (j.error === 'token' ? T.saveExpired : T.saveFailed);
        }).catch(() => { out.textContent = T.saveFailed; });
    }

    // ------------------------------------------------------------
    // QUIZ ENGINE
    // Bank format (assets/quizzes/<id>.js), loaded by a <script> tag in index.html / index_ro.html:
    //   EMQA_DATA.quizzes['<id>'] = { draw: 20, questions: [
    //     { correct: <index 0-3>, en: {title, text, options:[4], correctExplanation, incorrectExplanation}, ro: {...} } ] }
    // ------------------------------------------------------------
    let quiz = null;
    let activeLecture = null;

    function shuffle(arr) {
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
    }

    function renderQuizTabs() {
        $('quiz-tabs').innerHTML = D.lectures.map(l => {
            const has = !!D.quizzes[l.id];
            return `<button class="btn btn-outline${has ? '' : ' unavailable'}" data-ch="${l.id}" title="${esc(l.title[LANG])}">${T.chapterShort} ${l.num}</button>`;
        }).join('');
        $('quiz-tabs').querySelectorAll('button').forEach(b => {
            b.onclick = () => showQuiz(b.getAttribute('data-ch'));
        });
    }

    function showQuiz(id) {
        activeLecture = id;
        $('quiz-tabs').querySelectorAll('button').forEach(b =>
            b.classList.toggle('active', b.getAttribute('data-ch') === id));
        const l = D.lectures.find(c => c.id === id);
        const bank = D.quizzes[id];
        const box = $('quiz-container');
        const heading = `<h3>${T.chapter} ${l.num}: ${l.title[LANG]}</h3>`;
        if (!bank) {
            quiz = null;
            box.innerHTML = `${heading}<p class="quiz-intro">${T.quizSoon}</p>`;
            return;
        }
        if (loginEnabled() && !getUser()) {
            quiz = null;
            box.innerHTML = `${heading}<p class="quiz-intro">${T.loginRequired}</p>`;
            return;
        }
        box.innerHTML = `${heading}
            <p class="quiz-intro">${T.quizIntro}</p>
            <div id="quiz-questions"></div>
            <div class="quiz-actions">
                <button class="btn btn-primary" id="quiz-score">${T.calc}</button>
                <button class="btn btn-outline" id="quiz-reset">${T.reset}</button>
            </div>
            <p class="score-display" id="quiz-score-display" aria-live="polite"></p>
            <p class="save-status" id="quiz-save-status" aria-live="polite"></p>
            <div id="quiz-answer-key"></div>`;
        $('quiz-score').onclick = calculateScore;
        $('quiz-reset').onclick = () => showQuiz(id);
        newAttempt(l, bank);
    }

    function newAttempt(l, bank) {
        const n = Math.min(bank.draw || 20, bank.questions.length);
        const items = shuffle(bank.questions).slice(0, n).map(q => {
            const order = shuffle(q[LANG].options.map((_, i) => i));   // order[pos] = original option index
            return { q, order, correctPos: order.indexOf(q.correct) };
        });
        quiz = { lecture: l, items, answers: {} };

        $('quiz-questions').innerHTML = items.map((it, k) => {
            const L = it.q[LANG];
            return `<div class="quiz-question" id="qq${k}">
                <h4>${T.question} ${k + 1}: ${L.title}</h4>
                <p>${L.text}</p>
                <ul class="quiz-options" role="radiogroup">
                    ${it.order.map((orig, pos) =>
                        `<li tabindex="0" role="radio" aria-checked="false" data-k="${k}" data-pos="${pos}">
                            <input type="radio" name="qq${k}" tabindex="-1"> ${LETTERS[pos]}) ${L.options[orig]}</li>`).join('')}
                </ul>
                <div class="answer-reveal answer-correct" id="qq${k}-ok"><strong>${T.correct}</strong> ${L.correctExplanation}</div>
                <div class="answer-reveal answer-incorrect" id="qq${k}-ko"><strong>${T.incorrect}</strong>
                    ${T.correctIs} ${LETTERS[it.correctPos]}) ${L.options[it.q.correct]}. ${L.incorrectExplanation}</div>
            </div>`;
        }).join('');

        $('quiz-questions').querySelectorAll('.quiz-options li').forEach(li => {
            const pick = () => answer(parseInt(li.dataset.k, 10), parseInt(li.dataset.pos, 10));
            li.onclick = pick;
            li.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } };
        });
        typeset($('quiz-container'));
    }

    function answer(k, pos) {
        if (!quiz || quiz.answers[k] !== undefined) return;   // locked after the first answer
        quiz.answers[k] = pos;
        const qDiv = $('qq' + k);
        qDiv.querySelectorAll('.quiz-options li').forEach(li => {
            const mine = parseInt(li.dataset.pos, 10) === pos;
            li.classList.add('locked');
            li.classList.toggle('chosen', mine);
            li.setAttribute('aria-checked', mine ? 'true' : 'false');
            li.querySelector('input').checked = mine;
        });
        const ok = pos === quiz.items[k].correctPos;
        $('qq' + k + '-ok').style.display = ok ? 'block' : 'none';
        $('qq' + k + '-ko').style.display = ok ? 'none' : 'block';
    }

    function calculateScore() {
        if (!quiz) return;
        const total = quiz.items.length;
        let score = 0, answered = 0;
        quiz.items.forEach((it, k) => {
            if (quiz.answers[k] !== undefined) {
                answered++;
                if (quiz.answers[k] === it.correctPos) score++;
            }
        });
        const pct = Math.round((score / total) * 100);
        let msg = `${T.score}: ${score}/${total} (${pct}%)`;
        if (answered < total) msg += ` - ${total - answered} ${T.unanswered}`;
        msg += ' - ' + T.verdicts[pct >= 90 ? 3 : pct >= 70 ? 2 : pct >= 50 ? 1 : 0];
        $('quiz-score-display').textContent = msg;
        if (!quiz.sent) { quiz.sent = true; sendResults(quiz.lecture, score, total); }

        const rows = quiz.items.map((it, k) => {
            const L = it.q[LANG];
            const a = quiz.answers[k];
            const cls = a === undefined ? '' : (a === it.correctPos ? 'ok' : 'ko');
            const res = a === undefined ? '-' : (a === it.correctPos ? '<span class="res-ok">OK</span>' : '<span class="res-ko">X</span>');
            const yours = a === undefined ? '-' : `${LETTERS[a]}) ${L.options[it.order[a]]}`;
            return `<tr class="${cls}"><td class="c"><strong>${k + 1}</strong></td><td>${L.text}</td>
                <td>${LETTERS[it.correctPos]}) ${L.options[it.q.correct]}</td><td>${yours}</td><td class="c">${res}</td></tr>`;
        }).join('');
        $('quiz-answer-key').innerHTML = `<div class="answer-key"><h4>${T.detailed}</h4><table>
            <tr><th class="c">${T.colQ}</th><th>${T.colQuestion}</th><th>${T.colCorrect}</th><th>${T.colYours}</th><th class="c">${T.colResult}</th></tr>
            ${rows}</table></div>`;
        typeset($('quiz-answer-key'));
    }

    // ------------------------------------------------------------
    // INIT
    // ------------------------------------------------------------
    // left sidebar with the page sections (wide screens): built from the visible <section id> headings, current one highlighted
    function renderSideToc() {
        const main = document.querySelector('main');
        if (!main || main.querySelector('.side-toc')) return;
        const secs = [...main.querySelectorAll(':scope > section[id]')].filter(s => !s.hidden && s.querySelector('h2'));
        if (secs.length < 3) return;
        const aside = document.createElement('aside');
        aside.className = 'side-toc';
        aside.setAttribute('aria-label', LANG === 'ro' ? 'Secțiunile paginii' : 'Page sections');
        aside.innerHTML = `<p class="side-toc-h">${LANG === 'ro' ? 'Pe această pagină' : 'On this page'}</p><ol>` +
            secs.map(s => `<li><a href="#${s.id}">${esc(s.querySelector('h2').textContent.trim())}</a></li>`).join('') + '</ol>';
        main.prepend(aside);
        main.classList.add('with-side-toc');
        const links = [...aside.querySelectorAll('a')];
        const mark = () => {
            let cur = secs[0];
            for (const s of secs) if (!s.hidden && s.getBoundingClientRect().top < 200) cur = s;
            links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur.id));
        };
        window.addEventListener('scroll', mark, { passive: true });
        mark();
    }

    function init() {
        renderStatic();
        renderOverview();
        renderLectures();
        probeLectures();
        renderCases();
        renderData();
        renderResources();
        renderContact();
        renderLogin();
        renderQuizTabs();
        const first = D.lectures.find(c => D.quizzes[c.id]) || D.lectures[0];
        showQuiz(first.id);
        renderSideToc();
        typeset();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
