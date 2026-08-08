import textwrap
from datetime import datetime
import urllib.parse
from PIL import Image, ImageDraw
import streamlit as st

# ==========================================
# 1. دالة توليد الإعلان التسويقي
# ==========================================
def generate_marketing_ad(image1_path, image2_path, sector, city):
    """Génère un Collage 2160x1080 + Message WhatsApp en Français"""
    try:
        img1 = Image.open(image1_path).resize((1080, 1080)) # Bien Immobilier
        img2 = Image.open(image2_path).resize((1080, 1080)) # Fleurs/Nature
    except: return None, "Veuillez télécharger les 2 images d'abord"

    # Création du Collage "Contraste & Luxe"
    collage = Image.new('RGB', (2160, 1080))
    collage.paste(img1, (0, 0))
    collage.paste(img2, (1080, 0))
    
    draw = ImageDraw.Draw(collage)
    
    # Texte sur l'image
    ad_text_on_image = textwrap.fill(
        f"Au cœur de {city}, nous allions la beauté de la nature à "
        f"l'élégance du design moderne. Le Bureau Tassaout Digital vous propose "
        f"des opportunités d'investissement en {sector} alliant luxe et authenticité.", width=45
    )
    
    draw.rectangle([(50, 750), (2110, 1030)], fill=(0,0,0,180)) # Fond transparent
    draw.text((100, 780), ad_text_on_image, fill="white") 
    draw.text((100, 980), "📱 Contact: +212 691 897 126", fill="#FFD700") # Or
    draw.text((100, 700), "👑 BUREAU TASSAOUT DIGITAL | IMMOBILIER & AFFAIRES", fill="#FFD700")

    # Sauvegarde
    ad_path = f"AD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    collage.save(ad_path, quality=95)
    
    # Message WhatsApp Officiel en Français
    whatsapp_msg = f"""--- 👑 BUREAU TASSAOUT DIGITAL | IMMOBILIER & AFFAIRES À EL KELAA DES SRAGHNA 👑 ---
[ TASSAOUT OMEGA PREMIUM - 100MP PRO-GRADE ]

Secteur: {sector} | Ville: {city}
Style Visuel: Mode Bright
    
📢 ANNONCE PROMOTIONNELLE:
Ces deux images peuvent être utilisées de manière créative pour créer du matériel marketing unique pour le bureau "Tassaout Digital" à {city}. L'idée est de combiner la modernité du {sector} et l'élégance intemporelle pour positionner le bureau comme une destination offrant le meilleur des deux mondes.

Caméra tassaout omega go
    
📸 DOCUMENTATION VISUELLE:
- Traitement: 100MP Super-Résolution
- Équilibre Visuel: Mode Bright Optimisé

✒️ Signature Officielle: Ameur signature
⚡ Système TASSAOUT OMEGA OS"""

    return ad_path, whatsapp_msg

# ==========================================
# 2. تعريف الألسنة (Tabs) والواجهة
# ==========================================
# تأكد من دمج هذه الألسنة مع الألسنة الموجودة لديك في المشروع
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 التصوير أو تحميل الصور", 
    "🧠 عروض الوكيل والتفاعل", 
    "📦 الأرشيف",
    "🎨 Centre de Création Publicitaire"
])

with tab4:
    st.subheader("🎨 Centre de Création Publicitaire - Contraste & Luxe")
    st.write("Téléchargez deux images : Propriété immobilière + Nature/Fleurs")

    col1, col2 = st.columns(2)
    with col1: 
        ad_img1 = st.file_uploader("📷 1. Propriété / Immeuble", type=["jpg", "png"], key="ad1")
    with col2: 
        ad_img2 = st.file_uploader("🌹 2. Fleurs / Nature", type=["jpg", "png"], key="ad2")

    # تحديد القوائم الافتراضية للقطاعات والمدن (تأكد من توافقها مع ملفك)
    sectors_list = ["عقار سكني وتجاري", "أراضي فلاحية", "شقق للكراء"]
    cities_list = ["قلعة السراغنة", "مراكش"]

    ad_sector = st.selectbox("Secteur de l'annonce:", sectors_list, key="ad_sec")
    ad_city = st.selectbox("Ville:", cities_list, key="ad_city")

    if st.button("🚀 Générer l'Annonce Professionnelle", type="primary"):
        if ad_img1 and ad_img2:
            ad_path, ad_message = generate_marketing_ad(ad_img1, ad_img2, ad_sector, ad_city)
            
            if ad_path:
                st.image(ad_path, caption="Annonce prête à être publiée", use_container_width=True)
                st.success("✅ Annonce générée avec succès via TASSAOUT OMEGA OS !")
                
                st.code(ad_message, language="markdown")
                
                whatsapp_url = f"https://wa.me/212691897126?text={urllib.parse.quote(ad_message)}"
                st.link_button("📱 Partager l'annonce sur WhatsApp", whatsapp_url)
            else:
                st.error(ad_message)
        else:
            st.error("Veuillez télécharger les deux images.")
