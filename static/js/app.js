// Dismiss feedback after a short pause; Bootstrap still owns the alert behavior.
document.querySelectorAll("[data-auto-dismiss]").forEach((alert) => {
  window.setTimeout(() => {
    bootstrap.Alert.getOrCreateInstance(alert).close();
  }, 5000);
});