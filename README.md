# 🌿 WildBg (DivotoBg)

A community-driven web application built with **Python & Django** that enables users to discover, share, and plan visits to **natural, archaeological, and architectural landmarks in Bulgaria**.

> ⚠️ Note: The initial load of the site may take 1–2 minutes because it’s hosted on Render’s free plan.

<p align="center">
  <a href="https://wild-bg.onrender.com/"><strong><ion-icon name="enter-outline"></ion-icon>Live Demo</strong></a>
</p>


## 📌 Overview

**WildBg (DivotoBg)** is a platform designed for travelers, explorers, and nature enthusiasts. It combines social media functionality with travel planning tools, allowing users to discover new destinations and share their experiences.

The application helps users:
- Explore interesting places across Bulgaria  
- Learn from community-generated content  
- Plan future visits efficiently  

Homepage view
<img width="1788" height="1365" alt="wildbg_homepage" src="https://github.com/user-attachments/assets/642d3711-f1fa-4cb2-ae0f-d136c1a68616" />


## 🚀 Features

### 👤 Authentication
- Register and log in using **username or email**
- Secure authentication system
- Registration view

<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/69c94e8a-c79a-4a7c-a211-dbf673ad1b8d" />

### 👀 Guest Access
- Browse all public content  
- View posts and landmarks  
- Use search functionality  

### 🔐 Logged-in Users
- 📝 Create posts with images  
- 💬 Comment on posts  
- 🗺️ Add new landmarks  
- 🧑 Manage personal profiles  
- 🏷️ Categorize landmarks (natural, archaeological, architectural)  

### 🧩 Core Concepts
- User-generated content – Users create and share places
- Exploration-focused – Discover new and interesting destinations
- Trip planning – Organize visits to landmarks
- Interactive experience – Feed, comments, maps, and profiles

---

### 📝 Post Structure

Each post in the application contains the following elements:

- 🖼️ **Image** – Visual representation of the location  
- 👤 **Author** – The user who created the post  
- 📍 **Location** – The landmark or place associated with the post  
- ⏱️ **Time** – Date and time of publishing  
- 📄 **Description** – Detailed information about the place or experience  

### 💬 Interaction Features

- 💬 **Comments** – Users can discuss and share opinions  
- ❤️ **Like Button** – Express appreciation for the post  
- 🔗 **Share Button** – Share the post with others  


<img width="682" height="938" alt="image" src="https://github.com/user-attachments/assets/521f6f57-ec55-495d-9c7b-3cd64245284e" />

---

### 🗺️ Landmark (Object) Structure

Each landmark in the application includes detailed information to help users explore and plan visits:

- 📛 **Name** – The name of the landmark  
- 📍 **Region** – Geographic area or region in Bulgaria  
- 🖼️ **Image** – Main photo representing the place  
- ⭐ **Rating** – User-based rating system  
- 📄 **Description** – General description of the landmark  
- ℹ️ **Additional Info** – Details about the location or route (e.g. difficulty, accessibility, tips)  
- 🌍 **Location (Map)** – Integrated Google Maps view for navigation  

### 🔘 Interaction Features

- ❤️ **Like Button** – Mark the place as liked  
- ✅ **Visited Button** – Mark the place as visited  
- 🔗 **Share Button** – Share the landmark  
- ✍️ **Add Review** – Write a review about the experience  
- 💬 **Comment Section** – Users can leave comments and discuss  

<img width="600" height="1400" alt="image (2)crop" src="https://github.com/user-attachments/assets/716fe6fc-0033-490b-b5bf-85fe392d879c" />

## ⭐ Top Locations Sidebar

The left sidebar highlights the **Top 3 Most Liked Landmarks** in the platform.

### 📊 Features

- 🥇 Displays the **top 3 locations based on user likes**
- 🔄 Updates dynamically based on user activity  
- 🖼️ Includes preview (image + name) of each location  
- 🚀 Quick access to the most popular places  

This section helps users quickly discover trending and highly recommended destinations.

<img width="300" height="540" alt="image (1)" src="https://github.com/user-attachments/assets/5a148617-d69c-4238-9244-63f468178a9d" />

---

## 🔍 Discovery & Navigation
- **Social Feed** – Browse content like a social media platform  
- **Search System** – Find landmarks quickly  
- **Categories & Tags** – Filter and explore places  
- **Map Integration** – View locations and plan visits  

## 🏗️ Tech Stack

- **Backend:** Python, Django  
- **Database:** PostgreSQL (Supabase)  
- **Hosting:** Render  
- **Frontend:** Django Templates (HTML, CSS)  
- **Maps:** Leaflet / Google Maps  

## 🎯 Future Improvements
- ❤️ Like / Favorite system
- 📍 Save places for later
- 🧭 Advanced trip planner
- 🔔 Notifications system
- 📱 Mobile optimization


##💡 About
- WildBg (DivotoBg) is inspired by the idea of making Bulgaria’s hidden beauty more accessible through technology and community sharing.
