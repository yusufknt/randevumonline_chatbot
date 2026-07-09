## SIP Trunk Özelliği ile Gelen Çağrıların Sunucunuza Yönlendirilmesi

Kurumsal iletişim altyapısında **SIP Trunk** teknolojisi, işletmelerin telefon trafiğini IP tabanlı sistemler üzerinden yönetmesini sağlar.

Netgsm altyapısıyla sunulan SIP Trunk Özelliği sayesinde, firmanızın numarasına gelen çağrı istekleri, belirleyeceğiniz IP adresine veya domain (alan adı) adresine SIP protokolü aracılığıyla yönlendirilebilir.

Bu yönlendirme sırasında, **Arayan** ve **Aranan Prefix** ayarları sayesinde, çağrıyı başlatan numara ile çağrıyı alan abone numaranız, belirttiğiniz IP adresindeki sunucuya **seçtiğiniz ön eklerle birlikte** iletilebilir.

---

### SIP Trunk Nedir?

**SIP Trunk (Session Initiation Protocol Trunk)**, IP tabanlı ses haberleşmesinde santral (PBX) ile operatör arasında sanal bir hat (trunk) oluşturur.  
Bu yapı sayesinde gelen ve giden çağrılar internet protokolü üzerinden yönetilir, fiziksel hat veya kablo bağlantısına ihtiyaç kalmaz.

---

### SIP Trunk Yönlendirme Ayarları Nasıl Yapılır?

SIP Trunk hizmetini aktif etmek için Netgsm Web Portal’a kullanıcı bilgilerinizle giriş yapın. Ardından **Ses Hizmeti > Ayarlar > SIP Bilgileri** bölümüne giderek **SIP Trunk** özelliğini etkinleştirmelisiniz.

![1760103077110-55cc799af13b4fd608789d88.png](https://dosyaindir.netgsm.com.tr/download?p=639063fda30de268e38f93f3d607f1b22ba8ab45ec7ebaeed19f4fa0729bdfc4a3be033fefcfa2d92bcfc167a23e8eea6b8d304969ca8a1ad0a3351db2c90e83938e0c70700073decd24ca354882ae07cc18e23fd957f04d6e6f7a8d624dbe73cd0b0c8e6c93c8722c5539ee0b4875b88f1ba80176711e589ca909b2d2e6cd8f%3A%3A622acf7c9ccf9f7eb9bee7ae76cf029d&h=6f734dd28d4e4a637780da4e4992e42c3641edae6721c629dea76d5b153ccacc&v=990d1e4068faa71e23d16442a123c542%3A%3Abbca1bba3ebc82491ccf4cab5c77885d)

- **IP:** Çağrıların yönlendirileceği santral veya sunucunun IP adresi
- **Port:** Genellikle 5060 veya operatörün belirttiği özel port
- **Prefix Ayarları:** Arayan ve aranan numaralarda ülke veya operatör kodlarını yöneterek sunucunuza hangi şekilde gönderilmesini istiyorsanız seçim sağlayabilirsiniz.

Bu ayarların ardından “ **SIP Trunk Ayarlarını Kaydet** ” butonu ile yapılandırma aktif hale gelir.

![1760103105918-890db3473110719af0eb9c3c.png](https://dosyaindir.netgsm.com.tr/download?p=1b495c99549bec2b6c19623493811499d8f667fb786d8f37d80c6f8ae6e580e306e5e37bf10a5ac92271096bcb11d61a7387ea8e9a81e184161c0f4e247f2d8ce8620f1ca1a7150977565bdac0140b2dd64fde36c36fa735edb73b05b698d534f026e615a31817b340b176c98f98a748b0339be077150ad331aeb22084492fb4%3A%3Ab4f57beaf7d3ca597777fc34656b10bc&h=e6a444ce965d3f71a971c6c8136c7831837ae1cac39b4c717f85459408530668&v=c43050c6869b968145f492ca70640402%3A%3Af9958dddfc8e00d4437ff55bf98329cf)

Görseldeki örnekte olduğu gibi:

- **Arayan Prefix:** 0 (Default) olarak belirlenmiş böylece arayan numara sunucunuza 0532XXXXXXX şeklinde iletilecektir.
- **Aranan Prefix:** +90 olarak belirlenmiş böylece aranan numara sunucunuza +90312XXXXXXX şeklinde iletilecektir.

Prefix ayarları ardından **“Prefix Ayarlarını Kaydet”** butonu ile yapılan işlem kaydedilmelidir.