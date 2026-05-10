function digitsOnly(s) {
  return String(s || "").replace(/\D/g, "");
}

function telHrefFromPhone(phone) {
  var d = digitsOnly(phone);
  if (!d) return "";
  if (d.charAt(0) === "0" && d.length === 11) return "tel:+44" + d.slice(1);
  return "tel:" + d;
}

function formatPhoneDisplay(phone) {
  var d = digitsOnly(phone);
  if (d.length === 11 && d.charAt(0) === "0") return d.slice(0, 5) + " " + d.slice(5);
  return phone;
}

function categoryLabel(category) {
  var map = { laptop: "Laptop", keys: "Keys", wallet: "Wallet", other: "Other" };
  return map[String(category)] || category;
}

window.ItemFocusUi = {
  digitsOnly: digitsOnly,
  telHrefFromPhone: telHrefFromPhone,
  formatPhoneDisplay: formatPhoneDisplay,
  categoryLabel: categoryLabel,
};
