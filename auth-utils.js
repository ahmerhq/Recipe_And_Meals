// Shared authentication utilities used across multiple pages

// Refresh access + refresh token
async function refreshToken() {
  try {
    const response = await fetch("http://127.0.0.1:8000/refresh", {
      method: "POST",
      credentials: "include",
    });

    if (response.ok) {
      const data = await response.json();

      // only update access token in memory, httpOnly cookie is secure
      window.accessToken = data.access_token;

      return data.access_token;
    } else {
      // refresh failed
      const error = await response.json();
      window.accessToken = null;
      return null;
    }
  } catch (error) {
    window.accessToken = null;
    return null;
  }
} 

// --- Wrapper for protected requests ---

async function fetchWithAuth(url, options = {}) {
  let token = window.accessToken; // access tok kept in memory

  // Build headers safely
  const headers = { ...options.headers };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  let response = await fetch(url, {
    ...options, // ... spreads up everything inside.
    headers: { ...options.headers, Authorization: `Bearer ${token}` },
    credentials: "include", // ensures cookies are sent
  });
  if (response.status === 401) {
    token = await refreshToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
      response = await fetch(url, {
        ...options,
        headers: { ...options.headers, Authorization: `Bearer ${token}` },
        credentials: "include",
      });
    }
  }
  return response;
}
