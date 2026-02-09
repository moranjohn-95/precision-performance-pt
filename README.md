# precision-performance-pt
Precision performance PT provide both online and in person personal training, as well as group classes. Precisison Performance also provide dashbaord access to personal training clients where by joiners will have a 24/7 access to a number of resources including trainer supprot, body metrics tracking as well as strength tracking.

## Table of Contents

1. [Project Overview](#1-project-overview)  
2. [Project Aims](#2-project-aims)  
3. [User Goals](#3-user-goals)  
4. [Site Owner Goals](#4-site-owner-goals)  
5. [Target Audience](#5-target-audience)  
6. [User Experience (UX)](#6-user-experience-ux)  
7. [User Stories](#7-user-stories)  
8. [Design](#8-design)  
   - [Colour Scheme](#81-colour-scheme)  
   - [Typography](#82-typography)  
   - [Wireframes](#desktop-wireframes)  
   - [Responsive Design](#84-responsive-design)  
9. [Features](#9-features)  
   - [Features & User Journeys](#features--user-journeys)  
10. [Application Flow & Logic](#10-application-flow--logic)  
11. [Database & Data Models](#11-database--data-models)  
12. [Authentication & Authorisation](#12-authentication--authorisation)  
13. [Role-Based Access Control](#13-role-based-access-control)  
14. [Security Features](#14-security-features)  
15. [Validation & Error Handling](#15-validation--error-handling)  
16. [Technologies Used](#16-technologies-used)  
17. [Testing](#17-testing)  
   - [Automated Testing](#171-automated-testing)  
   - [Manual Testing](#172-manual-testing)  
   - [Validator & Accessibility Testing](#173-validator--accessibility-testing)  
   - [User Story Testing](#174-user-story-testing)  
18. [Bugs & Fixes](#18-bugs--fixes)  
19. [Deployment](#19-deployment)  
   - [Heroku Deployment](#191-heroku-deployment)  
   - [Local Deployment](#192-local-deployment)  
   - [How to Fork](#193-how-to-fork-the-repository)  
   - [How to Clone](#194-how-to-clone-the-repository)  
20. [Future Features](#20-future-features)  
21. [Credits](#21-credits)  
22. [Acknowledgements](#22-acknowledgements)

## 1. Project Overview
Precision Performance PT is a full stack web application designed to support online and in person personal training businesses. The platform allows clients, trainers, and the business owner to manage training programmes, track progress, and communicate through a single, centralised system.
The application replaces fragmented tools such as spreadsheets, messaging apps, and manual notes by providing structured dashboards for each user role. Clients can view their workout plans, log completed sessions, track body metrics, and contact their trainer directly. Trainers can manage assigned clients, tailor workout programmes, and review client progress. The owner has full visibility across the business and can assign consultations, oversee trainers, and manage clients.
The project was built using Django as the backend framework, with HTML, CSS, and JavaScript used for the front end. Role based permisions ensure that each user only has access to appropriate data and features. The application is fully responsive and designed to work across desktop, tablet, and mobile devices.

Precision Performance PT was developed as a Portfolio Project for the Code Institute Full-Stack Software Development Diploma, with a strong focus on usability, data integrity, and real-world application.
## 2. Project Aims
The aim of the Precision Performance PT project is to provide a structured and user-friendly online coaching platform for personal trainers and their clients.
The application is designed to support the full personal training journey, from initial consultation through to programme delivery, workout logging, progress tracking, and ongoing communication. By centralising all training data in one syste.Tthe platform reduces the need for more difficult spreadsheets, messaging apps, and manual tracking.
A key aim of the project is to clearly separate user roles. Clients, trainers, and the business owner each see only the features relevant to them. This improves security, reduces confusion, and ensures sensitive data is accessed appropriately.

The project also aims to demonstrate full-stack development skills using Django, including authentication, role-based access control, database design, and responsive front-end development, in line with Code Institute assessment criteria.
## 3. User Goals
The primary users of the Precision Performance PT platform are clients who want a clear, simple, and structured way to follow their training programmes online.
Clients want to easily understand what workouts they need to complete, see their progress over time, and communicate with their assigned trainer when needed. The platform aims to remove confusion by presenting only relevant information to the client, such as todays workout, recent sessions, and progress metrics.

Users also want a smooth and intuitive experience across all devices. Clear navigation, readable layouts, and straightforward actions help ensure clients can focus on their training rather than learning how to use the system.
## 4. Site Owner Goals
The site owners primary goal is to manage the personal training business efficiently from one central platform. Precision Performance PT was designed to give the owner full visibility of clients, trainers, consultations, and any ongoing activity withot needing to rely on external tools or manual processes.
The owner needs to be able to oversee the entire system at a high level, while still having the option to act as a trainer when required. This includes assigning consultations, reviewing client progress, managing trainers, and responding to support queries.
By centralising all business operations into a single dashboard, the platform helps reduce admin time, improve organisation, and ensure a consistent and professional experience for both clients and trainers.

## 5. Target Audience
The target audience is simple, men or women looking to take charge of their fitness journey. The target audienece is those looking to improve in this aspect but still need some guidance and accountability. Ideally suited to those who want this accountability in the form of a expert trainer and have the support of not only in person training sessions but the backfall of a community 
like feel with 24/7 support. 

## 6. User Experience (UX)
The user experience of Precision Performance PT was designed to be clear, structured, and easy to follow for all users, regardless of technical ability. The platform supports three distinct user roles (Client, Trainer, Owner), each with different goals, while maintaining a consistent layout and interaction style across the application.
A strong focus was placed on clarity, accessibility, and reducing load, ensuring users can complete key tasks with minimal friction.

### Navigation & Layout

- Public pages use a simple top navigation with clear calls to action (e.g. *Book a Consultation*).
- Authenticated dashboards use a persistent sidebar for quick access to key sections.
- Page titles, subtitles, and helper text clearly explain context and current location.
- Consistent spacing and layout patterns help users orient themselves easily.

### Client-Focused UX

Client pages are designed to minimise effort and confusion:

- The client dashboard immediately highlights Todays Workout, reducing decision fatigue.
- Logging workouts is pre-filled with trainer-defined targets to reduce manual input.
- Body metrics are logged through simple forms and visualised using charts for easy progress tracking.
- Support messaging uses a familiar ticket style interface to keep communication clear and organised.

### Trainer & Owner UX

Trainer and Owner dashboards share the same core layout to reduce learning overhead:

- Trainers only see their assigned clients, preventing information overload.
- Owners see extended data sets but within the same familiar interface.
- Filters, tables, and actions are clearly labelled to support fast decision-making.
- Editing and saving programmes follows predictable interaction patterns.

## 7. User Stories
User stories were created to get a better understanding of what a typical user would feel while navigating through an online personal training dashbaord, this was done to represent a normal site user,a client, trainer and owner. We look at user stories more in testing further brlow.

Stories were grouped into Epics and managed using a GitHub Project board.  
Each user story includes acceptance criteria and supporting tasks to guide development and testing.

The Agile board for this project can be viewed here:  
https://github.com/users/moranjohn-95/projects/10

### User Stories Table

| Title | User Story |
|------|-----------|
| **All Users - Auth Registration, Login / Logout** | I want to be able to register, log in, and log out securely so that my account and personal data are protected. |
| **All Users  Clear, Consistent and Visually Appealing Interface** | I want the website to be visually clear and consistent so that it is easy to use and understand across all pages. |
| **Client  Dashboard & View Workout Plan** | I want to access my dashboard and view my assigned workout plan so that I clearly know what training I need to complete. |
| **Client  Log & Manage Workout Sessions** | I want to log my workout sessions so that I can track completed training and review past workouts. |
| **Client  Record & View Body Metrics** | I want to record and view body metrics so that I can track physical progress over time. |
| **Owner  Business Dashboard** | I want to view a high level business dashboard so that I can understand overall activity and performance. |
| **Owner  View All Clients** | I want to view all clients across the business so that I can oversee client activity and assignments. |
| **Owner  View All Trainers** | I want to view all trainers working in the business so that I can manage staff and understand capacity. |
| **Trainer  Client List & Profiles** | I want to see a list of my assigned clients and access their profiles so that I can manage coaching effectively. |
| **Trainer  Create Workout Plans** | I want to create structured workout plans so that clients receive clear and organised training programmes. |
| **Trainer  Edit & Save Workout Plans** | I want to edit and save workout plans over time so that programmes stay aligned with client progress. |

#### Agile Board & Development Journey

User stories and epics were tracked using a **GitHub Project board** and were organised into the following groupings and stages, As seen below. Having a visual aid like this was a big help in planning and structuring the design/development of this project.

- **Epics**  High level project goals and feature groupings. 
- **To Do**  User stories planned but not yet started.
- **In Progress**  User stories actively being developed. 
- **Testing / In Review**  Completed features undergoing testing. 
- **Done**  Fully implemented and verified user stories. 

Each user story was linked to an epic and labelled to reflect priority and user role (Client, Trainer, Owner, All Users).

This Agile workflow helped ensure:
- features were built in manageable steps.
- progress was visible throughout development.
- testing aligned directly with user needs.

#### Agile Board Progression

The screenshots below show how user stories moved through the Agile workflow during the project lifecycle.

At the start of the project, epics and user stories were defined and placed into the **To Do** column.  
This stage focused on identifying core functionality, user roles, and UX requirements before development began.

![Agile board  initial planning](documentation/agile/agile-board.png)

As development progressed, user stories were moved into **In Progress** and **Testing**.  
This ensured features were built incrementally and reviewed before being marked as complete.

![Agile board  development in progress](documentation/agile/agile-step-2.png)

### Completion Stage

Once features were fully implemented and tested, user stories were moved into the **Done** column.  
This confirms that acceptance criteria were met and functionality was working as intended.

![Agile board  completed user stories](documentation/agile/agile-end.png)



## 8. Design
The thinking behind the design for The Precisison Performance apllication was to ensure user experience was the main focus. Data relating to fitness and health is always complicated and it cna be difficult to express this data in a way that isnt overwhelming and confusing. As such it was important that the design was clearly thought out of. Consistent and clear colour hierarchys and consistnet text strucutres were key here. 

### 8.1 Colour Scheme

![Precision Performance PT colour palette](documentation/design/pppt-colour-palette.png)

*Colour palette created using [Coolors](https://coolors.co/?home).*

The colour scheme for **Precision Performance PT** was designed to reflect performance, clarity, and professionalism while remaining highly usable across a feature-heavy dashboard application.

A dark navy base is used throughout the platform to establish a strong, premium brand identity and provide clear visual structure. This is paired with a clean white background and soft light grey surfaces to ensure content such as tables, forms, charts, and metrics remain easy to read during extended use.

A bright accent green is used sparingly to highlight important actions, progress indicators, and key points of focus. This colour was chosen to symbolise growth, progression, and performance improvement, which aligns closely with the purpose of the platform. A strong digital blue is used for primary buttons and links, ensuring interactive elements are instantly recognisable and accessible.

Care was taken to maintain sufficient colour contrast across all areas of the site to support accessibility, readability, and WCAG guidelines. Muted tones are used for secondary information to reduce visual noise while keeping the interface clean and structured.

The primary colours used throughout the application are defined as CSS root variables to ensure consistency across all templates and components:

- **Background colour:** `#F7FAFC`  clean, neutral background for pages and cards  
- **Primary brand navy:** `#0B1F3B`  headers, navigation, and key headings  
- **Body text colour:** `#0F172A`  main readable text  
- **Accent colour:** `#B6F400`  highlights, progress indicators, emphasis points  
- **Primary action blue:** `#1F6DE8`  buttons, links, and interactive elements  
- **Surface white:** `#FFFFFF`  cards, tables, and form containers  

This combination ensures the interface feels professional and focused, while remaining easy to navigate for clients, trainers, and owners across desktop, tablet, and mobile devices.

### 8.2 Typography

Typography played an important role in ensuring the Precision Performance PT application feels professional, clear, and easy to use across all user roles.

Two primary fonts are used throughout the application:

- **Open Sans**  for body text, forms, tables, and longer content.
- **Montserrat**  for headings, section titles, and key UI labels.

#### Open Sans Body Text

**Open Sans** is used as the main body font across the platform.

It was chosen because:
- It offers excellent readability at small sizes, which is important for dashboards, tables, and data heavy views.
- Its open letterforms reduce eye strain during longer sessions, such as reviewing workout logs or reading support messages.
- It maintains clarity across mobile, tablet, and desktop devices.

This makes Open Sans particularly suitable for a personal training platform where users regularly read structured information such as exercises, sets, reps, and progress data.

#### Montserrat Headings & UI Hierarchy

**Montserrat** is used for headings and prominent UI elements.

It was selected because:
- It has a strong, modern appearance that reflects confidence and professionalism.
- Its clean style aligns well with a fitness and performance focused brand.
- It creates clear visual separation between headings and body content, improving overall UX and scannability.

Using Montserrat for headings helps guide users through the interface and makes key sections such as dashboards, programme titles, and call-to-action areas stand out clearly.

Both fonts are also web safe and widely supported. Easy to read for users with visual impairments.

## Desktop Wireframes
Wireframes were created at the start of this project to aid in the desing process and really helped gain a better sense for overall planning of the various web pages. Wireframes were only designed for desktop as with the amount of data/charts etc that was to be used it was easier to start with desktop and downsize as opposed to the standard mobile first design. The following wireframes illustrate the core user journeys across the Precision Performance PT platform. They are grouped below to reflect public pages, authentication, and authenticated dashboard experiences.

---

### Public- Pages (Discovery & Conversion)
The below wireframesw were initially developed thinking of the everyday user and how important it was to have a simplistic and easy to use interface, so that potential clients werent lost straight away.

| Homepage | Book a Consultation |
|--------|---------------------|
| ![Homepage wireframe](documentation/design/desktop-home-1.png) | ![Book a consultation wireframe](documentation/design/desktop-booking-con.png) |
| **Homepage**  Introduces the brand, coaching options, and key value propositions, with strong calls to action. | **Book a Consultation**  Primary conversion form capturing contact details, training preferences, and availability. |

---

### Contact & Authentication
The contact and login wireframes below were also  desinged with a simplistic viewpoint of not wanting to over stimulate the user with distracting features. 

| Contact Us | Trainer / Client Login |
|-----------|------------------------|
| ![Contact form wireframe](documentation/design/desktop-contact-form.png) | ![Login wireframe](documentation/design/desktop-client-trainer-login.png) |
| **Contact Us** General enquiries for non-consultation queries with follow-up preferences. | **Login** Shared authentication entry point for trainers and clients. |

---

### Authenticated Dashboards
The overall structure seen below is very close to the actual live structure with the sidebar for pages being a key feature throughout both dashboards. This inital design thougt paid dividends as it was key in creating a good UX and being easy to change with regards to responsiveness. 

| Client Dashboard | Trainer Dashboard |
|------------------|------------------|
| ![Client dashboard wireframe](documentation/design/desktop-clientdashboard1.png) | ![Trainer dashboard wireframe](documentation/design/desktop-trainerdashboard.png) |
*Wireframes were created using [Balsamiq](https://balsamiq.com/).*



| **Client Dashboard**  Displays next workout, weekly stats, and quick links to key actions. | **Trainer Dashboard**  Central workspace for managing consultations, classes, and client activity. |

### 8.4 Responsive Design
Precision Performance PT has been designed to be fully responsive across desktop, tablet, and mobile. As such media queries werre used throughout the wenbiste at key break points of min width of 993px (desktop), max-width of 992px (tablet and below), max width od 576 (mobiles.)
The fact the platform contains data heavy views (tables, forms, charts, and logs), responsiveness focused on keeping key actions accessible while preventing layouts from becoming cluttered on smaller screens. A good example of this is the sidebar featurea and how its leveraged on differnet devices.

On **desktop**, the sidebar remains visible to provide reliable navigation between dashboard sections.  
On **tablet and mobile**, the sidebar becomes an **off-canvas menu** (opened via a menu toggle). preventing it from taking up valuable screen space while still keeping navigation easy to access.

| Tablet / Mobile (Off-canvas sidebar) | Desktop (Sidebar visible) |
|---|---|
| ![Trainer sidebar - tablet view](documentation/design/feature-trainer-boardsidebar.jpg) | ![Trainer dashboard - desktop view](documentation/design/feature-trainerdahsbaord-desktop-responsive.png) |

**Key responsive behaviour:**
- Desktop view uses a fixed sidebar so the user can move between sections quickly.
- Tablet/mobile view uses a slide-out sidebar to keep the main content readable.
- Navigation labels remain consistent across all breakpoints so users never have to “re-learn” the UI.
- Buttons and links remain large enough for touch interaction on smaller devices.


## 9. Features
The below sections cover the key features of the precision perfromance application, all images are screenshots from a tablet to showacse a happy medium betweem mobile and desktop.

### Features & User Journeys

This section outlines the core features of the Precision Performance PT platform and demonstrates how users interact with the system through real-world journeys. Screenshots are provided as evidence of implemented functionality.

### Features & Role Access Overview

| Feature | Public User | Client | Trainer | Owner | Notes |
|-------|:-----------:|:------:|:-------:|:-----:|------|
| **Booking Consultation** | ✓ | — | — | — | Prospective clients submit a consultation form with contact details, goals, coaching preferences, and availability. Data is stored securely for trainers and owners. |
| **Dedicated Login & Account Access** | — | ✓ | ✓ | ✓ | Each role has its own login flow, ensuring correct role-based access (client, trainer, owner). |
| **Dashboard Overview** | — | ✓ | ✓ | ✓ | Clients see today’s workout and weekly summary. Trainers and owners see consultations, clients, and key metrics relevant to their role. |
| **View Programme & Daily Workouts** | — | ✓ | ✓ | ✓ | Clients view assigned programmes by week and day. Trainers and owners can view programme details for each client. |
| **Log & Manage Workout Sessions** | — | ✓ | ✓ | ✓ | Clients log workouts with pre-filled targets. Trainers and owners can review logged sessions and progress. |
| **Body Metrics Tracking & Check-Ins** | — | ✓ | ✓ | ✓ | Clients submit metrics (e.g. bodyweight, waist, sleep). Trainers and owners review entries and visualise progress via charts. |
| **Support & Messaging** | — | ✓ | ✓ | ✓ | Clients open support tickets to contact trainers. Trainers and owners reply through the support system until resolved. |
| **Client List & Profiles** | — | — | ✓ | ✓ | Trainers see only their assigned clients. Owners can view all clients across the platform. |
| **Programme Creation & Tailoring** | — | — | ✓ | ✓ | Trainers create and tailor programmes. Owners can also create and assign programmes. |
| **Consultation & Query Management** | — | — | ✓ | ✓ | Trainers can accept consultations for themselves only. Owners can assign consultations and queries to any trainer or themselves. |
| **Administrative Oversight** | — | — | — | ✓ | Owners have full system visibility across trainers, clients, consultations, and support tickets. |

**Note:** Trainers cannot view other trainers’ clients or assign consultations to other trainers. All access is enforced through role-based permissions.


---

## Client User Journey
The below sections demonstrate a clients journey while using the precision performance application.

### Booking a Consultation (Public User)
A prospective client begins their journey by submitting a consultation request via the public website.

- The consultation form collects contact details, training goals, coaching preference, and availability.
- This data is stored securely and made available to trainers and the owner via their dashboards.

![Consultation form](documentation/features/feature-consultation.jpg)
![Consultation form  step view](documentation/features/feature-consultation-2.jpg)

---

### Client Account Access & Login

Once a consultation has been accepted and a trainer assigned, the client is provided with login access to the platform.

- Clients log in via a dedicated client login page.
- Authentication ensures clients only access their own data.

![Client login](documentation/features/feature-clientlogin.png)

---

### Client Dashboard Overview

After logging in, clients land on their dashboard overview.

- The dashboard highlights todays workout.
- A clear call to action allows the client to start their training session.
- Weekly summaries display recent activity and key metrics.

![Client dashboard overview](documentation/features/feature-clientdashboard.jpg)
![Client dashboard sidebar](documentation/features/feature-clientdashboardsidebar.jpg)

---

### Todays Workout & Programme Viewing

Clients can view their active training programme and see daily workout breakdowns.

- Programmes are structured by week and day.
- Exercises include target sets, reps, and weights defined by the trainer.

![Client programme view](documentation/features/feature-clientprogrammeview.jpg)

---

### Logging a Workout Session

Clients log completed workouts using the workout log feature.

- Pre-filled targets are loaded automatically.
- Clients can adjust weights or reps if required.
- Logged sessions are stored and visible to both client and assigned trainer.

![Client workout log](documentation/features/feature_clientworkoutlog.jpg)

---

### Viewing & Editing Recent Sessions

Clients can view previously logged sessions.

- Recent sessions are listed clearly.
- Sessions can be reopened for review or editing if required.

![Client workout log  recent sessions](documentation/features/feature_clientworkoutlog.jpg)

---

### Body Metrics Tracking

Clients can log regular body metrics to track progress over time.

- Metrics include bodyweight, waist measurement, bench top set, and sleep hours.
- Entries are stored chronologically and visualised using charts.

![Client body metrics overview](documentation/features/feature-clientbodymetrics.jpg)

---

### Body Metrics Check-in

Clients submit new metric entries using a dedicated check-in form.

- All inputs are optional to support flexible tracking.
- Data feeds directly into progress charts.

![Client body metrics check-in](documentation/features/feature-cllient-bodymetricscheckin.jpg)

---

### Client Support & Messaging

Clients can contact their assigned trainer using the support system.

- Support tickets include a subject and message.
- Clients can track ticket status and view replies.

![Client support page](documentation/features/feature-clientsupport.jpg)

---

### Viewing & Replying to Support Tickets

Clients can view individual support tickets and ongoing message threads.

- Tickets remain open until resolved.
- Clients can close tickets once their issue is resolved.

![Client support ticket](documentation/features/feature-clientsupportticket.jpg)

---

## Trainer & Owner Feature Overview (Context)

While the primary focus of this section is the **client journey**, the platform also includes a set of supporting features for **trainers and owners** that enable the client experience to function smoothly behind the scenes.

These features are intentionally role-restricted to ensure clarity, security, and maintain correct data access.

---

### Trainer Features (Supporting Client Experience)

Trainers are responsible for managing client relationships, tailoring programmes, and monitoring progress.  
They only have access to **their own assigned clients**, ensuring data separation between trainers.

**Trainer dashboard overview**

The trainer dashbaord overview is the same as the owner dashbaord overivew just with somehwat mroe restrictive fucntionality. As can be sen below each consultation request that comes in is stored 
here and can be filtered  ny consutations that are still open (yet to be assinged to a client") or assigned. the clients looking for access to classes are then accepted but filter down into the classes section. these clients do not receive access to the dashbboard. 

![Trainer overview](documentation/features/feature-traineroverview.jpg)

**Trainer client list and access to individual client profiles**

The below images shows a view of a trainer checking in on his client bia the client overview page. Here the trainer has selected the below client and can see all his body metric entries and workout logs. All fo which are stored and reflected on the charts. A trainer can also edit a client entry if needs be via the recent check ins tab.

![Trainer clients overview](documentation/features/feature-trainerclinetsoverview.jpg)
![Trainer clients overview expanded](documentation/features/feature-trainerclinetsoverview2.jpg)

**Trainer programme creation and tailoring**

Trainers can build programmes from base templates and customise them per client, including exercises, sets, reps, and target weights. 
This is an important feature as each client is different and needs to receive a programm taiolred to their abilities.

![Trainer programme overview](documentation/features/feature-trainerprogrammeoverview.jpg)
![Trainer programme tailoring](documentation/features/feature-trainer-programmetailoring.jpg)
![Trainer programme block tailoring](documentation/features/feature-trainer-programmeblocktailoring.jpg)

**Trainer access to consultations and queries**
So for a trainer to access the dashbaord and all their clients information etc. They also need to login via a secure login page. This ensures that only the trainer can access this infomration 
and thete is no mix up woth a client login.

![Trainer login](documentation/features/feature-trainerlogin.jpg)
![Trainer my clients](documentation/features/feature-trainermyclients.jpg)

Trainers can only assign consultations to themselves, cannot see other trainers clients information and cannot delegate tasks to other trainers, reinforcing role-based responsibility.

---

### Owner Features (Administrative Oversight)

The owner role extends the trainer interface with **full administrative visibility** across the platform.  
Owners can manage trainers, clients, consultations, and support tickets.

**Owner dashboard overview**
The owner dashhbaord from a far looks the exact same as the trainer dashbaord and they almost are. However th owner has some very important extra functionality as seen below.
![Owner overview](documentation/features/feature-owneroverview.jpg)

**Owner access to all clients**
Owner of precision perfroamnce can view all clients regardless of assigned trainer. Including clients metrics data.
![Owner all clients](documentation/features/owner-allclients.jpg)

**Owner consultation assignment and query management**

Owners can assign clients via the consultations to any trainer or themselves, providing flexibility and operational control. Owners can also assign queries to trainers or themselves. (Trainers can only assing to themsleves)

![Owner client assignment](documentation/features/owner-clientassignment.jpg)
![Owner queries](documentation/features/owner-queries.jpg)
![Owner query ticket](documentation/features/owner-queryticket.jpg)

**Owner support ticket management**
The functionality here is the exact same as trainers. Owners cannot see trainers messages to clients and visa versa as to keep a standard of trainer/client confidentiallity.  Owners can however recieve and reply to messages from clients of their own.

![Owner support ticket](documentation/features/owner-supportticket.jpg)
![Owner support inbox](documentation/features/owmer-support.jpg)

Owners can view and manage all client/ trainer support interactions across the system.

---

## Summary

The client journey within Precision Performance PT is designed to be simple and data driven, while being fully supported by trainer and owner workflows behind the scenes.

- Clients move from initial consultation to active training in a structured and intuitive way.
- Trainers support clients through programme creation, progress tracking, and direct communication.
- Owners provide oversight, consultation assignment, and administrative control. While also maintianing trainer responsibilities to their own clients.
- All features operate under clear role-based permissions to protect data and ensure clarity.

The screenshots above demonstrate that all core client-facing features and supporting trainer/owner features are fully implemented and operational.


## 10. Application Flow & Logic
This section explains how users move through the Precision Performance PT application and how core actions are handled behind the scenes.  
All flows are **role-based** (Public, Client, Trainer, Owner) and are enforced through Django views, decorators, and route level access checks.

The aim of this logic is to keep user journeys clear, predictable, and secure while ensuring the correct data is created and used at each step.

---

### 10.1 Public Consultation Submission (Public User)

This is the entry point for new clients.

| Step | Description |
|----|------------|
| Visit page | User visits `/consultation/` |
| Form render | `consultation.html` is rendered using `ConsultationRequestForm` |
| Form submit | A `ConsultationRequest` record is created (POST request) |
| Feedback | A success message is shown to the user |
| Redirect | User is redirected back to the consultation page (Post/Redirect/Get pattern) |

This prevents duplicate submissions and provides clear feedback to the user.

---

### 10.2 Consultation Review & Assignment (Trainer / Owner)

Once submitted, consultations are reviewed by staff users.

| Step | Description |
|----|------------|
| Login | Trainer or owner logs in |
| Dashboard | User lands on the trainer dashboard |
| Review | Consultation requests are listed with filters (Open, Assigned, Classes) |
| Assignment | Trainer can assign to themselves, owner can assign to any trainer |
| Business rules | Group coaching requests cannot be added to individual client lists |

When a consultation is assigned, the following logic is executed:

- A portal **User** is created using the client’s email address (email = username).
- A **ClientProfile** is created or linked.
- The preferred trainer is set.
- A password setup email is sent if required.
- Consultation status is updated to **Assigned**.

Assignment logic is handled centrally in `assign_consultation_to_trainer()`.

---

### 10.3 Client Account Access & Login (Client)

Clients access the platform after a consultation has been accepted.

| Role | Login URL | Redirect |
|----|----------|---------|
| Client | `/accounts/client/login/` | Client dashboard |
| Trainer / Owner | `/accounts/trainer/login/` | Trainer dashboard |

- Client accounts are created automatically during consultation assignment.
- Clients receive a password setup email if they do not already have credentials.
- Separate login paths ensure role separation and clarity.

---

### 10.4 Client Programme Viewing (Client)

Clients access their training plans through the programme library.

| Step | Description |
|----|------------|
| Page | `/accounts/client/programme-library/` |
| Data loaded | Active programme assignments for the client |
| Optimisation | Programme days and exercises are prefetched |
| Output | `programme_library.html` rendered |

Each programme day includes a **“Log this session”** action that passes:
- Programme day
- Week number
- Session name  
into the workout logging flow.

---

### 10.5 Workout Logging (Client)

Clients record completed training sessions.

| Step | Description |
|----|------------|
| Page | `/accounts/client/workout-log/` |
| Default logic | First available programme day selected if none provided |
| Form submit | Exercise inputs compiled into structured session notes |
| Validation | Duplicate sessions for the same day/week are blocked |
| Save | Session is linked to programme, day, and week |

Clients can also edit existing sessions via:
- `/accounts/client/workout-log/edit/`

This updates session name, notes, and completion status.

---

### 10.6 Body Metrics Check-ins & Charts (Client / Trainer)

Clients and trainers track physical progress through metrics.

| Feature | Description |
|------|-------------|
| Page | `/accounts/client/metrics/` |
| Form | `BodyMetricEntryForm` |
| Actions | Add, update, or delete metric entries |
| Data | Summary rows and chart datasets built in the view |
| Charts | Rendered using Chart.js and `client_metrics_charts.js` |

- Clients see their own metrics and charts.
- Trainers can view assigned clients’ metrics via the client detail page.
- Owners can view metrics for all clients.

---

### 10.7 Support Tickets & Messaging (Client / Trainer / Owner)

The support system enables structured communication.

| Step | Description |
|----|------------|
| Create ticket | Client submits subject and message |
| Data created | `SupportTicket` and `SupportMessage` records |
| Assignment | Ticket assigned to preferred trainer (if set) |
| Client view | Clients can reply and close tickets |
| Trainer/Owner view | Trainers and owners see only assigned tickets |

Support privacy rules ensure:
- Clients only see their own tickets.
- Trainers only see tickets assigned to them.
- Owners can view and respond to their own assigned tickets.

---

### Key Business Rules

| Rule | Description |
|----|------------|
| Role enforcement | `is_staff` and `is_superuser` control access |
| Staff redirects | Staff users are redirected away from client-only pages |
| Group coaching | Group consultations cannot create client accounts |
| Ticket privacy | Only assigned trainer/owner can view or reply |
| Workout integrity | Duplicate workout logs for the same day/week are blocked |


## 11. Database & Data Models
The Precision Performance PT application uses a relational database designed around **clear ownership of data**, **role separation**, and **real-world training workflows**.

All data models are split across two Django apps:

- **accounts** – user profiles, support, consultations, and queries  
- **training** – programmes, workouts, and body metrics  

Django’s built-in **User** model is used as the core identity for all users.  
Additional profile and training-specific data is linked to this User model through related tables.

---

## Accounts App (`accounts`)

### ClientProfile

| Aspect | Description |
|------|------------|
| Purpose | Stores additional client specific information linked to a user account |
| Linked user | One-to-one relationship with Django `User` |
| Optional links | Consultation request, preferred trainer |
| Why | Keeps authentication separate from client only metadata |

This allows every client to have a standard Django user account, while storing training-specific details safely alongside it.

---

### ConsultationRequest

| Aspect | Description |
|------|------------|
| Purpose | Stores consultation submissions from public users |
| Created by | Public users via the consultation form |
| Assigned trainer | Optional link to a trainer or owner |
| Status | Tracks whether the consultation is open or assigned |

This model is the entry point for new clients into the system.

---

### ContactQuery

| Aspect | Description |
|------|------------|
| Purpose | Stores general contact us enquiries |
| Use case | Non consultation questions and follow-ups |
| Assignment | Can be assigned to a trainer or owner |

This keeps business enquiries separate from training consultations.

---

### SupportTicket

| Aspect | Description |
|------|------------|
| Purpose | Represents a client support conversation |
| Client | Linked to the client user |
| Trainer | Optional link to the assigned trainer |
| Privacy | Only assigned trainer/owner can view and reply |

Support tickets act as containers for message threads.

---

### SupportMessage

| Aspect | Description |
|------|------------|
| Purpose | Individual messages within a support ticket |
| Linked ticket | Foreign key to `SupportTicket` |
| Sender | Linked to the sending user (client or staff) |

This allows structured, readable support conversations.

---

## Training App (`training`)

### ProgrammeBlock

| Aspect | Description |
|------|------------|
| Purpose | Defines a programme template or a tailored version |
| Created by | Trainer or owner |
| Templates | Supports parent/child relationship for tailored copies |

This structure allows base templates to be reused and customised per client.

---

### ProgrammeDay

| Aspect | Description |
|------|------------|
| Purpose | Groups exercises for a single day |
| Linked block | Foreign key to `ProgrammeBlock` |

---

### ProgrammeExercise

| Aspect | Description |
|------|------------|
| Purpose | Defines an individual exercise |
| Linked day | Foreign key to `ProgrammeDay` |
| Data | Stores sets, reps, weights, and notes |

---

### ClientProgramme

| Aspect | Description |
|------|------------|
| Purpose | Assigns a programme to a client |
| Client | Linked to the client user |
| Trainer | Linked to assigned trainer |
| Status | Active, planned, or completed |

This model connects clients to specific training programmes.

---

### WorkoutSession

| Aspect | Description |
|------|------------|
| Purpose | Represents a logged workout |
| Client | Linked to the client user |
| Programme | Optional link to `ClientProgramme` |
| Day | Optional link to `ProgrammeDay` |

Each workout session represents one completed training day.

---

### WorkoutSet

| Aspect | Description |
|------|------------|
| Purpose | Stores individual sets within a workout |
| Linked session | Foreign key to `WorkoutSession` |

This allows detailed tracking of performance within a workout.

---

### BodyMetricEntry

| Aspect | Description |
|------|------------|
| Purpose | Stores client body-metric check-ins |
| Client | Linked to the client user |
| Data | Weight, measurements, strength metrics, sleep |

These entries are used to generate charts and progress summaries.

---

## Data Relationships Overview

The data model is structured to reflect real world coaching workflows:

- Client profiles extend Django users and link to consultations and trainers.
- Programme templates flow from **ProgrammeBlock → ProgrammeDay → ProgrammeExercise**.
- Tailored programmes inherit from base templates using a parent reference.
- Client programme assignments live in **ClientProgramme**.
- Workout logging uses **WorkoutSession** with optional **WorkoutSet** rows.
- Body metrics are stored per client in **BodyMetricEntry**.
- Support conversations are handled through **SupportTicket** and **SupportMessage**.
- Consultations and contact enquiries are handled separately to maintain clarity.

This structure ensures data integrity, scalability, and clear separation of responsibilities across user roles.

## 12. Authentication & Authorisation

Authentication and authorisation in Precision Performance PT are handled via Django’s authentication system. This provides a secure and tested foundation while allowing custom logic for different user roles (in this case - Client, Trainer, Owner).

The application uses session-based authentication, meaning users remain logged in across requests until they explicitly log out or their session expires.

---

### Authentication Setup

The following Django components are enabled:

- `django.contrib.auth`
- `django.contrib.sessions`
- `AuthenticationMiddleware`
- `SessionMiddleware`

These are configured in `settings.py` and provide login, logout, session handling, and password management.

---

### Authentication Flow Overview

| Feature | Implementation |
|------|----------------|
| **Trainer Login** | `/accounts/trainer/login/` using Django `LoginView` and `trainer_login.html` |
| **Client Login** | `/accounts/client/login/` using Django `LoginView` and `client_login.html` |
| **Logout** | `/accounts/logout/` using Django `LogoutView`, redirects to home page |
| **Password Reset** | Django built-in password reset views under `/accounts/password-reset/…` |
| **Session Handling** | Managed automatically by Django sessions |

Separate login pages are used for trainers and clients to clearly separate access paths and reduce confusion during authentication processes.

---

### Post-Login Redirect Logic

After successful authentication, users are redirected based on their role:

| User Role | Redirect Destination |
|---------|----------------------|
| **Trainer / Owner** | `accounts:trainer_dashboard` |
| **Client** | `accounts:client_dashboard` |

This logic is handled in custom `get_success_url()` methods on the respective login views, ensuring users land directly on the correct dashboard.

---

### Authorisation & Protected Routes

Access to private areas of the application is restricted using Django decorators:

| Protection Type | Usage |
|---------------|------|
| **Login required** | Most dashboard and account views use `@login_required` |
| **Staff-only access** | Restricted views use a custom `staff_required` decorator |
| **Admin access** | Some routes use Django’s `@staff_member_required` |

The `staff_required` decorator wraps Django’s `user_passes_test`, checking `user.is_staff` and redirecting unauthorised users to the trainer login page.

This ensures:
- Clients cannot access trainer or owner dashboards.
- Trainers cannot access admin-only functionality.
- Owners (superusers) inherit full trainer access.

## 13. Role-Based Access Control

Role-based access control in Precision Performance PT ensures that each user only sees and interacts with the parts of the system relevant to their role.  
This is handled using Django’s built-in user flags rather than custom groups, keeping the logic simple, secure, and easy to maintain.

---

### Role Determination

User roles are derived directly from fields on Django’s `User` model.

| Role | Conditions | Description |
|----|-----------|-------------|
| **Client** | `is_staff == False` | Standard user with access only to client-facing features |
| **Trainer** | `is_staff == True` and `is_superuser == False` | Staff user responsible for managing assigned clients |
| **Owner** | `is_superuser == True` (also `is_staff`) | Full administrative access across the platform |

This approach avoids unnecessary complexity while still enforcing strict separation of responsibilities.

---

### Client Permissions

| Area | Access Rules |
|----|--------------|
| Client dashboard | Login required |
| Programme library | Login required |
| Workout log | Login required |
| Body metrics | Login required |
| Support tickets | Login required |

Additional rules:
- All client views are protected using `@login_required`.
- If a **staff user** attempts to access a client-only route, they are automatically redirected to the trainer dashboard.
- Clients cannot access any trainer or owner pages.

---

### Trainer Permissions

| Area | Access Rules |
|----|--------------|
| Trainer dashboard | Staff-only |
| Client list & profiles | Only assigned clients |
| Programme creation & editing | Staff-only |
| Consultations | Can assign consultations **only to themselves** |
| Support tickets | Only tickets assigned to the trainer |

Implementation details:
- Trainer routes require login using the trainer login page.
- Access checks are enforced using `staff_required` or `staff_member_required`.
- Non-staff users attempting to access trainer routes are redirected to the client dashboard.

---

### Owner Permissions

| Area | Access Rules |
|----|--------------|
| Owner dashboard | Superuser-only |
| All clients | Full visibility |
| All trainers | Full visibility |
| Programme management | Full access |
| Consultations & queries | Can assign to any trainer or themselves |
| Support tickets | Access to tickets assigned to the owner |

Additional rules:
- Owner-only views explicitly check `request.user.is_superuser`.
- Non-superusers attempting to access owner routes are redirected or shown a 404 response.
- Owners can access owner-branded versions of trainer pages with expanded data visibility.

---

### Data Separation & Query Enforcement

Access control is reinforced at the database query level to prevent data leakage.

| Feature | Enforcement |
|------|-------------|
| Trainer client lists | Filtered by `assigned_trainer == request.user` |
| Trainer client detail | Blocked unless client is assigned to the trainer |
| Support tickets (client) | Filtered by `SupportTicket.client == request.user` |
| Support tickets (trainer) | Filtered by `SupportTicket.trainer == request.user` |
| Owner views | Not restricted by trainer assignment |

This ensures that even if a URL is guessed or manually entered, unauthorised data cannot be accessed.

---

### Examples of Access Restrictions

- Non-staff users are redirected away from trainer-only routes.
- Staff users are redirected away from client-only routes.
- Trainer support ticket detail views use `get_object_or_404(trainer=request.user)`, preventing access to unassigned tickets.
- Owner-only routes explicitly block non-superusers.l

## 14. Security Features

Security within Precision Performance PT is handled primarily through Djangos built-in security features, combined with a small number of explicit configuration choices.  
This approach ensures the application follows industry standards while remaining simple, reliable, and suitable for a real world deployment.

---

### Core Security Protections

| Feature | Description |
|------|-------------|
| **Authentication & Sessions** | Djangos authentication and session framework is used (`django.contrib.auth`, `django.contrib.sessions`). User sesions are securely managed using cookies. |
| **CSRF Protection** | `CsrfViewMiddleware` is enabled globally. All forms include `{% csrf_token %}` to protect against cross site request forgery attacks. |
| **Access Control** | Views are protected using `@login_required`, `staff_required`, and `@staff_member_required` decorators to ensure users only access permitted areas. |
| **Security Middleware** | Django’s `SecurityMiddleware` and `XFrameOptionsMiddleware` are enabled to protect against common web vulnerabilities such as clickjacking. |

---

### Form & Request Security

All user input is handled through Django forms and protected templates:

| Area | Protection Used |
|----|-----------------|
| Login forms | CSRF tokens, Django auth validation |
| Consultation form | CSRF token, server side form validation |
| Workout log | CSRF token, authenticated access only |
| Support tickets | CSRF token, role based access checks |

This ensures that all submitted data is validated serverside and cannot be manipulated by unauthorised users.

---

### Environment-Driven Security Settings

Sensitive configuration values are not hard coded and are instead managed through environment variables.  
This supports secure deployment and prevents sensitive data from being exposed in version control.

| Setting | Purpose |
|------|---------|
| `DJANGO_SECRET_KEY` | Stores the Django secret key securely outside the codebase |
| `DJANGO_DEBUG` | Controls debug mode (disabled in production by default) |
| `DJANGO_ALLOWED_HOSTS` | Restricts which domains can serve the application |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Defines trusted origins for CSRF protection |

Local fallback values are used only during development.

---

### Additional Security Considerations

- Password handling is managed entirely by Djangos authentication system.
- Password reset functionality uses Django’s built in secure token system.
- Role based restrictions ensure clients, trainers, and owners never see unauthorised data.
- Sensitive actions (assignment, editing, deleting) are always protected by server side checks.

---

## 15. Validation & Error Handling

Validation and error handling within **Precision Performance PT** are designed to keep user input safe, clear, and easy to understand.  
Most validation is handled by Django forms and model constraints, with clear feedback provided to users through messages and inline error displays.

---

### Input Validation

### Django Forms

Django’s form system is used throughout the application to validate user input before it is saved to the database.

| Form | Purpose | Validation Applied |
|----|--------|--------------------|
| `ConsultationRequestForm` | Public consultation submissions | Required fields, consent confirmation, message length checks |
| `ContactQueryForm` | Public contact enquiries | Required fields, message length validation |
| `BodyMetricEntryForm` | Client body metrics check-ins | Numeric validation, optional fields handled safely |
| `WorkoutSessionForm` | Client workout logging | Required session data, safe handling of exercise inputs |

Forms use Django’s built-in validation as well as custom `clean_*` methods where additional checks are required.

---

### Model-Level Validation

Certain business rules are enforced directly at the database level to prevent invalid or duplicate data.

| Model | Constraint | Purpose |
|----|-----------|--------|
| `WorkoutSession` | Unique per client, programme day, and week | Prevents duplicate workout logs |
| `ClientProgramme` | Unique combination of client and programme block | Prevents assigning the same programme twice |

These constraints ensure data integrity even if a view-level check is bypassed.

---

### User Feedback & Error Messages

Clear feedback is provided to users so they understand what happened and how to correct issues.

### Messages Framework

The Django messages framework is used for global feedback:

- **Success messages** – confirm actions such as logging a workout or submitting a consultation.
- **Error messages** – explain why an action failed.
- **Info messages** – provide helpful guidance where needed.

Messages are rendered consistently in `base.html` so feedback is visible across all pages.

---

### Error Handling Strategies

### HTTP Errors & Access Protection

| Error Type | Handling |
|----|---------|
| **404 Not Found** | `get_object_or_404` used when data does not exist |
| **403 Forbidden** | Returned when users attempt restricted actions |
| **Custom 404 page** | A custom `404.html` template improves UX for missing pages |

Owner-only routes explicitly raise `Http404` if accessed by non-owners.

---

### Graceful Failure Handling

Some actions are wrapped in `try/except` blocks to avoid breaking the user flow:

- Password invite email sending in `consultation_assignment.py` is wrapped in `try/except`.
- If email delivery fails, the consultation assignment still completes successfully.

This ensures critical actions are not blocked by external services.

---

## Validation Touchpoints (Confirmed)

| Feature | Validation Location |
|------|--------------------|
| Consultation requests | `ConsultationRequestForm` + `training.views.consultation` |
| Contact form | `ContactQueryForm` + `training.views.contact_us` |
| Workout logging | `WorkoutSessionForm` + duplicate session checks |
| Body metrics | `BodyMetricEntryForm` + create/update/delete logic |
| Support tickets | View level checks in client and trainer support views |

## 16. Technologies Used

## 17. Testing
The below section features all of the testing that was done during amnd after the development of the precision performance application. 

### 17.1 Automated Testing

#### Python Code Validation (CI Python Linter)

All custom Python code was tested using the **Code Institute Python Linter (PEP8CI)** to ensure the backend codebase is readable, maintainable, and free from syntax or formatting errors.

The purpose of this testing was to confirm that:

- Python code follows PEP8 styling conventions  
- There are no syntax or indentation errors  
- The code meets Code Institute assessment requirements  

Only **custom-written project logic** was tested.  
Auto-generated files such as migrations, virtual environments, and third-party framework code were intentionally excluded.

All tested files returned **�All clear, no errors found�**.

##### Python Files Tested

| App / Area | File | Validator Confirmation | Result |
|-----------|------|------------------------|--------|
| training | `training/models.py` | ![training models](documentation/testing/python/python-trainingmodels-test.png) | No errors |
| training | `training/views.py` | ![training views](documentation/testing/python/python-trainingviewspy-test.png) | No errors |
| accounts | `accounts/models.py` | ![accounts models](documentation/testing/python/python-accountsmodels-test.png) | No errors |
| accounts/services | `consultation_assignment.py` | ![consultation service](documentation/testing/python/python-accountsservicesconultation-test.png) | No errors |
| accounts | `accounts/urls.py` | ![accounts urls](documentation/testing/python/python-accountsurlspy-test.png) | No errors |
| accounts | `accounts/views.py` | ![accounts views](documentation/testing/python/python-accountsviewspy-test.png) | No errors |
| training/management/commands | `backfill_consultation_statuses.py` | ![management command](documentation/testing/python/python-backfillconsultation-test.png) | No errors |
| precision_performance | `precision_performance/urls.py` | ![project urls](documentation/testing/python/python-precisionperformanceurlspy-test.png) | No errors |
| scripts | `run_testing_audit.py` | ![testing audit](documentation/testing/python/python-runtestingaudit-test.png) | No errors |
| training | `training/forms.py` | ![training forms](documentation/testing/python/python-trainingformspy-test.png) | No errors |

##### Python Testing Summary

- All selected Python files passed the CI Python Linter  
- No PEP8 errors or warnings were reported  
- Code structure is clear, readable, and maintainable  

#### JavaScript validation (JSHint)

All JavaScript code was tested using **JSHint** to check for errors, warnings, and overall code quality.

To keep this project easier to maintain, all JavaScript was stored in separate files inside the `assets/js/` folder.  
Inline JavaScript was also removed from HTML templates and replaced with `data-*` attributes where needed.  
This was done in an attempt to keep templates cleaner and easier to work through.

##### Notes
- Please notesSome pages use **Chart.js** to display charts. Chart.js provides a global `Chart` object in the browser.
  To avoid false warnings, `/* global Chart */` is seen at the top of chart-related files.
- JSHint shows a minor style warning for `new Chart(...)`. This is expected behaviour with Chart.js and does not affect how the charts work.

| File | Description | JSHint Result |
| --- | --- | --- |
| `main.js` | Controls the public programme details modal | ![JSHint - main.js](documentation/testing/jshint/js-main-check.png) |
| `nav.js` | Handles the public navigation burger menu | ![JSHint - nav.js](documentation/testing/jshint/js-nav-check.png) |
| `portal_link_copy.js` | Allows portal links to be selected and copied | ![JSHint - portal_link_copy.js](documentation/testing/jshint/js-portallink-check.png) |
| `programme_library_highlight.js` | Highlights a programme card based on the page URL | ![JSHint - programme library](documentation/testing/jshint/js-programmelibrary-check.png) |
| `workout_log.js` | Manages the workout log modal and session actions | ![JSHint - workout log](documentation/testing/jshint/js-workoutlog-check.png) |
| `client_detail_charts.js` | Displays trainer-facing client progress charts | ![JSHint - client detail charts](documentation/testing/jshint/js-clientdetails-check.png) |
| `client_metrics_charts.js` | Displays client body metric charts | ![JSHint - client metrics charts](documentation/testing/jshint/js-clientmetrics-check.png) |
| `consultation_assign.js` | Enables the assign button when a trainer is selected | ![JSHint - consultation assign](documentation/testing/jshint/js-consultationassign-check.png) |
| `dashboard_interactions.js` | Handles auto-submit filters and confirm prompts | ![JSHint - dashboard interactions](documentation/testing/jshint/js-dashboardinteractions-check.png) |
| `dashboard_menu.js` | Controls the mobile dashboard menu toggle | ![JSHint - dashboard menu](documentation/testing/jshint/js-dashboardmenu-check.png) |
| `body_metrics_modal.js` | Controls the body metrics modal and form values | ![JSHint - body metrics modal](documentation/testing/jshint/js-body-metrcis-check.png) 

### 17.2 Manual Testing

Manual testing was carried out throughout development to confirm that the application behaves as expected across all user roles (Public User, Client, Trainer, Owner).  
Testing focused on core user journeys, permissions, data handling, and general usability across different screen sizes.

All manually tested features behaved as intended, with no critical issues identified.

#### Manual Testing Summary Table

| Feature Area | User Role | Test Action | Expected Result | Outcome |
|------------|----------|------------|----------------|--------|
| Consultation Form | Public User | Submit consultation form with valid data | Consultation saved and success message shown | Pass |
| Consultation Form | Public User | Submit form with missing required fields | Form errors displayed | Pass |
| Client Login | Client | Log in with valid credentials | Redirected to client dashboard | Pass |
| Client Login | Client | Log in with invalid credentials | Error message shown | Pass |
| Dashboard Navigation | Client | Navigate via sidebar links | Correct pages load | Pass |
| Today’s Workout | Client | View today’s assigned workout | Correct workout displayed | Pass |
| Workout Logging | Client | Log a workout session | Session saved successfully | Pass |
| Workout Logging | Client | Attempt duplicate session for same day | Error message shown | Pass |
| Body Metrics | Client | Add new metrics check-in | Entry saved and chart updated | Pass |
| Body Metrics | Client | Edit/delete existing metrics | Changes saved correctly | Pass |
| Support Tickets | Client | Create support ticket | Ticket created and visible in list | Pass |
| Support Tickets | Client | Reply to existing ticket | Message added to thread | Pass |
| Trainer Login | Trainer | Log in with valid credentials | Redirected to trainer dashboard | Pass |
| Client Access | Trainer | View assigned clients only | Only assigned clients visible | Pass |
| Programme Creation | Trainer | Create and edit programme | Programme saved correctly | Pass |
| Consultation Assignment | Trainer | Assign consultation to self | Client created and assigned | Pass |
| Owner Access | Owner | View all clients and trainers | Full access available | Pass |
| Owner Assignment | Owner | Assign consultation to trainer | Assignment completed successfully | Pass |
| Role Restrictions | All Roles | Attempt unauthorised page access | Redirect or access denied | Pass |
| Responsiveness | All Users | Resize across desktop/tablet/mobile | Layout adapts correctly | Pass |

---

#### Manual Testing Conclusion

- All core user journeys were manually tested.
- Role-based permissions behaved as expected.
- Forms, navigation, and data handling worked correctly.
- No blocking or critical usability issues were found.

Manual testing confirms that the platform is stable, intuitive, and suitable for real-world use.


### 17.3 Validator & Accessibility Testing

#### HTML Validation (Nu HTML Checker)

Key pages across all user roles (Client,Owner,Trainer) as well as public pages were tested using the Nu HTML Checker (W3C). Public pages were validated using **Check by address (URL)**.
- Authenticated dashboard pages are protected behind login. As such when direct URL validation was not possible, the  **Check by text input** feature was used to validate pages.

All tested pages returned no errors or warnings to show as seen below.

##### Public Pages

| Page | Validator Confirmation | Result |
|------|------------------------|--------|
| Home | [![Home HTML validation](documentation/testing/html/homepage-html-test.png)](documentation/testing/html/homepage-html-test.png) | No errors or warnings |
| Consultation | [![Consultation HTML validation](documentation/testing/html/consultation-html-test.png)](documentation/testing/html/consultation-html-test.png) | No errors or warnings |
| Contact | [![Contact HTML validation](documentation/testing/html/Contact-html-test.png)](documentation/testing/html/Contact-html-test.png) | No errors or warnings |


##### Client (Authenticated)

| Page | Validator Confirmation | Result |
|------|------------------------|--------|
| Client Login | [![Client login HTML validation](documentation/testing/html/client-html-test.png)](documentation/testing/html/client-html-test.png) | No errors or warnings |
| Dashboard | [![Client dashboard HTML validation](documentation/testing/html/client-dash-html-test.png)](documentation/testing/html/client-dash-html-test.png) | No errors or warnings |
| Today�s Plan | [![Client today plan HTML validation](documentation/testing/html/client-todaysplan-html-test.png)](documentation/testing/html/client-todaysplan-html-test.png) | No errors or warnings |
| Programme Library | [![Client programme HTML validation](documentation/testing/html/client-programme-html-test.png)](documentation/testing/html/client-programme-html-test.png) | No errors or warnings |
| Workout Log | [![Client workout HTML validation](documentation/testing/html/client-workout-html-test.png)](documentation/testing/html/client-workout-html-test.png) | No errors or warnings |
| Body Metrics | [![Client body metrics HTML validation](documentation/testing/html/client-bodymetrics-html-test.png)](documentation/testing/html/client-bodymetrics-html-test.png) | No errors or warnings |
| Support | [![Client support HTML validation](documentation/testing/html/client-support-html.png)](documentation/testing/html/client-support-html.png) | No errors or warnings |


##### Trainer (Authenticated)

| Page | Validator Confirmation | Result |
|------|------------------------|--------|
| Trainer Login | [![Trainer login HTML validation](documentation/testing/html/trainer-html-test.png)](documentation/testing/html/trainer-html-test.png) | No errors or warnings |
| Trainer Dashboard | [![Trainer dashboard HTML validation](documentation/testing/html/trainer-dash-html-test.png)](documentation/testing/html/trainer-dash-html-test.png) | No errors or warnings |
| Trainer Clients | [![Trainer clients HTML validation](documentation/testing/html/trainer-clients-html-test.png)](documentation/testing/html/trainer-clients-html-test.png) | No errors or warnings |
| Trainer Programmes | [![Trainer programmes HTML validation](documentation/testing/html/trainer-programmes-html-test.png)](documentation/testing/html/trainer-programmes-html-test.png) | No errors or warnings |
| Trainer Support | [![Trainer support HTML validation](documentation/testing/html/trainer-support-html-test.png)](documentation/testing/html/trainer-support-html-test.png) | No errors or warnings |
| Trainer Queries | [![Trainer queries HTML validation](documentation/testing/html/trainer-queries-page-html-test.png)](documentation/testing/html/trainer-queries-page-html-test.png) | No errors or warnings |
| Trainer Support Detail | [![Trainer support detail HTML validation](documentation/testing/html/trainer-owner-supportdetailspage-html-check.png)](documentation/testing/html/trainer-owner-supportdetailspage-html-check.png) | No errors or warnings |
| Trainer Query Detail | [![Trainer query detail HTML validation](documentation/testing/html/trainer-owner-queery-detail-page-html-test.png)](documentation/testing/html/trainer-owner-queery-detail-page-html-test.png) | No errors or warnings |


##### Owner (Authenticated)

| Page | Validator Confirmation | Result |
|------|------------------------|--------|
| Owner Dashboard | [![Owner dashboard HTML validation](documentation/testing/html/owner-dash-html-test.png)](documentation/testing/html/owner-dash-html-test.png) | No errors or warnings |
| Owner Clients | [![Owner clients HTML validation](documentation/testing/html/owner-clientspage-html-test.png)](documentation/testing/html/owner-clientspage-html-test.png) | No errors or warnings |
| Owner Programmes | [![Owner programmes HTML validation](documentation/testing/html/owner-programmes-html-test.png)](documentation/testing/html/owner-programmes-html-test.png) | No errors or warnings |
| Owner Queries | [![Owner queries HTML validation](documentation/testing/html/owner-queries-html-test.png)](documentation/testing/html/owner-queries-html-test.png) | No errors or warnings |
| Owner Support | [![Owner support HTML validation](documentation/testing/html/owner-support-html-test.png)](documentation/testing/html/owner-support-html-test.png) | No errors or warnings |
| Owner Tailored Programme Detail | [![Owner tailored programme HTML validation](documentation/testing/html/owner-trainer-programme-detail-tailored-page-html-test.png)](documentation/testing/html/owner-trainer-programme-detail-tailored-page-html-test.png) | No errors or warnings |
| Owner Query Detail | [![Owner query detail HTML validation](documentation/testing/html/owner-trainer-querydetail-html-test.png)](documentation/testing/html/owner-trainer-querydetail-html-test.png) | No errors or warnings |

#### CSS Validation (W3C CSS Validator)

All CSS via the stlyseheet for the Precision performance website was also tested using the W3C CSS Validator. Validation was carried out via **direct text input** to ensure the full custom stylesheet was assessed independently of deployment configuration or static file handling.

Thankfully no errors were found as seen below.

| File | Validator Confirmation | Result |
|------|------------------------|--------|
| assets/css/style.css | [![CSS validation](documentation/testing/css/css-precision-performance-test.png)](documentation/testing/css/css-precision-performance-test.png) | No errors found |

#### Lighthouse Testing

Lighthouse testing was carried out using **Google Chrome DevTools** on both **mobile and desktop** views.  
Testing focused on key pages across **public**, **client**, and **staff (trainer & owner)** areas of the application.

Mobile scores are generally lower than desktop scores due to Lighthouse simulated mobile environment, which applies CPU throttling and slower network conditions.

---

##### Lighthouse Scoring Criteria

- **Performance**: Influenced by JavaScript execution, dynamic data rendering, and Lighthouse�s simulated device constraints.
- **Accessibility**: : High scores achieved through semantic HTML, proper labels, good contrast and ARIA friendly patterns.
- **Best Practices**: Strong results are due to modern standards, secure contexts, and valid markup.
- **SEO**: High scores are driven by appropriate meta tags, descriptive page titles and crawlable content.

---

##### Public Pages (Unauthenticated)

Public pages are more content focused and lightweight compared to dashboard pages, which results in consistently strong Lighthouse scores.

| Page | View | Result |
|-----|-----|--------|
| Home | Desktop | [![Home Desktop](documentation/testing/lighthouse/lighthouse-homepage-desktop.png)](documentation/testing/lighthouse/lighthouse-homepage-desktop.png) |
| Home | Mobile | [![Home Mobile](documentation/testing/lighthouse/lighthouse-homepage-mobile.png)](documentation/testing/lighthouse/lighthouse-homepage-mobile.png) |
| Consultation | Desktop | [![Consultation Desktop](documentation/testing/lighthouse/lighthouse-consultation-desktop.png)](documentation/testing/lighthouse/lighthouse-consultation-desktop.png) |
| Consultation | Mobile | [![Consultation Mobile](documentation/testing/lighthouse/lighthouse-consultation-mobile.png)](documentation/testing/lighthouse/lighthouse-consultation-mobile.png) |
| Contact | Desktop | [![Contact Desktop](documentation/testing/lighthouse/lighthouse-contact-desktop.png)](documentation/testing/lighthouse/lighthouse-contact-desktop.png) |
| Contact | Mobile | [![Contact Mobile](documentation/testing/lighthouse/lighthouse-contact-mobile.png)](documentation/testing/lighthouse/lighthouse-contact-mobile.png) |

**Notes**  
Lower mobile performance scores are expected due to the large hero image on the homepage and Lighthouse simulated mobile CPU throttling.

---

##### Client Area (Authenticated)

Client pages include dashboards, logs, and metrics, all of which involve dynamic data rendering and content specific to the client.

| Page | View | Result |
|-----|-----|--------|
| Client Login | Desktop | [![Client Login Desktop](documentation/testing/lighthouse/lighthouse-clientlogin-desktop.png)](documentation/testing/lighthouse/lighthouse-clientlogin-desktop.png) |
| Client Login | Mobile | [![Client Login Mobile](documentation/testing/lighthouse/lighthouse-clientlogin-mobile.png)](documentation/testing/lighthouse/lighthouse-clientlogin-mobile.png) |
| Dashboard | Desktop | [![Client Dashboard Desktop](documentation/testing/lighthouse/lighthouse-client-overview-desktop.png)](documentation/testing/lighthouse/lighthouse-client-overview-desktop.png) |
| Dashboard | Mobile | [![Client Dashboard Mobile](documentation/testing/lighthouse/lighthouse-client-overview-mobile.png)](documentation/testing/lighthouse/lighthouse-client-overview-mobile.png) |
| Today�s Plan | Desktop | [![Today Desktop](documentation/testing/lighthouse/lighthouse-client-todayplan-desktop.png)](documentation/testing/lighthouse/lighthouse-client-todayplan-desktop.png) |
| Today�s Plan | Mobile | [![Today Mobile](documentation/testing/lighthouse/lighthouse-client-todayplan-mobile.png)](documentation/testing/lighthouse/lighthouse-client-todayplan-mobile.png) |
| Programme Library | Desktop | [![Programme Desktop](documentation/testing/lighthouse/lighthouse-client-programme-desktop.png)](documentation/testing/lighthouse/lighthouse-client-programme-desktop.png) |
| Programme Library | Mobile | [![Programme Mobile](documentation/testing/lighthouse/lighthouse-client-programme-mobile.png)](documentation/testing/lighthouse/lighthouse-client-programme-mobile.png) |
| Workout Log | Desktop | [![Workout Desktop](documentation/testing/lighthouse/lighthouse-client-workout-desktop.png)](documentation/testing/lighthouse/lighthouse-client-workout-desktop.png) |
| Workout Log | Mobile | [![Workout Mobile](documentation/testing/lighthouselighthouse-client-workout-mobile.png)](documentation/testing/lighthouse/lighthouse-client-workout-mobile.png) |
| Support | Desktop | [![Support Desktop](documentation/testing/lighthouse/lighthouse-client-support-desktop.png)](documentation/testing/lighthouse/lighthouse-client-support-desktop.png) |
| Support | Mobile | [![Support Mobile](documentation/testing/lighthouse/lighthouse-client-support-mobile.png)](documentation/testing/lighthouse/lighthouse-client-support-mobile.png) |

**Notes**  
Client pages have lower mobile performance scores because they include tables, conditional rendering, and JavaScript for live data updates.

---

##### Staff Area (Trainer & Owner)

Trainer and Owner dashboards **share the same core layout and components**.  
The Owner role includes all Trainer functionality, with additional administrative features that are displayed only when the user has the appropriate permissions. (This is looked at in more detail in the user roles/permissions section)

As a result, Lighthouse scores across Trainer and Owner pages are comparable, since the Owner role extends the Trainer interface rather than introducing a separate layout or rendering path.

| Page | View | Result |
|-----|-----|--------|
| Dashboard | Desktop | [![Staff Dashboard Desktop](documentation/testing/lighthouse/lighthouse-trainer-overview-desktop.png)](documentation/testing/lighthouse/lighthouse-trainer-overview-desktop.png) |
| Dashboard | Mobile | [![Staff Dashboard Mobile](documentation/testing/lighthouse/lighthouse-trainer-overview-mobile.png)](documentation/testing/lighthouse/lighthouse-trainer-overview-mobile.png) |
| My Clients | Desktop | [![Clients Desktop](documentation/testing/lighthouse/lighthouse-trainer-myclients-desktop.png)](documentation/testing/lighthouse/lighthouse-trainer-myclients-desktop.png) |
| My Clients | Mobile | [![Clients Mobile](documentation/testing/lighthouse/lighthouse-trainer-myclients-mobile.png)](documentation/testing/lighthouse/lighthouse-trainer-myclients-mobile.png) |
| Programmes | Desktop | [![Programmes Desktop](documentation/testing/lighthouse/lighthouse-trainer-programmes-desktop.png)](documentation/testing/lighthouse/staff/lighthouse-trainer-programmes-desktop.png) |
| Programmes | Mobile | [![Programmes Mobile](documentation/testing/lighthouse/lighthouse-trainer-programmes-mobile.png)](documentation/testing/lighthouse/lighthouse-trainer-programmes-mobile.png) |
| Tailored Programmes | Desktop | [![Tailored Desktop](documentation/testing/lighthouse/lighthouse-trainer-tailoredprogrammes-desktop.png)](documentation/testing/lighthouse/lighthouse-trainer-tailoredprogrammes-desktop.png) |
| Tailored Programmes | Mobile | [![Tailored Mobile](documentation/testing/lighthouse/lighthouse-trainer-tailoredprogrammes-mobile.png)](documentation/testing/lighthouse/lighthouse-trainer-tailoredprogrammes-mobile.png) |

**Notes**  
Lower mobile performance scores expected and reflect:
- the presence of larger datasets.
- the use of editable forms and data entrys.
- Additional JavaScript execution that supports role-based features.

---

##### Lighthouse Summary

- Performance differences are normal in a feature-heavy and role-based django application (pages with larger datasets, tables/forms, and extra JavaScript tend to score lower).
- Accessibility, Best Practices, and SEO results are consistent and strong across key pages.
- Mobile performance scores are affected by Lighthouse�s simulated throttling (CPU/network constraints) and don�t necessarily showcase real world usability on modern devices.

#### Accessibility Testing (WAVE)

Accessibility testing was carried out using the **WAVE Web Accessibility Evaluation Tool (WebAIM)**.  
The aim of this testing was to check that pages are easy to read, easy to navigate, and usable for people using assistive technologies.

Testing was completed for thr below:
- Public pages (not logged in).
- Client dashboard pages (logged in).
- Staff dashboard pages (owner and trainer roles).

WAVE was used to check for:
- Accessibility errors.
- Colour contrast issues.
- Page structure and heading order.
- Use of ARIA labels where needed.

---

##### Public Pages (Unauthenticated)

| Page | Result |
|------|--------|
| Home page | [![WAVE - Home page](documentation/testing/wave/wave-homepage.png)](documentation/testing/wave/wave-homepage.png) |
| Book a consultation | [![WAVE - Consultation page](documentation/testing/wave/wave-consultation.png)](documentation/testing/wave/wave-consultation.png) |
| Contact page | [![WAVE - Contact page](documentation/testing/wave/wave-contact.png)](documentation/testing/wave/wave-contact.png) |
| Client login | [![WAVE - Client login](documentation/testing/wave/wave-client-login.png)](documentation/testing/wave/wave-client-login.png) |
| Trainer login | [![WAVE - Trainer login](documentation/testing/wave/wave-trainer-login.png)](documentation/testing/wave/wave-trainer-login.png) |

**Public pages summary**
- No accessibility errors were detected.
- Clear headings are used on each page.
- Forms include visible labels and helper text.
- Pages can be navigated to and from using a keyboard.

---

##### Client Area (Authenticated)

| Page | Result |
|------|--------|
| Client dashboard (overview) | [![WAVE - Client dashboard](documentation/testing/wave/wave-client-dasbaord-explain.png)](documentation/testing/wave/wave-client-dasbaord-explain.png) |
| Today�s plan | [![WAVE - Client today plan](documentation/testing/wave/wave-client-todaysplan-explain.png)](documentation/testing/wave/wave-client-todaysplan-explain.png) |
| Programme library | [![WAVE - Programme library](documentation/testing/wave/wave-client-programmelibrary-explain.png)](documentation/testing/wave/wave-client-programmelibrary-explain.png) |
| Workout log | [![WAVE - Workout log](documentation/testing/wave/wave-client-workoutlog-explain.png)](documentation/testing/wave/wave-client-workoutlog-explain.png) |
| Client support (ticket list) | [![WAVE - Client support](documentation/testing/wave/wave-client-support-explain.png)](documentation/testing/wave/wave-client-support-explain.png) |
| Support ticket detail | [![WAVE - Support ticket detail](documentation/testing/wave/wave-client-supportmessage-explain.png)](documentation/testing/wave/wave-client-supportmessage-explain.png) |

**Client area summary**
- No critical accessibility errors were found.
- Headings clearly describe each section of the page.
- Tables and lists are readable by screen readers.
- Buttons and links are clearly labelld.

---

##### Staff Area (Owner & Trainer Dashboards)

| Page | Result |
|------|--------|
| Owner � Dashboard overview | [![WAVE - Owner dashboard overview](documentation/testing/wave/wave-ownertrianer-dasbaord-explain.png)](documentation/testing/wave/wave-ownertrianer-dasbaord-explain.png) |
| Owner � My clients | [![WAVE - Owner clients](documentation/testing/wave/wave-ownertrianer-clients-explain.png)](documentation/testing/wave/wave-ownertrianer-clients-explain.png) |
| Owner � Programmes | [![WAVE - Owner programmes](documentation/testing/wave/wave-ownertrianer-programmes-explain.png)](documentation/testing/wave/wave-ownertrianer-programmes-explain.png) |
| Owner � Queries (contact forms) | [![WAVE - Owner queries](documentation/testing/wave/wave-ownertrianer-queries-explain.png)](documentation/testing/wave/wave-ownertrianer-queries-explain.png) |
| Owner � Support inbox | [![WAVE - Owner support inbox](documentation/testing/wave/wave-ownertrianer-support-explain.png)](documentation/testing/wave/wave-ownertrianer-support-explain.png) |
| Trainer � Consultation detail | [![WAVE - Trainer consultation detail](documentation/testing/wave/wave-trainer-consultationdetails-explain.png)](documentation/testing/wave/wave-trainer-consultationdetails-explain.png) |

**Staff area summary**
- Dashboard layouts are consistent across owner and trainer roles.
- Navigation menus are readable and easy to follow.
- Forms and tables use clear labels and headings.
- ARIA attributes are used where needed.

---

**Final Notes & Summary**  
- Public pages and dashboards were tested with WAVE.
- Pages show strong accessibility structure (headings, labels, ARIA where needed).
- Minor flags were reviewed and documented, with intentional design choices kept where they improve clarity.

Some dashboard pages show flags relating to **muted metadata text**, relating to the below:
- **Logged in: [username]** is intentionally styled as subtle helper text and is not meant to stand out.
  It is designed to sit in the background and not distract from more important content or the overall visual hierarchy.
  For this reason, it was intentionally kept in this style.

WAVE flagged this as low contrast depending on the page, but it is:
- non-interactive.
- not required to complete tasks.
- used only as supporting context.
- kept intentionally to reduce visual noise and improve layout clarity.

---|

### 17.4 User Story Testing
User stories were tested manually against the live application to confirm that the acceptance criteria were met. The table below summarises key user stories and the evidence that supports each one.

| User Story | How it was tested | Result | Evidence |
|-----------|-------------------|--------|----------|
| All Users – Auth (Login / Logout) | Logged in and out using the client and trainer login pages. Confirmed redirects go to the correct dashboards and logout returns to home page. | Pass | ![Client login](documentation/features/feature-clientlogin.png) / ![Trainer login](documentation/features/feature-trainerlogin.jpg) |
| All Users – Clear, consistent UI | Checked main public pages and all dashboard pages for consistent layout, typography, spacing, and button styles. Tested on mobile, tablet, desktop. | Pass | ![Client dashboard](documentation/features/feature-clientdashboard.jpg) |
| Client – Dashboard & view workout plan | Logged in as a client, confirmed dashboard loads correctly and programme can be viewed from programme library / today’s plan. | Pass | ![Client programme view](documentation/features/feature-clientprogrammeview.jpg) |
| Client – Log & manage workout sessions | Logged a workout session with pre-filled targets, saved session, confirmed it appears in recent sessions and can be edited. | Pass | ![Client workout log](documentation/features/feature_clientworkoutlog.jpg) |
| Client – Record & view body metrics | Added new body metrics check-in and confirmed entries appear in the metrics list and charts update. | Pass | ![Client body metrics](documentation/features/feature-clientbodymetrics.jpg) |
| Trainer – Client list & profiles | Logged in as trainer, viewed assigned clients list, opened a client profile and confirmed access to logs/metrics. | Pass | ![Trainer clients](documentation/features/feature-trainerclinetsoverview.jpg) |
| Trainer – Create/edit workout plans | Opened programme editor, updated exercises/sets/reps/weights and saved changes successfully. | Pass | ![Trainer programme tailoring](documentation/features/feature-trainer-programmetailoring.jpg) |
| Owner – Business dashboard oversight | Logged in as owner, confirmed access to all clients and admin level pages, and verified owner-specific features are visible. | Pass | ![Owner overview](documentation/features/feature-owneroverview.jpg) |
| Owner – Assign consultations to trainers | Opened consultations list as owner and assigned a consultation to a selected trainer (not just self). | Pass | ![Owner assignment](documentation/features/owner-clientassignment.jpg) |

## 18. Bugs & Fixes
During development, bugs were tracked and resolved as they appeared through testing and iterative improvements. The table below summarises key issues and how they were fixed.

| Bug / Issue | Cause | Fix | Status |
|------------|-------|-----|--------|
| Client login routed to trainer dashboard | Role routing was not correctly separated between staff and non-staff users | Updated login redirect logic so staff go to trainer dashboard and non-staff go to client dashboard | Fixed |
| Duplicate workout sessions could be created for the same day/week | No blocking logic when saving sessions | Added a duplicate session check (per client/day/week) and returned an error message instead of saving | Fixed |
| Workout log notes were being overwritten unintentionally | Auto-generated session notes were being appended on page loads without a programme day context | Updated view logic to only generate session details when a programme day is present | Fixed |
| Support tickets could be accessed outside assigned trainer scope | Ticket detail query did not fully enforce trainer scoping | Restricted queries using trainer=request.user to prevent unassigned ticket access | Fixed |
| Mobile/tablet tables overflowed and became hard to use | Tables were too wide for smaller devices | Added responsive table handling (horizontal scroll on tablet, stacked/grid layout on mobile) | Fixed |

## 19. Deployment

### 19.1 Heroku Deployment

Precision Performance PT was deployed to Heroku, a cloud platform that allows Django applications to be hosted and accessed online.

The following steps were taken to deploy the application:

1. **Prepare the project for deployment**
   - Added `gunicorn` to `requirements.txt` to serve the application.
   - Created a `Procfile` with the following command:
     ```
     web: gunicorn precision_performance.wsgi
     ```
   - Ensured `DEBUG` is set using an environment variable.

2. **Environment variables**
   The following environment variables were configured in the Heroku dashboard:

   | Variable | Purpose |
   |--------|--------|
   | `DJANGO_SECRET_KEY` | Keeps the Django application secure |
   | `DJANGO_DEBUG` | Controls debug mode (set to `False` in production) |
   | `DJANGO_ALLOWED_HOSTS` | Specifies allowed domains |
   | `DATABASE_URL` | Automatically provided by Heroku (PostgreSQL) |
   | `DJANGO_CSRF_TRUSTED_ORIGINS` | Allows secure form submissions |

3. **Database setup**
   - Heroku Postgres was added as the production database.
   - Django migrations were run on Heroku to create database tables.

4. **Static files**
   - Static files were collected using:
     ```
     python manage.py collectstatic
     ```
   - WhiteNoise was used to serve static files in production.

5. **Deployment**
   - The project was connected to a GitHub repository.
   - Automatic deploys were enabled so each push to the `main` branch triggered a redeploy.
   - The live application is accessible via the Heroku app URL.

Heroku was chosen because it integrates well with Django and allows rapid, reliable deployment for portfolio projects.

### 19.2 Local Deployment

### 19.3 How to Fork the Repository

To create your own copy of the **Precision Performance PT** repository, follow these steps:

1. Log in (or sign up if required) to **GitHub**.
2. Navigate to the project repository:  
   [Project link](https://github.com/moranjohn-95/precision-performance-pt)
3. In the top-right corner of the repository page, click the **Fork** button.
4. This will create a copy of the repository in your own GitHub account.

---

### 19.4 How to Clone the Repository

To clone the repository to your local machine, follow these steps:

1. Log in (or sign up if required) to **GitHub**.
2. Navigate to this [Project link](https://github.com/moranjohn-95/precision-performance-pt)
 repository.
3. Click the **Code** button at the top of the repository.
4. Choose one of the following options:
   - **HTTPS**
   - **SSH**
   - **GitHub CLI**
5. Copy the repository URL provided.
6. Open your code editor and terminal.
7. Change the current working directory to the location where you want the cloned repository to be stored.
8. Run the following command in the terminal:


## 20. Future Features
The following features were identified as realistic next steps after the initial release. These focus on improving communication, automation, and long-term usability across the client, trainer, and owner workflows.

| Future Feature | Priority | Who Benefits | Why It Matters | Notes / Implementation Idea |
|---|:---:|---|---|---|
| **Mailgun Email Integration (Production Emails)** | High | All users | Enables real email sending for password resets, consultation invites, notifications, and support updates (instead of console email in development). | Configure Mailgun SMTP/API, set environment variables on Heroku, update `EMAIL_BACKEND` for production, and add email templates for key events. |
| **Automated Notifications** | High | Clients / Trainers | Keeps users engaged and reduces missed check-ins (e.g., reminders for workouts, metrics, and ticket replies). | Trigger emails on: assigned consultation, new programme assigned, support reply posted, upcoming workout day. |
| **Trainer Notes / Coaching Comments on Sessions** | Medium | Clients / Trainers | Improves coaching quality by allowing trainers to leave feedback on logged sessions. | Add a trainer comment field on `WorkoutSession` (visible to client, editable by trainer). |
| **Programme Version History / Change Tracking** | Medium | Trainers / Owners | Prevents confusion when programmes are updated and supports auditing. | Store programme “snapshots” or log edits with timestamp + editor. |
| **In-App Messaging Notifications** | Medium | Clients / Trainers | Clients don’t need to keep checking support tickets manually. | Add a “new reply” badge/count in sidebar + optional email alerts. |
| **Expanded Metrics (Photos & Measurements)** | Medium | Clients / Trainers | More complete progress tracking beyond numbers. | Add optional progress photo uploads + more measurement fields. |
| **Payments / Subscription Management** | Low | Owner / Clients | Supports real business operations for online coaching. | Integrate Stripe for monthly coaching plans and payment history. |
| **Class Management Enhancements** | Low | Owner / Trainers | Improves handling of group coaching clients (currently separated from dashboard access). | Add class attendance tracking, group programming, and class-based progress summaries. |

## Credits
- Code Institute — learning material.
- JavaScript: The Definitive Guide (7th ed.) — David Flanagan (book) — learning material and coding tips.
  Fluent Python - (Book) Learning materials and coding tips.
- W3Schools — troubleshooting and coding tips.

### Content
- Brio Catering, Budget Planner, The Spanish Language Quiz -  README — inspiration for the README layout and structure.

### Tools & Libraries
- Balsamiq — wireframe creation.
- Bootstrap — responsive layout framework.
- Fireworks.js — fireworks effect at the end of the quiz.
- Favicon.io — favicon generation.
- Font Awesome — social media icons.
- Google Fonts — font sourcing.
- ChatGPT  — brainstorming, troubleshooting, and refining code/documentation during development.


## Acknowledgements
- All Code Institute lecturers and staff — continued support throughout this project.




