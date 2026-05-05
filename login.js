const loginForm = document.querySelector("#loginForm");
const googleLoginBtn = document.querySelector("#googleLogin");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.querySelector("#username").value.trim();
  const password = document.querySelector("#password").value.trim();

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    body: formData,
  });

  if (res.ok) {
    const data = await res.json();
    alert(`login successfull`);
    localStorage.setItem("access_token", data.access_token);  // store acccess token
    localStorage.setItem("access_token", data.refresh_token); // store refresh token.
    loginForm.reset();
    window.location.href = "/index.html"

    updateNavbar()
  } else {
    const err = await res.json();
    alert(`error occured. ${err.detail}`);
  }
});




// handle google login button
googleLoginBtn.addEventListener("click", () => {
  window.location.href= "http://127.0.0.1:8000/auth/google/login";
})


// handle redirect back to frontend
const params= new URLSearchParams(window.location.search);
const token= params.get("token"); // take value after url?token=

if (token){
  localStorage.setItem("access_token", token);
  alert("login successfull")

  window.location.href= "/index.html";
  window.history.replaceState({}, document.title, window.location.pathname);

  updateNavbar();
}





