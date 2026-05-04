// for search page //

const searchButton = document.querySelector("#searchButton");
const searchInput = document.querySelector(".search-input");

const resultContainer = document.createElement("div"); // creating div
resultContainer.className = "recipe-result"; // giving that div a class

document.body.appendChild(resultContainer); // append at the last of the body

if (searchButton) {
  searchButton.addEventListener("click", async () => {
    const dishName = searchInput.value.trim();
    if (!dishName) {
      resultContainer.innerHTML =
        "<p style='color:Red;'><strong>Please enter a dish name</strong></p>";
      return;
    }
    try {
      const response = await fetch("http://127.0.0.1:8000/recipe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item: dishName }),
      });

      if (!response.ok) {
        throw new Error("Recipe not found");
      }

      const data = await response.json();

      resultContainer.innerHTML = `
              <div class="recipe-card">
                <h2>${data.item_name}</h2>
                <p><strong>Country:</strong> ${data.item_country}</p>
                <p><strong>Category:</strong> ${data.item_category}</p>
                <p><strong>Instructions:</strong></p>
                <div class="instructions">${data.item_recipe}</div>
              </div>
            `;
    } catch (error) {
      resultContainer.innerHTML = `<p style='color:red;'>${error.message}</p>`;
    }
  });
}

// for search page //

const randomButton = document.querySelector("#random-button");

const containerForRandom = document.createElement("div");
containerForRandom.className = "recipe-result";
document.body.appendChild(containerForRandom);

if (randomButton) {
  randomButton.addEventListener("click", async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/recipe/random");
      const data = await response.json();

      containerForRandom.innerHTML = `
            <div class="recipe-card">
                <h2>${data.item_name}</h2>
                <p><strong>Country:</strong> ${data.item_country}</p>
                <p><strong>Category:</strong> ${data.item_category}</p>
                <p><strong>Instructions:</strong></p>
                <div class="instructions">${data.item_recipe}</div>
            </div>
            `;
    } catch (error) {
      containerForRandom.innerHTML = `<p style='color=Red'><strong>${error.message}</strong></p>`;
    }
  });
}

// for filter by category page //

// Category filter

const categoryBtn = document.querySelector("#categoryBtn");
const categoryResults = document.querySelector("#categoryResults");

if (categoryBtn) {
  categoryBtn.addEventListener("click", async () => {
    const category = document.querySelector("#categorySelect").value;
    const response = await fetch(
      `http://127.0.0.1:8000/recipe/filter/${category}`,
      {
        method: "POST",
      },
    );
    const data = await response.json();
    categoryResults.innerHTML = data.map((meal) => `<p>${meal}</p>`).join("");
  });
}

// Country filter

const countryBtn = document.querySelector("#countryBtn");
const countryResults = document.querySelector("#countryResults");

if (countryBtn) {
  countryBtn.addEventListener("click", async () => {
    const country = document.querySelector("#countrySelect").value;
    const response = await fetch(`http://127.0.0.1:8000/recipe/${country}`, {
      method: "POST",
    });
    const data = await response.json();
    countryResults.innerHTML = data.map((meal) => `<p>${meal}</p>`).join("");
  });
}

//  FAVORITE ITEM PAGE

// ...existing code...

const favForm = document.querySelector("#select-fav");
const userFavResult = document.querySelector("#userFavResult");
const getRecipeBtn = document.querySelector("#getRecipeBtn"); // for getting fav recipe

document.addEventListener("DOMContentLoaded", async () => {
  if (!userFavResult || !getRecipeBtn) return;

  const token = localStorage.getItem("access_token");
  if (!token) {
    userFavResult.innerHTML = "<p>Please login first.</p>";
    getRecipeBtn.style.display = "none";
    return;
  }

  const re = await fetch("http://127.0.0.1:8000/recipe/favorite", {
    method: "GET",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (re.ok) {
    getRecipeBtn.style.display = "inline-block";
    userFavResult.innerHTML =
      "<p>You already have favorite food set. Either update it by choosing above, or get its recipe by clicking the button below.</p>";
  } else {
    getRecipeBtn.style.display = "none";
    userFavResult.innerHTML = "<p>No favorite set. Choose one above.</p>";
  }
});

if (favForm) {
  favForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const favorite_food = document.querySelector("#favorite").value.trim();
    const token = localStorage.getItem("access_token");

    const response = await fetch(`http://127.0.0.1:8000/favorite_meal`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ favorite_food }),
    });
    if (response.ok) {
      const data = await response.json();
      userFavResult.innerHTML = `<p>${data.message}</p>`;
      getRecipeBtn.style.display = "inline-block";
    } else {
      const error = await response.json();
      userFavResult.innerHTML = `<p>${error.detail}</p>`;
      getRecipeBtn.style.display = "none";
    }
  });
}

if (getRecipeBtn) {
  getRecipeBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("access_token");
    const res = await fetch("http://127.0.0.1:8000/recipe/favorite", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });

    const recipeBox = document.querySelector("#recipeBox");

    if (res.ok) {
      const data = await res.json();
      recipeBox.innerHTML = `
        <h3>${data.item_name}</h3>
        <p><strong>Category:</strong> ${data.item_category}</p>
        <p><strong>Country:</strong> ${data.item_country}</p>
        <p><strong>Instructions:</strong></p>
        <pre>${data.item_recipe}</pre>
      `;
    } else {
      const error = await res.json();
      recipeBox.innerHTML = `<p style="color:red;">${error.detail}</p>`;
    }
  });
}

// delete account

const dltBtn = document.querySelector("#dltBtn");
const dltText = document.querySelector("#dltText");

if (dltBtn) {
  dltBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      dltText.innerHTML = "<div>Please sign in first to delete account</div>";
      return;
    }
    const response = await fetch("http://127.0.0.1:8000/delete", {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      const data = await response.json();
      dltText.innerHTML = `<div>${data.message}</div>`;
      localStorage.removeItem("access_token");
    } else {
      const error = await response.json();
      dltText.innerHTML = `<div>${error.detail}</div>`;
    }
  });
}
