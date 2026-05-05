// Extract token from URL query parameter and store in localStorage
function extractAndStoreToken() {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get('token');
  if (token) {
    localStorage.setItem('access_token', token);
    // Clean up URL to remove the token query parameter
    window.history.replaceState({}, document.title, window.location.pathname);
  }
}

function updateNavbar() {
  const token = localStorage.getItem("access_token");
  const loginBtn = document.querySelector(".sign-log a[href='login.html'] button");
  const signupBtn = document.querySelector(".sign-log a[href='signup.html'] button");
  if (!loginBtn || !signupBtn) return;

  if (token) {
    loginBtn.textContent = "Logout";
    signupBtn.style.display = "none";

    loginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("access_token");
      location.reload();
    });
  } else {
    signupBtn.style.display = "inline-block";
    loginBtn.textContent = "Login";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  extractAndStoreToken();
  updateNavbar();
});
