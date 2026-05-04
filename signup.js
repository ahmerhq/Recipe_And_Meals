const signUpForm = document.querySelector("#signupForm");

signUpForm.addEventListener("submit", async (e) => {
  const username = document.querySelector("#username").value.trim();
  const email = document.querySelector("#email").value.trim();
  const password = document.querySelector("#password").value.trim();
  const signupButton = document.querySelector("#signup");

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
