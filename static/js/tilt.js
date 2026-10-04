// Subtle "reactive" hover tilt for cards and buttons — moves gently toward
// the cursor angle, then eases back on mouse-leave. Pure CSS transforms,
// no external library, and safe on touch devices (mouse-only events).
document.addEventListener("DOMContentLoaded", function () {
  const tiltEls = document.querySelectorAll(".tilt-card, .tilt-btn, .card, .btn, .stat-card");

  tiltEls.forEach((el) => {
    el.addEventListener("mousemove", (e) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -4; // max ~4deg
      const rotateY = ((x - centerX) / centerX) * 4;
      el.style.transform = `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)`;
    });
    el.addEventListener("mouseleave", () => {
      el.style.transform = "";
    });
  });
});
