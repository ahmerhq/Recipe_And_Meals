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

document.addEventListener("DOMContentLoaded", updateNavbar);
