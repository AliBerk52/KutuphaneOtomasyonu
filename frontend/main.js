// Genel olarak tüm sayfalarda kullanılabilecek ortak işlemler ve yardımcı fonksiyonlar burada tanımlanabilir.

function showMsg(msg, isOk = true) {
  // msg: gösterilecek mesaj veya element id'si
  // isOk: true -> başarılı mesaj, false -> hata
  let el;
  if (typeof msg === "string" && document.getElementById("msg")) {
    // Direkt bir element varsa onu kullanalım
    el = document.getElementById("msg");
    el.style.display = "block";
    el.textContent = msg;
    el.className = isOk ? "msg-ok" : "msg-error";
    if (msg.length > 0) {
      setTimeout(() => { el.style.display = "none"; }, 3500);
    }
  } else if (typeof msg === "string" && !document.getElementById("msg")) {
    // Element yoksa alert ile göster
    if (msg.length > 0) alert(msg);
  }
}

async function fetchMe() {
  // Kullanıcı (me) bilgisini çek ve localStorage'a kaydet
  try {
    const resp = await fetch('/api/me');
    if (resp.ok) {
      const me = await resp.json();
      localStorage.setItem('me', JSON.stringify(me));
      return me;
    } else {
      localStorage.removeItem('me');
      return null;
    }
  } catch (e) {
    localStorage.removeItem('me');
    return null;
  }
}

// Login durumunu kontrol eden fonksiyon. Gerekirse login sayfasına yönlendirir.
async function ensureAuth(redirectUrl = "/login.html") {
  const me = await fetchMe();
  if (!me) {
    window.location.href = redirectUrl;
    return false;
  }
  return true;
}

// Logout işlemi
async function logout() {
  try {
    await fetch('/api/logout', { method: "POST" });
  } catch (e) {}
  localStorage.removeItem('me');
  window.location.href = '/login.html';
}

// Kullanıcı nesnesini localStorage'dan alma fonksiyonu
function getMe() {
  try {
    const me = localStorage.getItem('me');
    return me ? JSON.parse(me) : null;
  } catch (e) {
    return null;
  }
}

