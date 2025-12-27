document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.");
            window.location.href = '/login';
        } else {
            alert(data.message || "Kayıt hatası!");
        }
    } catch (err) { console.error("Hata:", err); }
});