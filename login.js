const loginForm = document.querySelector("#loginForm");
const googleLoginBtn = document.querySelector("#googleLogin");

// LOGIN FLOW
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.querySelector("#username").value.trim();
    const password = document.querySelector("#password").value.trim();

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        body: formData,
        credentials: "include" // important to send/recieve tokens
      });

      if (res.ok) {
        const data = await res.json();
        alert(`login successfull`);
        
        window.accessToken = data.access_token;  // store in memory only, httpOnly cookie is secure

        loginForm.reset();
        window.location.href = "/index.html";

        updateNavbar();
      } else {
        const err = await res.json();
        alert(`error occured. ${err.detail}`);
      }
    } catch (error) {
      alert(`Network error ${error.message}`);
    }
  });
}





// // handle google login button
if (googleLoginBtn) {
  googleLoginBtn.addEventListener("click", () => {
    window.location.href = "http://127.0.0.1:8000/auth/google/login";
  });
}

// handle redirect back to frontend
const params = new URLSearchParams(window.location.search);
const token = params.get("token"); // take value after url?token=

if (token) {
  // store access token only in memory, httpOnly cookie is secure
  window.accessToken = token;
  alert("login successfull");
   
  // clean url
  window.history.replaceState({}, document.title, window.location.pathname);
  
  // update navbar
  updateNavbar();
   
}


