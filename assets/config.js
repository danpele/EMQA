// ============================================================
// EMQA site configuration (shared by index.html and index_ro.html)
// GOOGLE_CLIENT_ID: OAuth client (Web) of the Google Cloud project "MFM Quiz Login", valid for the
//   origin https://danpele.github.io; the quizzes require "Sign in with Google" with an ASE account.
// QUIZ_SCORES_URL: Google Apps Script web app (../tools/quiz_scores.gs, not published) that verifies
//   the Google token and stores the score in the sheet "EMQA 2026/2027 - Scoruri quiz".
//   While it starts with 'YOUR_', no score is sent.
// ============================================================
window.EMQA_CONFIG = {
    GOOGLE_CLIENT_ID: '1095360272769-rhjjncfor0gumhev6a0l6tnnrnmdrnna.apps.googleusercontent.com',
    QUIZ_SCORES_URL: 'YOUR_QUIZ_SCORES_URL'
};
