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

function finderQrImageUrl(finderUrl) {
  return (
    "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data=" + encodeURIComponent(String(finderUrl || ""))
  );
}

var ADMIN_TOKEN_KEY = "itemfocus_admin_token";

window.ItemFocusUi = {
  digitsOnly: digitsOnly,
  telHrefFromPhone: telHrefFromPhone,
  formatPhoneDisplay: formatPhoneDisplay,
  categoryLabel: categoryLabel,
  finderQrImageUrl: finderQrImageUrl,
};

window.ItemFocusAdmin = {
  tokenKey: ADMIN_TOKEN_KEY,
  getToken: function () {
    return sessionStorage.getItem(ADMIN_TOKEN_KEY);
  },
  setToken: function (t) {
    sessionStorage.setItem(ADMIN_TOKEN_KEY, t);
  },
  clearToken: function () {
    sessionStorage.removeItem(ADMIN_TOKEN_KEY);
  },
  authHeaders: function () {
    var t = sessionStorage.getItem(ADMIN_TOKEN_KEY);
    var h = { "Content-Type": "application/json" };
    if (t) h.Authorization = "Bearer " + t;
    return h;
  },
};
