# IcaeWelfareZones Classifier

**IcaeWelfareZones** is a community-facing geolocation tool that classifies any address in Edmonton into one of seven welfare coordination zones based on major road boundaries. The platform is designed to support localized outreach, service delivery, and case assignments under the *Onye Mara Nwanne Ya* initiative.

---

## 🌐 Live Demo

> Coming soon: [https://icaewelfarezones.streamlit.app](https://icaewelfarezones.streamlit.app)

---

## 🗺 Zone Classification Logic

| Zone Name              | Road Boundaries                                               |
|------------------------|---------------------------------------------------------------|
| **Oguta Lake Zone**    | North of Yellowhead Trail, West of 97 Street                 |
| **Nkwu Zone**          | North of Yellowhead Trail, East of 97 Street                 |
| **Omambala Zone**      | Between Yellowhead & Whitemud, West of 170 Street            |
| **Ogene Zone**         | Between Yellowhead & Whitemud, between 170 Street & 75 Street|
| **Ogbunike Cave Zone** | Between Yellowhead & Whitemud, East of 75 Street             |
| **Ichaka Zone**        | South of Whitemud, West of Gateway Boulevard                 |
| **Orji Zone**          | South of Whitemud, East of Gateway Boulevard                 |

---

## 🔧 How It Works

1. User enters a valid Edmonton address.
2. Common abbreviations (e.g., `St`, `Rd`) are automatically standardized.
3. The app geocodes the address using the [OpenCage Data API](https://opencagedata.com/).
4. Based on latitude and longitude, it classifies the address into the correct Welfare Zone.
5. Results include:
   - ✅ Cleaned Location
   - ✅ Boundary logic
   - ✅ **Welfare Zone** (bolded in a success callout)

---

## 🧩 Tech Stack

- [Streamlit](https://streamlit.io) – UI Framework
- [OpenCage Geocoder](https://opencagedata.com/) – Address resolution
- Python 3.10+

---

## 📦 Installation & Run Locally

```bash
git clone https://github.com/YOUR-USERNAME/icae-welfare-zones.git
cd icae-welfare-zones
pip install -r requirements.txt
streamlit run app.py
