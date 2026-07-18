# 📝 Bluestock Fintech - Sprint 4 Engineering Retrospective

Is document mein Sprint 4 ke dauran liye gaye important design decisions, data handling rules aur performance testing ke results ko document kiya gaya hai.

---

## 🎨 1. UX / UI Decisions (Design Layout)

* **Wide-Screen Layout Standard:** Dashboard par heavy tables aur complex Plotly graphs (jaise 4D Bubble chart aur Treemap) ko acche se fit karne ke liye humne Streamlit mein default rendering ko wide-screen par set kiya. Isse charts page ke baahar overflow nahi hote aur responsive rehte hain.
* **Proactive Feedback Indicators:** User experience ko behtar banane ke liye humne blank pages ya system crash hone ki jagah custom red alert text elements lagaye hain. Jaise:
  * Jab user galat ticker daalta hai: `Ticker not found – please try another` ka error popup aata hai.
  * Jab annual report ka server link 404 response deta hai: Link ki jagah `Report unavailable` ka red badge dikhta hai.
* **Sidebar Optimization:** Filter controls (year dropdown aur 10 metric sliders) ko sidebar mein freeze kiya gaya hai taaki main layout par content badalne par bhi filter controls hamesha access ho sakein.

---

## 🐛 2. Data Edge Cases Discovered & Solved (Data Fault Tolerance)

* **Null/NaN Value Injection:** Data analysis ke dauran pata chala ki kuch companies ke liye data loading pipelines mein `None` ya `NaN` (Not a Number) values aa rahi thi, jisse tables aur text screens crash ho rahe the. 
  * **Solution:** Humne ek central logic add kiya jo aisi kisi bhi khali/null value ko automatic trace karke UI frontend par `N/A` text string mein convert kar deta hai, jisse crash zero ho gaye.
* **Partial History Listings:** Kuch companies aisi thin jinhe market mein list huye 10 saal se kam ka samay hua hai (fewer than 10 years of data). Unke financial matrices ko plot karne par line charts toot rahe the.
  * **Solution:** Dashboard ko update kiya gaya ki jitne bhi saal ka data available ho (jaise 3 ya 5 saal), chart sirf utne hi periods ko smoothly map kare aur bache huye saalon ke liye clear note user ko dikhaye.

---

## ⚡ 3. Performance Findings & Load Testing (Latency Benchmarks)

* **Caching Layer Architecture:** Dashboard mein multiple data-heavy screens hain, jiske wajah se database se baar-baar call hone par page laggy ho raha tha. Isko bypass karne ke liye humne shared data loader par `@st.cache_data(ttl=600)` ka use kiya.
* **Under 3-Second Rule:** 10-minute caching lagane ke baad, humne test suite ke jariye 5 high-volume core tickers par load speed test chalaya.
  * **Result:** Saare profile screens ka data retrieval aur financial graph rendering pipeline **3 seconds ke andar (under 3.0 seconds maximum target threshold)** complete ho gaya, jo system loading benchmark ko satisfy karta hai.