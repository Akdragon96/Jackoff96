const loginTab = document.querySelector("#loginTab");
const registerTab = document.querySelector("#registerTab");
const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");
const statusBox = document.querySelector("#status");
const accountBox = document.querySelector("#account");
const accountName = document.querySelector("#accountName");
const accountEmail = document.querySelector("#accountEmail");
const logoutButton = document.querySelector("#logoutButton");

function setActiveForm(formName) {
  const isLogin = formName === "login";
  loginTab.classList.toggle("active", isLogin);
  registerTab.classList.toggle("active", !isLogin);
  loginTab.setAttribute("aria-selected", String(isLogin));
  registerTab.setAttribute("aria-selected", String(!isLogin));
  loginForm.classList.toggle("active", isLogin);
  registerForm.classList.toggle("active", !isLogin);
  clearStatus();
}

function showStatus(message, type = "success") {
  statusBox.textContent = message;
  statusBox.className = `status show ${type}`;
}

function clearStatus() {
  statusBox.textContent = "";
  statusBox.className = "status";
}

function setAccount(user) {
  accountBox.hidden = !user;
  if (!user) {
    accountName.textContent = "";
    accountEmail.textContent = "";
    return;
  }

  accountName.textContent = user.username;
  accountEmail.textContent = user.email;
}

async function sendJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong.");
  }

  return data;
}

loginTab.addEventListener("click", () => setActiveForm("login"));
registerTab.addEventListener("click", () => setActiveForm("register"));

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearStatus();

  const formData = new FormData(loginForm);
  try {
    const data = await sendJson("/api/login", {
      identifier: formData.get("identifier"),
      password: formData.get("password"),
    });
    setAccount(data.user);
    loginForm.reset();
    showStatus(`Welcome back, ${data.user.username}.`);
  } catch (error) {
    showStatus(error.message, "error");
  }
});

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearStatus();

  const formData = new FormData(registerForm);
  try {
    const data = await sendJson("/api/register", {
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
    });
    setAccount(data.user);
    registerForm.reset();
    showStatus(`Account created for ${data.user.username}.`);
  } catch (error) {
    showStatus(error.message, "error");
  }
});

logoutButton.addEventListener("click", async () => {
  await sendJson("/api/logout", {});
  setAccount(null);
  showStatus("You have been logged out.");
});

async function restoreSession() {
  const response = await fetch("/api/me");
  const data = await response.json();
  if (data.authenticated) {
    setAccount(data.user);
  }
}

restoreSession();
