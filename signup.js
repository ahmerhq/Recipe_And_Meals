const signUpForm = document.querySelector("#signupForm");
const googleLoginBtn = document.querySelector("#googleSignUp");

if (signUpForm) {
  signUpForm.addEventListener("submit", async (e) => {
    const username = document.querySelector("#username").value.trim();
    const email = document.querySelector("#email").value.trim();
    const password = document.querySelector("#password").value.trim();

    e.preventDefault();
    const response = await fetch(`http://127.0.0.1:8000/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, username, password }),
    });
    if (response.ok) {
      const data = await response.json();
      alert(`signup successful: Welcome on board ${data.username}`);
      signUpForm.reset();
    } else {
      const error = await response.json();
      alert(`signup failed. ${error.msg}`);
    }
  });
}




// SIGNUP WITH GOOGLE FLOW
if (googleLoginBtn) {
  googleLoginBtn.addEventListener("click", async () => {
    window.location.href = "http://127.0.0.1:8000/auth/google/login";
  });
}

const params = new URLSearchParams(window.location.search);
const token = params.get("token");

if (token) {
  // store access token only in memory
  window.accessToken = token;
  alert("signup successfull");

  window.history.replaceState({}, document.title, window.location.pathname);

  updateNavbar();
}


