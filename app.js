// Nav scroll effect
const nav = document.getElementById("nav");
window.addEventListener("scroll", () => {
  nav.classList.toggle("scrolled", window.scrollY > 40);
});

// Subscribe form
const form = document.getElementById("subscribe-form");
const msg = document.getElementById("form-message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  msg.className = "form-message";
  msg.style.display = "none";

  const btn = form.querySelector("button[type=submit]");
  btn.disabled = true;
  btn.textContent = "Joining...";

  try {
    const res = await fetch("https://formspree.io/f/xeepgoqg", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        interest: form.interest.value,
      }),
    });

    if (res.ok) {
      msg.className = "form-message success";
      msg.textContent = "Welcome to the Stars&Bears community!";
      msg.style.display = "block";
      form.reset();
    } else {
      const data = await res.json();
      msg.className = "form-message error";
      msg.textContent = (data.errors && data.errors.map(e => e.message).join(", ")) || "Something went wrong. Please try again.";
      msg.style.display = "block";
    }
  } catch {
    msg.className = "form-message error";
    msg.textContent = "Network error. Please check your connection and try again.";
    msg.style.display = "block";
  } finally {
    btn.disabled = false;
    btn.textContent = "Join the Community";
  }
});

// Smooth reveal on scroll
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll(".section").forEach((section) => {
  section.style.opacity = "0";
  section.style.transform = "translateY(30px)";
  section.style.transition = "opacity 0.7s ease, transform 0.7s ease";
  observer.observe(section);
});
