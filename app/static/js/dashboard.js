// app/static/js/dashboard.js

const BOOK_API_URL = '/api/v1/books';
const LOAN_API_URL = '/api/v1/loans';
// Hem accessToken hem access_token kontrolü yaparak login.js ile tam uyum sağlıyoruz
const token = localStorage.getItem('access_token') || localStorage.getItem('accessToken');
const userRole = localStorage.getItem('userRole');
const userName = localStorage.getItem('userName');

if (!token) {
    window.location.href = '/login';
}

function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` 
    };
}

document.addEventListener('DOMContentLoaded', () => {
    // Admin linkini göster/gizle
    const adminLink = document.getElementById('adminLink');
    if (adminLink && userRole === 'admin') {
        adminLink.style.display = 'inline';
    }
    
    const welcomeUser = document.getElementById('welcomeUser');
    if (welcomeUser) {
        welcomeUser.textContent = `${userName || 'Kullanıcı'} (${userRole})`;
    }
    
    // Hangi sayfadaysak ona göre başlangıç verisini yükle
    if (window.location.pathname.includes('admin-panel')) {
        loadAllUserLoans();
    } else {
        searchBooks(); // Dashboard açıldığında kitapları getir
        loadMyLoans();  // Kullanıcının kendi ödünçlerini getir
    }
});

// --- Kitap Arama ve Listeleme ---
async function searchBooks() {
    const queryInput = document.getElementById('searchQuery');
    const query = queryInput ? queryInput.value : '';
    const tableBody = document.querySelector('#bookTable tbody');
    
    if (!tableBody) return;

    tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Yükleniyor...</td></tr>';

    try {
        // API isteği
        const response = await fetch(`${BOOK_API_URL}/?q=${query}`, {
            headers: getAuthHeaders()
        });
        const data = await response.json();

        tableBody.innerHTML = ''; 

        // Veri yapısı kontrolü: Backend bazen direkt liste, bazen obje içinde liste döner
        const books = Array.isArray(data) ? data : (data.data || []);

        if (books.length > 0) {
            books.forEach(book => {
                const row = tableBody.insertRow();
                row.insertCell().textContent = book.title;
                // Yazarları birleştir
                const authorNames = Array.isArray(book.authors) ? 
                    book.authors.map(a => typeof a === 'object' ? a.name : a).join(', ') : 
                    (book.authors || '-');
                
                row.insertCell().textContent = authorNames;
                row.insertCell().textContent = book.category?.name || book.category || '-';
                row.insertCell().textContent = book.stock;
                
                const actionCell = row.insertCell();
                if (userRole === 'admin') {
                    actionCell.innerHTML = '<span class="badge bg-info">Admin Gözlemi</span>';
                } else if (book.stock > 0) {
                    const btn = document.createElement('button');
                    btn.textContent = 'Ödünç Al';
                    btn.onclick = () => borrowBook(book.id);
                    actionCell.appendChild(btn);
                } else {
                    actionCell.innerHTML = '<span style="color:red">Stok Yok</span>';
                }
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Kitap bulunamadı.</td></tr>';
        }
    } catch (error) {
        console.error('Kitap yükleme hatası:', error);
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:red;">Hata oluştu!</td></tr>';
    }
}

// --- Admin: Tüm Ödünçleri Takip Et ---
function loadAllUserLoans() {
    const tableBody = document.getElementById('adminAllLoansTable');
    if (!tableBody) return;

    fetch(`${LOAN_API_URL}/admin/all-loans`, {
        headers: getAuthHeaders()
    })
    .then(response => response.json())
    .then(data => {
        tableBody.innerHTML = '';
        const loans = Array.isArray(data) ? data : (data.data || []);

        if (loans.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Kayıt yok.</td></tr>';
            return;
        }

        loans.forEach(loan => {
            const statusStyle = loan.return_date ? 'background:#28a745' : 'background:#ffc107; color:black';
            tableBody.innerHTML += `
                <tr>
                    <td>${loan.user_email}</td>
                    <td>${loan.book_title}</td>
                    <td>${loan.loan_date}</td>
                    <td><span style="padding:2px 8px; border-radius:4px; ${statusStyle}">
                        ${loan.return_date ? 'İade Edildi' : 'Ödünçte'}
                    </span></td>
                </tr>`;
        });
    })
    .catch(err => console.error('Admin yükleme hatası:', err));
}

async function borrowBook(bookId) {
    if (userRole !== 'user') {
        alert("Sadece kullanıcılar kitap ödünç alabilir.");
        return;
    }

    try {
        // Backend /borrow rotasında parametre DEĞİL, JSON gövdesi bekliyor
        const response = await fetch(`${LOAN_API_URL}/borrow`, { 
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ book_id: bookId }) // Veriyi gövde içinde gönderiyoruz
        });

        const data = await response.json();
        
        if (response.ok) {
            alert(data.message || "Kitap başarıyla ödünç alındı!");
            searchBooks(); // Listeyi yenile
            loadMyLoans();  // Ödünçlerimi yenile
        } else {
            alert("Hata: " + (data.message || "İşlem başarısız."));
        }

    } catch (error) {
        console.error('Borrow error:', error);
        alert('Ödünç alma işlemi sırasında bir bağlantı hatası oluştu.');
    }
}

async function loadMyLoans() {
    const container = document.getElementById('activeLoansContainer');
    if (!container) return;

    try {
        const response = await fetch(`${LOAN_API_URL}/my-loans`, { 
            headers: getAuthHeaders() 
        });
        
        if (!response.ok) throw new Error('Yükleme başarısız');
        
        const result = await response.json();
        // Backend'den gelen veri "result.data" içinde
        const loans = result.data || []; 

        if (loans.length > 0) {
            let html = '<table class="u-full-width"><thead><tr><th>Kitap</th><th>Tarih</th><th>İşlem</th></tr></thead><tbody>';
            loans.forEach(loan => {
                html += `
                <tr>
                    <td>${loan.book_title}</td>
                    <td>${loan.issue_date}</td>
                    <td><button onclick="returnBook(${loan.loan_id})">İade Et</button></td>
                </tr>`;
            });
            container.innerHTML = html + '</tbody></table>';
        } else {
            container.innerHTML = '<p>Şu an aktif bir ödünç işleminiz bulunmuyor.</p>';
        }
    } catch (e) {
        container.innerHTML = '<p style="color:red">Ödünç listesi yüklenemedi.</p>';
    }
}

function logout() { localStorage.clear(); window.location.href = '/login'; }

/**
 * Kitap iade işlemini başlatır ve varsa ceza bilgisini gösterir.
 */
async function returnBook(loanId) {
    // 1. Kullanıcı onayı al
    if (!confirm('Bu kitabı iade etmek istediğinizden emin misiniz?')) return;

    try {
        // 2. Backend'deki iade rotasına POST isteği gönder
        const response = await fetch(`${LOAN_API_URL}/return/${loanId}`, {
            method: 'POST',
            headers: getAuthHeaders() // Token içeren headerlar
        });

        const data = await response.json();
        
        if (response.ok) {
            // 3. Başarı mesajını ve ceza bilgisini hazırla
            let successMessage = data.message || 'Kitap başarıyla iade edildi.';
            
            // Eğer backend'den gelen penalty (ceza) 0'dan büyükse kullanıcıyı uyar
            if (data.penalty && data.penalty > 0) {
                successMessage += `\n\n⚠️ Gecikme Bedeli: ${data.penalty} TL olarak hesaplanmıştır.`;
                successMessage += `\nDetaylı bilgi e-posta adresinize gönderildi.`;
            } else {
                successMessage += `\n✅ Kitabı zamanında iade ettiğiniz için teşekkür ederiz.`;
            }
            
            alert(successMessage);

            // 4. Arayüzü güncelle (Stokları ve aktif ödünçleri yenile)
            searchBooks(); 
            loadMyLoans(); 
            
        } else {
            // Hata durumunda (Yetki hatası, yanlış ID vb.)
            alert('Hata: ' + (data.message || 'İade işlemi gerçekleştirilemedi.'));
        }
    } catch (error) {
        console.error('İade hatası:', error);
        alert('Sunucuyla bağlantı kurulurken bir hata oluştu.');
    }
}