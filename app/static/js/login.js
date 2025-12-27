// app/static/js/login.js

const API_BASE_URL = '/api/v1/auth';

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const messageElement = document.getElementById('message');
    
    // Mesaj alanını temizle ve göster
    messageElement.textContent = 'Giriş yapılıyor...';
    messageElement.style.display = 'block';
    messageElement.classList.remove('success', 'error');

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Giriş başarılı: JWT Token ve Rol bilgisini Local Storage'a kaydet
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('userRole', data.role);
            localStorage.setItem('userName', email); // Kullanıcı adını da saklayabiliriz
            
            messageElement.classList.add('success');
            messageElement.textContent = 'Giriş başarılı! Yönlendiriliyorsunuz...';

            // Başarılı girişten sonra kullanıcıyı dashboard'a yönlendir
            setTimeout(() => {
                window.location.href = '/dashboard'; 
            }, 1000);
            
        } else {
            messageElement.classList.add('error');
            messageElement.textContent = data.message || 'Giriş başarısız oldu.';
        }
    } catch (error) {
        messageElement.classList.add('error');
        messageElement.textContent = 'Bağlantı hatası oluştu.';
        console.error('Login error:', error);
    }
});