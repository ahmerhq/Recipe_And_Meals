const loginForm = document.querySelector("#loginForm");

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
    localStorage.setItem("access_token", data.access_token);
    loginForm.reset();
    window.location.href = "/index.html"

    updateNavbar()
  } else {
    const err = await res.json();
    alert(`error occured. ${err.detail}`);
  }
});

