<!-- القائمة المنسدلة للبوابات والقطاعات -->
<div style="text-align: center; margin: 15px 0;">
    <select id="categoryFilter" onchange="filterListings()" style="width: 95%; max-width: 500px; padding: 14px; border-radius: 8px; background-color: #062314; color: #4ade80; border: 2px solid #22c55e; font-size: 16px; font-weight: bold; outline: none; cursor: pointer;">
        <option value="all">جميع القطاعات</option>
        <option value="العقاري الفلاحي">العقاري الفلاحي</option>
        <option value="العقاري الصناعي والتجاري">العقاري الصناعي والتجاري</option>
        <option value="العقاري المهني">العقاري المهني</option>
        <option value="العقاري الاستثماري">العقاري الاستثماري</option>
        <option value="بيع مواد البناء">بيع مواد البناء</option>
        <option value="مكتب الدراسات والاستثمار والهندسة الصناعية والميكانيكية">مكتب الدراسات والاستثمار والهندسة الصناعية والميكانيكية</option>
        <option value="الهندسة الرقمية والتصوير الفوتوغرافي الاحترافي">الهندسة الرقمية والتصوير الفوتوغرافي الاحترافي</option>
        <option value="التسويق العقاري والتجاري">التسويق العقاري والتجاري</option>
    </select>
</div>

<!-- حاوية عرض البطاقات -->
<div id="listingsContainer" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; padding: 20px;"></div>

<script>
// قاعدة البيانات بصيغة JSON
const listingsData = {
  "listings": [
    {
      "id": "prop-001",
      "title": "أرض فلاحية خصبة ومجهزة للبيع",
      "category": "العقاري الفلاحي",
      "location": "قلعة السراغنة",
      "price": "1,200,000 DH",
      "area": "5 هكتارات",
      "image": "https://via.placeholder.com/400x250?text=Agri+Land",
      "description": "أرض فلاحية ممتازة تحتوي على بئر مجهز بالسقي الموضعي ومربوطة بالكهرباء."
    },
    {
      "id": "prop-002",
      "title": "محل تجاري بموقع استراتيجي للبيع أو الكراء",
      "category": "العقاري الصناعي والتجاري",
      "location": "مراكش - وسط المدينة",
      "price": "850,000 DH",
      "area": "120 م²",
      "image": "https://via.placeholder.com/400x250?text=Commercial+Store",
      "description": "محل تجاري بأسقف عالية وواجهة واسعة مناسب لجميع الأنشطة التجارية والصناعية الخفيفة."
    },
    {
      "id": "prop-003",
      "title": "مكتب إداري مجهز بالكامل للشركات",
      "category": "العقاري المهني",
      "location": "مراكش - جليز",
      "price": "6,500 DH / شهرياً",
      "area": "75 م²",
      "image": "https://via.placeholder.com/400x250?text=Office+Space",
      "description": "مكتب عصري في عمارة إدارية راقية، مناسب للمهن الحرة، المحامين، والشركات الرقمية."
    },
    {
      "id": "prop-004",
      "title": "بقعة أرضية مخصصة لبناء مجمع استثماري",
      "category": "العقاري الاستثماري",
      "location": "قلعة السراغنة - المنطقة الحضارية",
      "price": "3,500,000 DH",
      "area": "1,500 م²",
      "image": "https://via.placeholder.com/400x250?text=Investment+Plot",
      "description": "مشروع عقاري استثماري ذو عائد ممتاز مخصص لبناء العمارات التجارية والرافعات الاستثمارية."
    },
    {
      "id": "prop-005",
      "title": "توريد مواد البناء بالجملة والتقسيط",
      "category": "بيع مواد البناء",
      "location": "جهة مراكش آسفي",
      "price": "حسب الطلب",
      "area": "توصيل مباشر",
      "image": "https://via.placeholder.com/400x250?text=Building+Materials",
      "description": "توفير كافة مواد البناء الأساسية (الإسمنت، الحديد، الرمل، الياجور) بأسعار تنافسية وتوصيل مباشر."
    },
    {
      "id": "prop-006",
      "title": "دراسات الجدوى والهندسة الصناعية والميكانيكية",
      "category": "مكتب الدراسات والاستثمار والهندسة الصناعية والميكانيكية",
      "location": "المغرب",
      "price": "استشارة مجانية",
      "area": "خدمات هندسية",
      "image": "https://via.placeholder.com/400x250?text=Engineering+Office",
      "description": "تقديم استشارات استثمارية، إعداد دفاتر التحملات، والدراسات التقنية والميكانيكية للمشاريع."
    },
    {
      "id": "prop-007",
      "title": "خدمات التصوير الجوي والافتراضي والعلامات الرقمية",
      "category": "الهندسة الرقمية والتصوير الفوتوغرافي الاحترافي",
      "location": "مراكش / قلعة السراغنة",
      "price": "حسب الباقة",
      "area": "جودة 4K",
      "image": "https://via.placeholder.com/400x250?text=Digital+Media",
      "description": "تصوير العقارات بجودة عالية وإنتاج مجسمات 3D وجولات افتراضية للتسويق المتقدم."
    },
    {
      "id": "prop-008",
      "title": "حملة تسويق عقاري وتجاري متكاملة",
      "category": "التسويق العقاري والتجاري",
      "location": "شامل",
      "price": "حسب الاتفاق",
      "area": "تغطية رقمية",
      "image": "https://via.placeholder.com/400x250?text=Real+Estate+Marketing",
      "description": "إدارة الحملات الإعلانية المستهدفة للمشاريع العقارية والمحلات التجارية لضمان أفضل نسبة مبيعات."
    }
  ]
};

// دالة عرض البطاقات في الصفحة
function renderListings(items) {
    const container = document.getElementById("listingsContainer");
    container.innerHTML = "";

    items.forEach(item => {
        const card = document.createElement("div");
        card.className = "prop-card";
        card.setAttribute("data-category", item.category);
        card.style.cssText = "border: 1px solid #22c55e; background-color: #062314; color: #fff; border-radius: 12px; width: 300px; padding: 15px; margin: 10px; box-sizing: border-box;";

        card.innerHTML = `
            <img src="${item.image}" alt="${item.title}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; object-fit: cover; height: 160px;">
            <span style="background: #22c55e; color: #000; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-bottom: 5px;">${item.category}</span>
            <h3 style="color: #4ade80; font-size: 18px; margin: 5px 0 10px 0;">${item.title}</h3>
            <p style="font-size: 14px; color: #ccc; margin: 5px 0;">📍 ${item.location} | 📐 ${item.area}</p>
            <p style="font-size: 13px; color: #aaa; margin: 5px 0 10px 0;">${item.description}</p>
            <div style="font-size: 16px; font-weight: bold; color: #4ade80; border-top: 1px solid #14532d; padding-top: 8px; margin-top: 8px;">${item.price}</div>
        `;
        container.appendChild(card);
    });
}

// دالة الفلترة عند تغيير الاختيار من القائمة المنسدلة
function filterListings() {
    var selectElement = document.getElementById("categoryFilter");
    var selectedValue = selectElement.value;
    var cards = document.querySelectorAll(".prop-card");
    
    cards.forEach(function(card) {
        var cardCategory = card.getAttribute("data-category");
        if (selectedValue === "all" || cardCategory === selectedValue) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// تشغيل العرض التلقائي عند تحميل الصفحة
window.onload = function() {
    renderListings(listingsData.listings);
};
</script>
