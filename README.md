# MusicLab
MusicLab is a music blog - a place where artists can share their creations, give and receive constructive feedback, and explore fresh avenues of collaboration. It is a space for musicians of each and every skill level and all genres to show their music to the public and start conversations about music-related topics.

![Site view across devices]()

The live link for "MusicLab" can be found [HERE](https://music-lab-11c9945eb758.herokuapp.com/)

## Table of Contents


## UX

### Site Purpose:
The intent of the site is to provide a space for a community of aspiring musicians and songwriters of all skill levels where they can share their work, discuss it with others, receive feedback on works in progress, and maybe even make friends or start a band.

### Site Goal:
The goal is to have a platform that connects creators and helps them support each other. It aims to reduce the hurdle of getting your own music heard as an amateur by encouraging drafts and work-in-progress uploads.

### Audience:
Creators, musicians, songwriters of all ages and skill levels with a passion for music. The site is mainly geared toward amateurs, hobbyists and unpublished creators looking for feedback or collaboration opportunities.

### Current User Goals:
For creators to quickly upload their music with a description and to browse and comment on other creators' entries.

### New User Goals:
For visitors to get immediate access to all published musical creations and to feel intrigued about joining and uploading their own work.

### Future Goals:
- Collaboration page that allows creators to start joint projects
- Flagging option to allow users to report inappropriate content
- Direct messaging system for private user communication
- Notifications that inform creators about new comments or likes
- Follower feature

## User Stories

### Admin stories:
#### As an admin:
1. I can **moderate entries** so that **they are tagged correctly and no inappropriate content is uploaded**.
2. I can **moderate comments** so that **the feedback provided is appropriate**.
3. I can **delete users who break the rules** so that **toxic behavior is discouraged**.

### Visitor stories:
#### As a visitor:
1. I can **visit the site** so that **I can browse entries made by the creators**.
2. I can **open individual user profiles** so that **I can find information about a creator**.
3. I can **sort all entries by date or likes** so that **I can easily find the newest and the most popular entries**.
4. I can **filter all entries by tag** so that **I can explore certain styles, languages, instruments etc**.
5. I can **filter all entries by username** so that **I can explore new artists**.
6. I can **read the 'About' page** so that **I am informed about the principles and rules of this website**.
7. I can **sign up** so that **I can start contributing by liking, commenting, or adding entries**.

### Creator stories:
#### As a creator:
1. I can **update my user profile** so that **others get to know me and find out how to contact me**.
2. I can **upload my work** so that **I can share it with others and receive feedback**.
3. I can **edit my entries** so that **I can change their presentation and add additional audio files**.
4. I can **add audio files to my existing entry** so that **others can follow my work in progress**.
5. I can **make my entry private** so that **it is not shown to others**.
6. I can **delete my entry** so that **it gets deleted from the database and becomes unavailable**.
7. I can **like an entry** so that **other creators feel appreciated**.
8. I can **unlike an entry** so that **I can remove entries from my favorites**.
9. I can **view all entries I liked** so that **I can quickly find my favorite creations**.
10. I can **leave a comment for an entry** so that **I can start or partake in discussions and connect with others**.
11. I can **edit my comment** so that **I can fix errors**.
12. I can **delete my comment** so that **it is no longer available**.
13. I can **view all comments I have written** so that **I can continue my discussions**.
14. I can **submit a message to the admin** so that **I can give feedback on the site functionality, report an issue or ask something**.
15. I can **log out of my account** so that **unauthorized access is prevented**.

## Design

### Planning
As part of the planning process, I made a list of all basic functions that an MVP should have and drafted the basic page layout.

The project's kanban board can be found here: [MusicLab Kanban board](https://github.com/users/RikaIljina/projects/2/views/1)

### Wireframes:

#### Main page:
![Main page wireframe](static/readme-assets/mainpage-wireframe.png)

#### Main page on mobile:
![Main page wireframe on mobile](static/readme-assets/mobile-wireframe.png)

#### 'User profile' page:
![User profile page wireframe](static/readme-assets/profile-wireframe.png)

#### 'Add new entry' page:
![Add new entry page wireframe](static/readme-assets/add-entry-wireframe.png)

### Sitemap:
![Sitemap of the website](static/readme-assets/.drawio.svg)

### Database schema:
![Database schema](static/readme-assets/musiclab-erd.jpg)

### Color Scheme:
![alt text](static/readme-assets/palette.PNG)

### Typography:
The page uses the font "Raleway" for all text.
The font is being imported from Google Fonts.
When users add a profile bio or a song description, they can use the Summernote richtext editor to format their text. There, they can add some basic formatting as well as choose one of the following fonts:
- Arial
- Arial Black
- Courier New
- Helvetica

### Imagery:
The website uses images sparingly to not distract from the main purpose of the site.
The logo was adapted from an icon found on Flaticon.
The background images on the Login, Signup and Signout pages are taken from Freepik. They create a pleasant backdrop for the otherwise plain pages, while their musical theme prepares the user for a hopefully amazing musical experience.
See credits for source attribution.
<img src="static\images\logo-inst-l.webp" width="300" alt="Logo with stylized instruments next to the name MusicLab">
<img src="static\images\hands-holding-music-instruments_53876-148189.webp" width="300" alt="Hands holding music instruments">
<img src="static\images\musical-background-with-musical-keys-white-flat-lay-copy-space.webp" width="300" alt="Keyboard in the lower right corner">

## Features

### Existing Features:

#### Main page:

#### Navigation bar:

##### Desktop:

##### Mobile:

#### Sidebar:

##### Desktop:

##### Mobile:


### Future Features:

- [ ] Collaboration page that allows creators to start joint projects
- [ ] Flagging option to allow users to report inappropriate content
- [ ] Direct messaging system for private user communication
- [ ] Notifications that inform creators about new comments or likes
- [ ] Follower feature


## Codebase

### Project tree

<details>
<summary>Project file structure</summary>

```

PortfolioProject4
├─ comments
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  ├─ models.py
│  ├─ templates
│  │  └─ comments
│  │     └─ snippets
│  │        └─ comment_section.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ entries
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  ├─ models.py
│  ├─ templates
│  │  └─ entries
│  │     ├─ entry_details.html
│  │     ├─ entry_form.html
│  │     └─ snippets
│  │        ├─ entry_cards.html
│  │        └─ entry_fullpage.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ likes
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  ├─ models.py
│  ├─ templates
│  │  └─ likes
│  │     └─ snippets
│  │        └─ like_comment_summary.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ mainpage
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  ├─ models.py
│  ├─ signals.py
│  ├─ templates
│  │  └─ mainpage
│  │     ├─ about.html
│  │     ├─ index.html
│  │     └─ snippets
│  │        └─ modal.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ manage.py
├─ musiclab
│  ├─ adapter.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ __init__.py
│  └─ __pycache__
├─ Procfile
├─ requirements.txt
├─ runtime.txt
├─ static
│  ├─ css
│  │  ├─ base-styles.css
│  │  ├─ entries-styles.css
│  │  ├─ form-styles.css
│  │  ├─ mainpage-styles.css
│  │  ├─ modal-styles.css
│  │  └─ user-profile-styles.css
│  ├─ images
│  │  ├─ default_profile.webp
│  │  ├─ hands-holding-music-instruments_53876-148189.webp
│  │  ├─ logo-inst-l.webp
│  │  └─ saxophone-white-background_lg.webp
│  ├─ js
│  │  ├─ base.js
│  │  ├─ comments.js
│  │  ├─ entries.js
│  │  ├─ filters.js
│  │  ├─ form_script.js
│  │  └─ likes.js
│  └─ readme-assets
│     └─ musiclab-erd.jpg
├─ staticfiles
├─ templates
│  ├─ 400.html
│  ├─ 403.html
│  ├─ 404.html
│  ├─ 500.html
│  ├─ account
│  │  ├─ login.html
│  │  ├─ logout.html
│  │  ├─ signup.html
│  ├─ base.html
│  ├─ navbar.html
│  ├─ pagination.html
│  ├─ sidebar.html
├─ users
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  ├─ models.py
│  ├─ signals.py
│  ├─ templates
│  │  └─ users
│  │     ├─ dashboard.html
│  │     ├─ dashboard_entry.html
│  │     ├─ dashboard_user_comments.html
│  │     ├─ dashboard_user_likes.html
│  │     ├─ profile.html
│  │     ├─ profile_form.html
│  │     └─ snippets
│  │        └─ profile_card.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
└─ __pycache__
```

</details>

### Database
- postgres was used
- reduce queries, also in admin
- automatically create user profile via signal

#### Custom validation
- user name length via adapter
- create custom slug and validate
- file pre-validation

#### Taggit integration
- automatically delete empty tags

#### Cloudinary integration
- handle file destruction

#### Summernote integration
- handle html safely
- disable code/file embed in settings

### HTML files
- snippets for reusability

### Site functionality
- JS for sidebar

## Testing

### Validator Testing
### Responsiveness testing
### C.R.U.D. testing
### FEATURES

### Fixed bugs
- admin slug, created new ModelForm with clean() method and linked it as form to admin
- force-show user/tag section instead of using proper bootstrap call
- couldn't save form without ```enctype="multipart/form-data"```
- relied on changed_data and tried to get file attribute; file field was changed but 'file' was empty

### Unfixed bug

## Technologies Used
### Main Languages Used
- HTML5
- CSS3
- Javascript
- Python
- Django
- SQL - Postgres

### Frameworks, Libraries & Programs Used

### Installed Packages:

## Deployment

## Credits
### Code used

All Python code was written by me unless clearly stated otherwise.
### Content
### Acknowledgments
