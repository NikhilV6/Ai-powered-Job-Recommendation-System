# Job Portal API

A RESTful API for managing users, companies, jobs, and job applications.

---

## 🧍 User Entity (`users`)

Represents candidates, recruiters, or admins.

| Field | Type | Required | Description |
|--------|------|-----------|--------------|
| _id | ObjectId | Auto | Unique identifier |
| name | String | ✅ | Full name of the user |
| email | String | ✅ | Unique email address |
| password | String | ✅ | Hashed password |
| role | String | Default: candidate | Enum: candidate, recruiter, admin |
| profile.resumeUrl | String | ❌ | Resume file link |
| profile.skills | [String] | ❌ | List of user skills |
| profile.experience | String | ❌ | Work experience summary |
| profile.education | String | ❌ | Education details |
| profile.portfolio | String | ❌ | Portfolio link |
| profile.location | String | ❌ | User’s location |
| appliedJobs | [ObjectId] | ❌ | References Application collection |
| createdAt | Date | Auto | Registration timestamp |

---

## 🏢 Company Entity (`companies`)

Represents an organization that posts jobs.

| Field | Type | Required | Description |
|--------|------|-----------|--------------|
| _id | ObjectId | Auto | Unique company ID |
| name | String | ✅ | Company name |
| industry | String | ✅ | Industry type (e.g., IT, Finance) |
| website | String | ❌ | Company website |
| description | String | ❌ | Company description |
| logoUrl | String | ❌ | Company logo |
| location.city | String | ❌ | City |
| location.state | String | ❌ | State |
| location.country | String | ❌ | Country |
| jobs | [ObjectId] | ❌ | References Job collection |
| createdAt | Date | Auto | Creation timestamp |

---

## 💼 Job Entity (`jobs`)

Represents job postings created by a company.

| Field | Type | Required | Description |
|--------|------|-----------|--------------|
| _id | ObjectId | Auto | Unique job ID |
| company | ObjectId | ✅ | Reference to Company |
| title | String | ✅ | Job title |
| description | String | ✅ | Detailed job description |
| requirements | [String] | ❌ | Required skills or qualifications |
| employmentType | String | ✅ | Enum: Full-time, Part-time, Internship, Contract |
| location.city | String | ❌ | City |
| location.state | String | ❌ | State |
| location.country | String | ❌ | Country |
| location.remote | Boolean | ❌ | True if remote job |
| salaryRange.min | Number | ❌ | Minimum salary |
| salaryRange.max | Number | ❌ | Maximum salary |
| salaryRange.currency | String | Default: "USD" | Salary currency |
| postedBy | ObjectId | ❌ | Reference to User (recruiter/admin) |
| applicantsCount | Number | Auto | No. of applicants |
| status | String | Default: "Open" | Enum: Open, Closed |
| createdAt | Date | Auto | Posting date |
| expiresAt | Date | ❌ | Job expiry date |

---

## 📨 Application Entity (`applications`)

Represents a user applying for a job.

| Field | Type | Required | Description |
|--------|------|-----------|--------------|
| _id | ObjectId | Auto | Unique application ID |
| job | ObjectId | ✅ | Reference to Job |
| applicant | ObjectId | ✅ | Reference to User |
| company | ObjectId | ✅ | Reference to Company |
| coverLetter | String | ❌ | User’s cover letter |
| status | String | Default: "Applied" | Enum: Applied, Under Review, Interview, Rejected, Hired |
| appliedAt | Date | Auto | Application timestamp |
| updatedAt | Date | Auto | Last status update |
| Index | { job, applicant } | Unique | Prevents duplicate applications |

---

## 🌐 API Endpoints

### 🧍 User Routes (`/api/users`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| POST | /register | Register a new user | ❌ |
| POST | /login | Login user and return JWT | ❌ |
| GET | /me | Get logged-in user profile | ✅ |

### 🏢 Company Routes (`/api/companies`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| POST | / | Create a new company | ✅ (Recruiter/Admin) |
| GET | / | Get all companies | ❌ |
| GET | /:id | Get company by ID with job listings | ❌ |
| PUT | /:id | Update company details | ✅ |
| DELETE | /:id | Delete a company | ✅ (Admin) |

### 💼 Job Routes (`/api/jobs`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| POST | / | Create a new job posting | ✅ (Recruiter/Admin) |
| GET | / | Get all jobs with company info | ❌ |
| GET | /:id | Get job details by ID | ❌ |
| PUT | /:id | Update job info | ✅ (Recruiter/Admin) |
| DELETE | /:id | Delete a job | ✅ (Recruiter/Admin) |

### 📨 Application Routes (`/api/applications`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| POST | / | Apply for a job | ✅ (Candidate) |
| GET | /user/:userId | Get all applications by a user | ✅ |
| PATCH | /:id | Update application status | ✅ (Recruiter/Admin) |

---

## ⚙️ Tech Stack

- **Backend:** Node.js, Express.js  
- **Database:** MongoDB (Mongoose ODM)  
- **Auth:** JWT Authentication  
- **Validation:** Express Validator  
- **Hashing:** bcrypt.js  

---
