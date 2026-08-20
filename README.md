<div align="center">

# Skill Match Academic Platform

### *Bridging the Gap Between Academic Skills and Real-World Training Opportunities*

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTMX](https://img.shields.io/badge/HTMX-1.27-336791?style=for-the-badge&logo=htmx&logoColor=white)

---

</div>

## Overview

**Skill Match** is a Django-based academic training platform that connects university graduates with internship and training opportunities offered by companies, government agencies, NGOs, and research institutions. The platform solves a critical disconnect in the job market: students struggle to find training aligned with their skills and academic performance, while organizations lack an efficient, data-driven way to identify the right candidates.

At its core, Skill Match employs a **weighted scoring algorithm** that evaluates student-opportunity compatibility across three dimensions -- technical skills alignment, academic specialization match, and GPA thresholds -- producing a unified 0-100 match score that surfaces the most relevant opportunities for each student and the most qualified candidates for each organization.

---

## Key Features

- **Smart Matching Algorithm** -- Multi-factor scoring engine (skills, specialization, GPA) with automatic GPA scale normalization across 4.0, 5.0, and 100% systems.
- **Role-Based Access Control (RBAC)** -- Configurable identity roles (`student`, `training_entity`) with approval workflows, profile completion gates, and per-role dashboard routing.
- **Admin Dashboard (Unfold)** -- Modern, Tailwind-styled admin panel with nested inlines for geographic data, industry management, and full application lifecycle control.
- **Corporate/Entity Dashboard** -- Training entities can post opportunities, match students, send invitations, and manage incoming applications through a unified interface.
- **Student Dashboard** -- Students can complete profiles, browse matched opportunities, track application status, and manage their CV uploads.
- **Dynamic Cascading Filters** -- AJAX-powered dropdowns (University > College > Major) powered by HTMX for seamless partial page updates.
- **Application Lifecycle Management** -- 7-state workflow (draft > invited > pending > accepted/rejected > on_training > completed) with status tracking and progress percentages.
- **Approval Workflow** -- Training entities require admin approval before gaining platform access, ensuring verified organizational profiles.
- **Reusable UI Component Library** -- 12+ template tags (`ui_components`) for buttons, cards, inputs, progress bars, and profile displays -- registered as builtins for zero-import template usage.
- **Dark Mode & i18n Support** -- User preference persistence for dark/light themes and Arabic/English language switching.

---

## Architecture & Directory Structure

### Django MVT + Modular App Architecture

The project follows a strict **Separation of Concerns** pattern within Django's MVT paradigm. Each domain is encapsulated in its own Django app, with shared logic centralized in the `core` module:

- **`core/enums.py`** -- Domain enumeration definitions (reserved for centralized enum management)
- **`core/constants.py`** -- Shared message strings, form error templates, and configuration constants
- **`core/routes.py`** -- Centralized URL name registry (`Routes` class) for type-safe reverse lookups
- **`core/validators.py`** -- Reusable field validators (file size/extension, phone prefix/length)
- **`core/base_models.py`** -- Abstract `BaseModel` and `BaseProfile` for consistent model inheritance
- **`core/base_admin.py`** -- Tailwind-styled admin base classes for consistent admin UI

```
Job-Market-Training-Platform/
|
|-- config/                         # Project configuration
|   |-- settings.py                 # Django settings (env-driven)
|   |-- urls.py                     # Root URL dispatcher
|   |-- wsgi.py                     # WSGI entry point
|   |-- management/commands/
|       |-- generate_apps.py        # Auto-generate identity apps from SITE_ROLES
|
|-- core/                           # Shared foundation module
|   |-- base_models.py              # Abstract BaseModel, BaseProfile
|   |-- base_admin.py               # Tailwind-styled BaseModelAdmin
|   |-- models.py                   # Country, Region, City (geography)
|   |-- views.py                    # Home, search, opportunity views, error handlers
|   |-- urls.py                     # Core URL patterns
|   |-- forms.py                    # Base ModelForm with Tailwind styling
|   |-- middleware.py               # ProfileCompletionMiddleware
|   |-- context_processors.py      # Global user prefs (dark mode, avatar)
|   |-- constants.py               # BaseMessages, FormErrorMessages
|   |-- enums.py                   # Domain enumerations
|   |-- routes.py                  # Routes class (URL name constants)
|   |-- utils.py                   # calculate_match_score (matching algorithm)
|   |-- validators.py              # FileValidator, PhoneValidator
|   |-- helpers.py                 # URL/directory resolution utilities
|   |-- templatetags/
|       |-- ui_components.py       # 12+ reusable template tags (builtins)
|   |-- fixtures/
|       |-- regions.json           # Saudi geographic seed data
|
|-- accounts/                       # Authentication & user management
|   |-- models.py                   # CustomUser (email-based, GFK profile)
|   |-- views.py                    # Signup, login redirect, waiting approval
|   |-- forms.py                    # CustomSignupForm (extends allauth)
|   |-- signals.py                 # post_save: role sync, profile creation
|   |-- adapters.py                # MyAccountAdapter (verification checks)
|   |-- utils.py                   # Role sync, profile binding utilities
|
|-- students/                       # Student-facing application
|   |-- models.py                   # StudentProfile (GPA, skills, CV)
|   |-- views.py                    # Dashboard, matching, application views
|   |-- forms.py                   # StudentProfileForm (cascading dropdowns)
|   |-- decorators.py              # @student_required (RBAC)
|   |-- utils.py                   # student_match_opportunities
|
|-- training_entities/              # Organization/company application
|   |-- models.py                   # TrainingEntityProfile, Industry, TrainingOpportunity
|   |-- views.py                    # Opportunity CRUD, student matching, invitations
|   |-- forms.py                   # EntityProfileForm, OpportunityForm
|   |-- decorators.py              # @training_entity_required, @training_entity_approval_required
|   |-- constants.py               # TrainingMessages
|   |-- enums.py                   # EntityType (PRIVATE, GOV, NGO, RESEARCH)
|   |-- utils.py                   # can_company_invite
|
|-- applications/                   # Application lifecycle management
|   |-- models.py                   # JoinTrainingOpportunity (7-state workflow)
|   |-- views.py                    # Join, cancel, application details
|   |-- utils.py                   # change_application_status, active_opportunities
|
|-- academy/                        # Academic reference data
|   |-- models.py                   # University, College, Major, SkillCategory, Skill
|   |-- views.py                    # AJAX loaders for cascading dropdowns
|   |-- enums.py                   # UniversityType (PUB, PRI, INT, TEC)
|
|-- theme/                          # Django-Tailwind integration
|   |-- static_src/
|       |-- src/styles.css          # Tailwind CSS entry point
|       |-- package.json            # Node.js dependencies
|       |-- postcss.config.js       # PostCSS configuration
|
|-- Seeds/                          # Database seed scripts
|   |-- seeds.py                    # Master seeder
|   |-- seed_region.py              # Saudi geographic data
|   |-- seed_universities.py        # University/college/major data
|   |-- seed_skills.py              # Skill categories and skills
|   |-- seed_training_entities.py   # Sample organizations
|   |-- seed_training_opportunities.py
|
|-- templates/                      # Project-level template overrides
|   |-- account/                    # allauth overrides
|   |-- admin/                      # Admin panel overrides
|
|-- static/                         # Project static files
|   |-- css/                        # Custom CSS + admin styles
|   |-- js/                         # Custom JS + HTMX library
|   |-- img/                        # Static images
|
|-- .env                            # Environment variables (auto-generated)
|-- manage.py                       # Django management entry point
|-- requirements.txt                # Python dependencies
|-- db.sqlite3                      # SQLite database
```

---

## Matching Algorithm

The core matching engine (`core/utils.py:calculate_match_score`) evaluates compatibility on a **0-100 point scale**:

| Factor | Max Points | Logic |
|--------|-----------|-------|
| **Skills Match** | 60 | Set intersection of student skills vs. required skills, weighted by ratio |
| **Skills Bonus** | 10 | +10 bonus for 100% skills match |
| **Specialization Match** | 30 | Exact major match, or full marks if opportunity is open to all majors |
| **GPA Score** | 10 | Normalized percentage comparison with incentive bonus (0.5 pts per 1% surplus, capped at 10) |

> The algorithm auto-detects GPA scales (4.0 / 5.0 / 100%) and normalizes all values to a unified percentage before comparison, ensuring fair cross-system evaluation.

---

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Backend** | Python 3.14 | Core runtime |
| | Django 6.0.2 | MVT web framework |
| | django-allauth 65.14 | Email-based authentication |
| | django-unfold 0.84 | Modern admin UI |
| | django-environ 0.13 | Environment variable management |
| | django-htmx 1.27 | Partial page updates |
| | Pillow 12.1 | Image processing |
| **Frontend** | Tailwind CSS 4.x | Utility-first CSS framework |
| | DaisyUI 5.x | Tailwind component library |
| | HTMX | Declarative AJAX interactions |
| | django-crispy-forms 2.6 | Form rendering with Tailwind pack |
| | django-widget-tweaks 1.5 | Template form manipulation |
| **Database** | SQLite 3 | Lightweight local data persistence |
| **Architecture** | Modular Django Apps | Domain-driven separation of concerns |
| | GenericForeignKey | Polymorphic profile linkage |
| | Abstract Base Models | Inheritance-based code reuse |
| | RBAC + Decorators | Role-based access control |

---

## Setup & Installation

### Prerequisites

- **Python 3.14+**
- **Node.js** (for Tailwind CSS compilation)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/azzaldeen-tech/Job-Market-Training-Platform.git
cd Job-Market-Training-Platform
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

A `.env` file is auto-generated on first run with a random `SECRET_KEY`. Customize it as needed:

```env
APP_NAME=Skill Match
SECRET_KEY=your-secret-key
EMAIL_SERVICE=console          # 'console' for dev, 'smtp' for production
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Install Node Dependencies & Build Tailwind

```bash
cd theme/static_src
npm install
npm run build            # One-time build
cd ../..
```

### 6. Run Migrations & Seed Data

```bash
python manage.py migrate           # Creates tables + auto-syncs roles
python manage.py createsuperuser   # Create admin account
python Seeds/seeds.py              # Populate reference data (Saudi regions, universities, skills)
```

### 7. Run the Development Server

Open **two terminals**:

```bash
# Terminal 1 -- Tailwind CSS watcher
python manage.py tailwind start

# Terminal 2 -- Django development server
python manage.py runserver
```

### 8. Access the Platform

| URL | Description |
|-----|-------------|
| [http://127.0.0.1:8000](http://127.0.0.1:8000) | Application |
| [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) | Admin Dashboard |

---

## License

This project is for academic and training purposes.

---

<div align="center">

### Azzaldeen Al-Qashaei

[![GitHub](https://img.shields.io/badge/GitHub-azzaldeen--tech-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/azzaldeen-tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-azzaldeen__eng-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/azzaldeen-al-qashaei-0a6928206)

</div>
