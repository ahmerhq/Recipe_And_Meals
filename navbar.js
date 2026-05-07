// Extract token from URL query parameter and store in 
function extractAndStoreToken() {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get('token');
  if (token) {
    window.accessToken = token;
    // Clean up URL to remove the token query parameter
    window.history.replaceState({}, document.title, window.location.pathname);
  }
}


async function updateNavbar() {
  const loginBtn = document.querySelector(".sign-log a[href='login.html'] button");
  const signupBtn = document.querySelector(".sign-log a[href='signup.html'] button");
  if (!loginBtn || !signupBtn) return;

  if (!window.accessToken){
    await refreshToken(); // will set window.accessToken if cookie is valid
  }

  if (window.accessToken) {
    loginBtn.textContent = "Logout";
    signupBtn.style.display = "none";

    loginBtn.addEventListener("click", async (e) => {
      if (loginBtn.textContent === "Logout"){
        e.preventDefault();
        
        // Call logout endpoint to clear refresh token cookie
        try {
          await fetch("http://127.0.0.1:8000/logout", {
            method: "POST",
            credentials: "include"
          });
        } catch (error) {
          console.log("Logout request sent");
        }
        
        // Clear access token from memory
        window.accessToken = null;
        location.reload();
      }
    });
  } else {
    signupBtn.style.display = "inline-block";
    loginBtn.textContent = "Login";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  extractAndStoreToken();
  await updateNavbar();
});
