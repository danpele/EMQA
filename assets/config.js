// ============================================================
// EMQA site configuration (shared by index.html and index_ro.html)
// GOOGLE_CLIENT_ID: OAuth client (Web) for "Sign in with Google" on the quizzes (ASE accounts only).
//   The SFM / TSA client of the origin https://danpele.github.io can be reused once the
//   instructor decides how quiz scores are used.
// QUIZ_SCORES_URL: Google Apps Script web app that verifies the Google token and stores the score.
// While a value starts with 'YOUR_' the feature stays switched off: quizzes run without login
// and no score is sent anywhere.
// TODO: decide whether quiz scores are recorded (and whether they count toward the grade),
//       then fill in both values.
// ============================================================
window.EMQA_CONFIG = {
    GOOGLE_CLIENT_ID: 'YOUR_GOOGLE_CLIENT_ID',
    QUIZ_SCORES_URL: 'YOUR_QUIZ_SCORES_URL'
};
